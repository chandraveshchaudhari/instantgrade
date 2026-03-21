# Quick Start Guide - InstantGrade Solution Notebooks

## TL;DR (Too Long; Didn't Read)

### 30-Second Summary

1. **Create solution notebook** with this pattern (repeat 3X for each question):
   - Markdown cell: `## Question Title`
   - Code cell: `def function_name(): ...`
   - Code cell: `assert function_name(...) == expected`

2. **Run evaluator**:
   ```python
   from instantgrade import Evaluator
   evaluator = Evaluator(solution_file_path="./sample_solutions.ipynb",
                        submission_folder_path="./submissions/")
   report = evaluator.run()
   evaluator.to_html("./report.html")
   ```

3. **View results** in the HTML report

---

## 5-Minute Setup

### 1. Create Solution Notebook

**File**: `sample_solutions.ipynb`

```
Cell 1 (Code):
    name = "Instructor"
    roll_number = "0000"

Cell 2 (Markdown):
    ## Question 1: Sum of two numbers
    **Example:** Input (3, 5) → 8

Cell 3 (Code):
    def sum_two(a: int, b: int) -> int:
        return a + b

Cell 4 (Code):
    assert sum_two(3, 5) == 8
    assert sum_two(0, 0) == 0
    assert sum_two(-1, 1) == 0

Cell 5 (Markdown):
    ## Question 2: Check if even
    **Example:** Input 4 → 'Even'

Cell 6 (Code):
    def check_even(n: int) -> str:
        if n % 2 == 0:
            return 'Even'
        else:
            return 'Odd'

Cell 7 (Code):
    assert check_even(4) == 'Even'
    assert check_even(5) == 'Odd'
    assert check_even(0) == 'Even'
```

### 2. Place Student Notebooks

```
project/
├── sample_solutions.ipynb
└── submissions/
    ├── student1.ipynb
    ├── student2.ipynb
    └── ... (all student notebooks)
```

### 3. Run Evaluation Script

**File**: `evaluate.py`

```python
from instantgrade import Evaluator
from pathlib import Path

# Setup paths
solution_file = Path("./sample_solutions.ipynb")
submission_folder = Path("./submissions")
output_file = Path("./report.html")

# Create evaluator
evaluator = Evaluator(
    solution_file_path=str(solution_file),
    submission_folder_path=str(submission_folder),
    use_docker=False,  # Use local execution
)

# Run evaluation
print("Running evaluation...")
report = evaluator.run()

# Generate report
print("Generating HTML report...")
evaluator.to_html(str(output_file))
print(f"Report saved to: {output_file}")
```

### 4. View Report

Open `report.html` in your browser.

---

## What You Get

### HTML Report Shows:

✅ **Overall Statistics**
- Total students
- Total assertions passed/failed
- Pass rate percentage

✅ **Per-Student Breakdown**
- Score for each student
- Questions with issues
- Detailed assertion failures

✅ **Per-Question Analysis**
- Which questions have common failures
- Test cases that are problematic
- Student error patterns

---

## Real Example: In Class Practice Exam

### What We Created

**Solution Notebook**: 7 questions, 21 assertions

```
1. check_number
   assert check_number(5) == 'Positive'
   assert check_number(-3) == 'Negative'
   assert check_number(0) == 'Zero'

2. numbers_1_to_n
   assert numbers_1_to_n(5) == [1, 2, 3, 4, 5]
   assert numbers_1_to_n(1) == [1]
   assert numbers_1_to_n(0) == []

3. even_numbers_1_to_n
   assert even_numbers_1_to_n(11) == [2, 4, 6, 8, 10]
   assert even_numbers_1_to_n(6) == [2, 4, 6]
   assert even_numbers_1_to_n(1) == []

... (4 more questions with 3 assertions each)
```

### Results

```
Total Students: 26
Total Assertions: 546
Passed: 519 ✅
Failed: 27
Pass Rate: 95.1%

Top Performers: 23 students (100% score)
Good: 2 students (85-90%)
Needs Help: 1 student (81%)
```

### Generated Files

```
/data/4ecoCPCG/
├── sample_solutions.ipynb ................ Solution with assertions
├── basic_python_flow.ipynb .............. Evaluation notebook
├── EVALUATION_SUMMARY.md ................. Overview and statistics
├── STUDENT_PERFORMANCE_DETAILS.md ........ Detailed per-student breakdown
├── TECHNICAL_GUIDE.md ................... How it works (documentation)
├── In class Practice Exam/ .............. Student submissions (26 files)
├── logs/ ............................... Debug logs
└── reports/
    └── evaluation_report.html ........... Interactive HTML report (189 KB)
```

---

## Common Questions

### Q: How do I add more questions?

**A:** Repeat the 3-cell pattern:
1. Markdown cell with `## Question Title`
2. Code cell with function definition
3. Code cell with assertions

No limit to number of questions!

### Q: What if a student names their function differently?

**A:** Their submission won't have the correct function. The evaluation will report "NameError" and they'll get 0 points for that question. This teaches proper function naming.

### Q: Can I use Docker for security?

**A:** Yes! Change to `use_docker=True`:
```python
evaluator = Evaluator(
    solution_file_path=str(solution_file),
    submission_folder_path=str(submission_folder),
    use_docker=True,  # Runs in sandboxed containers
)
```

Note: Docker containers use `/workspace/` path internally.

### Q: How do I reuse this for a different assessment?

**A:** Copy the template:
```bash
cp -r /data/4ecoCPCG/ /data/my_new_assessment/
# Edit sample_solutions.ipynb with your questions
# Place student notebooks in In class Practice Exam/
# Run evaluation
```

### Q: Can I grade non-function code?

**A:** The current system expects functions. For other patterns, you'd need custom evaluation logic. Future versions may support script-based assessments.

### Q: What if evaluation takes too long?

**A:** 
- Local execution (~20 seconds for 26 students with 21 assertions each)
- Docker execution (~2-3x slower due to container overhead)
- Configure timeout: `QUESTION_TIMEOUT=60` environment variable

### Q: Can students see the solution?

**A:** Students see the HTML report showing their:
- ✅ Passed assertions
- ❌ Failed assertions
- Full test error messages

They don't see the instructor's function implementation, only the assertions (which teach them what the expected behavior should be).

---

## Troubleshooting

### "0 questions found"

**Fix**: Check markdown cells start with exactly `##`:
```markdown
❌ # Only one hash
❌ ### Three hashes
✅ ## Exactly two hashes
```

### "AssertionError" on all tests

**Fix**: Check student function name matches solution:
- Solution: `def check_number(n):`
- Student must have: `def check_number(n):` (same name!)

### "ModuleNotFoundError"

**Fix**: Add to student notebooks or solution:
```python
import sys
from pathlib import Path
sys.path.append(str(Path().resolve().parent.parent / "src"))
```

### Only first question evaluated

**Fix**: Check cells are in correct order:
1. Markdown (##)
2. Code (function)
3. Code (asserts)
4. [Next question markdown]

All three must be consecutive!

---

## Next Steps

1. **Read**: `EVALUATION_SUMMARY.md` for overview
2. **Learn**: `TECHNICAL_GUIDE.md` for how it works
3. **Examine**: `sample_solutions.ipynb` as template
4. **Adapt**: Create your own solution notebook
5. **Run**: `basic_python_flow.ipynb` on student submissions
6. **View**: `report.html` for results

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `sample_solutions.ipynb` | ⭐ Use this as template for your assessments |
| `basic_python_flow.ipynb` | ⭐ Run this to evaluate students |
| `EVALUATION_SUMMARY.md` | Overview of what was done |
| `STUDENT_PERFORMANCE_DETAILS.md` | Per-student breakdown with analysis |
| `TECHNICAL_GUIDE.md` | Deep dive into how InstantGrade works |
| `README.md` | This file (you are here) |
| `In class Practice Exam/` | Student submissions (26 notebooks) |
| `reports/` | HTML report and results |
| `logs/` | Debug information |

---

## Key Takeaways

✅ **Easy to create** - Just a normal Jupyter notebook with a specific pattern

✅ **Automatic grading** - Evaluator runs all assertions

✅ **Detailed reports** - HTML report shows exactly where each student struggled

✅ **Reusable** - Copy and adapt for any Python function-based assessment

✅ **Safe** - Docker sandboxing available for untrusted student code

✅ **Scalable** - Works with 1 student or 100+ students

---

## Example: Your First Assessment (10 minutes)

### 1. Create `my_assessment.ipynb`

```
Cell 1: name = "Me"; roll_number = "0000"
Cell 2: ## Add two numbers | Example: 3+5=8
Cell 3: def add(a, b): return a + b
Cell 4: assert add(3, 5) == 8
        assert add(0, 0) == 0
```

### 2. Get student notebooks

```bash
mkdir submissions
# Copy student .ipynb files to submissions/
```

### 3. Run evaluation

```bash
python << 'EOF'
from instantgrade import Evaluator
evaluator = Evaluator(
    solution_file_path="./my_assessment.ipynb",
    submission_folder_path="./submissions",
    use_docker=False,
)
report = evaluator.run()
evaluator.to_html("./result.html")
EOF
```

### 4. Open `result.html` in browser

Done! ✅

---

## Support

For issues or questions:
1. Check `TECHNICAL_GUIDE.md` for how it works
2. Review `sample_solutions.ipynb` for pattern examples
3. Check `logs/` for error details
4. Re-read this guide's Troubleshooting section

Happy grading! 🎓
