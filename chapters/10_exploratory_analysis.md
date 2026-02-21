# Exploratory Data Analysis

Before diving into complex models or hypothesis tests, every good analyst starts with **Exploratory Data Analysis (EDA)**. This is the process of getting to know your data — understanding its structure, spotting patterns, identifying problems, and forming questions to investigate further.

Think of EDA as a first date with your data. You're asking questions, looking for red flags, and figuring out what makes it interesting.

---

## Why EDA Matters

You might be tempted to jump straight into fancy statistical tests or machine learning models. But without proper exploration first, you risk:

- **Missing data quality issues** — nulls, duplicates, or nonsense values can ruin your analysis
- **Misunderstanding relationships** — variables might behave differently than you expect
- **Drawing wrong conclusions** — outliers or data entry errors can skew your results
- **Wasting time** — building models on flawed data means starting over

EDA helps you avoid these pitfalls by giving you a solid understanding of what you're working with.

---

## The EDA Workflow

A typical EDA process follows these steps:

| Step | Question to Answer | Key Methods |
|------|-------------------|-------------|
| 1. Structure | What does the data look like? | `.shape`, `.dtypes`, `.head()` |
| 2. Summary | What are the typical values? | `.describe()`, `.value_counts()` |
| 3. Missing | What data is missing? | `.isna().sum()`, `.info()` |
| 4. Distribution | How are values spread? | `.hist()`, histograms, box plots |
| 5. Relationships | How do variables relate? | `.corr()`, scatter plots |
| 6. Outliers | Are there unusual values? | IQR method, visualisation |
| 7. Groups | Do patterns differ by group? | `.groupby()`, `.agg()` |

Let's work through each of these using a real dataset.

---

## Setting Up

We'll use the **Billion Prices Project** dataset, which compares online and offline prices across different countries. This is a fascinating dataset that helps economists study price dynamics.

```python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Billion Prices Project data
bpp = pd.read_csv("https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/billion_prices.csv", encoding="latin-1")
```

```{tip}
You can also [download the dataset](https://github.com/sakibanwar/python-notes/tree/main/data) and load it locally:

    bpp = pd.read_csv("billion_prices.csv", encoding="latin-1")

The `encoding="latin-1"` parameter handles special characters in international data. Without it, you might get encoding errors.
```

---

## Step 1: Understanding Structure

The first thing you should always do is understand the basic structure of your data.

### How big is the data?

```python
bpp.shape
```

```
(45253, 21)
```

We have 45,253 rows (observations) and 21 columns (variables). That's a decent-sized dataset!

### What columns do we have?

```python
bpp.columns.tolist()
```

```
['COUNTRY', 'retailer', 'retailer_s', 'date', 'day', 'month', 'year',
 'id', 'price', 'price_online', 'imputed', 'DEVICEID', 'TIME', 'ZIPCODE',
 'PHOTO', 'OTHERSKUITEM', 'COMMENTS', 'PRICETYPE', 'CODE', 'sale_online',
 'country_s']
```

### What types of data do we have?

```python
bpp.dtypes
```

```
COUNTRY         object
retailer         int64
retailer_s      object
date            object
day            float64
month          float64
year           float64
id              object
price          float64
price_online   float64
imputed        float64
DEVICEID        object
TIME            object
ZIPCODE         object
PHOTO           object
OTHERSKUITEM    object
COMMENTS        object
PRICETYPE       object
CODE           float64
sale_online    float64
country_s       object
dtype: object
```

Notice that `day`, `month`, and `year` are `float64` instead of integers. This often happens when there are missing values — pandas converts integers to floats to accommodate `NaN` values.

### Peek at the first few rows

```python
bpp.head()
```

```
     COUNTRY  retailer    retailer_s        date   day  month    year  \
0  ARGENTINA         1  ARGENTINA_1  2015-03-19  19.0    3.0  2015.0
1  ARGENTINA         1  ARGENTINA_1  2015-03-19  19.0    3.0  2015.0
2  ARGENTINA         1  ARGENTINA_1  2015-03-19  19.0    3.0  2015.0
3  ARGENTINA         1  ARGENTINA_1  2015-03-19  19.0    3.0  2015.0
4  ARGENTINA         1  ARGENTINA_1  2015-03-19  19.0    3.0  2015.0

             id   price  price_online  ...
0  201209030113   429.0         429.0  ...
1  4710268235965  189.0         189.0  ...
2  4905524916874  6999.0        6999.0  ...
3  4905524925784  1999.0        2099.0  ...
4  4905524931310  2899.0        2899.0  ...
```

### Get a complete overview with info()

The `.info()` method gives you a comprehensive summary:

```python
bpp.info()
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 45253 entries, 0 to 45252
Data columns (total 21 columns):
 #   Column        Non-Null Count  Dtype
---  ------        --------------  -----
 0   COUNTRY       45253 non-null  object
 1   retailer      45253 non-null  int64
 2   retailer_s    45253 non-null  object
 3   date          45253 non-null  object
 4   day           44928 non-null  float64
 5   month         44928 non-null  float64
 6   year          44928 non-null  float64
 7   id            45253 non-null  object
 8   price         45253 non-null  float64
 9   price_online  45253 non-null  float64
 10  imputed       22414 non-null  float64
 11  DEVICEID      45253 non-null  object
 12  TIME          45253 non-null  object
 13  ZIPCODE       45253 non-null  object
 14  PHOTO         45253 non-null  object
 15  OTHERSKUITEM  0 non-null      object
 16  COMMENTS      0 non-null      object
 17  PRICETYPE     45253 non-null  object
 18  CODE          42233 non-null  float64
 19  sale_online   4144 non-null   float64
 20  country_s     45253 non-null  object
dtypes: float64(8), int64(1), object(12)
memory usage: 7.2+ MB
```

Notice that `OTHERSKUITEM` and `COMMENTS` have 0 non-null values — they're completely empty! We might want to drop these columns.

---

## Step 2: Summary Statistics with describe()

The `.describe()` method is your best friend for understanding numeric variables:

```python
bpp.describe()
```

```
           retailer           day         month          year  \
count  45253.000000  44928.000000  44928.000000  44928.000000
mean      34.087751     15.743523      5.301126   2015.079817
std       19.149542      8.440930      3.440339      1.035976
min        1.000000      1.000000      1.000000   2000.000000
25%       16.000000      9.000000      3.000000   2015.000000
50%       37.000000     16.000000      5.000000   2015.000000
75%       50.000000     23.000000      8.000000   2015.000000
max       62.000000     31.000000     12.000000   2016.000000

              price  price_online
count  4.525300e+04  45253.000000
mean   1.737368e+04    353.416684
std    2.671665e+06   5269.492998
min    0.000000e+00      0.030000
25%    7.000000e+00      6.990000
50%    1.999000e+01     19.990000
75%    5.799000e+01     56.990000
max    5.534910e+08 261690.000000
```

Whoa! Look at the `price` column:
- The **mean** is about 17,374 but the **median** (50%) is only 19.99
- The **max** is over 553 million!

This huge difference between mean and median is a classic sign of **extreme outliers** or data errors. The median is typically a better measure of "typical" when you have outliers.

### Selecting Specific Columns with filter()

Often you don't want statistics for every column. Use `.filter()` to select just the columns you care about:

```python
bpp.filter(["price", "price_online"]).describe()
```

```
              price  price_online
count  4.525300e+04  45253.000000
mean   1.737368e+04    353.416684
std    2.671665e+06   5269.492998
min    0.000000e+00      0.030000
25%    7.000000e+00      6.990000
50%    1.999000e+01     19.990000
75%    5.799000e+01     56.990000
max    5.534910e+08 261690.000000
```

### Making Output Easier to Read with transpose()

When comparing multiple variables, it's often easier to read if variables are in rows. Use `.transpose()` (or `.T` for short):

```python
bpp.filter(["price", "price_online"]).describe().transpose()
```

```
                count          mean           std  min   25%    50%    75%  \
price         45253.0  17373.683164  2.671665e+06  0.0  7.00  19.99  57.99
price_online  45253.0    353.416684  5.269493e+03  0.03  6.99  19.99  56.99

                       max
price         553490984.0
price_online     261690.0
```

Now it's much easier to compare the two price columns side by side.

---

## Step 3: Creating New Variables

A key part of EDA is creating variables that help you answer your research questions. Here, we want to compare online and offline prices:

```python
# Calculate price difference: online minus offline
bpp["p_diff"] = bpp["price_online"] - bpp["price"]
```

Now let's look at this new variable:

```python
bpp.filter(["price", "price_online", "p_diff"]).describe().T
```

```
                count          mean           std           min   25%    50%  \
price         45253.0  17373.683164  2.671665e+06  0.000000e+00  7.00  19.99
price_online  45253.0    353.416684  5.269493e+03  3.000000e-02  6.99  19.99
p_diff        45253.0 -17020.266480  2.671661e+06 -5.534910e+08  0.00   0.00

                 75%           max
price          57.99  553490984.0
price_online   56.99     261690.0
p_diff          0.00     233070.0
```

The median price difference is 0 — meaning for most products, the online and offline prices are the same. But those extreme values (min of -553 million!) suggest we have data quality issues to address.

---

## Step 4: Visualising Distributions

Numbers alone don't tell the full story. Let's visualise the price distribution:

```python
bpp["price"].hist(bins=50)
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.title("Distribution of Prices")
plt.show()
```

```
[Histogram showing almost all values concentrated near 0, with a tiny bar
 far to the right representing the extreme outliers]
```

This histogram is almost useless because those extreme outliers compress everything else! This is a clear signal that we need to filter our data.

---

## Step 5: Data Filtering During EDA

EDA isn't just about looking — it's about making decisions. Based on what we've seen, we should filter out problematic observations:

```python
# Filter the data:
# - Exclude items that were on sale online
# - Keep only rows with valid prices
# - Keep only "Regular Price" items

bpp_clean = bpp[
    (bpp["sale_online"].isnull()) &           # Not on sale online
    (bpp["price"].notnull()) &                 # Has offline price
    (bpp["price_online"].notnull()) &          # Has online price
    (bpp["PRICETYPE"] == "Regular Price")      # Regular price only
]

print(f"Original rows: {len(bpp):,}")
print(f"After filtering: {len(bpp_clean):,}")
```

```
Original rows: 45,253
After filtering: 8,169
```

We've reduced our dataset significantly, but we now have cleaner, more reliable data.

```{tip}
You can also write this filtering using the `.loc` chaining approach:

```python
bpp_clean = (
    bpp.loc[bpp["sale_online"].isnull()]
    .loc[bpp["price"].notnull()]
    .loc[bpp["price_online"].notnull()]
    .loc[bpp["PRICETYPE"] == "Regular Price"]
)
```

Both approaches give the same result — use whichever you find more readable.
```

### Check the cleaned data

```python
bpp_clean.filter(["price", "price_online", "p_diff"]).describe().T
```

```
                count         mean           std           min   25%    50%  \
price          8169.0  7650.827638  664156.25...  2.500000e-01  5.99  14.99
price_online   8169.0   133.364610     495.47...  2.500000e-01  5.99  14.99
p_diff         8169.0 -7517.463028  664157.37... -6.002112e+07 -0.10   0.00

                 75%          max
price          43.99  60021128.0
price_online   44.95      6362.0
p_diff          0.00       920.01
```

Still some extreme values! Let's filter more aggressively:

```python
# Remove obviously wrong prices (greater than $1000)
bpp_clean = bpp_clean.loc[bpp_clean["price"] < 1000]

print(f"After removing expensive items: {len(bpp_clean):,}")
```

```
After removing expensive items: 7,893
```

Now let's check again:

```python
bpp_clean.filter(["price", "price_online", "p_diff"]).describe().T
```

```
                count       mean         std      min   25%    50%    75%  \
price          7893.0  55.211356  135.469561  0.25000  5.99  14.49  38.19
price_online   7893.0  54.913554  134.315549  0.25000  5.79  13.99  39.00
p_diff         7893.0  -0.297802   20.141510 -380.13  0.00   0.00   0.00

                   max
price           970.00
price_online    970.00
p_diff          920.01
```

Much better! The mean prices are now around $55, which seems reasonable for retail products.

Let's visualise again:

```python
bpp_clean["price"].hist(bins=50)
plt.xlabel("Price ($)")
plt.ylabel("Frequency")
plt.title("Distribution of Prices (Cleaned Data)")
plt.show()
```

```
[Histogram showing a right-skewed distribution with most prices under $200,
 and progressively fewer items at higher price points]
```

Now we can actually see the distribution — most products are under $200, with a long tail of more expensive items. This right-skewed distribution is typical for price data.

---

## Step 6: Grouped Descriptive Statistics

One of the most powerful EDA techniques is comparing statistics across groups. Let's see how prices differ by country:

```python
bpp_clean.groupby("COUNTRY").agg(
    mean_price_diff=("p_diff", "mean"),
    median_price_diff=("p_diff", "median"),
    count=("p_diff", "count")
)
```

```
             mean_price_diff  median_price_diff  count
COUNTRY
BRAZIL             -0.905328                0.0    122
CHINA              -0.510526                0.0     19
GERMANY             7.065190                0.0    422
JAPAN             -11.982857                0.0    350
SOUTHAFRICA        -2.529723                0.0    541
USA                 0.054460                0.0   6439
```

Interesting! Let's break down what this tells us:

- **USA** has the most observations (6,439) and almost no price difference
- **Germany** is the only country where online prices are *higher* on average (+$7.07)
- **Japan** has the biggest negative difference — online prices are about $12 cheaper than offline

The median is 0 for all countries, meaning for the typical product, prices are the same online and offline.

### Adding More Statistics

You can calculate multiple statistics at once:

```python
summary_by_country = bpp_clean.groupby("COUNTRY").agg(
    mean_pdiff=("p_diff", "mean"),
    se_pdiff=("p_diff", "sem"),      # Standard error of mean
    num_obs=("p_diff", "count")
)
summary_by_country
```

```
             mean_pdiff  se_pdiff  num_obs
COUNTRY
BRAZIL        -0.905328  0.784719      122
CHINA         -0.510526  0.841118       19
GERMANY        7.065190  3.102340      422
JAPAN        -11.982857  2.146688      350
SOUTHAFRICA   -2.529723  0.831934      541
USA            0.054460  0.124552     6439
```

Notice we used `"sem"` for the **standard error of the mean**. This is useful when you want to calculate confidence intervals or t-statistics.

---

## Step 7: Reshaping Data with melt()

Sometimes your data is in "wide" format but you need it in "long" format for analysis or plotting. The `.melt()` function transforms columns into rows.

```python
# Melt price columns into long format
price_long = bpp_clean.melt(
    id_vars=["COUNTRY"],                              # Keep this column
    value_vars=["price", "price_online", "p_diff"]    # Stack these columns
)

price_long.head(10)
```

```
     COUNTRY variable   value
0  ARGENTINA    price  429.00
1  ARGENTINA    price  189.00
2  ARGENTINA    price 6999.00
3  ARGENTINA    price 1999.00
4  ARGENTINA    price 2899.00
5  ARGENTINA    price   59.00
6  ARGENTINA    price   55.00
7  ARGENTINA    price   69.00
8  ARGENTINA    price  199.00
9  ARGENTINA    price  369.00
```

Notice how the three price columns are now stacked into a single `value` column, with a `variable` column indicating which original column the value came from.

### Why is this useful?

Long format makes it easy to calculate grouped statistics across multiple variables:

```python
(
    price_long
    .groupby(["COUNTRY", "variable"])
    .agg(Mean=("value", "mean"), Median=("value", "median"))
)
```

```
                           Mean  Median
COUNTRY     variable
BRAZIL      p_diff      -0.905328    0.00
            price      338.507332   69.90
            price_online 300.583211  67.90
CHINA       p_diff      -0.510526    0.00
            price      141.923942   43.85
            price_online 141.091135  43.90
GERMANY     p_diff       7.065190    0.00
            price       31.831955   14.99
            price_online 36.409198  15.99
...
```

This gives you a comprehensive comparison of all price variables across all countries in one table!

---

## Step 8: Correlation Analysis

Understanding how variables relate to each other is crucial. The `.corr()` method calculates correlation coefficients:

```python
# Select numeric columns for correlation
numeric_cols = ["price", "price_online", "p_diff"]
bpp_clean[numeric_cols].corr()
```

```
              price  price_online    p_diff
price        1.000000      0.995891 -0.065264
price_online 0.995891      1.000000  0.041052
p_diff      -0.065264      0.041052  1.000000
```

Notice that `price` and `price_online` have a correlation of **0.996** — they're almost perfectly correlated! This makes sense: online and offline prices for the same product are usually very similar.

### Visualising Correlations

For datasets with many variables, a correlation heatmap is invaluable:

```python
# Create a correlation heatmap
correlation_matrix = bpp_clean[["price", "price_online", "p_diff"]].corr()

sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation Heatmap")
plt.show()
```

```
[Heatmap showing strong positive correlation between price and price_online,
 and weak correlations with p_diff]
```

The `annot=True` parameter displays the correlation values on the heatmap. The `cmap="coolwarm"` creates a blue-red colour scheme where blue = negative correlation, white = no correlation, and red = positive correlation.

---

## Step 9: Identifying Outliers

Outliers can significantly affect your analysis. There are several ways to identify them:

### Method 1: Visual Inspection with Box Plots

```python
sns.boxplot(data=bpp_clean, y="price")
plt.title("Price Distribution (Box Plot)")
plt.show()
```

```
[Box plot showing the median, quartiles, and whiskers, with many dots
 above the upper whisker representing outliers]
```

The dots above the whiskers are potential outliers.

### Method 2: The IQR Method

The **Interquartile Range (IQR)** method defines outliers as values more than 1.5 × IQR below Q1 or above Q3:

```python
Q1 = bpp_clean["price"].quantile(0.25)
Q3 = bpp_clean["price"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1: ${Q1:.2f}")
print(f"Q3: ${Q3:.2f}")
print(f"IQR: ${IQR:.2f}")
print(f"Lower bound: ${lower_bound:.2f}")
print(f"Upper bound: ${upper_bound:.2f}")
```

```
Q1: $5.99
Q3: $38.19
IQR: $32.20
Lower bound: $-42.31
Upper bound: $86.49
```

```python
# Count outliers
outliers = bpp_clean[
    (bpp_clean["price"] < lower_bound) |
    (bpp_clean["price"] > upper_bound)
]
print(f"Number of outliers: {len(outliers):,} ({len(outliers)/len(bpp_clean)*100:.1f}%)")
```

```
Number of outliers: 1,234 (15.6%)
```

About 15% of our data are outliers by this definition. Whether to remove them depends on your research question — sometimes outliers are the most interesting observations!

---

## Step 10: The Complete EDA Checklist

Here's a quick reference for your future EDA projects:

```python
def quick_eda(df):
    """
    Perform a quick exploratory data analysis on a DataFrame.
    """
    print("=" * 50)
    print("DATASET OVERVIEW")
    print("=" * 50)
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nColumn types:\n{df.dtypes.value_counts()}")

    print("\n" + "=" * 50)
    print("MISSING VALUES")
    print("=" * 50)
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(1)
    missing_df = pd.DataFrame({
        "Missing": missing,
        "Percent": missing_pct
    })
    print(missing_df[missing_df["Missing"] > 0])

    print("\n" + "=" * 50)
    print("NUMERIC SUMMARY")
    print("=" * 50)
    print(df.describe().T)

    print("\n" + "=" * 50)
    print("CATEGORICAL COLUMNS")
    print("=" * 50)
    for col in df.select_dtypes(include="object").columns:
        print(f"\n{col}: {df[col].nunique()} unique values")
        if df[col].nunique() <= 10:
            print(df[col].value_counts())
```

```python
# Use the function
quick_eda(bpp_clean)
```

This function provides a comprehensive overview of any dataset with a single line of code!

---

## Putting It All Together: A Complete EDA Workflow

Let's summarise what a typical EDA workflow looks like:

```python
# 1. Load and inspect structure
df = pd.read_csv("your_data.csv")
print(df.shape)
print(df.dtypes)
df.head()

# 2. Check for missing values
df.isnull().sum()
df.info()

# 3. Summary statistics
df.describe().T

# 4. Create derived variables
df["new_column"] = df["col_a"] - df["col_b"]

# 5. Visualise distributions
df["key_column"].hist()
sns.boxplot(data=df, y="key_column")

# 6. Check correlations
df.select_dtypes(include="number").corr()

# 7. Group comparisons
df.groupby("category").agg(
    mean=("value", "mean"),
    std=("value", "std"),
    count=("value", "count")
)

# 8. Filter problematic data
df_clean = df[
    (df["value"].notnull()) &
    (df["value"] > 0) &
    (df["value"] < df["value"].quantile(0.99))  # Remove top 1%
]

# 9. Document your findings!
```

---

## Key Takeaways

| Concept | Description |
|---------|-------------|
| `.describe()` | Quick summary statistics for numeric columns |
| `.describe().T` | Transpose for easier comparison |
| `.filter()` | Select specific columns |
| `.groupby().agg()` | Calculate statistics by group |
| `.melt()` | Reshape from wide to long format |
| `.corr()` | Calculate correlation matrix |
| `.hist()` | Quick histogram visualisation |
| IQR method | Identify outliers using quartiles |

```{warning}
**Always visualise before modelling!** Numbers can hide important patterns — a histogram showing a bimodal distribution or extreme skew tells you things that `.describe()` can't.
```

```{tip}
**Document as you go!** Keep notes about:
- What patterns you noticed
- What data quality issues you found
- What filtering decisions you made and why
- What questions emerged for further investigation

This documentation will be invaluable when you write up your analysis.
```

---

## Exercises

````{exercise}
:label: ex10-structure

**Exercise 1: Dataset Structure**

Load the built-in tips dataset from seaborn:

```python
tips = sns.load_dataset("tips")
```

Write code to answer:
1. How many rows and columns does it have?
2. What are the data types of each column?
3. Are there any missing values?
4. How many unique days are represented?
````

````{solution} ex10-structure
:class: dropdown

```python
import seaborn as sns
import pandas as pd

# Load the data
tips = sns.load_dataset("tips")

# 1. Shape
print(f"Rows: {tips.shape[0]}, Columns: {tips.shape[1]}")

# 2. Data types
print("\nData types:")
print(tips.dtypes)

# 3. Missing values
print("\nMissing values:")
print(tips.isnull().sum())

# 4. Unique days
print(f"\nUnique days: {tips['day'].nunique()}")
print(tips['day'].value_counts())
```

```
Rows: 244, Columns: 7

Data types:
total_bill    float64
tip           float64
sex          category
smoker       category
day          category
time         category
size            int64
dtype: object

Missing values:
total_bill    0
tip           0
sex           0
smoker        0
day           0
time          0
size          0
dtype: int64

Unique days: 4
Sat     87
Sun     76
Thur    62
Fri     19
Name: day, dtype: int64
```
````

````{exercise}
:label: ex10-summary

**Exercise 2: Summary Statistics by Group**

Using the tips dataset, calculate the following for each day of the week:
- Mean total bill
- Mean tip
- Mean tip percentage (tip / total_bill × 100)
- Number of transactions

Which day has the highest average tip percentage?
````

````{solution} ex10-summary
:class: dropdown

```python
import seaborn as sns
import pandas as pd

tips = sns.load_dataset("tips")

# Create tip percentage column
tips["tip_pct"] = (tips["tip"] / tips["total_bill"]) * 100

# Group by day and calculate statistics
summary = tips.groupby("day").agg(
    mean_bill=("total_bill", "mean"),
    mean_tip=("tip", "mean"),
    mean_tip_pct=("tip_pct", "mean"),
    n_transactions=("total_bill", "count")
).round(2)

print(summary)
print(f"\nHighest average tip percentage: {summary['mean_tip_pct'].idxmax()}")
```

```
      mean_bill  mean_tip  mean_tip_pct  n_transactions
day
Thur      17.68      2.77         16.13              62
Fri       17.15      2.73         16.99              19
Sat       20.44      2.99         15.32              87
Sun       21.41      3.26         16.69              76

Highest average tip percentage: Fri
```
````

````{exercise}
:label: ex10-outliers

**Exercise 3: Outlier Detection**

Using the tips dataset:
1. Use the IQR method to identify outliers in the `total_bill` column
2. How many outliers are there?
3. What is the highest total bill that is NOT considered an outlier?
4. Create a box plot to visualise the distribution
````

````{solution} ex10-outliers
:class: dropdown

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# Calculate IQR bounds
Q1 = tips["total_bill"].quantile(0.25)
Q3 = tips["total_bill"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1: ${Q1:.2f}")
print(f"Q3: ${Q3:.2f}")
print(f"IQR: ${IQR:.2f}")
print(f"Lower bound: ${lower_bound:.2f}")
print(f"Upper bound: ${upper_bound:.2f}")

# Identify outliers
outliers = tips[
    (tips["total_bill"] < lower_bound) |
    (tips["total_bill"] > upper_bound)
]
print(f"\nNumber of outliers: {len(outliers)}")

# Highest non-outlier
non_outliers = tips[
    (tips["total_bill"] >= lower_bound) &
    (tips["total_bill"] <= upper_bound)
]
print(f"Highest non-outlier bill: ${non_outliers['total_bill'].max():.2f}")

# Create box plot
plt.figure(figsize=(8, 6))
sns.boxplot(data=tips, y="total_bill")
plt.title("Total Bill Distribution")
plt.ylabel("Total Bill ($)")
plt.show()
```

```
Q1: $13.35
Q3: $24.13
IQR: $10.78
Lower bound: $-2.82
Upper bound: $40.30

Number of outliers: 7
Highest non-outlier bill: $40.17
```
````

````{exercise}
:label: ex10-correlation

**Exercise 4: Correlation Analysis**

Using the tips dataset:
1. Calculate the correlation between `total_bill`, `tip`, and `size`
2. Which pair of variables has the strongest correlation?
3. Create a correlation heatmap with annotations
4. Does the relationship between `total_bill` and `tip` differ by time (Lunch vs Dinner)?
````

````{solution} ex10-correlation
:class: dropdown

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

# 1. Calculate correlation matrix
corr_matrix = tips[["total_bill", "tip", "size"]].corr()
print("Correlation Matrix:")
print(corr_matrix.round(3))

# 2. Find strongest correlation (excluding diagonal)
import numpy as np
# Mask the diagonal
mask = np.eye(corr_matrix.shape[0], dtype=bool)
corr_values = corr_matrix.where(~mask)
max_corr = corr_values.abs().max().max()
print(f"\nStrongest correlation: {max_corr:.3f} (total_bill and tip)")

# 3. Create heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0,
            fmt=".3f", square=True)
plt.title("Correlation Heatmap: Tips Dataset")
plt.show()

# 4. Correlation by time
print("\nCorrelation by time of day:")
for time in tips["time"].unique():
    subset = tips[tips["time"] == time]
    corr = subset["total_bill"].corr(subset["tip"])
    print(f"{time}: {corr:.3f}")
```

```
Correlation Matrix:
            total_bill   tip  size
total_bill       1.000  0.676  0.598
tip              0.676  1.000  0.489
size             0.598  0.489  1.000

Strongest correlation: 0.676 (total_bill and tip)

Correlation by time of day:
Lunch: 0.652
Dinner: 0.688
```

The correlation between total bill and tip is slightly stronger at dinner (0.688) than at lunch (0.652), but both show a moderately strong positive relationship.
````

---

*This chapter has been based on the AN7914 Week 11 Python materials, with additional examples and explanations.*
