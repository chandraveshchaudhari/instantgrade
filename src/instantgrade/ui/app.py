import os
import tempfile
from pathlib import Path
from flask import Flask, request, redirect, url_for, send_file, render_template_string, flash

from instantgrade.core.orchestrator import InstantGrader


FORM_HTML = """
<!doctype html>
<html>
  <head><meta charset='utf-8'><title>InstantGrade UI</title></head>
  <body>
    <h1>InstantGrade</h1>
    <form method="post" action="/grade">
      <div>
        <label>Instructor solution (.ipynb):</label><br>
        <input type="text" name="solution" placeholder="/path/to/solution.ipynb" size="80" required>
      </div>
      <div>
        <label>Student submissions (file or directory):</label><br>
        <input type="text" name="submissions" placeholder="/path/to/submissions_or_file" size="80" required>
      </div>
      <div>
        <label>Execution mode:</label>
        <select name="use_docker">
          <option value="true" selected>Docker (isolated)</option>
          <option value="false">Local (no Docker)</option>
        </select>
      </div>
      <div>
        <label>Best-N (optional):</label>
        <input type="number" name="best_n" min="0" placeholder="e.g., 3">
      </div>
      <div style="margin-top:8px">
        <button type="submit">Run Grader</button>
      </div>
    </form>
    <p style="margin-top:18px; color:#666">After grading finishes the report HTML will be returned for download/viewing.</p>
  </body>
 </html>
"""


def create_app():
    app = Flask(__name__)
    # Minimal secret for flashing; this UI is for local use only
    app.secret_key = os.environ.get("INSTANTGRADE_UI_SECRET", "instantgrade-local-secret")


    @app.route("/", methods=["GET"])
    def index():
        return render_template_string(FORM_HTML)


    @app.route("/grade", methods=["POST"])
    def grade():
        solution = request.form.get("solution")
        submissions = request.form.get("submissions")
        use_docker = request.form.get("use_docker", "true").lower() == "true"
        best_n_raw = request.form.get("best_n")

        if not solution or not submissions:
            flash("Both solution and submissions paths are required.")
            return redirect(url_for("index"))

        solp = Path(solution)
        subp = Path(submissions)

        if not solp.exists():
            flash(f"Solution path does not exist: {solp}")
            return redirect(url_for("index"))

        if not subp.exists():
            flash(f"Submissions path does not exist: {subp}")
            return redirect(url_for("index"))

        try:
            best_n = int(best_n_raw) if best_n_raw else None
        except Exception:
            best_n = None

        # Run grader synchronously (small classes of usage). Write report to a
        # temp HTML file and return it to the user.
        try:
            grader = InstantGrader(solp, subp, override_type="python", use_docker=use_docker, best_n=best_n)
            report = grader.run()

            tmp_dir = Path(tempfile.mkdtemp(prefix="instantgrade-"))
            out_path = tmp_dir / "report.html"
            # `report` should be a ReportingService; use its to_html
            if hasattr(report, "to_html"):
                report.to_html(str(out_path))
            else:
                # Fallback: try router to_html
                grader.to_html(str(out_path))

            return send_file(str(out_path), mimetype="text/html")

        except Exception as e:
            # For local UI usage show the error message
            return f"<h2>Grading failed</h2><pre>{str(e)}</pre>", 500


    return app
