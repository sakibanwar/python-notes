---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Statistical Inference: Hypothesis Testing

This is **Part 2** of statistical inference, building directly on the foundation in Chapter 9. Where Chapter 9 was about *estimation* — using a sample to put a sensible range on a population parameter — this chapter is about *decision-making*: using a sample to answer **yes/no questions** about a population.

For example:

- Is the proportion of students who support extending library hours **different from 50%**?
- Is the average birth weight of smokers' babies **different from non-smokers'** babies?
- Did students score **differently** on the reading and writing exams?

Each of those is a **hypothesis test**. The framework is always the same — we'll see it in detail below — and we just plug in different formulas for different kinds of data (proportions, means, paired samples).

```{code-cell} ipython3
:tags: [remove-cell]

# Imports for the plots and code in this chapter (kept hidden so students
# aren't distracted by plotting machinery while learning statistics).
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
```

---

## Hypothesis Testing: The Framework

Confidence intervals tell us *how precise* our estimates are. But what if we want to answer a yes/no question: "Is the rate of premature births *really different* between smokers and nonsmokers, or could the difference just be due to chance?"

That's what **hypothesis testing** does — it gives us a rigorous, repeatable way to make decisions about whether an observed difference is real.

### The Logic (It Feels Backwards at First)

Hypothesis testing follows a specific logic that might seem strange the first time you see it:

1. **Assume there's no effect** (the "null hypothesis")
2. **Calculate how likely** we'd see our data if this assumption were true
3. **If it's very unlikely**, reject the assumption and conclude there IS an effect

Think of it like a courtroom: we assume the defendant is innocent (null hypothesis) until the evidence is overwhelming enough to conclude guilt (reject the null). We never "prove innocence" — we either find enough evidence to convict, or we don't.

### Key Terms

Here are the terms you need to know. Don't worry if they feel abstract right now — we'll work through concrete examples shortly:

| Term | Definition | Example |
|------|------------|---------|
| **Null Hypothesis (H₀)** | The "no effect" assumption | "There's no difference between the two groups" |
| **Alternative Hypothesis (H₁)** | What we're trying to show | "There IS a difference between the two groups" |
| **p-value** | Probability of seeing our data (or more extreme) if H₀ is true | p = 0.03 means 3% chance |
| **Significance Level (α)** | Our threshold for "unlikely enough" | Typically α = 0.05 (5%) |
| **Test Statistic** | A number summarising how far our data is from H₀ | t-statistic, z-score |

### The Decision Rule

The decision is straightforward — compare the p-value to your chosen significance level:

| p-value | Decision | Interpretation |
|---------|----------|----------------|
| p < α | Reject H₀ | Evidence of a difference (statistically significant) |
| p ≥ α | Fail to reject H₀ | No evidence of a difference |

```{warning}
**"Fail to reject H₀" is NOT the same as "accept H₀"!** This is one of the most common mistakes in statistics. We never prove the null hypothesis is true — we just don't have enough evidence to reject it. It's like saying "not guilty" in court — it doesn't mean "innocent", just that the evidence wasn't strong enough.
```

---

## Hypothesis Test for Two Proportions (Z-Test)

Let's put the framework into practice. One of the most common tests compares proportions between two groups — for example: "Is the proportion of premature births different between smokers and nonsmokers?"

### Setting Up the Hypotheses

First, we write down what we're testing:

- **H₀**: p₁ = p₂ (the premature birth rates are the same for both groups)
- **H₁**: p₁ ≠ p₂ (the rates are different)

### The Pooled Proportion

Here's a concept that trips people up: when testing whether two proportions are equal, we calculate the standard error using the **pooled proportion** — the overall proportion assuming H₀ is true (i.e., treating both groups as one big group):

$$\hat{p}_{pool} = \frac{x_1 + x_2}{n_1 + n_2}$$

Why pool? Because under H₀, there's no difference — so our best estimate of the common proportion combines all the data.

### The Z-Statistic

The z-statistic measures how many standard errors the observed difference is from zero:

$$z = \frac{\hat{p}_1 - \hat{p}_2}{SE}$$

where:

$$SE = \sqrt{\hat{p}_{pool} \times (1 - \hat{p}_{pool}) \times \left(\frac{1}{n_1} + \frac{1}{n_2}\right)}$$

### Example: Premature Births and Smoking

The `births_smoking.csv` dataset has 1,000 births split into two groups — `nonsmoker` and `smoker` — each with a `premature` flag. To set up the test we need the per-group counts. A single `groupby` does the job:

```{code-cell} ipython3
# Load the data
births = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/births_smoking.csv")

# Get total births and number premature in each group
counts = births.groupby("habit")["premature"].agg(["sum", "count"])
print(counts)
print()

# Pull out the numbers we need
n1 = counts.loc["nonsmoker", "count"]
x1 = counts.loc["nonsmoker", "sum"]
n2 = counts.loc["smoker", "count"]
x2 = counts.loc["smoker", "sum"]

# Per-group premature rates
p1 = x1 / n1
p2 = x2 / n2

print("Nonsmoker premature rate:", round(p1, 4), "= about", round(p1 * 100, 1), "%")
print("Smoker premature rate:   ", round(p2, 4), "= about", round(p2 * 100, 1), "%")
print("Difference:", round(p2 - p1, 4))
```


So smokers have a 21.0% premature rate compared to 13.8% for nonsmokers — a 7.25 percentage point difference. But is this difference *statistically significant*, or could it just be due to random variation? Let's find out:

```{code-cell} ipython3
# Step 1: Calculate pooled proportion
p_pool = (x1 + x2) / (n1 + n2)
print("Pooled proportion: ", round(p_pool, 4))

# Step 2: Calculate standard error
se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
print("Standard error: ", round(se, 4))

# Step 3: Calculate z-statistic
z_stat = (p1 - p2) / se
print("z-statistic: ", round(z_stat, 4))

# Step 4: Calculate p-value (two-tailed)
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
print("p-value: ", round(p_value, 4))

# Step 5: Make decision
alpha = 0.05
if p_value < alpha:
    print("\nSince p-value (", round(p_value, 4), ") < α (", alpha, "): REJECT H₀")
    print("There IS a significant difference in premature birth rates.")
else:
    print("\nSince p-value (", round(p_value, 4), ") >= α (", alpha, "): FAIL TO REJECT H₀")
    print("No significant difference in premature birth rates.")
```


Let's make sure we understand what just happened:

1. We calculated the **pooled proportion** (0.152) — the overall premature rate assuming no difference
2. We calculated the **standard error** (0.029) — how much the difference would vary by chance
3. The **z-statistic** (-2.51) tells us the observed difference is 2.51 standard errors away from zero
4. The **p-value** (0.012) tells us: if there truly were no difference, we'd see a gap this large only 1.2% of the time

Since 1.2% is less than our threshold of 5%, we conclude: the evidence suggests smokers have a significantly higher rate of premature births (p = 0.012).

### Putting It in a Reusable Function

You'll likely run this test more than once, so let's wrap it in a function:

```{code-cell} ipython3
def z_test_two_proportions(x1, n1, x2, n2, alpha=0.05):
    """
    Two-proportion z-test using the pooled proportion.

    Parameters:
        x1, n1: successes and total for group 1
        x2, n2: successes and total for group 2
        alpha: significance level (default 0.05)
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)

    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z_stat = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    print("Group 1: ", x1, "/", n1, " = ", round(p1, 4))
    print("Group 2: ", x2, "/", n2, " = ", round(p2, 4))
    print("Pooled proportion: ", round(p_pool, 4))
    print("z-statistic: ", round(z_stat, 4))
    print("p-value: ", round(p_value, 4))

    if p_value < alpha:
        print("\nReject H₀ at α = ", alpha, ": significant difference")
    else:
        print("\nFail to reject H₀ at α = ", alpha, ": no significant difference")

    return z_stat, p_value
```

---

## Hypothesis Test for Two Means (t-Test)

The z-test compared **proportions**. But what if you want to compare **means** — like the average birth weight of smokers vs nonsmokers? That's where the **two-sample t-test** comes in.

### Setting Up

- **H₀**: μ₁ = μ₂ (the mean birth weights are equal)
- **H₁**: μ₁ ≠ μ₂ (the mean birth weights are different)

### Using `scipy.stats.ttest_ind()`

The good news: Python has a built-in function for this, so you don't need to calculate everything by hand:

```{code-cell} ipython3
from scipy.stats import ttest_ind

# Birth weight data: 800 nonsmokers and 200 smokers
births = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/births_smoking.csv")
nonsmoker_weights = births[births['habit'] == 'nonsmoker']['weight_lbs'].values
smoker_weights = births[births['habit'] == 'smoker']['weight_lbs'].values

# First, let's see the descriptive statistics
print("Nonsmoker mean weight: ", round(nonsmoker_weights.mean(), 3), " lbs")
print("Smoker mean weight:    ", round(smoker_weights.mean(), 3), " lbs")
print("Difference:            ", round(nonsmoker_weights.mean() - smoker_weights.mean(), 3), " lbs")
```


There's a half-pound difference. Is it statistically significant?

```{code-cell} ipython3
# Perform two-sample t-test (Welch's t-test by default)
t_stat, p_value = ttest_ind(nonsmoker_weights, smoker_weights)

print("\nt-statistic: ", round(t_stat, 4))
print("p-value: ", round(p_value, 4))

if p_value < 0.05:
    print("\nReject H₀: The difference in birth weights IS statistically significant.")
else:
    print("\nFail to reject H₀: No significant difference in birth weights.")
```


The p-value is essentially 0 — the difference is highly significant.

```{note}
By default, `ttest_ind()` performs **Welch's t-test**, which does NOT assume equal variances between groups. This is the recommended approach — it's more robust. If you specifically need the pooled (Student's) t-test, use `ttest_ind(a, b, equal_var=True)`, but Welch's is almost always the better choice.
```

### Interpreting the Output

Let's make sure we understand what these numbers mean:

| Output | What it tells you |
|--------|---------|
| **t-statistic** | How many standard errors the observed difference is from zero. Bigger = stronger evidence against H₀ |
| **p-value** | Probability of seeing a difference this large (or larger) if H₀ were true. Smaller = stronger evidence against H₀ |

A large absolute t-statistic (far from 0) and small p-value (< 0.05) both point to the same conclusion: the difference is unlikely to be due to chance alone.

### Working with Real Data

In the example above, we had two separate arrays. But in practice, your data will usually be in a DataFrame with a column indicating which group each observation belongs to. How do you split it? Using the filtering skills from Chapter 6:

```{code-cell} ipython3
# Create a DataFrame (as you'd typically load from a CSV)
births = pd.DataFrame({
    'weight': np.concatenate([nonsmoker_weights, smoker_weights]),
    'habit': ['nonsmoker'] * 800 + ['smoker'] * 200
})

# Split by group — this is just filtering!
nonsmoker = births[births['habit'] == 'nonsmoker']['weight']
smoker = births[births['habit'] == 'smoker']['weight']

# Run the test
t_stat, p_value = ttest_ind(nonsmoker, smoker)
print("t-statistic: ", round(t_stat, 4))
print("p-value: ", round(p_value, 4))
```


Notice how we used the same boolean filtering pattern from Chapter 6 — `births[births['habit'] == 'nonsmoker']` — to split the data into two groups before passing them to `ttest_ind()`. Everything we've learned builds on what came before!

---

## Statistical Significance vs Practical Significance

We've been focused on p-values and statistical significance. But here's something crucial that many people miss: **a result can be statistically significant without being practically important**.

### The Problem with Large Samples

Why? Because with a very large sample, even *tiny* differences become statistically significant. Watch what happens:

```{code-cell} ipython3
# Large sample with tiny difference — 10,000 observations per group
stat_practical = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/stat_vs_practical.csv")
group_1 = stat_practical[stat_practical['group'] == 'Group A']['score'].values
group_2 = stat_practical[stat_practical['group'] == 'Group B']['score'].values

t_stat, p_value = ttest_ind(group_1, group_2)
print("Difference in means: ", round(group_2.mean() - group_1.mean(), 2))
print("p-value: ", round(p_value, 6))
```


The result is "significant" (p < 0.05), but the actual difference is only 0.59 points on a scale where the standard deviation is 15. Would you change a business decision based on a difference this tiny? Probably not.

This is why you should always ask two questions, not just one:

1. **Is the difference statistically significant?** (What the p-value tells you)
2. **Is the difference big enough to matter?** (What the p-value does NOT tell you)

### Always Report Both

When reporting results, good practice is to state three things:

1. **Whether the result is statistically significant** (the p-value)
2. **The size of the effect** (the actual difference in means or proportions)
3. **Whether the effect matters practically** (your judgement, based on context)

For example, here's how you might write up our birth weight findings:

> "Nonsmoking mothers had babies weighing on average 0.50 lbs more than smoking mothers (7.18 vs 6.68 lbs). This difference was statistically significant (t = 4.78, p < 0.001). A half-pound difference in birth weight is also clinically meaningful, as it can affect neonatal health outcomes."

Notice how this reports the actual numbers, the statistical test, AND the practical interpretation.

```{tip}
Always interpret your results in context. Ask yourself: "Even though this is statistically significant, does the difference actually matter in the real world?" A p-value tells you whether the difference is **real**, not whether it's **important**.
```

---

## One-Tailed vs Two-Tailed Tests

By default, all the tests we've been running are **two-tailed** — they check for a difference in *either* direction. But sometimes you have a specific directional hypothesis. For example, you don't just think smokers are *different* — you specifically think smokers have *lower* birth weights.

### Two-Tailed Test (Default)

- **H₀**: μ₁ = μ₂
- **H₁**: μ₁ ≠ μ₂ (could be higher OR lower)

### One-Tailed Test

- **H₀**: μ₁ ≥ μ₂
- **H₁**: μ₁ < μ₂ (specifically testing if one group is **lower**)

How do you convert? Since `ttest_ind` always returns a two-tailed p-value, you simply divide by 2:

```{code-cell} ipython3
# For a one-tailed test, divide the two-tailed p-value by 2
# (only valid if the observed difference is in the expected direction)

t_stat, p_value_two_tailed = ttest_ind(smoker, nonsmoker)
p_value_one_tailed = p_value_two_tailed / 2

print("Two-tailed p-value: ", round(p_value_two_tailed, 4))
print("One-tailed p-value: ", round(p_value_one_tailed, 4))
```

```{warning}
One-tailed tests are more powerful (more likely to detect an effect), which makes them tempting. But they should **only** be used when you had a clear directional hypothesis **before** looking at the data. If you choose the direction *after* seeing the results, you're cheating — and your p-value is no longer valid. When in doubt, use the two-tailed test.
```

---

## Understanding p-Values More Deeply

The p-value is one of the most commonly used — and most commonly **misunderstood** — concepts in statistics. Let's be really clear about what it does and doesn't tell you.

### What the p-Value IS

The p-value is the probability of observing data as extreme as (or more extreme than) what we got, **assuming the null hypothesis is true**.

A p-value of 0.03 means: "If there really were no effect, we'd see results this extreme only 3% of the time." That's pretty unlikely — so we take it as evidence against the null.

### What the p-Value is NOT

This table is worth memorising — these mistakes appear in published research papers, news articles, and even some textbooks:

| Wrong Interpretation | Why It's Wrong |
|---------------------|----------------------|
| "There's a 3% chance the null is true" | The p-value says nothing about the probability that H₀ is true |
| "There's a 97% chance the alternative is true" | The p-value doesn't give probabilities of hypotheses being true or false |
| "The effect is important/large" | The p-value measures **evidence**, not **effect size** (remember our large-sample example!) |
| "The results are definitely real" | Low p-values can still be false positives — a 5% significance level means you'll be wrong about 1 in 20 times |

---

## Complete Inference Workflow

Let's tie everything together. Here's a reusable function that runs the complete inference workflow — from descriptive statistics through to the test decision. You can use this as a template for your own analyses:

```{code-cell} ipython3
def inference_workflow(data, group_col, value_col, alpha=0.05):
    """
    Complete inference workflow for comparing two groups.

    Parameters:
        data: DataFrame
        group_col: name of the grouping column
        value_col: name of the value column
        alpha: significance level
    """
    groups = data[group_col].unique()
    group1 = data[data[group_col] == groups[0]][value_col]
    group2 = data[data[group_col] == groups[1]][value_col]

    print("=" * 55)
    print("STATISTICAL INFERENCE WORKFLOW")
    print("=" * 55)

    # Step 1: Descriptive statistics
    print("\n1. DESCRIPTIVE STATISTICS")
    print("   ", groups[0], ": n=", len(group1), ", mean=", round(group1.mean(), 3), ", sd=", round(group1.std(), 3))
    print("   ", groups[1], ": n=", len(group2), ", mean=", round(group2.mean(), 3), ", sd=", round(group2.std(), 3))
    print("   Difference: ", round(group1.mean() - group2.mean(), 3))

    # Step 2: Hypotheses
    print("\n2. HYPOTHESES")
    print("   H₀: μ_", groups[0], " = μ_", groups[1])
    print("   H₁: μ_", groups[0], " ≠ μ_", groups[1])

    # Step 3: Test
    print("\n3. WELCH'S TWO-SAMPLE t-TEST")
    t_stat, p_value = ttest_ind(group1, group2)
    print("   t-statistic: ", round(t_stat, 4))
    print("   p-value: ", round(p_value, 4))

    # Step 4: Decision
    print("\n4. DECISION (α = ", alpha, ")")
    if p_value < alpha:
        print("   p-value (", round(p_value, 4), ") < α (", alpha, "): REJECT H₀")
        print("   There IS a statistically significant difference.")
    else:
        print("   p-value (", round(p_value, 4), ") ≥ α (", alpha, "): FAIL TO REJECT H₀")
        print("   No statistically significant difference.")

    print("=" * 55)
    return t_stat, p_value

# Example usage — load the births data
births = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/births_smoking.csv")
births = births.rename(columns={'weight_lbs': 'weight'})  # Match expected column name

inference_workflow(births, 'habit', 'weight')
```

---

## Summary

Here's a quick reference for the hypothesis testing tools we built in this chapter.

### Hypothesis Tests

| Test | When to Use | Python |
|------|------------|--------|
| Z-test for two proportions | Comparing proportions between groups | Manual (pooled proportion) |
| Two-sample t-test | Comparing means between two independent groups | `ttest_ind(group1, group2)` |

### Key Takeaways

1. **Hypothesis testing** starts with assuming no effect (H₀) and asks "how unlikely is our data?"
2. **p-value < 0.05** = statistically significant, but **significant ≠ important** — always consider effect size.
3. Use **Welch's t-test** (default in `ttest_ind`) for comparing means — it doesn't assume equal variances.
4. **"Fail to reject H₀" ≠ "accept H₀"** — we never *prove* the null is true.
5. With a **large enough sample**, even tiny differences become statistically significant. Always report the effect size alongside the p-value.
6. **One-tailed tests** are tempting (more "powerful") but only valid if you specified the direction *before* looking at the data.

---

## Exercises

````{exercise}
:label: ex10-z-test-proportions

**Exercise 1: Z-Test for Two Proportions**

A researcher wants to know if a new teaching method improves pass rates. In the traditional class, 65 out of 100 students passed. In the new method class, 78 out of 100 students passed.

1. State the null and alternative hypotheses
2. Calculate the pooled proportion
3. Calculate the standard error and z-statistic
4. Find the p-value and make a decision at α = 0.05
5. Write a one-sentence conclusion
````

````{solution} ex10-z-test-proportions
:class: dropdown

```python
import numpy as np
from scipy import stats

# Data
n1 = 100   # traditional class
x1 = 65    # passed in traditional
p1 = x1 / n1

n2 = 100   # new method class
x2 = 78    # passed in new method
p2 = x2 / n2

# 1. Hypotheses
print("1. HYPOTHESES")
print("   H₀: p_traditional = p_new (no difference in pass rates)")
print("   H₁: p_traditional ≠ p_new (there IS a difference)")

# 2. Pooled proportion
p_pool = (x1 + x2) / (n1 + n2)
print("\n2. Pooled proportion: ", round(p_pool, 4))

# 3. Standard error and z-statistic
se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
z_stat = (p1 - p2) / se
print("\n3. Standard error: ", round(se, 4))
print("   z-statistic: ", round(z_stat, 4))

# 4. p-value and decision
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
print("\n4. p-value: ", round(p_value, 4))
if p_value < 0.05:
    print("   Decision: REJECT H₀ — significant difference in pass rates")
else:
    print("   Decision: FAIL TO REJECT H₀ — no significant difference")

# 5. Conclusion
print("\n5. The new teaching method had a significantly higher pass rate")
print("   (78% vs 65%, z = ", round(z_stat, 2), ", p = ", round(p_value, 4), ").")
```

```
1. HYPOTHESES
   H₀: p_traditional = p_new (no difference in pass rates)
   H₁: p_traditional ≠ p_new (there IS a difference)

2. Pooled proportion: 0.7150

3. Standard error: 0.0639
   z-statistic: -2.0344

4. p-value: 0.0419
   Decision: REJECT H₀ — significant difference in pass rates

5. The new teaching method had a significantly higher pass rate
   (78% vs 65%, z = -2.03, p = 0.0419).
```
````

````{exercise}
:label: ex10-t-test

**Exercise 2: Two-Sample t-Test**

A company tested two versions of a website (A and B) to see which generates more time on page. The results (in seconds) are:

```python
import pandas as pd

# A/B test data — time spent on page (seconds) for two website versions
ab_test = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/ab_test_website.csv")
version_A = ab_test[ab_test['version'] == 'A']['time_on_page_seconds'].values  # 40 visitors
version_B = ab_test[ab_test['version'] == 'B']['time_on_page_seconds'].values  # 45 visitors
```

1. Calculate descriptive statistics for both groups
2. Perform a two-sample t-test
3. Is the difference statistically significant at α = 0.05?
4. Is the difference practically meaningful? (Consider: what's a meaningful difference in time on page?)
````

````{solution} ex10-t-test
:class: dropdown

```python
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Load the A/B test data
ab_test = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/ab_test_website.csv")
version_A = ab_test[ab_test['version'] == 'A']['time_on_page_seconds'].values
version_B = ab_test[ab_test['version'] == 'B']['time_on_page_seconds'].values

# 1. Descriptive statistics
print("1. DESCRIPTIVE STATISTICS")
print("   Version A: n=", len(version_A), ", mean=", round(version_A.mean(), 1), "s, sd=", round(version_A.std(), 1), "s")
print("   Version B: n=", len(version_B), ", mean=", round(version_B.mean(), 1), "s, sd=", round(version_B.std(), 1), "s")
print("   Difference: ", round(version_B.mean() - version_A.mean(), 1), "s")

# 2. Two-sample t-test
t_stat, p_value = ttest_ind(version_A, version_B)
print("\n2. TWO-SAMPLE t-TEST (Welch's)")
print("   t-statistic: ", round(t_stat, 4))
print("   p-value: ", round(p_value, 4))

# 3. Decision
print("\n3. DECISION")
if p_value < 0.05:
    print("   p-value (", round(p_value, 4), ") < 0.05: REJECT H₀")
    print("   The difference IS statistically significant.")
else:
    print("   p-value (", round(p_value, 4), ") >= 0.05: FAIL TO REJECT H₀")
    print("   The difference is NOT statistically significant.")

# 4. Practical significance
diff = version_B.mean() - version_A.mean()
print("\n4. PRACTICAL SIGNIFICANCE")
print("   The difference is ", round(diff, 1), " seconds.")
print("   Whether this is practically meaningful depends on context:")
print("   - For an e-commerce site: 15 extra seconds could mean more purchases")
print("   - For a news article: probably not meaningful enough to matter")
```

```
1. DESCRIPTIVE STATISTICS
   Version A: n=40, mean=118.7s, sd=28.1s
   Version B: n=45, mean=131.5s, sd=32.5s
   Difference: 12.8s

2. TWO-SAMPLE t-TEST (Welch's)
   t-statistic: -1.9403
   p-value: 0.0556

3. DECISION
   p-value (0.0556) >= 0.05: FAIL TO REJECT H₀
   The difference is NOT statistically significant.

4. PRACTICAL SIGNIFICANCE
   The difference is 12.8 seconds.
   Whether this is practically meaningful depends on context:
   - For an e-commerce site: 15 extra seconds could mean more purchases
   - For a news article: probably not meaningful enough to matter
```

Note: The result is borderline (p = 0.056). With more data, this might become significant. This illustrates why we should consider both statistical and practical significance.
````

---

## Appendix: How the Datasets Were Created

The datasets used in this chapter were generated using Python's `numpy.random` module to simulate realistic data. This appendix explains how each was created, so you can understand the data and learn how to simulate your own.

### Births and Smoking (`births_smoking.csv`)

A dataset of 1,000 births — 800 from nonsmoking mothers and 200 from smoking mothers. Each row also has a `premature` flag (1 = premature, 0 = full term). Nonsmokers' babies have a slightly higher mean birth weight, and a slightly lower premature birth rate (13.75% vs 21%).

```python
np.random.seed(42)

# Generate weights and habit
births = pd.DataFrame({
    'weight_lbs': np.concatenate([
        np.random.normal(7.2, 1.3, 800),   # Nonsmokers: mean 7.2 lbs, SD 1.3
        np.random.normal(6.7, 1.5, 200)    # Smokers: mean 6.7 lbs, SD 1.5
    ]).round(2),
    'habit': ['nonsmoker'] * 800 + ['smoker'] * 200
})

# Add a premature column: 110 of 800 nonsmokers (13.75%), 42 of 200 smokers (21%)
np.random.seed(42)
ns_idx = list(births[births['habit'] == 'nonsmoker'].index)
sm_idx = list(births[births['habit'] == 'smoker'].index)
np.random.shuffle(ns_idx)
np.random.shuffle(sm_idx)

births['premature'] = 0
births.loc[ns_idx[:110], 'premature'] = 1   # 110 random nonsmokers
births.loc[sm_idx[:42], 'premature'] = 1    # 42 random smokers

births.to_csv('births_smoking.csv', index=False)
```

**Why these numbers?** Research consistently shows that babies born to smoking mothers tend to weigh less on average and be premature more often. The 0.5 lb weight gap, the 13.75% / 21% premature rates and the sample sizes here are inspired by real studies, though the specific values are simulated.

### Statistical vs Practical Significance (`stat_vs_practical.csv`)

Two groups of 10,000 observations each, where the means differ by only 0.5 points. This demonstrates that with a very large sample, even a trivially small difference can be "statistically significant."

```python
np.random.seed(123)

stat_practical = pd.DataFrame({
    'group': ['Group A'] * 10000 + ['Group B'] * 10000,
    'score': np.concatenate([
        np.random.normal(100, 15, 10000),    # Group A: mean 100, SD 15
        np.random.normal(100.5, 15, 10000)   # Group B: mean 100.5, SD 15
    ]).round(2)
})

stat_practical.to_csv('stat_vs_practical.csv', index=False)
```

### A/B Test Website Data (`ab_test_website.csv`)

Time spent on a webpage (in seconds) for two versions of a website — 40 visitors saw Version A, 45 saw Version B.

```python
np.random.seed(42)

ab_test = pd.DataFrame({
    'version': ['A'] * 40 + ['B'] * 45,
    'time_on_page_seconds': np.concatenate([
        np.random.normal(120, 30, 40).round(2),   # Version A: mean ~120 seconds
        np.random.normal(135, 35, 45).round(2)    # Version B: mean ~135 seconds
    ])
})

ab_test.to_csv('ab_test_website.csv', index=False)
```
