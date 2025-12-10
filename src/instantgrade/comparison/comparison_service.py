import traceback
from typing import List, Dict, Optional


def extract_assertion_line(code: str) -> str:
    """
    Returns the first line containing an 'assert' statement.
    Helps improve student feedback.
    """
    for line in code.splitlines():
        if line.strip().startswith("assert"):
            return line.strip()
    return code.strip()  # fallback: return full code


class ComparisonService:
    """
    Compares student execution results against instructor-defined assertions.

    Runs entirely inside a pre-sandboxed process (Docker container).
    """

    def _format_assertion_error(self, code: str, exc: AssertionError) -> str:
        """
        Produce a readable error for assertion failures.
        """
        assertion_line = extract_assertion_line(code)

        # If assertion has a message ("assert cond, 'msg'")
        if exc.args:
            return (
                f"Assertion failed.\n"
                f"Assertion: {assertion_line}\n"
                f"Message: {exc.args[0]}"
            )

        # Generic failure with no message
        return (
            f"Assertion failed.\n"
            f"Assertion: {assertion_line}\n"
            f"No message was provided. Add an assertion message for clarity."
        )

    def _format_general_error(self, code: str, exc: Exception) -> str:
        """
        Produce readable errors for all non-assertion exceptions.
        """
        return (
            f"Execution error.\n"
            f"Code: {code.strip()}\n"
            f"Error Type: {type(exc).__name__}\n"
            f"Details: {str(exc)}"
        )

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

        # -----------------------------------------------------
        # 1. Execute context/setup code once
        # -----------------------------------------------------
        if context_code:
            try:
                exec(compile(context_code, "<context_code>", "exec"), ns)
            except Exception as exc:
                # Cleaner, readable message for context-level failure
                clean_err = (
                    "Context setup failed.\n"
                    f"Error Type: {type(exc).__name__}\n"
                    f"Details: {str(exc)}\n"
                )

                results.append(
                    {
                        "question": question_name or "unknown",
                        "assertion": "[context setup]",
                        "status": "failed",
                        "error": clean_err,
                        "score": 0,
                    }
                )
                return results

        # -----------------------------------------------------
        # 2. Execute each assertion independently
        # -----------------------------------------------------
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

            except AssertionError as ae:
                clean_err = self._format_assertion_error(code, ae)

                results.append(
                    {
                        "question": question_name or "unknown",
                        "assertion": code,
                        "status": "failed",
                        "error": clean_err,
                        "score": 0,
                    }
                )

            except Exception as exc:
                clean_err = self._format_general_error(code, exc)

                results.append(
                    {
                        "question": question_name or "unknown",
                        "assertion": code,
                        "status": "failed",
                        "error": clean_err,
                        "score": 0,
                    }
                )

        return results
