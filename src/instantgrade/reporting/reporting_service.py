import html as html_lib
from io import StringIO
from pathlib import Path
from typing import List, Dict, Optional, Tuple

import pandas as pd


class ReportingService:
    """
    Service for building, summarizing, and exporting grouped student evaluation reports.

    Features added/implemented:
      - Best-N questions scoring per attempt (default best_n=10).
      - Per-attempt scaled marks: map best-N raw totals to a target range (default scaled_range=(10,20)).
      - Per-attempt metrics merged into the main DataFrame for HTML rendering.
      - Summary modal shows highest Best-N across attempts and its scaled score.

    Usage:
      rs = ReportingService(executed_results=..., total_assertions=15, best_n=10, scaled_range=(10,20))
      rs.dataframe()    # builds internal df + attempt-level summaries
      rs.to_html("report.html")
    """

    def __init__(
        self,
        executed_results: Optional[List[Dict]] = None,
        solution: Optional[Dict] = None,
        debug: bool = False,
        logger=None,
        total_assertions: int = 0,
        best_n: int = 10,
        scaled_range: Tuple[float, float] = (10.0, 20.0),
    ):
        self.debug = debug
        self.solution = solution or {}
        self.executed_results = executed_results or []
        self.logger = logger
        self.total_assertions = total_assertions or 1  # avoid division by zero
        self.best_n = int(best_n)
        self.scaled_min, self.scaled_max = float(scaled_range[0]), float(scaled_range[1])

        # DataFrames to be built
        self.df: pd.DataFrame = pd.DataFrame()
        self.attempt_scores_df: pd.DataFrame = pd.DataFrame()  # one row per attempt (file)
        self.student_best_df: pd.DataFrame = pd.DataFrame()  # best across attempts per student

        # Build right away (keeps backward compatible behaviour)
        self.df = self.dataframe(self.executed_results)

        if self.logger:
            try:
                self.logger.info(f"[Reporting] Processed {len(self.df)} result rows.")
            except Exception:
                pass

    # -------------------------------------------------------------------------
    def dataframe(self, executed_results: Optional[List[Dict]] = None) -> pd.DataFrame:
        """
        Flatten evaluation results into a DataFrame, compute per-question totals,
        compute Best-N per attempt and scaled marks.
        """
        executed_results = executed_results if executed_results is not None else self.executed_results
        all_rows = []
        for item in executed_results or []:
            student_path = Path(item.get("student_path", ""))
            results = item.get("results", [])
            ns = item.get("execution", {}).get("namespace", {})
            meta = item.get("execution", {}).get("student_meta", {})

            student_name = meta.get("name") or ns.get("name") or student_path.stem
            roll_no = meta.get("roll_number") or ns.get("roll_number") or "N/A"

            for r in results:
                row = {
                    "file": str(student_path),
                    "student": student_name,
                    "roll_number": roll_no,
                    "question": r.get("question"),
                    "assertion": r.get("assertion"),
                    "status": r.get("status"),
                    "score": r.get("score", 0),
                    "error": r.get("error"),
                    "description": r.get("description", ""),
                }
                all_rows.append(row)

        df = pd.DataFrame(all_rows)
        if df.empty:
            if self.debug:
                print("Warning: Empty DataFrame in ReportingService.dataframe()")
            # Ensure other structures are empty but defined
            self.df = pd.DataFrame()
            self.attempt_scores_df = pd.DataFrame()
            self.student_best_df = pd.DataFrame()
            return self.df

        # Each assertion counts as 1 mark by default (keeps compatibility with prior code)
        df["max_score"] = 1
        df["total_possible"] = self.total_assertions
        df["score"] = df["score"].fillna(0).astype(float)
        df["percentage"] = (df["score"] / df["max_score"]) * 100

        # -------------------------
        # Compute per-question totals for each attempt (file)
        # -------------------------
        q_totals = (
            df.groupby(["file", "student", "roll_number", "question"], dropna=False)
            .agg(q_score=("score", "sum"))
            .reset_index()
        )

        # -------------------------
        # For each attempt (file), pick top-N questions by q_score and sum them -> best_n_total
        # -------------------------
        # Sort so top q_scores come first per attempt
        q_totals_sorted = q_totals.sort_values(
            ["file", "student", "roll_number", "q_score"],
            ascending=[True, True, True, False],
        )

        # Take top N questions per attempt and sum
        best_n_attempt = (
            q_totals_sorted.groupby(["file", "student", "roll_number"], sort=False)
            .head(self.best_n)
            .groupby(["file", "student", "roll_number"], sort=False)
            .agg(best_n_total=("q_score", "sum"))
            .reset_index()
        )

        # If an attempt has fewer than best_n questions, best_n_total will just be sum of whatever exists.
        # Ensure missing attempts (if any) are represented with zeros when merging
        best_n_attempt["best_n_total"] = best_n_attempt["best_n_total"].fillna(0).astype(float)

        # -------------------------
        # Scale best_n_total to desired range [scaled_min, scaled_max]
        # -------------------------
        # Determine raw min and max across attempts
        if best_n_attempt.empty:
            min_raw = max_raw = 0.0
        else:
            min_raw = float(best_n_attempt["best_n_total"].min())
            max_raw = float(best_n_attempt["best_n_total"].max())

        # Avoid division by zero: if all equal, set everyone to scaled_min
        if min_raw == max_raw:
            # assign scaled_min to all
            best_n_attempt["scaled"] = self.scaled_min
        else:
            scale_span = (self.scaled_max - self.scaled_min)
            best_n_attempt["scaled"] = (
                self.scaled_min
                + (best_n_attempt["best_n_total"] - min_raw) * scale_span / (max_raw - min_raw)
            )

        # Round scaled for nicer display but keep float precision in DataFrame
        best_n_attempt["scaled"] = best_n_attempt["scaled"].astype(float)

        # Save attempt-level DataFrame for use in HTML rendering
        self.attempt_scores_df = best_n_attempt.copy()

        # -------------------------
        # Merge attempt-level best_n_total back into main df for easy per-attempt rendering
        # -------------------------
        df = df.merge(
            best_n_attempt[["file", "student", "roll_number", "best_n_total", "scaled"]],
            on=["file", "student", "roll_number"],
            how="left",
        )

        # Fill missing best_n_total/scaled with zeros (e.g., attempts with no question rows)
        df["best_n_total"] = df["best_n_total"].fillna(0).astype(float)
        df["scaled"] = df["scaled"].fillna(self.scaled_min).astype(float)

        # -------------------------
        # Precompute student-level best across attempts (for summary modal)
        # Keep best_n_best (highest best_n_total across attempts) and its scaled value.
        # -------------------------
        if not self.attempt_scores_df.empty:
            # For each student, choose the attempt with maximum best_n_total. If multiple attempts
            # tie, pick the one with maximum scaled (should be same mapping).
            idx = self.attempt_scores_df.groupby(["student", "roll_number"])["best_n_total"].idxmax()
            student_best = self.attempt_scores_df.loc[idx].reset_index(drop=True)
            # If groupby.idxmax produced NaNs or duplicates, fallback safely
            student_best = (
                student_best[["student", "roll_number", "best_n_total", "scaled"]]
                .rename(columns={"best_n_total": "best_n_best", "scaled": "best_scaled"})
                .reset_index(drop=True)
            )
        else:
            student_best = pd.DataFrame(columns=["student", "roll_number", "best_n_best", "best_scaled"])

        self.student_best_df = student_best

        # Save df to object and return
        self.df = df
        return df

    # -------------------------------------------------------------------------
    def to_csv(self, path: str) -> Path:
        """Export the flattened DataFrame to CSV."""
        if self.df is None or self.df.empty:
            raise RuntimeError("Report not built yet or empty.")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(path, index=False)
        return path

    # -------------------------------------------------------------------------
    def to_html(self, path: str) -> Path:
        """
        Generate an interactive HTML report with filters.

        The output includes per-attempt info:
          - Total raw marks (sum of assertion scores)
          - Best-N questions total for that attempt
          - Scaled marks (mapped to scaled_range)

        Summary modal shows student-wise best (highest Best-N across attempts) and scaled.
        """
        if self.df is None:
            raise RuntimeError("Report not built yet.")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df = self.df.copy()

        # Include all rows for DataFrame completeness
        df_filtered = df.copy()

        # Filter out missing-identity rows for student dropdowns and summary only
        df_summary = df[df["assertion"] != "[missing student identity]"].copy()

        grouped = df_filtered.groupby(["file", "student", "roll_number"], sort=False)

        html_out = StringIO()

        html_out.write(
            """<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>Evaluator Report</title>
<style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    select, button { padding: 6px; font-size: 14px; margin-right: 10px; }
    table { border-collapse: collapse; width: 100%; margin-top: 10px; }
    th, td { border: 1px solid #ccc; padding: 6px; text-align: left; }
    th { background: #f2f2f2; }
    tr:nth-child(even) { background: #fafafa; }
    .student-block { margin-top: 20px; border: 1px solid #ddd; padding: 12px; border-radius: 6px; }
    .question-header { font-weight: bold; margin-top: 10px; font-size: 1.02em; color: #333; }
    .description { color: #555; margin-bottom: 8px; font-style: italic; }
    .passed { background-color: #e6ffe6; }
    .failed { background-color: #ffe6e6; }
    .summary { margin-top: 5px; font-weight: bold; color: #333; }
    #summaryModal { display: none; position: fixed; top: 8%; left: 50%; transform: translateX(-50%); width: 75%; max-height: 78vh; overflow-y: auto; background: white; border: 2px solid #555; border-radius: 8px; padding: 18px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); z-index: 1000; }
    #overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; }
    .close-btn { float: right; cursor: pointer; color: red; font-weight: bold; }
</style>
<script>
    function filterReports() {
        const studentVal = document.getElementById("studentSelect").value;
        const rollVal = document.getElementById("rollSelect").value;
        const fileVal = document.getElementById("fileSelect").value;
        document.querySelectorAll(".student-block").forEach(div => {
            const name = div.dataset.name;
            const roll = div.dataset.roll;
            const file = div.dataset.file;
            const show = (
                (studentVal === "" || name === studentVal) &&
                (rollVal === "" || roll === rollVal) &&
                (fileVal === "" || file === fileVal)
            );
            div.style.display = show ? "block" : "none";
        });
    }
    function sortStudents() {
        const sortType = document.getElementById("sortSelect").value;
        const container = document.getElementById("reportContainer");
        const blocks = Array.from(container.getElementsByClassName("student-block"));
        blocks.sort((a, b) => {
            const scoreA = parseFloat(a.dataset.total);
            const scoreB = parseFloat(b.dataset.total);
            const nameA = a.dataset.name.toLowerCase();
            const nameB = b.dataset.name.toLowerCase();
            const rollA = a.dataset.roll.toLowerCase();
            const rollB = b.dataset.roll.toLowerCase();
            const fileA = a.dataset.file.toLowerCase();
            const fileB = b.dataset.file.toLowerCase();
            switch(sortType) {
                case "marks": return scoreB - scoreA;
                case "name": return nameA.localeCompare(nameB);
                case "roll": return rollA.localeCompare(rollB);
                case "file": return fileA.localeCompare(fileB);
                default: return 0;
            }
        });
        blocks.forEach(b => container.appendChild(b));
    }
    function showSummary() {
        document.getElementById("overlay").style.display = "block";
        document.getElementById("summaryModal").style.display = "block";
    }
    function closeSummary() {
        document.getElementById("overlay").style.display = "none";
        document.getElementById("summaryModal").style.display = "none";
    }
</script>
</head>
<body>
<h2>Evaluator Report</h2>

<label for="sortSelect">Sort By:</label>
<select id="sortSelect" onchange="sortStudents()">
    <option value="marks">Total Marks (High → Low)</option>
    <option value="name">Student Name (A–Z)</option>
    <option value="roll">Roll Number (A–Z)</option>
    <option value="file">File Name (A–Z)</option>
</select>

<button onclick="showSummary()">Show Summary</button>

<label for="studentSelect">Student:</label>
<select id="studentSelect" onchange="filterReports()">
    <option value="">-- All Students --</option>
"""
        )

        # Student dropdowns (exclude missing identity rows)
        for student in sorted(df_summary["student"].dropna().unique()):
            html_out.write(f"<option value='{html_lib.escape(student)}'>{html_lib.escape(student)}</option>")
        html_out.write("</select>")

        html_out.write("""
<label for="rollSelect">Roll:</label>
<select id="rollSelect" onchange="filterReports()">
    <option value="">-- All Rolls --</option>
""")
        for roll in sorted(df_summary["roll_number"].dropna().astype(str).unique()):
            html_out.write(f"<option value='{html_lib.escape(str(roll))}'>{html_lib.escape(str(roll))}</option>")
        html_out.write("</select>")

        html_out.write("""
<label for="fileSelect">File:</label>
<select id="fileSelect" onchange="filterReports()">
    <option value="">-- All Files --</option>
""")
        for file in sorted({Path(f).name for f in df["file"].unique()}):
            html_out.write(f"<option value='{html_lib.escape(file)}'>{html_lib.escape(file)}</option>")
        html_out.write("</select><hr><div id='reportContainer'>")

        # --- Student sections (per attempt) ---
        for (file, student, roll_number), g in grouped:
            # total raw marks for the attempt
            total_score = float(g["score"].sum())
            total_possible = self.total_assertions
            percentage = round((total_score / total_possible) * 100, 2)

            # Best-N and scaled values (merged earlier into every row)
            best_n_val = float(g["best_n_total"].iloc[0]) if "best_n_total" in g.columns else 0.0
            scaled_val = float(g["scaled"].iloc[0]) if "scaled" in g.columns else float(self.scaled_min)

            html_out.write(
                f'<div class="student-block" data-name="{html_lib.escape(student)}" '
                f'data-roll="{html_lib.escape(str(roll_number))}" '
                f'data-file="{html_lib.escape(Path(file).name)}" '
                f'data-total="{total_score}">'
            )
            html_out.write(f"<h3>{html_lib.escape(student)} — {html_lib.escape(str(roll_number))}</h3>")
            html_out.write(f"<p><strong>File:</strong> {html_lib.escape(str(Path(file).name))}</p>")
            html_out.write(f"<p class='summary'>Total: {total_score}/{total_possible} ({percentage}%)</p>")

            # Add Best-N and Scaled info per attempt
            html_out.write(f"<p class='summary'>Best {self.best_n} Questions Total: {best_n_val}</p>")
            html_out.write(f"<p class='summary'>Scaled Marks ({self.scaled_min}–{self.scaled_max}): {round(scaled_val, 2)}</p>")

            # Per-question breakdown grouped by question
            for q, subdf in g.groupby("question", sort=False):
                html_out.write(f'<div class="question-block" data-qname="{html_lib.escape(str(q))}">')
                html_out.write(f'<div class="question-header">Question: {html_lib.escape(str(q))}</div>')
                desc = subdf["description"].iloc[0] if "description" in subdf.columns else ""
                if desc:
                    html_out.write(f'<div class="description">{html_lib.escape(desc)}</div>')
                html_out.write("<table><thead><tr><th>Assertion</th><th>Status</th><th>Score</th><th>Error</th></tr></thead><tbody>")
                for _, row in subdf.iterrows():
                    row_class = "passed" if row["status"] == "passed" else "failed"
                    html_out.write(
                        f"<tr class='{row_class}'><td>{html_lib.escape(str(row['assertion']))}</td>"
                        f"<td>{html_lib.escape(str(row['status']))}</td>"
                        f"<td>{row['score']}</td>"
                        f"<td>{html_lib.escape(str(row['error'])) if row.get('error') else ''}</td></tr>"
                    )
                html_out.write("</tbody></table></div>")
            html_out.write("</div>")  # end student-block

        # --- Summary modal (student-best across attempts) ---
        html_out.write("""
</div>
<div id="overlay" onclick="closeSummary()"></div>
<div id="summaryModal">
    <span class="close-btn" onclick="closeSummary()">✖</span>
    <h3>Student Summary (Highest Best-N Across Attempts)</h3>
    <table>
        <thead><tr>
        <th>Student</th><th>Roll Number</th>
        <th>Highest Best-N</th><th>Best out Of</th><th>Scaled Score</th>
        </tr></thead><tbody>
""")

        # Build summary rows from self.student_best_df
        out_of = min(self.best_n, self.total_assertions)  # Best-N score is at most N (each question worth 1)
        if not self.student_best_df.empty:
            for _, row in self.student_best_df.iterrows():
                student = row.get("student", "")
                roll = row.get("roll_number", "")
                best_n_best = float(row.get("best_n_best", 0.0))
                best_scaled = float(row.get("best_scaled", self.scaled_min))
                html_out.write(
                    f"<tr><td>{html_lib.escape(str(student))}</td>"
                    f"<td>{html_lib.escape(str(roll))}</td>"
                    f"<td>{best_n_best}</td>"
                    f"<td>{out_of}</td>"
                    f"<td>{round(best_scaled, 2)}</td></tr>"
                )
        else:
            html_out.write("<tr><td colspan='5'>No student summaries available.</td></tr>")

        html_out.write("</tbody></table></div></body></html>")

        # Write file
        path.write_text(html_out.getvalue(), encoding="utf8")
        return path


# -------------------------------------------------------------------------
# Example usage (uncomment to run as script / quick test)
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Quick synthetic example to demonstrate functionality.
    # Replace executed_results with your actual evaluator output structure.
    example_results = [
        {
            "student_path": "submissions/alice_attempt1.py",
            "execution": {
                "namespace": {"name": "Alice"},
                "student_meta": {"roll_number": "R001"}
            },
            "results": [
                {"question": "Q1", "assertion": "a1", "status": "passed", "score": 1, "description": "desc Q1"},
                {"question": "Q1", "assertion": "a2", "status": "failed", "score": 0},
                {"question": "Q2", "assertion": "b1", "status": "passed", "score": 1},
                {"question": "Q3", "assertion": "c1", "status": "passed", "score": 1},
            ]
        },
        {
            "student_path": "submissions/alice_attempt2.py",
            "execution": {
                "namespace": {"name": "Alice"},
                "student_meta": {"roll_number": "R001"}
            },
            "results": [
                {"question": "Q1", "assertion": "a1", "status": "passed", "score": 1},
                {"question": "Q2", "assertion": "b1", "status": "failed", "score": 0},
                {"question": "Q4", "assertion": "d1", "status": "passed", "score": 1},
                {"question": "Q5", "assertion": "e1", "status": "passed", "score": 1},
            ]
        },
        {
            "student_path": "submissions/bob_attempt1.py",
            "execution": {
                "namespace": {"name": "Bob"},
                "student_meta": {"roll_number": "R002"}
            },
            "results": [
                {"question": "Q1", "assertion": "a1", "status": "failed", "score": 0},
                {"question": "Q2", "assertion": "b1", "status": "failed", "score": 0},
                {"question": "Q3", "assertion": "c1", "status": "passed", "score": 1},
            ]
        },
    ]

    svc = ReportingService(
        executed_results=example_results,
        total_assertions=15,
        best_n=3,  # example: best 3 out of all questions (use 10 in real scenario)
        scaled_range=(10, 20),
        debug=True,
    )
    out_html = Path("evaluator_report_example.html")
    svc.to_html(out_html)
    print(f"HTML report written to: {out_html.resolve()}")
