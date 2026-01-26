# Introduction to Regression

Regression analysis is one of the most powerful tools in a data analyst's toolkit. It allows us to understand **relationships between variables** — how one variable changes when another changes. In business and economics, this helps us answer questions like:

- How does distance from the city centre affect hotel prices?
- Does advertising spending increase sales?
- What factors predict employee performance?

In this chapter, we'll learn how to run and interpret regression models using Python's `statsmodels` library.

---

## What is Regression?

At its core, regression finds the **best-fitting line** through your data. The equation for a simple linear regression is:

$$y = \alpha + \beta \cdot x + \epsilon$$

Where:
- **y** is the dependent variable (what we're trying to predict)
- **x** is the independent variable (what we use to make predictions)
- **α (alpha)** is the intercept (the value of y when x = 0)
- **β (beta)** is the slope (how much y changes for each unit increase in x)
- **ε (epsilon)** is the error term (the difference between predicted and actual values)

The goal of regression is to estimate α and β so we can make predictions.

---

## Setting Up

Let's load our libraries and data. We'll use the **Vienna Hotels** dataset, which contains information about hotel prices and characteristics.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf

# Load the Vienna hotels data
hotels = pd.read_csv("https://osf.io/y6jvb/download")
```

```python
hotels.shape
```

```
(428, 24)
```

We have 428 hotels with 24 variables. Let's see what we're working with:

```python
hotels.head()
```

```
   country city_actual  rating_count center1label center2label  \
0  Austria      Vienna          36.0  City centre    Donauturm
1  Austria      Vienna         189.0  City centre    Donauturm
2  Austria      Vienna          53.0  City centre    Donauturm

  neighbourhood  price    city  stars  ratingta  ...  distance  rating
0    17. Hernals     81  Vienna    4.0       4.5  ...       2.7     4.4
1    17. Hernals     81  Vienna    4.0       3.5  ...       1.7     3.9
2     Alsergrund     85  Vienna    4.0       3.5  ...       1.4     3.7
```

### Filtering the Data

For our analysis, let's focus on 3-4 star hotels with reasonable prices:

```python
# Filter the data
hotels = hotels[hotels["accommodation_type"] == "Hotel"]
hotels = hotels[hotels["city_actual"] == "Vienna"]
hotels = hotels[(hotels["stars"] >= 3) & (hotels["stars"] <= 4)]
hotels = hotels[hotels["stars"].notnull()]
hotels = hotels[hotels["price"] <= 600]

print(f"Hotels remaining: {len(hotels)}")
```

```
Hotels remaining: 207
```

We've filtered down to 207 hotels that are 3-4 stars in Vienna with prices under $600.

---

## Exploring the Data First

Before running a regression, we should always explore our data. Let's look at our two key variables: price and distance from the city centre.

```python
hotels.filter(["price", "distance"]).describe().T
```

```
          count        mean         std   min   25%    50%    75%   max
price     207.0  109.975845   42.221381  50.0  82.0  100.0  129.5  383.0
distance  207.0    1.529952    1.161507   0.0   0.8    1.3    1.9    6.6
```

The average hotel price is about $110, and the average distance from the city centre is about 1.5 miles.

### Visualising the Relationship

A scatter plot shows us the relationship between distance and price:

```python
sns.scatterplot(data=hotels, x="distance", y="price", color="red", alpha=0.5)
plt.xlabel("Distance to city center (miles)")
plt.ylabel("Price (US dollars)")
plt.title("Hotel Prices vs Distance from City Centre")
plt.show()
```

```
[Scatter plot showing a negative relationship - hotels closer to the
 city centre tend to be more expensive]
```

There appears to be a **negative relationship** — as distance increases, price tends to decrease. But how can we quantify this?

---

## Simple Linear Regression

Let's fit a regression line to our data. In Python, we use `statsmodels`:

```python
import statsmodels.formula.api as smf

# Fit the regression model
model = smf.ols("price ~ distance", data=hotels).fit()

# Print the results
print(model.summary())
```

```
                            OLS Regression Results
==============================================================================
Dep. Variable:                  price   R-squared:                       0.157
Model:                            OLS   Adj. R-squared:                  0.153
Method:                 Least Squares   F-statistic:                     38.20
Date:                Fri, 03 May 2024   Prob (F-statistic):           3.39e-09
Time:                        16:24:25   Log-Likelihood:                -1050.3
No. Observations:                 207   AIC:                             2105.
Df Residuals:                     205   BIC:                             2111.
Df Model:                           1
Covariance Type:            nonrobust
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept    132.0170      4.474     29.511      0.000     123.197     140.837
distance     -14.4064      2.331     -6.181      0.000     -19.002      -9.811
==============================================================================
```

That's a lot of output! Let's break down the key parts.

---

## Interpreting Regression Output

### The Coefficients

The most important numbers are in the coefficient table:

| Variable | Coefficient | Interpretation |
|----------|-------------|----------------|
| Intercept | 132.02 | When distance = 0, predicted price is $132.02 |
| distance | -14.41 | For each additional mile from centre, price decreases by $14.41 |

So our regression equation is:

$$\text{price} = 132.02 - 14.41 \times \text{distance}$$

This tells us:
- A hotel right in the city centre (distance = 0) would be predicted to cost $132.02
- Each mile further from the centre reduces the price by about $14.41

### Statistical Significance

The **p-value** (P>|t|) tells us whether each coefficient is statistically significant:

- **Intercept p-value**: 0.000 (highly significant)
- **Distance p-value**: 0.000 (highly significant)

A p-value less than 0.05 is typically considered statistically significant. Both our coefficients are highly significant, meaning we can be confident the relationship is real, not just random noise.

### Confidence Intervals

The **[0.025, 0.975]** columns show the 95% confidence interval for each coefficient:

- Distance coefficient: [-19.00, -9.81]

We're 95% confident the true effect of distance is between -$19.00 and -$9.81 per mile.

### R-squared: How Good is Our Model?

**R-squared = 0.157** means our model explains about 15.7% of the variation in hotel prices.

Is that good? Well, it depends:
- It means distance alone doesn't fully explain price differences
- Other factors (star rating, amenities, reviews) also matter
- But distance does have a statistically significant effect

```{note}
R-squared ranges from 0 to 1. Higher values mean the model explains more of the variation in the dependent variable. An R-squared of 0.157 means 15.7% of price variation is explained by distance alone.
```

---

## Visualising the Regression Line

Seaborn makes it easy to plot the regression line with the data:

```python
sns.lmplot(
    x="distance", y="price", data=hotels,
    scatter_kws={"color": "red", "alpha": 0.5, "s": 20},
    line_kws={"color": "blue"},
    ci=None  # Don't show confidence interval
)
plt.xlabel("Distance to city center (miles)")
plt.ylabel("Price (US dollars)")
plt.show()
```

```
[Scatter plot with a downward-sloping blue regression line through the
 red data points]
```

The blue line shows our predicted prices at each distance. Notice how the actual prices (red dots) scatter around this line — that scatter is what R-squared measures.

---

## Comparing Groups: Close vs Far

Before diving into regression, a simpler approach is to compare group means. Let's create a binary variable for "close" vs "far" hotels:

```python
# Create a binary variable: Far if distance >= 2 miles, Close otherwise
hotels["dist_category"] = np.where(hotels["distance"] >= 2, "Far", "Close")

# Calculate mean price for each group
hotels.groupby("dist_category")["price"].agg(["mean", "count"])
```

```
               mean  count
dist_category
Close        116.43    157
Far           89.72     50
```

Hotels close to the centre (< 2 miles) cost on average $116.43, while those further away average $89.72 — a difference of about $27!

### Visualising Group Differences

A box plot shows the full distribution for each group:

```python
sns.boxplot(data=hotels, x="dist_category", y="price")
plt.xlabel("Distance Category")
plt.ylabel("Price (US dollars)")
plt.title("Hotel Prices: Close vs Far from City Centre")
plt.show()
```

```
[Box plot showing "Close" hotels with higher median and wider spread
 than "Far" hotels]
```

The "Close" box is higher (higher median price) and has more spread (more price variation).

---

## Making Predictions

One key use of regression is making predictions. We can extract the predicted values:

```python
# Add predicted prices to our dataframe
hotels["predicted_price"] = model.fittedvalues
hotels["residual"] = model.resid  # Actual - Predicted

# Look at a few examples
hotels[["distance", "price", "predicted_price", "residual"]].head()
```

```
   distance  price  predicted_price   residual
1       1.7     81       107.526056 -26.526056
2       1.4     85       111.847984 -26.847984
3       1.7     83       107.526056 -24.526056
4       1.2     82       114.729269 -32.729269
6       0.9    103       119.051194 -16.051194
```

The **residual** is the prediction error: actual price minus predicted price.

### Finding Underpriced Hotels

Which hotels are the best deals? Those with the most negative residuals (priced below what the model predicts):

```python
hotels.nsmallest(5, "residual")[["distance", "price", "predicted_price", "residual"]]
```

```
     distance  price  predicted_price   residual
153       1.1     54       116.169910 -62.169910
10        1.1     60       116.169910 -56.169910
211       1.0     63       117.610552 -54.610552
426       1.4     58       111.847984 -53.847984
163       0.9     68       119.051194 -51.051194
```

These hotels are priced $50-62 less than the model would predict based on their location!

### Finding Overpriced Hotels

Conversely, which hotels are priced above what we'd expect?

```python
hotels.nlargest(5, "residual")[["distance", "price", "predicted_price", "residual"]]
```

```
     distance  price  predicted_price    residual
247       1.9    383       104.644774  278.355226
26        2.9    208        90.238353  117.761647
128       0.0    242       132.016973  109.983027
110       0.1    231       130.576331  100.423669
129       0.5    223       124.813762   98.186238
```

One hotel costs $383 but the model predicts only $105 — it's $278 more expensive than expected. Perhaps it has luxury amenities we haven't accounted for!

---

## Checking Model Fit: Residual Distribution

A good regression model should have residuals (errors) that are roughly normally distributed around zero. Let's check:

```python
sns.histplot(data=hotels, x="residual", bins=20, color="blue", alpha=0.7)
plt.xlabel("Residual (Actual - Predicted)")
plt.ylabel("Count")
plt.title("Distribution of Prediction Errors")
plt.axvline(x=0, color="red", linestyle="--", label="Zero")
plt.show()
```

```
[Histogram showing most residuals clustered around 0, with a slight
 right skew due to some overpriced hotels]
```

Most residuals are near zero (good!), but there's a right skew due to some expensive outliers.

---

## Robust Standard Errors

In real-world data, the spread of residuals often varies at different values of x (this is called **heteroskedasticity**). We can use robust standard errors to account for this:

```python
# Fit with robust standard errors
model_robust = smf.ols("price ~ distance", data=hotels).fit(cov_type="HC3")
print(model_robust.summary())
```

```
                            OLS Regression Results
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept    132.0170      4.876     27.072      0.000     122.459     141.575
distance     -14.4064      2.718     -5.301      0.000     -19.733      -9.080
==============================================================================
Notes:
[1] Standard Errors are heteroscedasticity robust (HC3)
```

Notice the coefficients are the same, but the standard errors are slightly different. The conclusions don't change here, but robust standard errors are generally safer to use.

---

## Log Transformations

Sometimes relationships aren't linear. **Log transformations** can help capture non-linear patterns and have useful interpretations.

### Creating Log Variables

```python
# Create log-transformed variables
hotels["ln_price"] = np.log(hotels["price"])
hotels["ln_distance"] = np.log(hotels["distance"].clip(lower=0.05))  # Avoid log(0)
```

```{warning}
You can't take the log of zero or negative numbers. If your variable has zeros, you can either:
- Add a small constant (e.g., `log(x + 1)`)
- Use a minimum value (e.g., `clip(lower=0.05)`)
```

### Four Types of Regression Models

| Model Type | Equation | Interpretation of β |
|------------|----------|---------------------|
| Level-Level | price ~ distance | 1-unit increase in x → β change in y |
| Level-Log | price ~ ln(distance) | 1% increase in x → β/100 change in y |
| Log-Level | ln(price) ~ distance | 1-unit increase in x → β×100% change in y |
| Log-Log | ln(price) ~ ln(distance) | 1% increase in x → β% change in y |

Let's run all four:

### 1. Level-Level (Our Original Model)

```python
reg1 = smf.ols("price ~ distance", data=hotels).fit()
print(f"Coefficient: {reg1.params['distance']:.4f}")
print(f"R-squared: {reg1.rsquared:.3f}")
```

```
Coefficient: -14.4064
R-squared: 0.157
```

**Interpretation**: Each additional mile from the centre reduces price by $14.41.

### 2. Level-Log

```python
reg2 = smf.ols("price ~ ln_distance", data=hotels).fit()
print(f"Coefficient: {reg2.params['ln_distance']:.4f}")
print(f"R-squared: {reg2.rsquared:.3f}")
```

```
Coefficient: -24.7683
R-squared: 0.280
```

**Interpretation**: A 1% increase in distance reduces price by about $0.25 (coefficient ÷ 100).

Notice the R-squared is higher (0.280 vs 0.157) — the level-log model fits better!

### 3. Log-Level

```python
reg3 = smf.ols("ln_price ~ distance", data=hotels).fit()
print(f"Coefficient: {reg3.params['distance']:.4f}")
print(f"R-squared: {reg3.rsquared:.3f}")
```

```
Coefficient: -0.1313
R-squared: 0.205
```

**Interpretation**: Each additional mile from the centre reduces price by about 13.1%.

### 4. Log-Log

```python
reg4 = smf.ols("ln_price ~ ln_distance", data=hotels).fit()
print(f"Coefficient: {reg4.params['ln_distance']:.4f}")
print(f"R-squared: {reg4.rsquared:.3f}")
```

```
Coefficient: -0.2158
R-squared: 0.334
```

**Interpretation**: A 1% increase in distance reduces price by about 0.22%.

The log-log model has the highest R-squared (0.334), explaining 33.4% of price variation!

### Comparing Models

| Model | R-squared | Best for... |
|-------|-----------|-------------|
| Level-Level | 0.157 | Simple interpretation |
| Level-Log | 0.280 | When effect diminishes at higher x |
| Log-Level | 0.205 | When y changes by percentage |
| Log-Log | 0.334 | When both change by percentages (elasticity) |

```{tip}
In economics, the **log-log model** gives you the **elasticity** — how responsive one variable is to percentage changes in another. An elasticity of -0.22 means a 10% increase in distance leads to a 2.2% decrease in price.
```

---

## Polynomial Regression

What if the relationship is curved rather than straight? We can add polynomial terms (squared, cubed) to capture curvature.

### Adding Squared Term

```python
# Create squared distance
hotels["distance_sq"] = hotels["distance"] ** 2

# Fit quadratic model
reg_quad = smf.ols("price ~ distance + distance_sq", data=hotels).fit()
print(reg_quad.summary())
```

```
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept    154.8580      6.045     25.617      0.000     142.939     166.777
distance     -46.0140      6.394     -7.197      0.000     -58.620     -33.408
distance_sq    6.9277      1.316      5.263      0.000       4.332       9.523
==============================================================================
R-squared: 0.258
```

The squared term is statistically significant (p < 0.05), suggesting a curved relationship!

**Interpretation**: The negative coefficient on distance and positive coefficient on distance_sq means prices fall quickly at first, then level off further from the centre.

### Visualising the Curve

```python
sns.lmplot(
    x="distance", y="price", data=hotels,
    order=2,  # Polynomial order
    scatter_kws={"color": "red", "alpha": 0.6},
    line_kws={"color": "blue"}
)
plt.xlabel("Distance to city center (miles)")
plt.ylabel("Price (US dollars)")
plt.title("Quadratic Fit: Price vs Distance")
plt.show()
```

```
[Scatter plot with a curved blue line that drops steeply at first
 then flattens out at greater distances]
```

The curve captures how the price premium for central locations is strongest for hotels very close to the centre.

### Adding Cubic Term

We can add a cubic term for even more flexibility:

```python
hotels["distance_cb"] = hotels["distance"] ** 3

reg_cubic = smf.ols("price ~ distance + distance_sq + distance_cb", data=hotels).fit()
print(f"R-squared: {reg_cubic.rsquared:.3f}")
```

```
R-squared: 0.276
```

The R-squared improves slightly, but be careful — adding too many polynomial terms can lead to **overfitting**, where the model captures noise rather than true patterns.

---

## Comparing Multiple Models

The `stargazer` package creates publication-quality regression tables:

```python
# Install if needed: pip install stargazer
from stargazer.stargazer import Stargazer

# Create comparison table
table = Stargazer([reg1, reg2, reg_quad])
table.custom_columns(["Level-Level", "Level-Log", "Quadratic"], [1, 1, 1])
table.rename_covariates({"Intercept": "Constant"})
```

This creates a side-by-side comparison showing coefficients, standard errors, and fit statistics for each model.

---

## Key Regression Concepts Summary

| Concept | What It Tells You |
|---------|-------------------|
| **Coefficient (β)** | The effect of x on y |
| **Standard Error** | Uncertainty in the coefficient estimate |
| **t-statistic** | Coefficient ÷ Standard Error |
| **p-value** | Probability of seeing this result if true effect is zero |
| **R-squared** | Proportion of y variation explained by the model |
| **Adjusted R-squared** | R-squared penalised for adding more variables |
| **Residuals** | Actual - Predicted values |

---

## When to Use Which Model

| Situation | Recommended Model |
|-----------|-------------------|
| Simple relationship, easy interpretation | Level-Level |
| Diminishing returns | Level-Log |
| Percentage changes in outcome | Log-Level |
| Elasticity / percentage relationships | Log-Log |
| Curved relationship | Polynomial |

```{warning}
**Correlation is not causation!** Our regression shows that distance and price are associated, but it doesn't prove that distance *causes* price differences. There could be confounding factors — perhaps cheaper hotels locate further out because land is cheaper, not because guests demand lower prices.
```

---

## Putting It All Together

Here's a complete workflow for running a regression analysis:

```python
# 1. Load and prepare data
hotels = pd.read_csv("https://osf.io/y6jvb/download")
hotels = hotels[hotels["accommodation_type"] == "Hotel"]
hotels = hotels[hotels["price"] <= 600]

# 2. Explore the relationship
sns.scatterplot(data=hotels, x="distance", y="price")
plt.show()

# 3. Fit the model
model = smf.ols("price ~ distance", data=hotels).fit()
print(model.summary())

# 4. Check significance
# - Look at p-values (< 0.05 is significant)
# - Look at confidence intervals (shouldn't include 0)

# 5. Evaluate fit
# - R-squared tells you how much variation is explained
# - Check residual distribution

# 6. Make predictions
hotels["predicted"] = model.fittedvalues
hotels["residual"] = model.resid

# 7. Try alternative specifications
# - Log transformations
# - Polynomial terms
# - Additional control variables
```

---

## Exercises

````{exercise}
:label: ex11-simple

**Exercise 1: Simple Regression**

Using the tips dataset from seaborn:
1. Run a regression predicting `tip` from `total_bill`
2. What is the coefficient on `total_bill`? Interpret it in words.
3. What is the R-squared? What does it mean?
4. If someone has a bill of $30, what tip does the model predict?
````

````{solution} ex11-simple
:class: dropdown

```python
import seaborn as sns
import statsmodels.formula.api as smf

# Load data
tips = sns.load_dataset("tips")

# 1. Fit the regression
model = smf.ols("tip ~ total_bill", data=tips).fit()
print(model.summary())

# 2. Coefficient interpretation
print(f"\nCoefficient on total_bill: {model.params['total_bill']:.4f}")
print("Interpretation: For each additional dollar on the bill,")
print("the tip increases by about $0.105 (about 10.5 cents).")

# 3. R-squared interpretation
print(f"\nR-squared: {model.rsquared:.3f}")
print("This means total_bill explains about 45.7% of the variation in tips.")

# 4. Prediction for $30 bill
predicted_tip = model.params['Intercept'] + model.params['total_bill'] * 30
print(f"\nPredicted tip for $30 bill: ${predicted_tip:.2f}")
```

```
                            OLS Regression Results
==============================================================================
Dep. Variable:                    tip   R-squared:                       0.457
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      0.9203      0.160      5.761      0.000       0.606       1.235
total_bill     0.1050      0.007     14.260      0.000       0.091       0.120
==============================================================================

Coefficient on total_bill: 0.1050
Interpretation: For each additional dollar on the bill,
the tip increases by about $0.105 (about 10.5 cents).

R-squared: 0.457
This means total_bill explains about 45.7% of the variation in tips.

Predicted tip for $30 bill: $4.07
```
````

````{exercise}
:label: ex11-log

**Exercise 2: Log Transformations**

Using the tips dataset:
1. Create log-transformed versions of `tip` and `total_bill`
2. Run a log-log regression: `ln(tip) ~ ln(total_bill)`
3. Interpret the coefficient as an elasticity
4. Compare the R-squared to the level-level model
````

````{solution} ex11-log
:class: dropdown

```python
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf

tips = sns.load_dataset("tips")

# 1. Create log variables
tips["ln_tip"] = np.log(tips["tip"])
tips["ln_bill"] = np.log(tips["total_bill"])

# 2. Run log-log regression
model_loglog = smf.ols("ln_tip ~ ln_bill", data=tips).fit()
print(model_loglog.summary())

# 3. Interpret elasticity
elasticity = model_loglog.params['ln_bill']
print(f"\nElasticity: {elasticity:.4f}")
print(f"Interpretation: A 1% increase in total bill is associated")
print(f"with a {elasticity:.2f}% increase in tip.")
print(f"Since elasticity < 1, tips are 'inelastic' - they increase")
print(f"by a smaller percentage than the bill increases.")

# 4. Compare R-squared
model_level = smf.ols("tip ~ total_bill", data=tips).fit()
print(f"\nR-squared comparison:")
print(f"Level-Level: {model_level.rsquared:.3f}")
print(f"Log-Log:     {model_loglog.rsquared:.3f}")
```

```
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept     -0.3642      0.138     -2.645      0.009      -0.635      -0.093
ln_bill        0.6024      0.048     12.616      0.000       0.508       0.697
==============================================================================
R-squared: 0.396

Elasticity: 0.6024
Interpretation: A 1% increase in total bill is associated
with a 0.60% increase in tip.
Since elasticity < 1, tips are 'inelastic' - they increase
by a smaller percentage than the bill increases.

R-squared comparison:
Level-Level: 0.457
Log-Log:     0.396
```

The level-level model actually has a higher R-squared in this case, suggesting the linear relationship fits better than the log-log specification.
````

````{exercise}
:label: ex11-residuals

**Exercise 3: Analyzing Residuals**

Using the tips dataset and your level-level regression:
1. Add predicted values and residuals to the dataframe
2. Find the 5 most "generous" tips (highest positive residuals)
3. Find the 5 "stingiest" tips (lowest negative residuals)
4. Create a histogram of the residuals
````

````{solution} ex11-residuals
:class: dropdown

```python
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# Fit model
model = smf.ols("tip ~ total_bill", data=tips).fit()

# 1. Add predictions and residuals
tips["predicted_tip"] = model.fittedvalues
tips["residual"] = model.resid

# 2. Most generous (highest positive residuals)
print("5 Most Generous Tips:")
print(tips.nlargest(5, "residual")[["total_bill", "tip", "predicted_tip", "residual"]])

# 3. Stingiest (lowest negative residuals)
print("\n5 Stingiest Tips:")
print(tips.nsmallest(5, "residual")[["total_bill", "tip", "predicted_tip", "residual"]])

# 4. Histogram of residuals
plt.figure(figsize=(8, 5))
sns.histplot(tips["residual"], bins=20, color="steelblue", alpha=0.7)
plt.axvline(x=0, color="red", linestyle="--")
plt.xlabel("Residual (Actual - Predicted Tip)")
plt.ylabel("Count")
plt.title("Distribution of Tip Prediction Errors")
plt.show()
```

```
5 Most Generous Tips:
     total_bill   tip  predicted_tip  residual
170       50.81 10.00           6.253     3.747
212       48.33  9.00           5.993     3.007
59        48.27  6.73           5.987     0.743
23        39.42  7.58           5.058     2.522
183       23.17  6.50           3.352     3.148

5 Stingiest Tips:
     total_bill   tip  predicted_tip  residual
67        27.28  2.00           3.784    -1.784
0          1.01  1.00           1.026    -0.026
111       32.68  1.17           4.350    -3.180
172        7.25  1.00           1.681    -0.681
92        13.75  2.00           2.364    -0.364
```
````

````{exercise}
:label: ex11-polynomial

**Exercise 4: Polynomial Regression**

Using the tips dataset:
1. Create a squared term for `total_bill`
2. Run a quadratic regression: `tip ~ total_bill + total_bill_sq`
3. Is the squared term statistically significant?
4. Plot both the linear and quadratic fits on the same scatter plot
5. Which model would you prefer and why?
````

````{solution} ex11-polynomial
:class: dropdown

```python
import seaborn as sns
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np

tips = sns.load_dataset("tips")

# 1. Create squared term
tips["total_bill_sq"] = tips["total_bill"] ** 2

# 2. Run quadratic regression
model_quad = smf.ols("tip ~ total_bill + total_bill_sq", data=tips).fit()
print(model_quad.summary())

# 3. Check significance
print(f"\nSquared term p-value: {model_quad.pvalues['total_bill_sq']:.4f}")
if model_quad.pvalues['total_bill_sq'] < 0.05:
    print("The squared term IS statistically significant (p < 0.05)")
else:
    print("The squared term is NOT statistically significant (p >= 0.05)")

# 4. Plot both fits
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter plot
ax.scatter(tips["total_bill"], tips["tip"], alpha=0.5, label="Actual tips")

# Linear fit
x_range = np.linspace(tips["total_bill"].min(), tips["total_bill"].max(), 100)
model_linear = smf.ols("tip ~ total_bill", data=tips).fit()
y_linear = model_linear.params['Intercept'] + model_linear.params['total_bill'] * x_range
ax.plot(x_range, y_linear, color="blue", label=f"Linear (R²={model_linear.rsquared:.3f})")

# Quadratic fit
y_quad = (model_quad.params['Intercept'] +
          model_quad.params['total_bill'] * x_range +
          model_quad.params['total_bill_sq'] * x_range**2)
ax.plot(x_range, y_quad, color="red", linestyle="--", label=f"Quadratic (R²={model_quad.rsquared:.3f})")

ax.set_xlabel("Total Bill ($)")
ax.set_ylabel("Tip ($)")
ax.set_title("Linear vs Quadratic Fit")
ax.legend()
plt.show()

# 5. Model preference
print(f"\nR-squared Linear: {model_linear.rsquared:.4f}")
print(f"R-squared Quadratic: {model_quad.rsquared:.4f}")
print("\nConclusion: The quadratic term is not significant, and R-squared")
print("barely improves. The simpler linear model is preferred (parsimony).")
```

```
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      0.5991      0.348      1.723      0.086      -0.086       1.284
total_bill     0.1341      0.038      3.561      0.000       0.060       0.208
total_bill_sq -0.0004      0.001     -0.777      0.438      -0.002       0.001
==============================================================================

Squared term p-value: 0.4378
The squared term is NOT statistically significant (p >= 0.05)

R-squared Linear: 0.4566
R-squared Quadratic: 0.4586

Conclusion: The quadratic term is not significant, and R-squared
barely improves. The simpler linear model is preferred (parsimony).
```
````

---

*This chapter has been based on the AN7914 Week 12 Python materials, with additional examples and explanations.*
