# How to Create and Use Solution Notebooks - Technical Guide

This guide explains the `InstantGrade` solution notebook format and how to create assessment materials that will be automatically graded.

---

## Understanding the Solution Notebook Format

### Core Concept

The `InstantGrade` system uses a **pattern-based parser** that looks for:

1. **Markdown cell starting with `##`** → Question description
2. **Immediately following code cell** → Function definition
3. **Next code cell** → Test assertions

This pattern is defined in `SolutionIngestion` class:

```python
# File: src/instantgrade/evaluators/python/ingestion/solution_ingestion.py

class SolutionIngestion:
    def understand_notebook_solution(self):
        """
        Expected pattern:
          [markdown: ## Question heading]
          [code: function definition]
          [code: asserts + helper code]
        """
```

### Why This Pattern?

The pattern-based approach allows:
- ✅ **Simple creation** - No special APIs needed, just normal notebooks
- ✅ **Visual clarity** - Questions and code are readable in Jupyter
- ✅ **Instructor-first** - Instructors write solutions normally
- ✅ **Flexible testing** - Multiple assertions per question
- ✅ **Easy maintenance** - Standard Jupyter notebook format

---

## Creating a Solution Notebook: Step-by-Step

### Step 1: Create a New Notebook

Create a blank Jupyter notebook. Add metadata cell first:

**Cell Type: Code**
```python
name = "Instructor Name"
roll_number = "0000"
```

This sets defaults that students will see. The system detects if a student hasn't changed these values and flags an identity error.

### Step 2: Create Your First Question

For each question, create THREE consecutive cells:

#### 2a. Question Description (Markdown Cell)

**Cell Type: Markdown**
```markdown
## Question 1: Find the maximum of three numbers
**Example:** Input `(4, 8, 10)` → `10`  
**Return:** The largest of the three numbers.
```

**Rules**:
- Must start with `##` (exactly 2 hashes)
- Can include markdown formatting
- Can have examples and requirements
- This becomes the "description" in grading reports

#### 2b. Function Definition (Code Cell)

**Cell Type: Code**
```python
def max_of_three(a: int, b: int, c: int) -> int:
    return max(a, b, c)
```

**Rules**:
- Must contain exactly ONE `def` statement
- The function name becomes the question identifier
- Type hints are recommended (for documentation)
- Keep it clean - no extra code here

#### 2c. Test Assertions (Code Cell)

**Cell Type: Code**
```python
assert max_of_three(4, 8, 10) == 10
assert max_of_three(20, 5, 15) == 20
assert max_of_three(1, 1, 1) == 1
```

**Rules**:
- Lines starting with `assert ` are test cases
- All other lines are considered "context code" (setup)
- Each assertion = 1 test point
- Can include helper functions BEFORE the assertions

#### Full Example with Context Code

```python
# Helper setup (optional)
test_data = {
    'case1': (4, 8, 10),
    'case2': (20, 5, 15),
    'case3': (1, 1, 1),
}

# Test assertions
assert max_of_three(4, 8, 10) == 10
assert max_of_three(20, 5, 15) == 20
assert max_of_three(1, 1, 1) == 1
```

### Step 3: Repeat for Each Question

Repeat the 3-cell pattern for as many questions as you have.

### Step 4: Save as `sample_solutions.ipynb`

Place the notebook in your assessment folder:

```
/path/to/assessment/
├── sample_solutions.ipynb    ← Your solution notebook
├── In class Practice Exam/   ← Student submissions folder
└── basic_python_flow.ipynb   ← Evaluation script
```

---

## How the Parser Works (Technical Details)

The `SolutionIngestion.understand_notebook_solution()` method:

### Step 1: Iterate Through Cells

```python
i = 0
while i < len(nb.cells):
    cell = nb.cells[i]
```

### Step 2: Detect Question Pattern

```python
if cell.cell_type == "markdown" and cell.source.strip().startswith("##"):
    description = cell.source.strip()
    # Found a question! Now look for function and assertions
```

### Step 3: Extract Function Definition

```python
if i + 1 < len(nb.cells):
    code_cell = nb.cells[i + 1]
    if code_cell.cell_type == "code":
        func_src = code_cell.source.strip()
        func_name = self._extract_function_name(func_src)
        # Extract the function name using AST parsing
```

### Step 4: Extract Assertions

```python
if func_name and i + 2 < len(nb.cells):
    test_cell = nb.cells[i + 2]
    if test_cell.cell_type == "code":
        for line in test_cell.source.splitlines():
            if line.strip().startswith("assert "):
                assert_lines.append(line.strip())
            else:
                # Treat as context/setup code
                setup_lines.append(line)
```

### Step 5: Store Question Metadata

```python
questions[func_name] = {
    "description": description,
    "function": func_src,
    "context_code": context_code,
    "tests": assert_lines,          # List of "assert ..." strings
    "assert_count": len(assert_lines),
}
```

### Output Structure

The parser returns:

```python
{
    "type": "notebook",
    "metadata": {"name": "...", "roll_number": "..."},
    "questions": {
        "max_of_three": {
            "description": "## Question 1: Find maximum...",
            "function": "def max_of_three(a, b, c):\n    return max(a, b, c)",
            "context_code": "",
            "tests": [
                "assert max_of_three(4, 8, 10) == 10",
                "assert max_of_three(20, 5, 15) == 20",
                "assert max_of_three(1, 1, 1) == 1",
            ],
            "assert_count": 3,
        },
        "other_function": {...},
    },
    "summary": {
        "total_questions": 2,
        "total_assertions": 6,  # 3 + 3
    }
}
```

---

## Running the Evaluation

### The Evaluator Pipeline

```python
from instantgrade import Evaluator

evaluator = Evaluator(
    solution_file_path="./sample_solutions.ipynb",
    submission_folder_path="./In class Practice Exam",
    use_docker=False,  # False = local execution, True = Docker sandbox
)

report = evaluator.run()
```

### Step 1: Parse Solution

```
SolutionIngestion.understand_notebook_solution()
  ↓
Returns: questions, metadata, summary
```

### Step 2: Discover Submissions

```
Find all *.ipynb files in submission folder
  ↓
Found: 26 notebooks
```

### Step 3: Execute Each Submission

For each student notebook:

```python
# Load student notebook
notebook = nbformat.read(student_file, as_version=4)

# Execute all cells (they define functions)
ExecutionService._execute_notebook_locally(notebook)
  ↓
Returns: student_namespace (contains all defined functions)
```

### Step 4: Run Assertions

For each question in the solution:

```python
# Get the student's function from their namespace
student_function = student_namespace["max_of_three"]

# Run each assertion
ComparisonService.run_assertions(
    student_namespace=student_namespace,
    assertions=[
        "assert max_of_three(4, 8, 10) == 10",
        "assert max_of_three(20, 5, 15) == 20",
        "assert max_of_three(1, 1, 1) == 1",
    ],
    question_name="max_of_three",
)
```

### Step 5: Collect Results

For each assertion:

```python
{
    "question": "max_of_three",
    "assertion": "assert max_of_three(4, 8, 10) == 10",
    "status": "passed" or "failed",
    "error": None or "AssertionError: 9 != 10",
    "score": 1 or 0,
    "description": "## Question 1: Find maximum..."
}
```

### Step 6: Generate Report

```python
evaluator.to_html(output_path)
  ↓
Creates: evaluation_report.html (189 KB)
```

---

## Assertion Evaluation Details

### How Assertions Are Executed

The `ComparisonService` evaluates assertions:

```python
# From src/instantgrade/evaluators/python/comparison/comparison_service.py

def run_assertions(self, assertions, student_namespace):
    for assertion_str in assertions:
        try:
            # Compile and execute: "assert student_func(...) == expected"
            exec(compile(assertion_str, "<assertion>", "exec"), student_namespace)
            # If it reaches here, assertion passed
            result = {"status": "passed", "error": None, "score": 1}
        except AssertionError as e:
            # Assertion failed
            result = {"status": "failed", "error": str(e), "score": 0}
```

### Rich Diff Generation

For comparison assertions like `assert result == expected`, the system generates diffs:

```python
# Example of rich diff
Expected: [1, 2, 3, 4, 5]
Actual:   [1, 2, 3, 4]
          Difference: Missing element 5
```

---

## Best Practices for Solution Notebooks

### ✅ DO

1. **Write clear question descriptions**
   ```markdown
   ## Calculate factorial of n
   **Example:** Input `5` → `120`
   **Edge cases:** Handle `n=0` → return `1`
   ```

2. **Use type annotations**
   ```python
   def factorial(n: int) -> int:
       if n <= 1:
           return 1
       return n * factorial(n - 1)
   ```

3. **Test edge cases**
   ```python
   assert factorial(0) == 1     # Edge case
   assert factorial(1) == 1     # Edge case
   assert factorial(5) == 120   # Normal case
   assert factorial(10) == 3628800  # Larger case
   ```

4. **Keep context code minimal**
   ```python
   # Good - minimal setup
   data = [1, 2, 3, 4, 5]
   assert sum(data) == 15
   
   # Avoid - complex setup makes debugging hard
   data = [i for i in range(100) if i % 2 == 0]
   complex_result = some_obscure_calculation(data)
   assert complex_result == 2450
   ```

### ❌ DON'T

1. **Don't mix code cells**
   ```python
   # ❌ BAD - Function and assertions in same cell
   def max_of_three(a, b, c):
       return max(a, b, c)
   
   assert max_of_three(4, 8, 10) == 10  # Should be separate cell!
   ```

2. **Don't skip markdown descriptions**
   ```python
   # ❌ BAD - No question heading
   def calculate_average(nums: list) -> float:
       ...
   ```

3. **Don't have multiple functions in one cell**
   ```python
   # ❌ BAD
   def function_a():
       ...
   
   def function_b():  # Parser only recognizes function_a!
       ...
   ```

4. **Don't use non-deterministic tests**
   ```python
   # ❌ BAD - Uses random numbers
   assert random.randint(1, 10) == 5
   
   # ✅ GOOD - Deterministic
   assert calculate_random_seed(42) == 5
   ```

---

## Troubleshooting

### Issue: Parser doesn't find questions

**Symptom**: Report shows "0 questions found"

**Cause**: Questions don't start with `##`

**Fix**:
```markdown
# Wrong - only one hash
## Correct - two hashes

## This will be recognized
```

### Issue: Assertions not evaluated

**Symptom**: Questions found but "0 assertions"

**Cause**: Assertions not in code cell OR not starting with `assert `

**Fix**:
```python
# ✅ Correct
assert function_name(...) == expected

# ❌ Wrong - comment instead of assert
# assert function_name(...) == expected

# ❌ Wrong - print statement
print(function_name(...) == expected)
```

### Issue: Student functions not found

**Symptom**: "NameError: name 'function_name' is not defined"

**Cause**: Student didn't define the function with correct name

**Fix**: Check student notebook contains:
```python
def function_name(...):
    # Implementation
```

### Issue: Type mismatch errors

**Symptom**: "AssertionError: True == False" (confusing)

**Cause**: Return type is different than expected

**Fix**: Ensure assertions match expected type:
```python
# If function returns string
assert function(...) == "Positive"  # Not 1 or True

# If function returns list
assert function(...) == [1, 2, 3]  # Not (1, 2, 3) or "1 2 3"
```

---

## Example: Complete Solution Notebook

Here's a minimal but complete example:

```python
# Cell 1: Metadata
name = "Dr. Smith"
roll_number = "0000"

# Cell 2: Question 1 Description (Markdown)
## Convert temperature from Celsius to Fahrenheit
**Formula:** F = (C × 9/5) + 32
**Example:** Input `0` → `32`, Input `100` → `212`

# Cell 3: Question 1 Solution (Code)
def celsius_to_fahrenheit(celsius: float) -> float:
    return (celsius * 9/5) + 32

# Cell 4: Question 1 Tests (Code)
assert celsius_to_fahrenheit(0) == 32
assert celsius_to_fahrenheit(100) == 212
assert celsius_to_fahrenheit(-40) == -40

# Cell 5: Question 2 Description (Markdown)
## Check if a string is a palindrome
**Example:** Input `"racecar"` → `True`, Input `"hello"` → `False`

# Cell 6: Question 2 Solution (Code)
def is_palindrome(text: str) -> bool:
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

# Cell 7: Question 2 Tests (Code)
assert is_palindrome("racecar") == True
assert is_palindrome("hello") == False
assert is_palindrome("A man a plan a canal Panama") == True
```

---

## Integration with Auto-Grading Infrastructure

The solution notebooks integrate with:

1. **Docker Execution** (`use_docker=True`)
   - Runs student code in isolated containers
   - Prevents malicious code from affecting host
   - Enforces timeouts (default 20s per question)

2. **HTML Reporting** (`evaluator.to_html()`)
   - Interactive student reports
   - Question-by-question breakdown
   - Visual pass/fail indicators

3. **CSV Export** (automatic fallback)
   - Tabular results for spreadsheet analysis
   - Grade book import compatible

4. **Logging & Debugging** (`log_level="DEBUG"`)
   - Detailed execution traces
   - Error diagnostics
   - Performance metrics

---

## Summary

Creating solution notebooks for InstantGrade:

1. ✅ Create a regular Jupyter notebook
2. ✅ Add metadata cell (name, roll_number)
3. ✅ For each question, add 3 consecutive cells:
   - Markdown: `## Question title` with description
   - Code: `def function_name():` with implementation
   - Code: `assert ...` with test cases (multiple OK)
4. ✅ Save as `sample_solutions.ipynb`
5. ✅ Run evaluator on submission folder
6. ✅ View HTML report with grades

The system automatically:
- Parses the notebook structure
- Extracts questions and assertions
- Executes student code safely
- Validates against test cases
- Generates detailed reports

This makes creating and grading assessments quick and repeatable!
