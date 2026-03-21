#!/usr/bin/env python3
"""
Evaluation script for midsem_fib_fne assignment folders
Evaluates student submissions against solution notebooks
"""

import sys
from pathlib import Path

# Setup paths
repo = Path(__file__).resolve().parents[0]
sys.path.insert(0, str(repo))
sys.path.insert(0, str(repo / "src"))

from instantgrade import InstantGrader

def evaluate_test(test_name, solution_path, submissions_path, report_output_dir):
    """Evaluate a single test folder"""
    print(f"\n{'='*80}")
    print(f"Evaluating: {test_name}")
    print(f"Solution: {solution_path}")
    print(f"Submissions: {submissions_path}")
    print(f"{'='*80}\n")

    try:
        grader = InstantGrader(
            solution_file_path=solution_path,
            submission_folder_path=submissions_path,
            use_docker=False,  # Using local execution for speed
        )

        report = grader.run()

        if report is None:
            print(f"Error: Grader returned None for {test_name}")
            return False

        print(f"\n✓ Grading completed for {test_name}")

        # Generate HTML report
        report_output_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_output_dir / f"{test_name}_evaluation_report.html"

        try:
            written_path = grader.to_html(report_path)
            print(f"  ✓ HTML Report saved: {written_path}")
        except Exception as e:
            print(f"  ✗ Warning: HTML generation failed: {e}")
            print(f"  Report object: {grader.report}")
            return False

        return True

    except Exception as e:
        print(f"Error evaluating {test_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    # Paths
    base_path = Path("/Volumes/MacSSD/Areas/Github_Repositories/evaluator/data/midsem_fib_fne")

    # Test 1: Mid SEM Test 2
    test1_name = "Mid_SEM_Test_2"
    test1_solution = base_path / "Mid SEM Test 2" / "solution.ipynb"
    test1_submissions = base_path / "Mid SEM Test 2"
    test1_reports = base_path / "reports_mid_sem_test_2"

    # Test 2: Mid Sem TEST 3
    test2_name = "Mid_Sem_TEST_3"
    test2_solution = base_path / "Mid Sem TEST 3" / "solution.ipynb"
    test2_submissions = base_path / "Mid Sem TEST 3"
    test2_reports = base_path / "reports_mid_sem_test_3"

    # Run evaluations
    results = []

    results.append(evaluate_test(test1_name, test1_solution, test1_submissions, test1_reports))
    results.append(evaluate_test(test2_name, test2_solution, test2_submissions, test2_reports))

    # Summary
    print(f"\n{'='*80}")
    print("EVALUATION SUMMARY")
    print(f"{'='*80}")
    print(f"Mid SEM Test 2: {'✓ Success' if results[0] else '✗ Failed'}")
    print(f"Mid Sem TEST 3: {'✓ Success' if results[1] else '✗ Failed'}")
    print(f"\nReports generated in:")
    print(f"  - {test1_reports}")
    print(f"  - {test2_reports}")
    print(f"{'='*80}\n")

    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
