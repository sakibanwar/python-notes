# Statistical Inference

Up to now, we've been **describing** data — calculating means, making plots, filtering rows. That's useful, but it only tells us about the data we have. What if we want to say something about the bigger picture?

For example, if the average birth weight in our sample of 1,000 babies is 7.1 lbs, can we say something about the average birth weight of *all* babies born in North Carolina? If smokers in our sample have more premature births than nonsmokers, is that a real pattern or just random chance in our particular sample?

This is what **statistical inference** is about — drawing conclusions about an entire **population** based on a **sample**. And this is where statistics gets really powerful.

We'll cover three big ideas:

1. **The normal distribution** — the foundation of most inference
2. **Confidence intervals** — estimating population parameters with a range
3. **Hypothesis testing** — deciding whether observed differences are real or just random noise

---

## The Normal Distribution

The **normal distribution** (also called the bell curve or Gaussian distribution) is the most important distribution in statistics. It shows up everywhere — heights, exam scores, measurement errors, and crucially, the distribution of sample statistics.

### Why Should You Care?

Here's the key insight — and this is genuinely one of the most remarkable results in all of statistics: even if your raw data isn't normally distributed, the **average** of many samples will be approximately normal. This is called the **Central Limit Theorem** (CLT), and it's why the normal distribution is the engine behind almost all statistical inference.

We'll come back to the CLT shortly. First, let's understand the normal distribution itself.

### Properties of the Normal Distribution

A normal distribution is completely defined by just two numbers:

| Parameter | Symbol | Meaning |
|-----------|--------|---------|
| Mean | μ (mu) | The centre of the distribution |
| Standard deviation | σ (sigma) | How spread out the values are |

The key properties to remember:
- It's **symmetric** around the mean
- About **68%** of values fall within 1 standard deviation of the mean
- About **95%** of values fall within 2 standard deviations
- About **99.7%** of values fall within 3 standard deviations

This is called the **68-95-99.7 rule** (or the empirical rule). We'll verify this with Python shortly!

### Setting Up

Python's `scipy.stats` module provides everything we need for working with distributions:

```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
```

### Z-Scores: Standardising Values

Before we can use the normal distribution, we need to understand **z-scores**. A z-score tells you how many standard deviations a value is from the mean:

$$z = \frac{x - \mu}{\sigma}$$

Let's try an example. Suppose exam scores have a mean of 70 and standard deviation of 10. A student scored 85 — how good is that?

```python
# What is the z-score for a student who scored 85?
x = 85
mu = 70
sigma = 10

z = (x - mu) / sigma
print(f"A score of {x} has a z-score of {z}")
```

```
A score of 85 has a z-score of 1.5
```

A z-score of 1.5 means the student scored 1.5 standard deviations above the mean. That sounds good, but *how* good exactly? What proportion of students did they beat? That's where `norm.cdf()` comes in.

### Finding Probabilities with `norm.cdf()`

The **CDF** (Cumulative Distribution Function) answers the question: *What proportion of values fall below a given point?* In Python, we use `stats.norm.cdf()`:

```python
# What proportion of students scored below 85?
prob_below_85 = stats.norm.cdf(85, loc=70, scale=10)
print(f"Proportion scoring below 85: {prob_below_85:.4f}")
print(f"That's {prob_below_85 * 100:.1f}% of students")
```

```
Proportion scoring below 85: 0.9332
That's 93.3% of students
```

So our student with a score of 85 did better than about 93% of the class. Not bad!

```{note}
In `stats.norm.cdf()`, `loc` is the mean (μ) and `scale` is the standard deviation (σ). If you're working with the **standard normal** (μ=0, σ=1), you can just pass the z-score directly: `stats.norm.cdf(1.5)` gives the same answer.
```

#### What about "above" a value?

Here's where beginners often get tripped up. `norm.cdf()` always gives you the area to the **left** (below). What if you want the area to the **right** (above)?

Since the total area under the curve is 1, you just subtract:

```python
# What proportion scored ABOVE 85?
prob_above_85 = 1 - stats.norm.cdf(85, loc=70, scale=10)
print(f"Proportion scoring above 85: {prob_above_85:.4f}")
print(f"That's {prob_above_85 * 100:.1f}% of students")
```

```
Proportion scoring above 85: 0.0668
That's 6.7% of students
```

Only about 6.7% scored above 85 — confirming it's a strong result.

```{warning}
A common mistake is using `norm.cdf()` when you want the area **above** a value. Remember: `norm.cdf()` always gives you the area **below**. For "above", you need `1 - norm.cdf()`.
```

#### Probability between two values

What if you want the probability of scoring between 60 and 80? Take the area below 80 and subtract the area below 60:

```python
# What proportion scored between 60 and 80?
prob_between = stats.norm.cdf(80, loc=70, scale=10) - stats.norm.cdf(60, loc=70, scale=10)
print(f"Proportion scoring between 60 and 80: {prob_between:.4f}")
print(f"That's {prob_between * 100:.1f}% of students")
```

```
Proportion scoring between 60 and 80: 0.6827
That's 68.3% of students
```

Wait — 68.3%? That's the 68-95-99.7 rule in action! The range 60 to 80 is exactly 1 standard deviation either side of the mean (70 ± 10), and we've just confirmed that about 68% of values fall in that range.

### Finding Values with `norm.ppf()` — The Inverse Question

`norm.cdf()` answers: "Given a value, what's the probability below it?"

But sometimes you want to go the other way: "Given a probability, what's the value?" For example: *What score do you need to be in the top 10%?*

That's what `norm.ppf()` does — it's the **inverse** of `cdf()`:

```python
# What score do you need to be in the top 10%?
# Top 10% means 90th percentile
score_90th = stats.norm.ppf(0.90, loc=70, scale=10)
print(f"90th percentile score: {score_90th:.1f}")
```

```
90th percentile score: 82.8
```

You'd need to score about 82.8 to be in the top 10%.

Now here's one that will come up again and again in this chapter:

```python
# What z-score leaves 2.5% in each tail?
z_95 = stats.norm.ppf(0.975)  # 0.975 because we want the upper tail for two-sided
print(f"z* for 95% confidence: {z_95:.4f}")
```

```
z* for 95% confidence: 1.9600
```

Why 0.975 and not 0.95? Because for a **two-sided** interval, we split the remaining 5% into two tails (2.5% each). So we need the value that leaves 97.5% below it.

This value — **1.96** — is perhaps the most famous number in statistics. It's the z-score that forms the basis of 95% confidence intervals, and you'll see it everywhere.

### Visualising the Normal Distribution

```python
# Generate x values
x = np.linspace(40, 100, 200)

# Calculate the normal distribution PDF
y = stats.norm.pdf(x, loc=70, scale=10)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(x, y, color='blue', linewidth=2)
plt.fill_between(x, y, where=(x >= 60) & (x <= 80), alpha=0.3, color='blue', label='Within 1 SD (68%)')
plt.axvline(x=70, color='red', linestyle='--', label='Mean (μ = 70)')
plt.xlabel('Exam Score')
plt.ylabel('Density')
plt.title('Normal Distribution: μ = 70, σ = 10')
plt.legend()
plt.show()
```

### Summary of Normal Distribution Functions

| Function | What it does | Example |
|----------|-------------|---------|
| `stats.norm.cdf(x, loc, scale)` | P(X ≤ x) — probability below x | "What % scored below 85?" |
| `stats.norm.ppf(p, loc, scale)` | Value at the p-th percentile | "What score is the 90th percentile?" |
| `stats.norm.pdf(x, loc, scale)` | Height of the curve at x | For plotting the distribution |
| `stats.norm.cdf(z)` | P(Z ≤ z) for the standard normal | When working with z-scores |
| `stats.norm.ppf(p)` | z-score at the p-th percentile | Finding critical values (z*) |

```{tip}
When using the **standard normal** distribution (μ=0, σ=1), you can omit `loc` and `scale`: `stats.norm.cdf(1.96)` gives you the same result as `stats.norm.cdf(1.96, loc=0, scale=1)`.
```

---

## Sampling Distributions and the Central Limit Theorem

Before we can do inference, we need to understand one of the most powerful ideas in all of statistics: the **sampling distribution**.

### The Key Idea

Imagine you take a random sample of 50 babies and calculate the average birth weight. Now imagine you take *another* random sample of 50 babies and calculate the average again. Would you get the exact same number? Almost certainly not — it would be slightly different.

If you repeated this process hundreds of times, those sample means would form their own distribution — the **sampling distribution of the mean**. And here's the remarkable part. The Central Limit Theorem (CLT) tells us three things about this distribution:

1. It will be approximately **normal** (even if the original data isn't!)
2. Its centre (mean) will equal the **population mean** (μ)
3. Its spread (standard deviation) will be **σ / √n** (where n is the sample size)

This standard deviation of the sampling distribution has a special name: the **standard error** (SE).

$$SE = \frac{\sigma}{\sqrt{n}}$$

### Why Should You Care?

The standard error tells us how much our sample statistics (like means or proportions) vary from sample to sample. A smaller SE means our estimates are more precise — more likely to be close to the true population value.

Two things reduce the SE:
- **Larger sample size** (n) — more data = more precision
- **Less variability** in the data (σ) — less noise = more precision

Notice something important: the sample size appears under a square root. That means to halve the standard error, you need to *quadruple* the sample size. Going from 100 to 400 observations halves the SE, but going from 100 to 200 only reduces it by about 30%.

---

## Confidence Intervals

So we've taken a sample and calculated a statistic — say, the average birth weight is 7.05 lbs. But we know that if we took a different sample, we'd get a slightly different number. So how precise is our estimate?

A **confidence interval** gives us a range of plausible values for the population parameter. Instead of saying "the average is 7.05", we can say "we're 95% confident the average is between 6.64 and 7.46". That's much more honest about the uncertainty in our estimate.

### Confidence Interval for a Proportion

Let's start with proportions (categorical data). The formula is:

$$\hat{p} \pm z^* \times SE_{\hat{p}}$$

where:

$$SE_{\hat{p}} = \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}$$

and z* = 1.96 for 95% confidence.

Let's break this down step by step with an example.

#### Example: Proportion of Premature Births

Suppose in a sample of 1,000 births, 152 were premature. What's the 95% confidence interval for the true proportion?

```python
# Step 1: Calculate the sample proportion
n = 1000
x = 152   # number of premature births
p_hat = x / n

print(f"Sample proportion: {p_hat:.4f}")

# Step 2: Calculate the standard error
se = np.sqrt(p_hat * (1 - p_hat) / n)
print(f"Standard error: {se:.4f}")

# Step 3: Find the critical value (z* for 95% confidence)
z_star = stats.norm.ppf(0.975)
print(f"z* for 95% confidence: {z_star:.4f}")

# Step 4: Calculate the confidence interval
lower = p_hat - z_star * se
upper = p_hat + z_star * se
print(f"\n95% Confidence Interval: ({lower:.4f}, {upper:.4f})")
print(f"We are 95% confident the true proportion of premature births")
print(f"is between {lower:.1%} and {upper:.1%}")
```

```
Sample proportion: 0.1520
Standard error: 0.0114
z* for 95% confidence: 1.9600

95% Confidence Interval: (0.1298, 0.1742)
We are 95% confident the true proportion of premature births
is between 13.0% and 17.4%
```

```{note}
What does "95% confident" actually mean? It does **not** mean there's a 95% probability the true value is in this particular interval. Instead, it means: if we repeated this study many times and constructed a confidence interval each time, about 95% of those intervals would contain the true population proportion. It's a statement about the **method**, not about any single interval.
```

### Confidence Interval for a Mean

For means, we use a similar formula but with the **t-distribution** instead of the normal distribution. Why? Because when we estimate the standard deviation from the sample (rather than knowing it from the population), we introduce extra uncertainty. The t-distribution accounts for this — it has wider tails than the normal, especially for small samples.

$$\bar{x} \pm t^* \times SE_{\bar{x}}$$

where:

$$SE_{\bar{x}} = \frac{s}{\sqrt{n}}$$

and t* comes from the t-distribution with n-1 degrees of freedom.

#### Example: Average Birth Weight

```python
# Birth weights from a sample of 50 babies (in pounds)
birth_sample = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/birth_weights_sample.csv")
weights = birth_sample['weight_lbs'].values

# Step 1: Calculate sample statistics
x_bar = weights.mean()
s = weights.std(ddof=1)  # ddof=1 for sample standard deviation
n = len(weights)
se = s / np.sqrt(n)

print(f"Sample mean: {x_bar:.3f} lbs")
print(f"Sample std: {s:.3f}")
print(f"Standard error: {se:.3f}")

# Step 2: Find the critical value (t* for 95% confidence)
t_star = stats.t.ppf(0.975, df=n-1)
print(f"t* for 95% confidence (df={n-1}): {t_star:.4f}")

# Step 3: Calculate the confidence interval
lower = x_bar - t_star * se
upper = x_bar + t_star * se
print(f"\n95% Confidence Interval: ({lower:.3f}, {upper:.3f})")
```

```
Sample mean: 7.052 lbs
Sample std: 1.447
Standard error: 0.205

t* for 95% confidence (df=49): 2.0096

95% Confidence Interval: (6.640, 7.463)
```

```{tip}
Notice that we used `ddof=1` when calculating the standard deviation. This gives us the **sample** standard deviation (dividing by n-1). Without `ddof=1`, pandas and numpy divide by n, which gives the **population** standard deviation. For inference, you almost always want `ddof=1`.
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

Let's work through this step by step. We have data from two groups:

```python
# Data from two groups
# Nonsmokers: 800 births, 110 premature
# Smokers: 200 births, 42 premature

n1 = 800    # nonsmokers
x1 = 110    # premature among nonsmokers
p1 = x1 / n1

n2 = 200    # smokers
x2 = 42     # premature among smokers
p2 = x2 / n2

print(f"Nonsmoker premature rate: {p1:.4f} ({p1:.1%})")
print(f"Smoker premature rate:    {p2:.4f} ({p2:.1%})")
print(f"Difference: {p2 - p1:.4f}")
```

```
Nonsmoker premature rate: 0.1375 (13.8%)
Smoker premature rate:    0.2100 (21.0%)
Difference: 0.0725
```

So smokers have a 21.0% premature rate compared to 13.8% for nonsmokers — a 7.25 percentage point difference. But is this difference *statistically significant*, or could it just be due to random variation? Let's find out:

```python
# Step 1: Calculate pooled proportion
p_pool = (x1 + x2) / (n1 + n2)
print(f"Pooled proportion: {p_pool:.4f}")

# Step 2: Calculate standard error
se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
print(f"Standard error: {se:.4f}")

# Step 3: Calculate z-statistic
z_stat = (p1 - p2) / se
print(f"z-statistic: {z_stat:.4f}")

# Step 4: Calculate p-value (two-tailed)
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
print(f"p-value: {p_value:.4f}")

# Step 5: Make decision
alpha = 0.05
if p_value < alpha:
    print(f"\nSince p-value ({p_value:.4f}) < α ({alpha}): REJECT H₀")
    print("There IS a significant difference in premature birth rates.")
else:
    print(f"\nSince p-value ({p_value:.4f}) >= α ({alpha}): FAIL TO REJECT H₀")
    print("No significant difference in premature birth rates.")
```

```
Pooled proportion: 0.1520
Standard error: 0.0289
z-statistic: -2.5103
p-value: 0.0121

Since p-value (0.0121) < α (0.05): REJECT H₀
There IS a significant difference in premature birth rates.
```

Let's make sure we understand what just happened:

1. We calculated the **pooled proportion** (0.152) — the overall premature rate assuming no difference
2. We calculated the **standard error** (0.029) — how much the difference would vary by chance
3. The **z-statistic** (-2.51) tells us the observed difference is 2.51 standard errors away from zero
4. The **p-value** (0.012) tells us: if there truly were no difference, we'd see a gap this large only 1.2% of the time

Since 1.2% is less than our threshold of 5%, we conclude: the evidence suggests smokers have a significantly higher rate of premature births (p = 0.012).

### Putting It in a Reusable Function

You'll likely run this test more than once, so let's wrap it in a function:

```python
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

    print(f"Group 1: {x1}/{n1} = {p1:.4f}")
    print(f"Group 2: {x2}/{n2} = {p2:.4f}")
    print(f"Pooled proportion: {p_pool:.4f}")
    print(f"z-statistic: {z_stat:.4f}")
    print(f"p-value: {p_value:.4f}")

    if p_value < alpha:
        print(f"\nReject H₀ at α = {alpha}: significant difference")
    else:
        print(f"\nFail to reject H₀ at α = {alpha}: no significant difference")

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

```python
from scipy.stats import ttest_ind

# Birth weight data: 800 nonsmokers and 200 smokers
births = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/births_smoking.csv")
nonsmoker_weights = births[births['habit'] == 'nonsmoker']['weight_lbs'].values
smoker_weights = births[births['habit'] == 'smoker']['weight_lbs'].values

# First, let's see the descriptive statistics
print(f"Nonsmoker mean weight: {nonsmoker_weights.mean():.3f} lbs")
print(f"Smoker mean weight:    {smoker_weights.mean():.3f} lbs")
print(f"Difference:            {nonsmoker_weights.mean() - smoker_weights.mean():.3f} lbs")
```

```
Nonsmoker mean weight: 7.178 lbs
Smoker mean weight:    6.678 lbs
Difference:            0.500 lbs
```

There's a half-pound difference. Is it statistically significant?

```python
# Perform two-sample t-test (Welch's t-test by default)
t_stat, p_value = ttest_ind(nonsmoker_weights, smoker_weights)

print(f"\nt-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("\nReject H₀: The difference in birth weights IS statistically significant.")
else:
    print("\nFail to reject H₀: No significant difference in birth weights.")
```

```
t-statistic: 4.7821
p-value: 0.0000

Reject H₀: The difference in birth weights IS statistically significant.
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

```python
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
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

```
t-statistic: 4.7821
p-value: 0.0000
```

Notice how we used the same boolean filtering pattern from Chapter 6 — `births[births['habit'] == 'nonsmoker']` — to split the data into two groups before passing them to `ttest_ind()`. Everything we've learned builds on what came before!

---

## Statistical Significance vs Practical Significance

We've been focused on p-values and statistical significance. But here's something crucial that many people miss: **a result can be statistically significant without being practically important**.

### The Problem with Large Samples

Why? Because with a very large sample, even *tiny* differences become statistically significant. Watch what happens:

```python
# Large sample with tiny difference — 10,000 observations per group
stat_practical = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/stat_vs_practical.csv")
group_1 = stat_practical[stat_practical['group'] == 'Group A']['score'].values
group_2 = stat_practical[stat_practical['group'] == 'Group B']['score'].values

t_stat, p_value = ttest_ind(group_1, group_2)
print(f"Difference in means: {group_2.mean() - group_1.mean():.2f}")
print(f"p-value: {p_value:.6f}")
```

```
Difference in means: 0.59
p-value: 0.002814
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

```python
# For a one-tailed test, divide the two-tailed p-value by 2
# (only valid if the observed difference is in the expected direction)

t_stat, p_value_two_tailed = ttest_ind(smoker, nonsmoker)
p_value_one_tailed = p_value_two_tailed / 2

print(f"Two-tailed p-value: {p_value_two_tailed:.4f}")
print(f"One-tailed p-value: {p_value_one_tailed:.4f}")
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

```python
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
    print(f"\n1. DESCRIPTIVE STATISTICS")
    print(f"   {groups[0]}: n={len(group1)}, mean={group1.mean():.3f}, sd={group1.std():.3f}")
    print(f"   {groups[1]}: n={len(group2)}, mean={group2.mean():.3f}, sd={group2.std():.3f}")
    print(f"   Difference: {group1.mean() - group2.mean():.3f}")

    # Step 2: Hypotheses
    print(f"\n2. HYPOTHESES")
    print(f"   H₀: μ_{groups[0]} = μ_{groups[1]}")
    print(f"   H₁: μ_{groups[0]} ≠ μ_{groups[1]}")

    # Step 3: Test
    print(f"\n3. WELCH'S TWO-SAMPLE t-TEST")
    t_stat, p_value = ttest_ind(group1, group2)
    print(f"   t-statistic: {t_stat:.4f}")
    print(f"   p-value: {p_value:.4f}")

    # Step 4: Decision
    print(f"\n4. DECISION (α = {alpha})")
    if p_value < alpha:
        print(f"   p-value ({p_value:.4f}) < α ({alpha}): REJECT H₀")
        print(f"   There IS a statistically significant difference.")
    else:
        print(f"   p-value ({p_value:.4f}) ≥ α ({alpha}): FAIL TO REJECT H₀")
        print(f"   No statistically significant difference.")

    print("=" * 55)
    return t_stat, p_value

# Example usage — load the births data
births = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/births_smoking.csv")
births = births.rename(columns={'weight_lbs': 'weight'})  # Match expected column name

inference_workflow(births, 'habit', 'weight')
```

---

## Summary

We've covered a lot in this chapter! Here's a quick reference to help you keep everything straight.

### Normal Distribution Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `stats.norm.cdf(x, loc, scale)` | P(X ≤ x) | "What % scored below 85?" |
| `stats.norm.ppf(p, loc, scale)` | Value at percentile p | "What score is the 90th percentile?" |
| `stats.norm.cdf(z)` | Standard normal P(Z ≤ z) | "What's the area to the left of z = 1.96?" |
| `stats.norm.ppf(0.975)` | z* for 95% CI | Returns 1.96 |

### Confidence Interval Formulas

| Parameter | Formula | Python |
|-----------|---------|--------|
| Proportion | p̂ ± z* × √(p̂(1-p̂)/n) | Manual calculation |
| Mean | x̄ ± t* × s/√n | Manual or `stats.t.ppf()` |

### Hypothesis Tests

| Test | When to Use | Python |
|------|------------|--------|
| Z-test for two proportions | Comparing proportions between groups | Manual (pooled proportion) |
| Two-sample t-test | Comparing means between groups | `ttest_ind(group1, group2)` |

### Key Takeaways

1. The **normal distribution** underpins most inference — learn `norm.cdf()` and `norm.ppf()` inside out
2. Remember: `norm.cdf()` gives the area **below**. For "above", use `1 - norm.cdf()`
3. **Confidence intervals** give a range of plausible values — not a "95% probability" of containing the truth
4. **Hypothesis testing** starts with assuming no effect (H₀) and asks "how unlikely is our data?"
5. **p-value < 0.05** = statistically significant, but **significant ≠ important** — always consider effect size
6. Use **Welch's t-test** (default in `ttest_ind`) for comparing means — it doesn't assume equal variances
7. "Fail to reject H₀" ≠ "accept H₀" — we never *prove* the null is true

---

## Exercises

````{exercise}
:label: ex9-normal-dist

**Exercise 1: The Normal Distribution**

The heights of adult males in the UK are approximately normally distributed with mean μ = 175 cm and standard deviation σ = 7 cm.

1. What proportion of men are taller than 185 cm?
2. What proportion of men are between 168 cm and 182 cm?
3. How tall does a man need to be to be in the tallest 5%?
4. What height marks the 25th percentile?
````

````{solution} ex9-normal-dist
:class: dropdown

```python
from scipy import stats

mu = 175
sigma = 7

# 1. Proportion taller than 185 cm
prop_above_185 = 1 - stats.norm.cdf(185, loc=mu, scale=sigma)
print(f"1. Proportion taller than 185 cm: {prop_above_185:.4f} ({prop_above_185:.1%})")

# 2. Proportion between 168 and 182 cm
prop_between = stats.norm.cdf(182, loc=mu, scale=sigma) - stats.norm.cdf(168, loc=mu, scale=sigma)
print(f"2. Proportion between 168 and 182 cm: {prop_between:.4f} ({prop_between:.1%})")

# 3. Height for tallest 5% (95th percentile)
height_95 = stats.norm.ppf(0.95, loc=mu, scale=sigma)
print(f"3. Tallest 5% threshold: {height_95:.1f} cm")

# 4. 25th percentile
height_25 = stats.norm.ppf(0.25, loc=mu, scale=sigma)
print(f"4. 25th percentile height: {height_25:.1f} cm")
```

```
1. Proportion taller than 185 cm: 0.0766 (7.7%)
2. Proportion between 168 and 182 cm: 0.6827 (68.3%)
3. Tallest 5% threshold: 186.5 cm
4. 25th percentile height: 170.3 cm
```
````

````{exercise}
:label: ex9-confidence-interval

**Exercise 2: Confidence Interval for a Proportion**

In a survey of 500 university students, 320 said they use public transport to get to campus.

1. Calculate the sample proportion
2. Calculate the standard error
3. Construct a 95% confidence interval for the true proportion
4. Would a 99% confidence interval be wider or narrower? Calculate it to verify.
````

````{solution} ex9-confidence-interval
:class: dropdown

```python
import numpy as np
from scipy import stats

n = 500
x = 320
p_hat = x / n

# 1. Sample proportion
print(f"1. Sample proportion: {p_hat:.4f} ({p_hat:.1%})")

# 2. Standard error
se = np.sqrt(p_hat * (1 - p_hat) / n)
print(f"2. Standard error: {se:.4f}")

# 3. 95% confidence interval
z_95 = stats.norm.ppf(0.975)
lower_95 = p_hat - z_95 * se
upper_95 = p_hat + z_95 * se
print(f"3. 95% CI: ({lower_95:.4f}, {upper_95:.4f})")

# 4. 99% confidence interval
z_99 = stats.norm.ppf(0.995)
lower_99 = p_hat - z_99 * se
upper_99 = p_hat + z_99 * se
print(f"4. 99% CI: ({lower_99:.4f}, {upper_99:.4f})")
print(f"   The 99% CI is WIDER — more confidence requires a wider range")
```

```
1. Sample proportion: 0.6400 (64.0%)
2. Standard error: 0.0215
3. 95% CI: (0.5979, 0.6821)
4. 99% CI: (0.5847, 0.6953)
   The 99% CI is WIDER — more confidence requires a wider range
```
````

````{exercise}
:label: ex9-z-test-proportions

**Exercise 3: Z-Test for Two Proportions**

A researcher wants to know if a new teaching method improves pass rates. In the traditional class, 65 out of 100 students passed. In the new method class, 78 out of 100 students passed.

1. State the null and alternative hypotheses
2. Calculate the pooled proportion
3. Calculate the standard error and z-statistic
4. Find the p-value and make a decision at α = 0.05
5. Write a one-sentence conclusion
````

````{solution} ex9-z-test-proportions
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
print(f"\n2. Pooled proportion: {p_pool:.4f}")

# 3. Standard error and z-statistic
se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
z_stat = (p1 - p2) / se
print(f"\n3. Standard error: {se:.4f}")
print(f"   z-statistic: {z_stat:.4f}")

# 4. p-value and decision
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
print(f"\n4. p-value: {p_value:.4f}")
if p_value < 0.05:
    print("   Decision: REJECT H₀ — significant difference in pass rates")
else:
    print("   Decision: FAIL TO REJECT H₀ — no significant difference")

# 5. Conclusion
print(f"\n5. The new teaching method had a significantly higher pass rate")
print(f"   (78% vs 65%, z = {z_stat:.2f}, p = {p_value:.4f}).")
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
:label: ex9-t-test

**Exercise 4: Two-Sample t-Test**

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

````{solution} ex9-t-test
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
print(f"   Version A: n={len(version_A)}, mean={version_A.mean():.1f}s, sd={version_A.std():.1f}s")
print(f"   Version B: n={len(version_B)}, mean={version_B.mean():.1f}s, sd={version_B.std():.1f}s")
print(f"   Difference: {version_B.mean() - version_A.mean():.1f}s")

# 2. Two-sample t-test
t_stat, p_value = ttest_ind(version_A, version_B)
print(f"\n2. TWO-SAMPLE t-TEST (Welch's)")
print(f"   t-statistic: {t_stat:.4f}")
print(f"   p-value: {p_value:.4f}")

# 3. Decision
print(f"\n3. DECISION")
if p_value < 0.05:
    print(f"   p-value ({p_value:.4f}) < 0.05: REJECT H₀")
    print(f"   The difference IS statistically significant.")
else:
    print(f"   p-value ({p_value:.4f}) >= 0.05: FAIL TO REJECT H₀")
    print(f"   The difference is NOT statistically significant.")

# 4. Practical significance
diff = version_B.mean() - version_A.mean()
print(f"\n4. PRACTICAL SIGNIFICANCE")
print(f"   The difference is {diff:.1f} seconds.")
print(f"   Whether this is practically meaningful depends on context:")
print(f"   - For an e-commerce site: 15 extra seconds could mean more purchases")
print(f"   - For a news article: probably not meaningful enough to matter")
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

### Birth Weights Sample (`birth_weights_sample.csv`)

A sample of 50 baby birth weights (in pounds), drawn from a normal distribution with a mean of 7.0 lbs and standard deviation of 1.5 lbs.

```python
import numpy as np
import pandas as pd

np.random.seed(42)  # Makes results reproducible

weights = pd.DataFrame({
    'weight_lbs': np.random.normal(7.0, 1.5, 50).round(2)
})

weights.to_csv('birth_weights_sample.csv', index=False)
```

**What's happening:**
- `np.random.seed(42)` ensures you get the same "random" numbers every time — this is called **reproducibility**
- `np.random.normal(7.0, 1.5, 50)` draws 50 values from a normal distribution with mean 7.0 and standard deviation 1.5
- `.round(2)` rounds to 2 decimal places

### Births and Smoking (`births_smoking.csv`)

A dataset of 1,000 births — 800 from nonsmoking mothers and 200 from smoking mothers. Nonsmokers' babies have a slightly higher mean birth weight.

```python
np.random.seed(42)

births = pd.DataFrame({
    'weight_lbs': np.concatenate([
        np.random.normal(7.2, 1.3, 800),   # Nonsmokers: mean 7.2 lbs, SD 1.3
        np.random.normal(6.7, 1.5, 200)    # Smokers: mean 6.7 lbs, SD 1.5
    ]).round(2),
    'habit': ['nonsmoker'] * 800 + ['smoker'] * 200
})

births.to_csv('births_smoking.csv', index=False)
```

**Why these numbers?** Research consistently shows that babies born to smoking mothers tend to weigh less on average. The 0.5 lb difference and the sample sizes here are inspired by real studies, though the specific values are simulated.

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
