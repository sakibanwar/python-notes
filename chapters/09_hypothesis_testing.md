# Hypothesis Testing

In this chapter, we'll learn how to use Python to answer questions like "Is this difference real or just random chance?" This is the realm of **hypothesis testing** — one of the most important tools in statistical analysis.

## Why Hypothesis Testing?

Imagine you're analysing exam scores from two classes. Class A has an average of 72% and Class B has an average of 75%. Is Class B genuinely better, or could this 3% difference just be due to random variation?

Without statistical testing, we're just guessing. Hypothesis testing gives us a rigorous framework to make decisions based on data.

## The Logic of Hypothesis Testing

Hypothesis testing follows a specific logic that might seem backwards at first:

1. **Assume there's no effect** (the "null hypothesis")
2. **Calculate how likely** we'd see our data if this assumption were true
3. **If it's very unlikely**, reject the assumption and conclude there IS an effect

Think of it like a courtroom: we assume innocence (null hypothesis) until the evidence is overwhelming enough to conclude guilt (reject the null).

### Key Terms

| Term | Definition | Example |
|------|------------|---------|
| **Null Hypothesis (H₀)** | The "no effect" assumption | "There's no difference between the two classes" |
| **Alternative Hypothesis (H₁)** | What we're trying to show | "There IS a difference between the two classes" |
| **p-value** | Probability of seeing our data (or more extreme) if H₀ is true | p = 0.03 means 3% chance |
| **Significance Level (α)** | Our threshold for "unlikely enough" | Typically α = 0.05 (5%) |
| **Test Statistic** | A number that summarises how far our data is from H₀ | t-statistic, z-score |

## Setting Up: The scipy Library

For hypothesis testing in Python, we'll use **scipy** (Scientific Python), specifically the `stats` module:

```python
import pandas as pd
import numpy as np
from scipy import stats
```

If scipy isn't installed, run `pip install scipy` in your terminal.

## The One-Sample t-Test

The simplest hypothesis test asks: "Is the mean of my sample different from a specific value?"

### Example: Testing Average Scores

A university claims that the average score on their entrance exam is 70. You collect scores from 15 students and want to test this claim.

```python
import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp

# Sample of 15 student scores
scores = pd.Series([72, 68, 75, 71, 69, 74, 73, 70, 76, 72, 71, 68, 74, 73, 72])

# Check the sample mean
print(f"Sample mean: {scores.mean():.2f}")
print(f"Sample size: {len(scores)}")
```

```
Sample mean: 71.87
Sample size: 15
```

The sample mean is 71.87, slightly higher than the claimed 70. But is this difference statistically significant?

### Setting Up the Hypotheses

- **H₀ (Null)**: The true mean equals 70 (μ = 70)
- **H₁ (Alternative)**: The true mean does not equal 70 (μ ≠ 70)

### Running the Test

```python
# Perform one-sample t-test
t_statistic, p_value = ttest_1samp(scores, popmean=70)

print(f"t-statistic: {t_statistic:.4f}")
print(f"p-value: {p_value:.4f}")
```

```
t-statistic: 2.5147
p-value: 0.0247
```

### Interpreting the Results

The **p-value of 0.0247** means: "If the true mean really were 70, there's only a 2.47% chance of seeing a sample mean this different (or more different) by random chance."

Since 0.0247 < 0.05 (our significance level), we **reject the null hypothesis**. The evidence suggests the true average score is different from 70.

```{note}
The t-statistic (2.51) tells us how many "standard errors" our sample mean is from the hypothesised value. The further from zero, the stronger the evidence against H₀.
```

### Making a Decision

The standard decision rule:

| p-value | Decision | Interpretation |
|---------|----------|----------------|
| p < 0.05 | Reject H₀ | Evidence of a difference (statistically significant) |
| p ≥ 0.05 | Fail to reject H₀ | No evidence of a difference |

```{warning}
"Fail to reject H₀" is NOT the same as "accept H₀"! We never prove the null hypothesis is true — we just don't have enough evidence to reject it.
```

## The Two-Sample t-Test

More commonly, we want to compare two groups: "Is there a difference between Group A and Group B?"

### Example: Comparing Two Classes

Let's compare exam scores from two different teaching methods:

```python
from scipy.stats import ttest_ind

# Scores from two classes
class_A = pd.Series([80, 90, 78, 60, 70, 85, 72, 68])
class_B = pd.Series([82, 87, 81, 68, 76, 88, 79, 73])

# Compare means
print(f"Class A mean: {class_A.mean():.2f}")
print(f"Class B mean: {class_B.mean():.2f}")
print(f"Difference: {class_B.mean() - class_A.mean():.2f}")
```

```
Class A mean: 75.38
Class B mean: 79.25
Difference: 3.88
```

Class B scored about 4 points higher on average. But is this difference real or just random variation?

### Setting Up the Hypotheses

- **H₀ (Null)**: The means are equal (μ_A = μ_B)
- **H₁ (Alternative)**: The means are different (μ_A ≠ μ_B)

### Running the Two-Sample t-Test

```python
# Perform independent samples t-test
t_statistic, p_value = ttest_ind(class_A, class_B)

print(f"t-statistic: {t_statistic:.4f}")
print(f"p-value: {p_value:.4f}")
```

```
t-statistic: -0.8879
p-value: 0.3911
```

### Interpreting the Results

The p-value of 0.3911 is **much greater than 0.05**. This means:

- If there truly were no difference between the classes, we'd see a difference this large (or larger) about 39% of the time just by chance.
- This is NOT unusual under the null hypothesis.
- We **fail to reject H₀** — there's no statistically significant evidence that the teaching methods produce different results.

```{tip}
A non-significant result doesn't mean the groups are identical. It means we don't have enough evidence to conclude they're different. With more data, we might find a significant difference.
```

## Practical Example: Analysing Survey Data

Let's work through a more realistic example using a larger dataset:

```python
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, ttest_1samp

# Set seed for reproducibility
np.random.seed(42)

# Create employee satisfaction survey data
survey = pd.DataFrame({
    'employee_id': range(1, 101),
    'department': ['Sales'] * 50 + ['Marketing'] * 50,
    'satisfaction': np.concatenate([
        np.random.normal(6.5, 1.5, 50),  # Sales: mean ~6.5
        np.random.normal(7.2, 1.4, 50)   # Marketing: mean ~7.2
    ]).clip(1, 10).round(1)
})

survey.head(10)
```

```
   employee_id department  satisfaction
0            1      Sales           5.7
1            2      Sales           6.3
2            3      Sales           7.5
3            4      Sales           8.8
4            5      Sales           6.1
5            6      Sales           6.1
6            7      Sales           8.9
7            8      Sales           6.5
8            9      Sales           6.8
9           10      Sales           7.2
```

### Question 1: Is Overall Satisfaction Different from 7.0?

The company's target is a satisfaction score of 7.0. Let's test whether the overall average meets this target.

```python
# Overall satisfaction statistics
print(f"Overall mean satisfaction: {survey['satisfaction'].mean():.2f}")
print(f"Overall std: {survey['satisfaction'].std():.2f}")

# One-sample t-test: is mean different from 7.0?
t_stat, p_value = ttest_1samp(survey['satisfaction'], 7.0)
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("\nResult: Reject H₀ - Average satisfaction IS significantly different from 7.0")
else:
    print("\nResult: Fail to reject H₀ - No significant difference from 7.0")
```

```
Overall mean satisfaction: 6.86
Overall std: 1.51

t-statistic: -0.9157
p-value: 0.3621

Result: Fail to reject H₀ - No significant difference from 7.0
```

### Question 2: Is There a Difference Between Departments?

```python
# Split by department
sales = survey[survey['department'] == 'Sales']['satisfaction']
marketing = survey[survey['department'] == 'Marketing']['satisfaction']

print(f"Sales mean: {sales.mean():.2f}")
print(f"Marketing mean: {marketing.mean():.2f}")
print(f"Difference: {marketing.mean() - sales.mean():.2f}")

# Two-sample t-test
t_stat, p_value = ttest_ind(sales, marketing)
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("\nResult: Reject H₀ - Departments have significantly different satisfaction")
else:
    print("\nResult: Fail to reject H₀ - No significant difference between departments")
```

```
Sales mean: 6.52
Marketing mean: 7.19
Difference: 0.67

t-statistic: -2.3012
p-value: 0.0235

Result: Reject H₀ - Departments have significantly different satisfaction
```

Marketing has significantly higher satisfaction than Sales (p = 0.023).

## One-Tailed vs Two-Tailed Tests

By default, `ttest_ind` performs a **two-tailed test** — it checks if the means are *different* (either higher or lower). Sometimes you want a **one-tailed test** that only checks one direction.

### Two-Tailed Test (Default)

- **H₀**: μ_A = μ_B
- **H₁**: μ_A ≠ μ_B
- Tests for any difference

### One-Tailed Test

- **H₀**: μ_A ≥ μ_B
- **H₁**: μ_A < μ_B
- Tests if A is specifically *lower* than B

```python
# For a one-tailed test, divide the p-value by 2
# (only valid if the observed difference is in the expected direction)

t_stat, p_value_two_tailed = ttest_ind(sales, marketing)
p_value_one_tailed = p_value_two_tailed / 2

print(f"Two-tailed p-value: {p_value_two_tailed:.4f}")
print(f"One-tailed p-value: {p_value_one_tailed:.4f}")
```

```
Two-tailed p-value: 0.0235
One-tailed p-value: 0.0118
```

```{note}
One-tailed tests are more powerful (more likely to detect an effect) but should only be used when you have a clear directional hypothesis *before* seeing the data. When in doubt, use the two-tailed test.
```

## Understanding p-Values More Deeply

### What the p-Value IS

The p-value is the probability of observing data as extreme as (or more extreme than) what we got, **assuming the null hypothesis is true**.

A p-value of 0.03 means: "If there really were no effect, we'd see results this extreme only 3% of the time."

### What the p-Value is NOT

Common misconceptions:

| Wrong Interpretation | Correct Understanding |
|---------------------|----------------------|
| "There's a 3% chance the null is true" | p-value says nothing about H₀ being true |
| "There's a 97% chance the alternative is true" | p-value doesn't give probability of hypotheses |
| "The effect is important/large" | p-value measures evidence, not effect size |
| "Results are definitely real" | Low p-values can still be false positives |

### Effect Size Matters Too

A statistically significant result isn't necessarily practically important. Consider:

```python
# Large sample with tiny difference
np.random.seed(123)
group_1 = np.random.normal(100, 15, 10000)  # Mean = 100
group_2 = np.random.normal(100.5, 15, 10000)  # Mean = 100.5

t_stat, p_value = ttest_ind(group_1, group_2)
print(f"Difference in means: {group_2.mean() - group_1.mean():.2f}")
print(f"p-value: {p_value:.6f}")
```

```
Difference in means: 0.59
p-value: 0.002814
```

The result is "significant" (p < 0.05), but the actual difference is tiny — only 0.6 points on a scale where the standard deviation is 15. This might not matter practically!

## Common Significance Levels

While 0.05 is the most common threshold, different fields use different standards:

| Level | Notation | Interpretation |
|-------|----------|----------------|
| 0.10 | * | Marginally significant |
| 0.05 | ** | Significant |
| 0.01 | *** | Highly significant |
| 0.001 | **** | Very highly significant |

```python
def interpret_p_value(p):
    """Return significance level interpretation."""
    if p < 0.001:
        return "*** (p < 0.001) - Very highly significant"
    elif p < 0.01:
        return "** (p < 0.01) - Highly significant"
    elif p < 0.05:
        return "* (p < 0.05) - Significant"
    elif p < 0.10:
        return ". (p < 0.10) - Marginally significant"
    else:
        return "ns (p >= 0.10) - Not significant"

# Example usage
print(interpret_p_value(0.0235))
```

```
* (p < 0.05) - Significant
```

## Other Common Tests

The t-test is just one of many hypothesis tests. Here are some others available in scipy:

### Chi-Square Test (for Categorical Data)

Tests whether two categorical variables are independent:

```python
from scipy.stats import chi2_contingency

# Contingency table: department vs satisfaction category
contingency = pd.DataFrame({
    'High': [15, 25],
    'Medium': [20, 18],
    'Low': [15, 7]
}, index=['Sales', 'Marketing'])

print(contingency)

chi2, p_value, dof, expected = chi2_contingency(contingency)
print(f"\nChi-square statistic: {chi2:.4f}")
print(f"p-value: {p_value:.4f}")
```

```
       High  Medium  Low
Sales    15      20   15
Marketing 25      18    7

Chi-square statistic: 5.4251
p-value: 0.0663
```

### Mann-Whitney U Test (Non-Parametric Alternative)

When data isn't normally distributed, use this instead of the t-test:

```python
from scipy.stats import mannwhitneyu

# Non-normal data
group_a = [1, 2, 2, 3, 3, 3, 4, 5, 100]  # Has outlier
group_b = [2, 3, 3, 4, 4, 4, 5, 5, 6]

stat, p_value = mannwhitneyu(group_a, group_b)
print(f"U statistic: {stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

```
U statistic: 28.5000
p-value: 0.3280
```

## A Complete Hypothesis Testing Workflow

Here's a step-by-step approach for any hypothesis test:

```python
def hypothesis_test_workflow(sample1, sample2=None, pop_mean=None, alpha=0.05):
    """
    Complete workflow for hypothesis testing.

    For one-sample: provide sample1 and pop_mean
    For two-sample: provide sample1 and sample2
    """
    from scipy.stats import ttest_1samp, ttest_ind

    print("="*50)
    print("HYPOTHESIS TESTING WORKFLOW")
    print("="*50)

    # Step 1: Descriptive statistics
    print("\n1. DESCRIPTIVE STATISTICS")
    print(f"   Sample 1: n={len(sample1)}, mean={np.mean(sample1):.2f}, std={np.std(sample1):.2f}")

    if sample2 is not None:
        print(f"   Sample 2: n={len(sample2)}, mean={np.mean(sample2):.2f}, std={np.std(sample2):.2f}")
        test_type = "Two-sample"
    else:
        print(f"   Population mean to test: {pop_mean}")
        test_type = "One-sample"

    # Step 2: State hypotheses
    print(f"\n2. HYPOTHESES ({test_type} t-test)")
    if sample2 is not None:
        print("   H₀: μ₁ = μ₂ (means are equal)")
        print("   H₁: μ₁ ≠ μ₂ (means are different)")
    else:
        print(f"   H₀: μ = {pop_mean}")
        print(f"   H₁: μ ≠ {pop_mean}")

    # Step 3: Perform test
    print("\n3. TEST RESULTS")
    if sample2 is not None:
        t_stat, p_value = ttest_ind(sample1, sample2)
    else:
        t_stat, p_value = ttest_1samp(sample1, pop_mean)

    print(f"   t-statistic: {t_stat:.4f}")
    print(f"   p-value: {p_value:.4f}")
    print(f"   Significance level (α): {alpha}")

    # Step 4: Decision
    print("\n4. DECISION")
    if p_value < alpha:
        print(f"   Since p-value ({p_value:.4f}) < α ({alpha}): REJECT H₀")
        print("   There IS a statistically significant difference.")
    else:
        print(f"   Since p-value ({p_value:.4f}) >= α ({alpha}): FAIL TO REJECT H₀")
        print("   There is NO statistically significant difference.")

    print("="*50)
    return t_stat, p_value

# Example usage
scores_a = [75, 82, 78, 85, 80, 77, 83, 79]
scores_b = [82, 88, 85, 90, 87, 84, 89, 86]

hypothesis_test_workflow(scores_a, scores_b)
```

```
==================================================
HYPOTHESIS TESTING WORKFLOW
==================================================

1. DESCRIPTIVE STATISTICS
   Sample 1: n=8, mean=79.88, std=3.00
   Sample 2: n=8, mean=86.38, std=2.56

2. HYPOTHESES (Two-sample t-test)
   H₀: μ₁ = μ₂ (means are equal)
   H₁: μ₁ ≠ μ₂ (means are different)

3. TEST RESULTS
   t-statistic: -4.6547
   p-value: 0.0003
   Significance level (α): 0.05

4. DECISION
   Since p-value (0.0003) < α (0.05): REJECT H₀
   There IS a statistically significant difference.
==================================================
```

## Summary

Here's a quick reference for hypothesis testing in Python:

| Task | Code |
|------|------|
| One-sample t-test | `ttest_1samp(sample, popmean)` |
| Two-sample t-test | `ttest_ind(sample1, sample2)` |
| Get t-statistic and p-value | `t_stat, p_value = ttest_ind(a, b)` |
| Chi-square test | `chi2_contingency(table)` |
| Mann-Whitney U test | `mannwhitneyu(sample1, sample2)` |

### Decision Rules

| p-value | Decision |
|---------|----------|
| p < 0.05 | Reject H₀ — significant evidence of a difference |
| p ≥ 0.05 | Fail to reject H₀ — no significant evidence |

### Key Takeaways

1. **Start with the null hypothesis** (assume no effect)
2. **p-value** tells you how surprising your data is under H₀
3. **Low p-value** (< 0.05) → evidence against H₀ → reject it
4. **High p-value** (≥ 0.05) → data consistent with H₀ → fail to reject
5. **Statistical significance ≠ practical importance** — always consider effect size

---

## Exercises

````{exercise}
:label: ex9-one-sample

**Exercise 1: One-Sample t-Test**

A coffee shop claims that their medium coffee contains 350ml on average. You measure 12 cups and get the following volumes (in ml):

```python
volumes = [345, 352, 348, 351, 347, 355, 349, 346, 353, 350, 348, 354]
```

1. Calculate the sample mean and standard deviation
2. Perform a one-sample t-test to test if the true mean equals 350ml
3. Interpret the result at α = 0.05
````

````{solution} ex9-one-sample
:class: dropdown

```python
import numpy as np
from scipy.stats import ttest_1samp

volumes = [345, 352, 348, 351, 347, 355, 349, 346, 353, 350, 348, 354]

# 1. Sample statistics
mean_vol = np.mean(volumes)
std_vol = np.std(volumes, ddof=1)  # ddof=1 for sample std
print(f"Sample mean: {mean_vol:.2f} ml")
print(f"Sample std: {std_vol:.2f} ml")

# 2. One-sample t-test
t_stat, p_value = ttest_1samp(volumes, 350)
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# 3. Interpretation
if p_value < 0.05:
    print("\nAt α = 0.05: Reject H₀")
    print("The average volume is significantly different from 350ml.")
else:
    print("\nAt α = 0.05: Fail to reject H₀")
    print("No significant evidence that the average differs from 350ml.")
```
````

````{exercise}
:label: ex9-two-sample

**Exercise 2: Two-Sample t-Test**

A company wants to test whether a new training programme improves employee productivity. They measure output before and after training:

```python
before = [45, 52, 48, 55, 50, 47, 51, 49, 53, 46]
after = [48, 56, 52, 58, 54, 51, 55, 53, 57, 50]
```

1. Calculate the means for both groups
2. Perform a two-sample t-test
3. Interpret the result and make a recommendation
````

````{solution} ex9-two-sample
:class: dropdown

```python
import numpy as np
from scipy.stats import ttest_ind

before = [45, 52, 48, 55, 50, 47, 51, 49, 53, 46]
after = [48, 56, 52, 58, 54, 51, 55, 53, 57, 50]

# 1. Calculate means
print(f"Mean BEFORE training: {np.mean(before):.2f}")
print(f"Mean AFTER training: {np.mean(after):.2f}")
print(f"Improvement: {np.mean(after) - np.mean(before):.2f}")

# 2. Two-sample t-test
t_stat, p_value = ttest_ind(before, after)
print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# 3. Interpretation
print("\n--- INTERPRETATION ---")
if p_value < 0.05:
    print("At α = 0.05: Reject H₀")
    print("The training programme significantly improved productivity.")
    print("Recommendation: Implement the training programme company-wide.")
else:
    print("At α = 0.05: Fail to reject H₀")
    print("No statistically significant improvement from training.")
    print("Recommendation: Consider redesigning the programme or collecting more data.")
```
````

````{exercise}
:label: ex9-interpret

**Exercise 3: Interpreting Results**

For each scenario, state whether you would reject or fail to reject H₀ at α = 0.05:

1. t = 2.45, p = 0.023
2. t = 1.67, p = 0.108
3. t = -3.21, p = 0.004
4. t = 0.89, p = 0.382

Also explain what each result means in plain English.
````

````{solution} ex9-interpret
:class: dropdown

```python
results = [
    (2.45, 0.023),
    (1.67, 0.108),
    (-3.21, 0.004),
    (0.89, 0.382)
]

alpha = 0.05

for i, (t, p) in enumerate(results, 1):
    print(f"Scenario {i}: t = {t:.2f}, p = {p:.3f}")

    if p < alpha:
        decision = "REJECT H₀"
        meaning = "There IS a statistically significant difference"
    else:
        decision = "FAIL TO REJECT H₀"
        meaning = "There is NO statistically significant difference"

    print(f"   Decision at α = 0.05: {decision}")
    print(f"   Meaning: {meaning}")
    print()

# Summary
print("--- SUMMARY ---")
print("Scenarios 1 and 3: Significant results (p < 0.05)")
print("Scenarios 2 and 4: Not significant (p >= 0.05)")
print("\nNote: The sign of t indicates direction (positive = sample > comparison)")
```
````

````{exercise}
:label: ex9-complete

**Exercise 4: Complete Analysis**

You have sales data from two regions and want to determine if there's a significant difference in average transaction values:

```python
import numpy as np
np.random.seed(42)

region_north = np.random.normal(85, 15, 30).round(2)  # 30 transactions
region_south = np.random.normal(92, 18, 35).round(2)  # 35 transactions
```

Complete a full hypothesis testing workflow:
1. State H₀ and H₁
2. Calculate descriptive statistics for both regions
3. Perform the appropriate test
4. Interpret the results at both α = 0.05 and α = 0.01
5. Write a brief business conclusion
````

````{solution} ex9-complete
:class: dropdown

```python
import numpy as np
from scipy.stats import ttest_ind

np.random.seed(42)
region_north = np.random.normal(85, 15, 30).round(2)
region_south = np.random.normal(92, 18, 35).round(2)

print("="*60)
print("SALES ANALYSIS: NORTH vs SOUTH REGIONS")
print("="*60)

# 1. Hypotheses
print("\n1. HYPOTHESES")
print("   H₀: μ_north = μ_south (no difference in average transaction value)")
print("   H₁: μ_north ≠ μ_south (there IS a difference)")

# 2. Descriptive Statistics
print("\n2. DESCRIPTIVE STATISTICS")
print(f"   North Region: n={len(region_north)}, mean=£{np.mean(region_north):.2f}, std=£{np.std(region_north):.2f}")
print(f"   South Region: n={len(region_south)}, mean=£{np.mean(region_south):.2f}, std=£{np.std(region_south):.2f}")
print(f"   Difference: £{np.mean(region_south) - np.mean(region_north):.2f}")

# 3. Hypothesis Test
print("\n3. TWO-SAMPLE T-TEST")
t_stat, p_value = ttest_ind(region_north, region_south)
print(f"   t-statistic: {t_stat:.4f}")
print(f"   p-value: {p_value:.4f}")

# 4. Interpretation at different alpha levels
print("\n4. INTERPRETATION")
print(f"   At α = 0.05: {'REJECT H₀' if p_value < 0.05 else 'FAIL TO REJECT H₀'}")
print(f"   At α = 0.01: {'REJECT H₀' if p_value < 0.01 else 'FAIL TO REJECT H₀'}")

# 5. Business Conclusion
print("\n5. BUSINESS CONCLUSION")
if p_value < 0.05:
    print("   The South region has significantly higher average transaction values")
    print("   than the North region. Consider investigating what practices in the")
    print("   South region lead to higher sales and whether they can be replicated.")
else:
    print("   There is no statistically significant difference between regions.")
    print("   The observed difference could be due to random variation.")

print("="*60)
```
````
