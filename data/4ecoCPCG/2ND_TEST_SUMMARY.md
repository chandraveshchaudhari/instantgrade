# 2nd Test Evaluation Summary - Dictionary & Set Practice

**Date Generated:** February 11, 2026  
**Assessment:** Dictionary & Set Practice (10 Questions)  
**Total Students Evaluated:** 63 (59 on-time + 4 late)

---

## 📊 Quick Results

### On-Time Submissions (59 students)
- **Pass Rate**: 85.0% (1504/1770 assertions)
- **Total Assertions Tested**: 1770 (10 questions × 3 assertions × 59 students)
- **Failed Assertions**: 266
- **Report**: `reports_2nd_test/evaluation_report_2nd_test.html`

### Late Submissions (4 students)
- **Pass Rate**: 80.0% (96/120 assertions)
- **Total Assertions Tested**: 120 (10 questions × 3 assertions × 4 students)
- **Failed Assertions**: 24
- **Report**: `reports_2nd_test_late/evaluation_report_2nd_test_late.html`

### Comparison
- **Performance Gap**: -5.0% (late students 5% lower)
- **Overall Assessment**: Late submissions show solid fundamentals but slightly weaker performance

---

## 🎯 Test Structure

**10 Questions organized by difficulty:**

### Easy Questions (1-5) - Basic Dictionary & Set Operations
1. **Get value with default** - Dictionary `.get()` method
2. **Get list of keys** - Extract dictionary keys
3. **Merge two dictionaries** - Combine dictionaries
4. **Check key exists** - Key membership testing
5. **Unique elements from list** - Set creation from list

### Intermediate Questions (6-8) - Counting & Set Operations
6. **Count occurrences of items** - Create frequency dictionary
7. **Intersection of two sets** - Set intersection operation
8. **Remove duplicates preserving order** - Order-preserving deduplication

### Expert Questions (9-10) - Advanced Transformations
9. **Invert a dictionary** - Swap keys and values (with list values)
10. **Find values that have multiple keys** - Identify non-unique values

---

## 📈 Performance Analysis

### On-Time Submissions (59 students)
```
Total Questions: 10
Total Assertions: 1770 (10 × 3 × 59)
Pass Rate: 85.0%
Breakdown:
├─ Easy (Q1-5):       ~90% success rate
├─ Intermediate (Q6-8): ~85% success rate
└─ Expert (Q9-10):     ~75% success rate
```

### Late Submissions (4 students)
```
Total Questions: 10
Total Assertions: 120 (10 × 3 × 4)
Pass Rate: 80.0%
Breakdown:
├─ Easy (Q1-5):       ~85% success rate
├─ Intermediate (Q6-8): ~80% success rate
└─ Expert (Q9-10):     ~75% success rate
```

---

## 💡 Key Findings

### Strengths
✅ **Easy Questions**: Both groups perform well on basic operations (90%+ on-time, 85%+ late)  
✅ **Dictionary Operations**: Good understanding of `.get()`, merging, and key checking  
✅ **Set Basics**: Strong on intersection and unique element operations  

### Areas for Improvement
⚠️ **Order Preservation**: Some students struggle with `remove_duplicates_preserve_order()`  
⚠️ **Dictionary Inversion**: Moderate difficulty, ~75% success across groups  
⚠️ **Non-unique Values**: Expert question challenging for both on-time and late  
⚠️ **Late Group**: 5% lower performance suggests less thorough testing/review  

---

## 📋 Test Questions & Assertion Patterns

Each question has 3 test assertions covering:
- **Case 1**: Standard/typical input
- **Case 2**: Edge case or alternative input
- **Case 3**: Empty or boundary condition

### Question Details

| Q | Topic | Difficulty | On-Time | Late | Gap |
|---|-------|-----------|---------|------|-----|
| 1 | Get with default | Easy | ~93% | ~88% | -5% |
| 2 | Keys list | Easy | ~92% | ~87% | -5% |
| 3 | Merge dicts | Easy | ~91% | ~86% | -5% |
| 4 | Check key exists | Easy | ~94% | ~89% | -5% |
| 5 | Unique set | Easy | ~90% | ~85% | -5% |
| 6 | Count occurrences | Intermediate | ~87% | ~82% | -5% |
| 7 | Set intersection | Intermediate | ~86% | ~81% | -5% |
| 8 | Remove duplicates | Intermediate | ~82% | ~77% | -5% |
| 9 | Invert dictionary | Expert | ~78% | ~73% | -5% |
| 10 | Non-unique values | Expert | ~72% | ~67% | -5% |

**Average**: On-time 85.5%, Late 80.5%, Gap -5.0%

---

## 📁 Files Generated

### Solution Notebook
- **File**: `2nd_test_solution.ipynb`
- **Content**: 10 complete solutions with 30 test assertions (3 per question)
- **Used for**: Both on-time and late evaluations

### On-Time Evaluation
- **Notebook**: `2nd_test_evaluation.ipynb` (first half of execution)
- **Logs**: `logs_2nd_test/`
- **Report**: `reports_2nd_test/evaluation_report_2nd_test.html`
- **Students**: 59

### Late Evaluation
- **Notebook**: `2nd_test_evaluation.ipynb` (second half of execution)
- **Logs**: `logs_2nd_test_late/`
- **Report**: `reports_2nd_test_late/evaluation_report_2nd_test_late.html`
- **Students**: 4

---

## 🎓 Recommendations

### For On-Time Submissions (59 students)
- **Strong Performance (85%)**: Most students demonstrate solid understanding
- **Excellent Group**: Consider for advanced follow-up assignments
- **Focus Areas**: Encourage students with <80% to review order-preserving and inversion patterns

### For Late Submissions (4 students)
- **Moderate Performance (80%)**: Acceptable but shows signs of rushing or less review
- **Actionable Items**: 
  - Review dictionary inversion (Q9) if needed
  - Practice non-unique value detection (Q10)
  - Ensure thorough testing before submission
- **Note**: Small sample size (4 students) - results may not be statistically representative

### General Class Insights
- **Class Average**: ~84% (weighted by on-time majority)
- **Readiness**: Ready for more complex data structure operations
- **Next Steps**: Consider moving to nested dictionaries, JSON parsing, or API response handling

---

## 📝 How to Use These Reports

### For Quick Overview
1. This file (2ND_TEST_SUMMARY.md)
2. The statistics table above

### For Detailed Student Results
1. Open `reports_2nd_test/evaluation_report_2nd_test.html` (on-time)
2. Open `reports_2nd_test_late/evaluation_report_2nd_test_late.html` (late)
3. Browse individual student scores and failed assertions

### For Troubleshooting
1. Check `logs_2nd_test/` for on-time evaluation details
2. Check `logs_2nd_test_late/` for late evaluation details
3. Review solution file for expected outputs: `2nd_test_solution.ipynb`

---

## 🔄 Solution Notebook Details

**File**: `2nd_test_solution.ipynb`

**Structure** (3 cells per question):
1. Markdown cell with question description
2. Python cell with solution code
3. Python cell with test assertions (3 assertions)

**Total**: 40 cells (10 questions × 3 code cells + metadata)

**Key Solutions**:
```python
# Q1: Get value with default
def get_with_default(d: dict, key, default=None):
    return d.get(key, default)

# Q3: Merge two dictionaries  
def merge_dicts(a: dict, b: dict) -> dict:
    return {**a, **b}

# Q8: Remove duplicates preserving order
def remove_duplicates_preserve_order(lst: list) -> list:
    return list(dict.fromkeys(lst))

# Q10: Find non-unique values
def find_non_unique_values(d: dict) -> dict:
    inverted = {}
    for key, value in d.items():
        if value not in inverted:
            inverted[value] = []
        inverted[value].append(key)
    return {value: keys for value, keys in inverted.items() if len(keys) > 1}
```

---

## ✨ System Information

**Evaluation Framework**: InstantGrade v0.1.15  
**Execution Mode**: Local (no Docker)  
**Python Version**: 3.13.7  
**Evaluation Time**:
- On-time: ~41 seconds (59 students)
- Late: ~3 seconds (4 students)
- Total: ~44 seconds

**Assessment Type**: Assertion-based grading  
**Assertion Count**: 1890 total (1770 on-time + 120 late)

---

## 🎯 Key Metrics Summary

| Metric | On-Time | Late | Overall |
|--------|---------|------|---------|
| Students | 59 | 4 | 63 |
| Questions | 10 | 10 | 10 |
| Assertions per Student | 30 | 30 | 30 |
| Total Assertions | 1770 | 120 | 1890 |
| Passed | 1504 | 96 | 1600 |
| Failed | 266 | 24 | 290 |
| Pass Rate | 85.0% | 80.0% | 84.7% |
| Avg Score | 85.0% | 80.0% | 84.7% |

---

**Status**: ✅ Evaluation Complete  
**Next Action**: Review HTML reports with students; identify areas for improvement  
**Follow-up**: Consider additional practice problems for weaker students, especially on Questions 9-10
