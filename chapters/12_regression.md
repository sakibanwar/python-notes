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

# Introduction to Regression

In the last chapter we used summary statistics, group means, and visualisations to *describe* our data. But describing data only takes us so far. To actually answer questions like "how much more do graduates earn than non-graduates?" or "does experience matter once we account for education?", we need a tool that goes further. That tool is **regression**.

Regression is the workhorse of empirical economics and business analytics. It lets us:

- Quantify how one variable changes when another changes
- Hold other factors constant so we can isolate a single effect
- Compare the size of different effects on the same outcome
- Make predictions for new observations

In this chapter we'll build up regression from the simplest possible case (one predictor) all the way to multiple regression with both numeric and categorical predictors. We'll work through everything using the classic `wage1` dataset from Wooldridge — exactly the kind of dataset you might see in your econometrics module.

```{note}
**About the dataset.** The `wage1` dataset comes from Wooldridge's *Introductory Econometrics* (2019, 7th edition, Cengage). It contains 526 observations from the 1976 U.S. Current Population Survey (CPS), with information on hourly wages and worker characteristics. We accessed it via the [`wooldridge` Python package](https://pypi.org/project/wooldridge/) and saved it as a CSV in this book's `data/` folder.

Because the data is from 1976, the wage figures look low by today's standards (the average is about $5.90/hour). The *relationships* between variables, however, still illustrate the mechanics of regression beautifully — and they're directly comparable to examples you'll encounter in textbooks like Wooldridge or Békés & Kézdi.
```

---

## What is Regression?

At its heart, a regression finds the **best-fitting straight line** through your data. For a single predictor, the equation is:

$$y = \alpha + \beta \cdot x + \epsilon$$

Where:

- **y** is the dependent variable — what we're trying to explain (e.g., wage)
- **x** is the independent variable — what we're using to explain it (e.g., years of education)
- **α (alpha)** is the intercept — the value of y when x = 0
- **β (beta)** is the slope — how much y changes for a one-unit increase in x
- **ε (epsilon)** is the error term — everything we *haven't* captured

The job of the regression is to estimate α and β from the data. Once we have them, we can interpret the slope, test whether it's statistically different from zero, and even predict y for new values of x.

---

## Setting Up

Let's load our libraries and the `wage1` data:

```{code-cell} ipython3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

# Load the wage1 dataset from the book's data folder
df = pd.read_csv("../data/wage1.csv")

df.shape
```

```{tip}
**Running this code outside the book?** If you copy this code into Google Colab or your own notebook, the relative path `"../data/wage1.csv"` won't work. Replace it with the dataset's GitHub URL instead:

    df = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv")

That URL points to the same file in the book's GitHub repository and works from anywhere.
```

We have 526 workers with 24 variables. Let's peek at the first few rows:

```{code-cell} ipython3
df.head()
```

The variables we'll focus on are:

| Variable | Meaning |
|----------|---------|
| `wage` | Hourly earnings, in 1976 US dollars |
| `educ` | Years of education |
| `exper` | Years of potential work experience |
| `tenure` | Years with current employer |
| `female` | 1 if female, 0 if male |
| `married` | 1 if married, 0 if not |
| `lwage` | Natural log of wage (already computed for us) |

---

## Exploring the Data First

Before running any regression, you should always look at your data. Let's start with the summary statistics for our key variables:

```{code-cell} ipython3
df[["wage", "educ", "exper", "tenure", "female"]].describe().round(2)
```

A few things to notice:

- The average worker earns **$5.90/hour** (remember: 1976 dollars).
- The typical worker has **12.56 years of education** — about a high-school diploma plus a bit of college.
- The mean of `female` is **0.48**, meaning 48% of the sample are women.

### Visualising the Relationship

Education is the most natural starting predictor for wage. Let's see how the two relate:

```{code-cell} ipython3
sns.scatterplot(data=df, x="educ", y="wage", alpha=0.5, color="steelblue")
plt.xlabel("Years of education")
plt.ylabel("Hourly wage ($)")
plt.title("Wage vs Education")
plt.show()
```

There's clearly an upward trend: more education tends to come with higher wages. But notice the **enormous spread** at every level of education. Two workers with 12 years of schooling can earn very different wages. So while education matters, it's clearly not the *only* thing that matters. Regression will help us put a number on the average effect, despite that spread.

---

## Simple Linear Regression

Let's now fit our first regression: wage as a function of education. In Python we use the `statsmodels` library — specifically the `formula.api` interface, which we imported above as `smf`. Here's the line that does it:

```{code-cell} ipython3
model = smf.ols("wage ~ educ", data=df).fit()
```

That's a lot packed into one line. Let's unpack each piece, because every part of it is important.

### `smf.ols(...)` — pick the type of regression

`ols` stands for **Ordinary Least Squares**. It's the classic way of fitting a regression line: find the line that minimises the sum of the squared distances between each data point and the line. There are other types of regression (logistic, robust, quantile…), but OLS is by far the most common, and "linear regression" almost always means "OLS regression" unless someone says otherwise.

### The formula `"wage ~ educ"`

The string inside the brackets is the **formula** — it tells `statsmodels` what we're predicting and what we're using as a predictor.

The character that separates the two is the **tilde** `~`. Read it aloud as "predicted by". So:

> *wage* predicted by *educ*

This corresponds exactly to the equation we wrote earlier:

$$\text{wage} = \alpha + \beta \cdot \text{educ} + \epsilon$$

The variable on the **left of the tilde** is the dependent variable. The variable on the **right** is the independent variable. The names you put in the formula must match the column names in your DataFrame exactly — `statsmodels` is going to look them up there.

```{tip}
The formula syntax (`y ~ x`) comes from the R programming language, where it's used for everything from regression to ANOVA. If you ever take a stats course that uses R, you'll see exactly the same notation.
```

### `data=df` — where to find the columns

This tells `statsmodels` *which* DataFrame contains the columns named `wage` and `educ`. Without it, Python wouldn't know where to look — `wage` and `educ` are just strings inside a formula until we connect them to actual data.

### `.fit()` — actually estimate the model

`smf.ols(...)` on its own only **defines** the model — it doesn't compute anything yet. The `.fit()` method is what actually crunches the numbers and estimates α and β from the data. The result gets stored in our variable `model`.

```{warning}
A common beginner mistake is forgetting `.fit()`. If you do, you'll get an unfitted model object back — there will be no coefficients to look at, and trying to look at the summary later will fail. Always remember to chain `.fit()` on the end.
```

### Looking at the results: `model.summary()`

Once the model is fitted, all the results — coefficients, standard errors, p-values, R-squared, the lot — are stored inside the `model` object. The simplest way to see them is the `summary()` method:

```{code-cell} ipython3
print(model.summary())
```

That's a lot of output! Don't let it intimidate you — it's organised into three blocks:

1. **Top block** — overall model statistics: R-squared, sample size, F-statistic.
2. **Middle block** — the coefficient table. This is the part you'll spend most of your time looking at.
3. **Bottom block** — diagnostic tests for things like normality of residuals. We'll come back to those in the case-study chapter.

Let's go through them in turn.

---

## Interpreting Regression Output

### The Coefficients

The numbers in the coefficient table are the heart of the output:

| Variable | Coefficient | What it means |
|----------|-------------|---------------|
| `Intercept` | -0.90 | Predicted wage when `educ = 0` (a person with zero years of schooling) |
| `educ` | 0.54 | For each additional year of education, wage increases by about **$0.54/hour** |

So our estimated regression equation is:

$$\widehat{\text{wage}} = -0.90 + 0.54 \times \text{educ}$$

A worker with 12 years of schooling is therefore predicted to earn:

$$-0.90 + 0.54 \times 12 = 5.58 \text{ dollars/hour}$$

```{note}
Don't read too much into the negative intercept. It's the predicted wage for someone with **zero** years of education — but almost no one in the sample has zero years of education, so we're extrapolating well outside the cloud of data. Intercepts often look strange. The slope is usually what we care about.
```

### Statistical Significance: the p-value

The column **`P>|t|`** (the p-value) tells us whether each coefficient is statistically different from zero. A small p-value means it's unlikely we'd see a coefficient this large just by random chance if the *true* effect were zero.

- The coefficient on `educ` has a p-value of **0.000** — extremely strong evidence that education really does have a non-zero effect on wages.
- The intercept has a p-value of 0.187 — meaning we can't reject the hypothesis that the *true* intercept is zero. That's fine; we usually don't care about the intercept's significance.

The convention is to call a coefficient "statistically significant" when its p-value is below 0.05.

### Confidence Intervals

The columns **`[0.025  0.975]`** give the 95% confidence interval for each coefficient. For `educ`, the interval is `[0.437, 0.646]`.

In plain English: we're 95% confident that the true effect of one extra year of education on wages is somewhere between **44 cents and 65 cents per hour**. Notice the interval doesn't contain zero — another way of saying the coefficient is statistically significant.

### R-squared: How Well Does the Model Fit?

The number **R-squared = 0.165** tells us that education explains about **16.5%** of the variation in wages.

Is that good? It depends on what you're modelling. In economics, R² values for cross-sectional models on individual-level data are often modest like this — there's a lot more to wages than education alone. We'll improve the R² as we add more predictors.

```{tip}
R-squared always lies between 0 and 1.

- An R² of 0 means the model explains nothing.
- An R² of 1 means the model fits the data perfectly (very rare with real-world data).

In economics, R² in the 0.1–0.4 range is common for individual-level regressions and shouldn't make you panic.
```

---

## Visualising the Regression Line

A picture is the easiest way to see what the regression has done. Seaborn's `regplot()` draws the data and the fitted line in one go:

```{code-cell} ipython3
sns.regplot(
    data=df, x="educ", y="wage", ci=None,
    scatter_kws={"alpha": 0.4, "color": "steelblue"},
    line_kws={"color": "red"}
)
plt.xlabel("Years of education")
plt.ylabel("Hourly wage ($)")
plt.title("Wage vs Education with Fitted Regression Line")
plt.show()
```

The red line is exactly the equation we computed above. Notice how it **summarises** the cloud of points with a single straight line — that's all a simple regression really is.

### What are `scatter_kws` and `line_kws`?

These are the two arguments that probably look most unfamiliar in the call above. They let us style the **scatter points** and the **regression line** *separately*. Each is a Python dictionary of styling options:

- **`scatter_kws={"alpha": 0.4, "color": "steelblue"}`** — styles the points.
  - `alpha=0.4` makes the points partially transparent (where 0 is fully transparent and 1 is fully opaque). Transparency matters here because a lot of workers in our sample share the same education value (almost everyone has 12, 14, or 16 years of schooling), so without transparency the points pile on top of each other and you can't tell where the data is densest.
  - `color="steelblue"` sets the colour of the points.
- **`line_kws={"color": "red"}`** — styles the fitted regression line. We've just set its colour to red so it stands out clearly against the blue points.

You can pass **any** matplotlib styling keyword through either dictionary — `marker` (point shape), `s` (point size), `linestyle`, `linewidth`, and so on — and seaborn will hand them straight through to the underlying matplotlib call. Why two separate dictionaries? Because seaborn needs to know which styling applies to the points and which applies to the line; bundling them together would be ambiguous.

```{tip}
The `ci=None` argument hides the shaded confidence band. Try setting it to `ci=95` to see the 95% confidence band around the fitted line — it's a nice visual cue for how precisely the line is estimated at different values of x.
```

---

## Making Predictions

One useful thing about a regression model is that it lets us predict y for any value of x. In `statsmodels`, the `.fittedvalues` attribute gives us the predicted wage for every observation in the data, and `.resid` gives us the residual (actual minus predicted):

```{code-cell} ipython3
df["predicted"] = model.fittedvalues
df["residual"] = model.resid

df[["wage", "educ", "predicted", "residual"]].head()
```

A **negative residual** means the worker earns *less* than the model predicts; a **positive residual** means they earn more.

### Who Are the "Underpaid" and "Overpaid"?

We can sort by residual to find the workers whose actual wages most differ from the model's prediction:

```{code-cell} ipython3
# 5 workers earning much more than the model predicts
df.nlargest(5, "residual")[["wage", "educ", "predicted", "residual"]]
```

These are the workers whose hourly wages are dramatically higher than education alone would predict — perhaps they have lots of experience, work in lucrative industries, or simply got lucky on the labour market. **The point of looking at residuals is exactly this**: they show what's left unexplained when we use only one variable. It's a hint that we need more predictors.

---

## Multiple Regression

Education isn't the only thing that determines wages. What about work experience? What about how long someone has been with their current employer? **Multiple regression** lets us include several predictors in the same model.

The good news: the syntax barely changes. We still use `smf.ols(...)`, the formula still has `~` separating the outcome from the predictors, and we still call `.fit()`. The only difference is that we add more variables to the **right-hand side** of the tilde, separated by `+`:

```{code-cell} ipython3
model_multi = smf.ols("wage ~ educ + exper + tenure", data=df).fit()
print(model_multi.summary())
```

The formula `"wage ~ educ + exper + tenure"` reads as:

> *wage* predicted by *educ*, *exper*, and *tenure*

which corresponds to the equation:

$$\text{wage} = \alpha + \beta_1 \cdot \text{educ} + \beta_2 \cdot \text{exper} + \beta_3 \cdot \text{tenure} + \epsilon$$

Each predictor now has its own coefficient (β₁, β₂, β₃), and `statsmodels` estimates all of them at the same time.

```{warning}
The `+` in a formula is **not** mathematical addition — it's just shorthand for "include this variable as another predictor". Whether you write `educ + exper` or `exper + educ` makes no difference to the result; the order of predictors doesn't matter.
```

Three things jumped:

1. **R-squared rose from 0.165 to 0.306** — adding `exper` and `tenure` nearly doubled the variation we can explain.
2. **The coefficient on `educ` shifted slightly**, from 0.54 to 0.60. Why? Because in the simple regression, `educ` was implicitly picking up some of the effect of variables correlated with it (like experience). Now those effects are separated out.
3. **A new phrase enters the interpretation**: "holding other variables constant".

### Interpreting the New Coefficients

- **`educ`**: *Holding experience and tenure constant*, each additional year of education increases the predicted wage by **$0.60/hour**.
- **`tenure`**: *Holding education and experience constant*, each additional year with the current employer adds about **$0.17/hour**.
- **`exper`**: *Holding education and tenure constant*, each year of experience adds only **$0.02/hour** — and the p-value (0.064) means this isn't quite statistically significant at the 5% level.

The phrase "holding constant" (sometimes called "controlling for") is the key idea behind multiple regression. When you read a coefficient, mentally append "all else equal" — that's what the partial coefficient represents.

### Predicting a New Worker's Wage

Let's predict the wage for a worker with 16 years of education, 5 years of experience, and 2 years of tenure:

```{code-cell} ipython3
# Plug in the values
predicted = (model_multi.params["Intercept"]
             + model_multi.params["educ"]   * 16
             + model_multi.params["exper"]  * 5
             + model_multi.params["tenure"] * 2)
print(f"Predicted wage: ${predicted:.2f}/hour")
```

In 1976 dollars, $7.16/hour for a recent graduate looks reasonable. Try changing the values and see how the prediction shifts!

---

## Dummy Variables: Adding a Categorical Predictor

So far all our predictors have been numeric. But many interesting variables are **categorical** — yes/no, male/female, in-the-city/not. To use these in a regression, we encode them as **dummy variables**: 0 for "no", 1 for "yes".

In `wage1` the variable `female` is already coded this way: `1` if the worker is female, `0` if male. Let's see what happens when we add it to the model:

```{code-cell} ipython3
model_dummy = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit()
print(model_dummy.summary())
```

The coefficient on `female` is **-1.81**, with a p-value of 0.000. Here's how to read it:

> *Holding education, experience, and tenure constant, women in this sample earn about $1.81 less per hour than men, on average.*

That's a substantial gender wage gap — and notice that we're not just comparing average male and female wages (which would mix in differences in education, experience, etc.). We're comparing male and female workers *with the same education, experience, and tenure*. This is the central reason multiple regression is so powerful.

```{note}
A binary dummy is the simplest categorical variable. The reference category — what the dummy is being compared to — is whichever level is coded as 0. Here, **men (`female = 0`) are the reference group**, and the coefficient -1.81 tells us how women's wages compare to men's, holding everything else constant.
```

### Sanity Check: Mean Wage by Gender

Just to confirm we're not making things up, here are the raw mean wages by gender:

```{code-cell} ipython3
df.groupby("female")["wage"].agg(["mean", "count"]).round(2)
```

The raw difference is **\$2.51/hour**. Our regression coefficient is \$1.81 — *smaller* in magnitude. The gap shrinks once we control for education, experience, and tenure, because women in this sample have, on average, slightly less work experience. The remaining \$1.81 is what *can't* be explained by those three variables.

---

## R-squared vs Adjusted R-squared

You might have noticed that R-squared keeps going up as we add variables. Compare our three models:

| Model | Predictors | R² | Adjusted R² |
|-------|------------|------|-------------|
| Simple | `educ` | 0.165 | 0.163 |
| Multiple | `educ + exper + tenure` | 0.306 | 0.302 |
| With dummy | `educ + exper + tenure + female` | 0.364 | 0.359 |

Here's the trap: **R-squared *always* increases when you add a variable, even if the new variable is total nonsense.** That's because pure random noise will explain at least *some* variation by chance.

Adjusted R-squared fixes this by applying a penalty for each additional variable. If the new variable genuinely helps, adjusted R² rises. If it's just noise, adjusted R² may even fall.

| Metric | What it measures | When to use it |
|--------|------------------|----------------|
| **R²** | Proportion of variance explained | Any model — but be cautious comparing models of different sizes |
| **Adjusted R²** | R² with a penalty for extra predictors | Comparing models with **different** numbers of predictors |

```{tip}
Whenever you compare regression models with different numbers of variables, **report adjusted R²**. If a new variable raises R² but lowers adjusted R², it's probably not pulling its weight.
```

---

## Robust Standard Errors

There's one final adjustment we should always consider before treating any regression as final.

The standard errors in the output we've seen so far are based on a strong assumption: that the variance of the regression errors is the **same at every value of x**. This is called **homoskedasticity**. But in real-world data — especially cross-sectional data like ours — the variance often *isn't* constant. The spread of wages around the prediction is much wider for highly-paid workers than for the lowest-paid, for example. That's called **heteroskedasticity** (literally, "different scatter").

When heteroskedasticity is present, the *coefficients* you estimate are still fine, but the *standard errors* are wrong — and that means the p-values and confidence intervals are wrong too. Luckily there's an easy fix: compute the standard errors in a way that doesn't assume constant variance. These are called **heteroskedasticity-robust standard errors** (or just "robust SEs", or "HC errors" — proposed by the econometrician Halbert White, whose surname lives on in the HC abbreviation).

In `statsmodels`, you ask for them by passing **one extra argument to `.fit()`**:

```{code-cell} ipython3
model_robust = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit(cov_type="HC3")
print(model_robust.summary())
```

The `cov_type="HC3"` argument is what selects the robust calculation. There are several variants — `HC0`, `HC1`, `HC2`, `HC3` — but `HC3` is the modern default in econometrics, so we'll stick with that.

Compare this to the previous output (the model with the gender dummy). Two things to notice:

| Variable | Default SE | Robust (HC3) SE |
|----------|------------|-----------------|
| `Intercept` | 0.725 | 0.838 |
| `educ` | 0.049 | 0.062 |
| `tenure` | 0.021 | 0.029 |

**The coefficients didn't move at all.** That's the whole point — robust SEs only adjust the *uncertainty* around each estimate, not the estimates themselves. The standard errors did move, and in this case several got bigger. Look closely at the intercept: its p-value went from 0.031 (significant at the 5% level) to 0.061 (not significant). For the `educ` coefficient the shift is small enough not to matter, but in a different dataset it could easily flip a borderline result the other way.

```{note}
**Why does the column header say `z` instead of `t`?** Once you ask for robust standard errors, `statsmodels` uses a normal distribution for inference rather than a t-distribution (which assumes homoskedasticity). For sample sizes above ~30 the practical difference is negligible, but that's why the column heading changes.
```

```{tip}
**Rule of thumb in applied work**: if you're running a cross-sectional regression on individuals, firms, or countries, just pass `cov_type="HC3"` by default. The cost is one extra argument; the benefit is you don't get caught out by hidden heteroskedasticity. Békés & Kézdi follow this convention throughout their textbook, and most empirical economics papers do the same.
```

---

## Advanced: Log Transformations

```{note}
**Optional on first read.** This subsection introduces the most useful trick from applied econometrics: putting variables in logs. If you're meeting regression for the first time, feel free to skip ahead, get comfortable with the basics, and return to this section later. We come back to log models in much more depth in Chapter 14's case study.
```

Sometimes a straight line is a poor fit because the relationship is *multiplicative* rather than *additive*. A 10% pay rise on a \$100,000 salary (\$10,000) is much bigger than a 10% raise on a \$20,000 salary (\$2,000) — but in additive (level-level) terms it's a wildly different number. Logs let us think in proportional terms.

The four model types you'll see in econometrics are:

| Name | Equation | Interpretation of β |
|------|----------|---------------------|
| **Level-Level** | y = α + β·x | A 1-unit increase in x → β-unit change in y |
| **Log-Level**   | ln(y) = α + β·x | A 1-unit increase in x → roughly **β × 100%** change in y |
| **Level-Log**   | y = α + β·ln(x) | A 1% increase in x → about **β/100** unit change in y |
| **Log-Log**     | ln(y) = α + β·ln(x) | A 1% increase in x → about **β%** change in y (this is an **elasticity**) |

The most common in wage equations is the **log-level** model — `ln(wage)` regressed on `educ`. The coefficient on education then has a percentage interpretation, which is much more natural than dollars.

Conveniently, `wage1` already includes a column called `lwage`, which is just `np.log(wage)`. Let's run all four models and put the results side by side.

### Setting Up the Models

```{code-cell} ipython3
# Create log of educ for the level-log and log-log models
df["ln_educ"] = np.log(df["educ"].clip(lower=1))   # clip avoids log(0)

m_level_level = smf.ols("wage  ~ educ",    data=df).fit()
m_log_level   = smf.ols("lwage ~ educ",    data=df).fit()
m_level_log   = smf.ols("wage  ~ ln_educ", data=df).fit()
m_log_log     = smf.ols("lwage ~ ln_educ", data=df).fit()
```

```{warning}
You can't take the natural log of zero or a negative number — Python will give you `-inf` or `nan`. The `.clip(lower=1)` trick replaces any zero values with 1 (so `ln(1) = 0`) before taking the log. There are 6 workers in `wage1` with zero years of education; this nudge avoids breaking the model.
```

### The Headline Result: Log-Level

Let's look at the log-level model first, since it's the most common:

```{code-cell} ipython3
print(f"Coefficient on educ (log-level): {m_log_level.params['educ']:.4f}")
print(f"R-squared:                       {m_log_level.rsquared:.4f}")
```

The coefficient is **0.083**. Multiplied by 100, that's **8.3%**:

> Each additional year of education is associated with about an **8.3% increase in hourly wage**, holding everything else constant.

That's the famous "**return to education**" result — and 8% per year of schooling is very close to numbers reported across decades and countries.

### Comparing All Four Specifications

Here are the four models side by side:

| Model | Equation | Coefficient | R² | Interpretation |
|-------|----------|-------------|------|----------------|
| Level-Level | `wage ~ educ` | 0.541 | 0.165 | One more year of educ → **$0.54/hour** more |
| Log-Level   | `lwage ~ educ` | 0.083 | 0.186 | One more year of educ → **8.3%** more |
| Level-Log   | `wage ~ ln(educ)` | 4.105 | 0.106 | A 1% increase in educ → **$0.04/hour** more |
| Log-Log     | `lwage ~ ln(educ)` | 0.637 | 0.123 | A 1% increase in educ → **0.64%** more (elasticity) |

```{tip}
**Which one should I use?** In practice, **log-level** is by far the most common form for wage equations because the coefficient gives you a clean percentage change for each additional unit of x. You'll see it written as `ln(wage)` (or `log(wage)`) in nearly every empirical labour economics paper.
```

For our purposes, the takeaway is: **the choice of functional form matters**. The same data can produce very different-looking coefficients depending on whether the variables are in levels or logs, and you should pick the form whose interpretation matches the question you're asking.

---

## Putting It All Together

A typical workflow for a regression analysis looks like this:

```python
# 1. Load the data
df = pd.read_csv("../data/wage1.csv")

# 2. Explore — describe, scatterplots, group means
df[["wage", "educ", "exper", "tenure"]].describe()
sns.regplot(data=df, x="educ", y="wage", ci=None)

# 3. Fit a simple model first
m1 = smf.ols("wage ~ educ", data=df).fit()
print(m1.summary())

# 4. Add more predictors
m2 = smf.ols("wage ~ educ + exper + tenure", data=df).fit()

# 5. Add dummies for categorical variables
m3 = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit()

# 6. Use robust standard errors for cross-sectional data
m3_robust = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit(cov_type="HC3")

# 7. Try a log specification for percentage interpretation
m4 = smf.ols("lwage ~ educ + exper + tenure + female", data=df).fit()

# 8. Compare R-squared / adjusted R-squared, look at residuals,
#    and think carefully about what each coefficient means
```

```{warning}
**Correlation is not causation.** A statistically significant regression coefficient tells you that two variables move together once others are controlled for — *not* that one causes the other. Our `female` coefficient of -1.81 doesn't prove gender causes lower wages; it could reflect occupational segregation, discrimination, differences in unmeasured experience, or many other factors. Be careful with the language you use when reporting results.
```

---

## What's Next

Now that you can run a regression and interpret the output, two natural questions follow:

- **"How do I get these results into my dissertation in Word?"** That's exactly what we tackle in the next chapter — Chapter 13 is dedicated to exporting regression tables, summary statistics, and Excel files in a way that survives data updates.
- **"What if the relationship between x and y isn't a straight line, or the residuals look weird?"** Chapter 14 is a full case study using a hotels dataset, where we work through log transformations, polynomial terms, robust standard errors, and full diagnostic checks end-to-end.

---

## Exercises

````{exercise}
:label: ex11-simple

**Exercise 1: A First Regression**

Using the `wage1` dataset:

1. Fit a simple linear regression of `wage` on `tenure`.
2. What is the coefficient on `tenure`? Interpret it in plain English.
3. Is the coefficient statistically significant at the 5% level?
4. What proportion of the variation in wages does `tenure` alone explain?
````

````{solution} ex11-simple
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("../data/wage1.csv")

m = smf.ols("wage ~ tenure", data=df).fit()
print(m.summary())

print(f"\nCoefficient on tenure: {m.params['tenure']:.4f}")
print(f"P-value: {m.pvalues['tenure']:.4f}")
print(f"R-squared: {m.rsquared:.4f}")
```

**Interpretation:** Each additional year with the current employer is associated with about a $0.17/hour increase in wages. The coefficient is highly significant (p < 0.001), but `tenure` alone only explains about 7% of the variation in wages — so there's a lot of other factors at play.
````

````{exercise}
:label: ex11-multi

**Exercise 2: Multiple Regression and "All Else Equal"**

Using `wage1`:

1. Fit a multiple regression of `wage` on `educ`, `exper`, and `tenure`.
2. Suppose Alice has 16 years of education, 5 years of experience, and 2 years of tenure. What is her predicted hourly wage?
3. Suppose Bob has 12 years of education, 25 years of experience, and 10 years of tenure. What is his predicted hourly wage?
4. Comparing them, what does the multiple regression tell you about which factor matters most for wages in this sample?
````

````{solution} ex11-multi
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("../data/wage1.csv")

m = smf.ols("wage ~ educ + exper + tenure", data=df).fit()

# Alice
alice = (m.params["Intercept"]
         + m.params["educ"]   * 16
         + m.params["exper"]  * 5
         + m.params["tenure"] * 2)

# Bob
bob = (m.params["Intercept"]
       + m.params["educ"]   * 12
       + m.params["exper"]  * 25
       + m.params["tenure"] * 10)

print(f"Predicted wage for Alice: ${alice:.2f}/hour")
print(f"Predicted wage for Bob:   ${bob:.2f}/hour")
```

```
Predicted wage for Alice: $7.16/hour
Predicted wage for Bob:   $6.49/hour
```

Alice earns slightly more despite having far less experience and tenure, because the coefficient on `educ` (\$0.60/year) is much larger than the coefficient on `exper` (\$0.02/year) or `tenure` (\$0.17/year). In this sample, education has the largest per-unit effect on wages.
````

````{exercise}
:label: ex11-dummy

**Exercise 3: The Gender Wage Gap**

Using `wage1`:

1. Fit a regression of `wage` on `female` only.
2. What does the coefficient on `female` tell you about the **raw** gender wage gap (without controlling for anything else)?
3. Now fit a regression of `wage` on `educ`, `exper`, `tenure`, and `female`.
4. How does the coefficient on `female` change once you control for these other variables? Why?
````

````{solution} ex11-dummy
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("../data/wage1.csv")

# Raw gap
m_raw = smf.ols("wage ~ female", data=df).fit()
print(f"Raw gap (female coef):      {m_raw.params['female']:.3f}")

# Controlled gap
m_ctrl = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit()
print(f"Controlled gap (female coef): {m_ctrl.params['female']:.3f}")
```

```
Raw gap (female coef):      -2.512
Controlled gap (female coef): -1.811
```

**Interpretation:** Without any controls, women in the sample earn \$2.51/hour less than men on average. Once we control for education, experience, and tenure, the gap shrinks to \$1.81/hour but doesn't disappear. The shrinkage tells us that part of the raw gap is explained by women in the sample having, on average, slightly less experience and tenure — and the remaining \$1.81 is the "unexplained" gap that controlling for those factors cannot account for.
````

````{exercise}
:label: ex11-loglevel

**Exercise 4: Log-Level Wage Equation**

Using `wage1`:

1. Fit a log-level regression: `lwage ~ educ + exper + tenure + female`.
2. Multiply the coefficient on `educ` by 100 and interpret it as a percentage return to schooling.
3. Multiply the coefficient on `female` by 100 and interpret it as a percentage gender wage gap (holding other variables constant).
4. Compare the R² of this log-level model to the R² of the level-level model with the same predictors. Which has a higher R²?
````

````{solution} ex11-loglevel
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv("../data/wage1.csv")

m_log   = smf.ols("lwage ~ educ + exper + tenure + female", data=df).fit()
m_level = smf.ols("wage  ~ educ + exper + tenure + female", data=df).fit()

print(f"Log-level coefficients:")
print(f"  educ   = {m_log.params['educ']:.4f}  →  {m_log.params['educ']*100:.1f}% per year")
print(f"  female = {m_log.params['female']:.4f}  →  {m_log.params['female']*100:.1f}% gap")

print(f"\nR-squared (log-level):  {m_log.rsquared:.4f}")
print(f"R-squared (level-level): {m_level.rsquared:.4f}")
```

```
Log-level coefficients:
  educ   = 0.0875  →  8.7% per year
  female = -0.3011  →  -30.1% gap

R-squared (log-level):  0.3923
R-squared (level-level): 0.3635
```

**Interpretation:** Each additional year of education is associated with roughly an 8.7% increase in hourly wage, holding everything else constant. Women in the sample earn about 30% less than men, holding education, experience, and tenure constant. The log-level model has a slightly higher R² (0.392 vs 0.364) — log models often fit wage data better because the spread of wages grows with the level of wages, which is exactly what taking logs accommodates.

```{note}
The R² from a log model and a level model are technically not directly comparable, because they explain variation in *different* dependent variables (`lwage` vs `wage`). The comparison above is a useful rule of thumb, but in serious applied work you'd use criteria like AIC or out-of-sample fit instead.
```
````
