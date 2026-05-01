"""Streamlit-based UI for InstantGrade.

Run with: `streamlit run /path/to/streamlit_app.py`
The CLI will point Streamlit to this file automatically.
"""
from pathlib import Path
import base64
import tempfile
import streamlit as st
import streamlit.components.v1 as components
import threading
import time
import logging
import json
import os
from datetime import datetime

from instantgrade.core.orchestrator import InstantGrader
import nbformat
import ast


st.set_page_config(page_title="InstantGrade UI", layout="centered")


RUNS_DIR = Path.home() / ".instantgrade" / "runs"


def _ensure_runs_dir():
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _render_html_report(html: str, *, height: int = 800) -> None:
    if hasattr(st, "iframe"):
        encoded = base64.b64encode(html.encode("utf8")).decode("ascii")
        st.iframe(f"data:text/html;base64,{encoded}", height=height)
        return

    components.html(html, height=height, scrolling=True)


def run_and_store(solution_path: str, submissions_path: str, use_docker: bool, best_n: int | None, ui_log_lines: list):
    """Run grader, capture logs into ui_log_lines and persist artifacts under RUNS_DIR.

    Returns: dict with run_dir and meta
    """
    _ensure_runs_dir()
    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # set up logging capture
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(run_dir / "run.log", encoding="utf8")
    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    file_handler.setFormatter(fmt)

    class UILogHandler(logging.Handler):
        def emit(self, record):
            try:
                msg = fmt.format(record)
            except Exception:
                msg = str(record)
            ui_log_lines.append(msg)
            # also write to file
            file_handler.emit(record)

    ui_handler = UILogHandler()
    ui_handler.setLevel(logging.INFO)

    root_logger.addHandler(ui_handler)
    root_logger.addHandler(file_handler)

    meta = {
        "solution": str(solution_path),
        "submissions": str(submissions_path),
        "use_docker": bool(use_docker),
        "best_n": int(best_n) if best_n else None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    try:
        solp = Path(solution_path)
        subp = Path(submissions_path)
        grader = InstantGrader(solp, subp, override_type="python", use_docker=use_docker, best_n=best_n)
        report = grader.run()

        # save HTML
        out_html = run_dir / "report.html"
        if hasattr(report, "to_html"):
            report.to_html(str(out_html))
        else:
            grader.to_html(str(out_html))

        # save executed results if available
        executed = getattr(report, "executed_results", None)
        if executed is None and hasattr(grader, "report"):
            executed = getattr(grader.report, "executed_results", None)
        if executed is not None:
            with open(run_dir / "executed.json", "w", encoding="utf8") as fhw:
                json.dump(executed, fhw, default=str, indent=2)

        # attempt PDF conversion (optional)
        pdf_path = None
        try:
            import pdfkit

            pdf_path = run_dir / "report.pdf"
            pdfkit.from_file(str(out_html), str(pdf_path))
            meta["pdf"] = str(pdf_path)
        except Exception:
            pdf_path = None

        meta["html"] = str(out_html)
        meta["log"] = str(run_dir / "run.log")

        # persist metadata
        with open(run_dir / "meta.json", "w", encoding="utf8") as mh:
            json.dump(meta, mh, indent=2, default=str)

        ui_log_lines.append("[Run completed]")
        return {"run_dir": str(run_dir), "meta": meta}

    except Exception as e:
        ui_log_lines.append(f"[Run failed] {e}")
        meta["error"] = str(e)
        with open(run_dir / "meta.json", "w", encoding="utf8") as mh:
            json.dump(meta, mh, indent=2, default=str)
        return {"run_dir": str(run_dir), "meta": meta}

    finally:
        try:
            root_logger.removeHandler(ui_handler)
            root_logger.removeHandler(file_handler)
        except Exception:
            pass


def list_runs():
    _ensure_runs_dir()
    runs = []
    for d in sorted(RUNS_DIR.iterdir(), reverse=True):
        meta_file = d / "meta.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf8") as fh:
                    meta = json.load(fh)
            except Exception:
                meta = {}
        else:
            meta = {}
        runs.append({"id": d.name, "dir": str(d), "meta": meta})
    return runs
 


def main():
    st.title("InstantGrade — Web UI")

    st.markdown("Provide the instructor solution notebook and a student submissions file or folder.")

    with st.form(key="grade_form"):
        st.markdown("**Instructor solution input**")
        sol_upload = st.file_uploader("Upload instructor .ipynb (optional)", type=["ipynb"], accept_multiple_files=False)
        solution_path = st.text_input("Or provide solution path on server", value="", help="Path to instructor solution notebook")

        st.markdown("**Student submissions input**")
        sub_upload = st.file_uploader("Upload student notebook(s) (optional, multiple allowed)", type=["ipynb"], accept_multiple_files=True)
        data_upload = st.file_uploader("Additional data files (CSV/JSON/etc., optional)", type=None, accept_multiple_files=True, help="Select any supporting data files required by student notebooks (e.g., .csv, .json). You can upload notebooks and data files together by multi-selecting them.")
        submissions_path = st.text_input("Or provide submissions folder/file path on server", value="", help="Path to student notebook or submissions directory")
        st.markdown(
            "**Upload options:** Use the file uploader to select multiple `.ipynb` files (Ctrl/Cmd+click) to upload a folder's contents without zipping, or paste a server path to the submissions folder. Uploading a ZIP is also supported and will be extracted."
        )

        use_docker = st.selectbox("Execution mode", ["docker", "local"], index=0) == "docker"
        best_n_raw = st.number_input("Best-N (optional)", min_value=0, value=0, step=1)
        submit = st.form_submit_button("Run Grader")

    if submit:
        # Decide solution path: uploaded file (saved to temp) or provided path
        try:
            if sol_upload is not None:
                tmp_sol = Path(tempfile.mkdtemp(prefix="instantgrade_sol_")) / "solution.ipynb"
                with open(tmp_sol, "wb") as fh:
                    fh.write(sol_upload.getbuffer())
                solp = str(tmp_sol)
            else:
                solp = solution_path.strip()

            # Decide submissions and data: uploaded files -> save to temp dir; or use provided path
            if (sub_upload and len(sub_upload) > 0) or (data_upload and len(data_upload) > 0):
                tmp_sub_dir = Path(tempfile.mkdtemp(prefix="instantgrade_subs_"))
                # Support uploading multiple notebooks and data files, or a single ZIP archive containing a submissions folder
                for f in (list(sub_upload) if sub_upload else []) + (list(data_upload) if data_upload else []):
                    outf = tmp_sub_dir / f.name
                    with open(outf, "wb") as fh:
                        fh.write(f.getbuffer())
                    # if a zip was uploaded, extract it
                    if f.name.lower().endswith('.zip'):
                        try:
                            import zipfile

                            with zipfile.ZipFile(outf, 'r') as zf:
                                zf.extractall(tmp_sub_dir)
                            # remove the zip after extraction
                            outf.unlink()
                        except Exception:
                            pass
                # If upload produced a single folder inside tmp_sub_dir, use that
                # otherwise use tmp_sub_dir itself
                children = [p for p in tmp_sub_dir.iterdir() if p.exists()]
                if len(children) == 1 and children[0].is_dir():
                    subp = str(children[0])
                else:
                    subp = str(tmp_sub_dir)
            else:
                subp = submissions_path.strip()

            if not solp or not subp:
                st.error("Please provide instructor solution and student submissions (either upload or server path).")
                return

            st.info("Starting grading — this may take a while for multiple submissions.")

            ui_logs = []
            result_holder = {}

            def worker():
                result_holder["res"] = run_and_store(solp, subp, use_docker, best_n_raw or None, ui_logs)

            t = threading.Thread(target=worker, daemon=True)
            t.start()

            log_box = st.empty()
            status_box = st.empty()
            last_len = 0
            while t.is_alive():
                if len(ui_logs) != last_len:
                    log_box.code("\n".join(ui_logs[-500:]))
                    last_len = len(ui_logs)
                status_box.info("Grading in progress...")
                time.sleep(0.5)

            # final flush
            if ui_logs:
                log_box.code("\n".join(ui_logs[-1000:]))
            status_box.empty()

            res = result_holder.get("res")
            if not res:
                st.error("Grading did not produce results.")
                return

            meta = res.get("meta", {})
            out_html = meta.get("html")
            out_pdf = meta.get("pdf")
            out_log = meta.get("log")

            st.success("Grading finished.")
            if out_html and Path(out_html).exists():
                html = Path(out_html).read_text(encoding="utf8")
                _render_html_report(html, height=800)
                with open(out_html, "rb") as fh:
                    st.download_button("Download report HTML", fh, file_name=f"instantgrade_report_{res['run_dir'].split(os.sep)[-1]}.html")

            if out_pdf and Path(out_pdf).exists():
                with open(out_pdf, "rb") as pf:
                    st.download_button("Download report PDF", pf, file_name=f"instantgrade_report_{res['run_dir'].split(os.sep)[-1]}.pdf")
            else:
                st.info("PDF export not available (requires pdfkit + wkhtmltopdf installed).")

            if out_log and Path(out_log).exists():
                with open(out_log, "rb") as lf:
                    st.download_button("Download run log", lf, file_name=f"instantgrade_runlog_{res['run_dir'].split(os.sep)[-1]}.txt")

        except Exception as e:
            st.exception(e)

    # --- Runs history ---
    st.markdown("---")
    st.header("Previous runs")
    runs = list_runs()
    if not runs:
        st.info("No previous runs found.")
    else:
        opts = [f"{r['id']} — {r['meta'].get('timestamp', '')} — {Path(r['meta'].get('html', '')).name if r['meta'].get('html') else ''}" for r in runs]
        sel = st.selectbox("Select a run to view", options=opts)
        idx = opts.index(sel)
        sel_run = runs[idx]
        st.write(sel_run['meta'])
        htmlp = sel_run['meta'].get('html')
        pdfp = sel_run['meta'].get('pdf')
        logp = sel_run['meta'].get('log')
        if htmlp and Path(htmlp).exists():
            if st.button("Open selected run HTML"):
                html = Path(htmlp).read_text(encoding='utf8')
                _render_html_report(html, height=800)
        if pdfp and Path(pdfp).exists():
            with open(pdfp, 'rb') as pf:
                st.download_button("Download selected run PDF", pf, file_name=Path(pdfp).name)
        if logp and Path(logp).exists():
            with open(logp, 'rb') as lf:
                st.download_button("Download selected run log", lf, file_name=Path(logp).name)
        
    # --- Generate student notebook from instructor solution ---
    st.markdown("---")
    st.header("Generate student notebook")
    st.markdown("Provide an instructor solution (`.ipynb`) to generate a student-facing notebook (stubs, no asserts).")
    gen_sol_upload = st.file_uploader("Upload instructor .ipynb for generation", type=["ipynb"], accept_multiple_files=False, key="gen_sol")
    gen_solution_path = st.text_input("Or provide solution path on server (for generation)", value="", help="Path to instructor solution notebook for generating student copy")
    if st.button("Generate student notebook"):
        try:
            # load notebook
            if gen_sol_upload is not None:
                raw = gen_sol_upload.getbuffer().tobytes()
                nb = nbformat.reads(raw.decode('utf8'), as_version=4)
            else:
                gp = gen_solution_path.strip()
                if not gp:
                    st.error("Please upload or provide a solution path to generate from.")
                else:
                    nb = nbformat.read(gp, as_version=4)

            # transform notebook: replace function bodies with pass and remove assert lines
            new_nb = nbformat.v4.new_notebook()
            new_cells = []
            i = 0
            # ensure there is a name/roll cell at top
            pasted_name = False
            while i < len(nb.cells):
                cell = nb.cells[i]
                if cell.cell_type == 'code' and 'name' in cell.source and 'roll_number' in cell.source and not pasted_name:
                    # replace with student placeholders
                    new_cells.append(nbformat.v4.new_code_cell("name = ''\nroll_number = ''"))
                    pasted_name = True
                    i += 1
                    continue

                if cell.cell_type == 'markdown' and cell.source.strip().startswith('##'):
                    # keep question markdown
                    new_cells.append(nbformat.v4.new_markdown_cell(cell.source))
                    # next should be function def
                    if i + 1 < len(nb.cells) and nb.cells[i+1].cell_type == 'code':
                        func_src = nb.cells[i+1].source
                        try:
                            tree = ast.parse(func_src)
                            func_node = None
                            for n in tree.body:
                                if isinstance(n, ast.FunctionDef):
                                    func_node = n
                                    break
                            if func_node is not None:
                                func_node.body = [ast.Pass()]
                                new_src = ast.unparse(func_node)
                                new_cells.append(nbformat.v4.new_code_cell(new_src))
                            else:
                                # just add empty code cell
                                new_cells.append(nbformat.v4.new_code_cell('# implement function here'))
                        except Exception:
                            new_cells.append(nbformat.v4.new_code_cell('# implement function here'))
                        # skip the next test/context cell if present
                        i += 3
                        continue

                # default: copy non-test cells that are not assertions
                if cell.cell_type == 'code':
                    # remove asserts from code cells
                    lines = []
                    for ln in cell.source.splitlines():
                        if ln.strip().startswith('assert '):
                            continue
                        lines.append(ln)
                    new_cells.append(nbformat.v4.new_code_cell('\n'.join(lines)))
                else:
                    new_cells.append(nbformat.v4.new_markdown_cell(cell.source))

                i += 1

            new_nb['cells'] = new_cells

            out_bytes = nbformat.writes(new_nb).encode('utf8')
            st.download_button('Download generated student notebook', out_bytes, file_name='student_copy.ipynb')

        except Exception as e:
            st.exception(e)
if __name__ == "__main__":
    main()
