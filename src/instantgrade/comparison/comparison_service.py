import traceback
from typing import List, Dict, Optional


class ComparisonService:
    """
    Compares student execution results against instructor-defined assertions.

    Runs entirely inside a pre-sandboxed process (Docker container).
    """

    def run_assertions(
        self,
        student_namespace: dict,
        assertions: List[str],
        question_name: Optional[str] = None,
        context_code: Optional[str] = None,
        timeout: Optional[int] = None,  # accepted but not enforced here
    ) -> List[Dict]:
        results: List[Dict] = []
        ns = student_namespace  # operate directly on the given namespace

        # 1. Execute context/setup code once
        if context_code:
            try:
                exec(compile(context_code, "<context_code>", "exec"), ns)
            except Exception:
                tb = traceback.format_exc()
                results.append(
                    {
                        "question": question_name or "unknown",
                        "assertion": "[context setup]",
                        "status": "failed",
                        "error": tb,
                        "score": 0,
                    }
                )
                # If context fails, we do not run assertions for this question
                return results

        # 2. Execute each assertion
        for code in assertions:
            try:
                exec(compile(code, "<assertion>", "exec"), ns)
                results.append(
                    {
                        "question": question_name or "unknown",
                        "assertion": code,
                        "status": "passed",
                        "error": None,
                        "score": 1,
                    }
                )
            except Exception:
                tb = traceback.format_exc()
                results.append(
                    {
                        "question": question_name or "unknown",
                        "assertion": code,
                        "status": "failed",
                        "error": tb,
                        "score": 0,
                    }
                )

        return results
