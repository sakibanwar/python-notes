# Data Cleaning

In this chapter, we'll learn how to clean messy data — arguably the most important (and time-consuming) part of any data analysis project. Real-world data is rarely perfect. It contains missing values, inconsistent formats, typos, and unexpected entries that can cause errors or misleading results.

## Why Data Cleaning Matters

Consider this scenario: you're analysing salary data, but some entries are stored as text ("50k"), some have missing values shown as "N/A", and others contain typos. If you try to calculate the average salary without cleaning, you'll either get an error or a completely wrong answer.

Data cleaning typically involves:

- **Handling missing values** — deciding whether to remove or fill them
- **Fixing data types** — ensuring numbers are stored as numbers, dates as dates
- **Standardising formats** — making sure "UK", "United Kingdom", and "uk" all mean the same thing
- **Removing duplicates** — ensuring each record appears only once
- **Correcting errors** — fixing typos, impossible values, or outliers

Let's start by creating a messy dataset to practice with:

```python
import pandas as pd
import numpy as np

# Create a messy dataset
people = {
    'first_name': ['Alice', 'Bob', 'Charlie', 'Diana', np.nan, None, 'NA'],
    'last_name': ['Smith', 'Jones', 'Brown', 'Wilson', np.nan, np.nan, 'Missing'],
    'email': ['alice@email.com', 'bob@email.com', 'charlie@email.com',
              None, np.nan, 'anonymous@email.com', 'NA'],
    'age': ['28', '35', '42', '31', None, None, 'Missing']
}

df = pd.DataFrame(people)
df
```

```
  first_name last_name                email      age
0      Alice     Smith      alice@email.com       28
1        Bob     Jones        bob@email.com       35
2    Charlie     Brown    charlie@email.com       42
3      Diana    Wilson                 None       31
4        NaN       NaN                  NaN     None
5       None       NaN  anonymous@email.com     None
6         NA   Missing                   NA  Missing
```

Notice the mess we're dealing with:
- Missing values shown as `NaN`, `None`, `'NA'`, and `'Missing'`
- Age stored as strings (text) instead of numbers
- Some rows are completely empty

## Detecting Missing Values

The first step in cleaning is understanding where the problems are. Pandas provides several methods for detecting missing values.

### Using `isna()` to Find Missing Values

The `isna()` method returns `True` for each cell that contains a missing value (`NaN` or `None`):

```python
df.isna()
```

```
   first_name  last_name  email    age
0       False      False  False  False
1       False      False  False  False
2       False      False  False  False
3       False      False   True  False
4        True       True   True   True
5        True       True  False   True
6       False      False  False  False
```

Notice that row 6 shows all `False` — pandas doesn't recognise the strings `'NA'` and `'Missing'` as missing values. We'll deal with this later.

```{tip}
`isnull()` is an alias for `isna()` — they do exactly the same thing. Use whichever you find more readable.
```

### Counting Missing Values

To get a summary of missing values per column:

```python
df.isna().sum()
```

```
first_name    2
last_name     2
email         2
age           2
dtype: int64
```

To see the percentage of missing values:

```python
(df.isna().sum() / len(df) * 100).round(1)
```

```
first_name    28.6
last_name     28.6
email         28.6
age           28.6
dtype: float64
```

### Finding Rows with Any Missing Values

```python
# Rows that have at least one missing value
df[df.isna().any(axis=1)]
```

```
  first_name last_name                email   age
3      Diana    Wilson                 None    31
4        NaN       NaN                  NaN  None
5       None       NaN  anonymous@email.com  None
```

## Handling Missing Values

Once you've identified missing values, you have two main options: **remove** them or **fill** them.

### Option 1: Removing Missing Values with `dropna()`

The `dropna()` method removes rows (or columns) containing missing values:

```python
# Remove rows with ANY missing values
df.dropna()
```

```
  first_name last_name              email      age
0      Alice     Smith    alice@email.com       28
1        Bob     Jones      bob@email.com       35
2    Charlie     Brown  charlie@email.com       42
6         NA   Missing                 NA  Missing
```

By default, `dropna()` removes any row that has at least one missing value.

```{warning}
`dropna()` returns a new DataFrame — it doesn't modify the original unless you use `inplace=True` or reassign the result.
```

### Controlling What Gets Dropped

You can customise `dropna()` behaviour with parameters:

| Parameter | Description |
|-----------|-------------|
| `axis='index'` | Drop rows (default) |
| `axis='columns'` | Drop columns |
| `how='any'` | Drop if ANY values are missing (default) |
| `how='all'` | Drop only if ALL values are missing |
| `subset=['col1', 'col2']` | Only consider specific columns |

#### Drop only if ALL values are missing:

```python
df.dropna(how='all')
```

```
  first_name last_name                email      age
0      Alice     Smith      alice@email.com       28
1        Bob     Jones        bob@email.com       35
2    Charlie     Brown    charlie@email.com       42
3      Diana    Wilson                 None       31
4        NaN       NaN                  NaN     None
5       None       NaN  anonymous@email.com     None
6         NA   Missing                   NA  Missing
```

All rows are kept because none have ALL values missing.

#### Drop based on specific columns:

```python
# Drop rows where BOTH last_name AND email are missing
df.dropna(subset=['last_name', 'email'], how='all')
```

```
  first_name last_name                email      age
0      Alice     Smith      alice@email.com       28
1        Bob     Jones        bob@email.com       35
2    Charlie     Brown    charlie@email.com       42
3      Diana    Wilson                 None       31
5       None       NaN  anonymous@email.com     None
6         NA   Missing                   NA  Missing
```

Row 4 was dropped because both `last_name` and `email` were missing.

### Option 2: Filling Missing Values with `fillna()`

Instead of removing missing data, you can replace it with a specific value:

```python
# Fill all missing values with 0
df.fillna(0)
```

```
  first_name last_name                email      age
0      Alice     Smith      alice@email.com       28
1        Bob     Jones        bob@email.com       35
2    Charlie     Brown    charlie@email.com       42
3      Diana    Wilson                    0       31
4          0         0                    0        0
5          0         0  anonymous@email.com        0
6         NA   Missing                   NA  Missing
```

Filling with 0 doesn't make sense for names! Let's use more appropriate values:

```python
# Fill different columns with different values
df_filled = df.copy()
df_filled['first_name'] = df_filled['first_name'].fillna('Unknown')
df_filled['last_name'] = df_filled['last_name'].fillna('Unknown')
df_filled['email'] = df_filled['email'].fillna('no_email@example.com')
df_filled['age'] = df_filled['age'].fillna('0')

df_filled
```

```
  first_name last_name                 email      age
0      Alice     Smith       alice@email.com       28
1        Bob     Jones         bob@email.com       35
2    Charlie     Brown     charlie@email.com       42
3      Diana    Wilson  no_email@example.com       31
4    Unknown   Unknown  no_email@example.com        0
5    Unknown   Unknown   anonymous@email.com        0
6         NA   Missing                    NA  Missing
```

### Filling with Statistics

For numerical columns, you often want to fill with the mean or median:

```python
# Example with numeric data
sales = pd.DataFrame({
    'product': ['A', 'B', 'C', 'D', 'E'],
    'price': [10.0, np.nan, 15.0, np.nan, 20.0],
    'quantity': [100, 150, np.nan, 200, 180]
})

# Fill price with the mean
sales['price'] = sales['price'].fillna(sales['price'].mean())

# Fill quantity with the median
sales['quantity'] = sales['quantity'].fillna(sales['quantity'].median())

sales
```

```
  product  price  quantity
0       A   10.0     100.0
1       B   15.0     150.0
2       C   15.0     162.5
3       D   15.0     200.0
4       E   20.0     180.0
```

## Replacing Non-Standard Missing Values

Remember how pandas didn't recognise `'NA'` and `'Missing'` as missing values? We need to replace these with proper `NaN` values:

```python
# Replace custom missing value indicators with np.nan
df.replace('NA', np.nan, inplace=True)
df.replace('Missing', np.nan, inplace=True)

df
```

```
  first_name last_name                email   age
0      Alice     Smith      alice@email.com    28
1        Bob     Jones        bob@email.com    35
2    Charlie     Brown    charlie@email.com    42
3      Diana    Wilson                 None    31
4        NaN       NaN                  NaN  None
5       None       NaN  anonymous@email.com  None
6        NaN       NaN                  NaN   NaN
```

Now `isna()` will correctly identify all missing values:

```python
df.isna().sum()
```

```
first_name    3
last_name     3
email         3
age           3
dtype: int64
```

### Replace Multiple Values at Once

```python
# Replace multiple values at once
df.replace(['NA', 'Missing', 'N/A', '-', ''], np.nan, inplace=True)
```

### Using `na_values` When Reading Data

Even better — you can tell pandas to treat certain values as missing when you first read the file:

```python
# Specify custom NA values when reading
df = pd.read_csv('data.csv', na_values=['NA', 'Missing', 'N/A', '-', ''])
```

## Data Type Conversions

One of the most common data cleaning tasks is converting columns to the correct data type. Let's check our current data types:

```python
df.dtypes
```

```
first_name    object
last_name     object
email         object
age           object
dtype: object
```

Everything is `object` (pandas' way of saying "text/string"). But `age` should be a number!

### The Problem with Wrong Data Types

What happens if we try to calculate the mean age?

```python
df['age'].mean()
```

```
TypeError: can only concatenate str (not "int") to str
```

This error occurs because pandas is trying to "add" strings together, not numbers.

### Converting with `astype()`

The `astype()` method converts a column to a specified data type:

```python
# First, let's work with clean data
clean_df = df.dropna()
clean_df['age'] = clean_df['age'].astype(float)
clean_df.dtypes
```

```
first_name     object
last_name      object
email          object
age           float64
dtype: object
```

Now we can calculate statistics:

```python
clean_df['age'].mean()
```

```
35.0
```

### Common Data Type Conversions

| From | To | Method |
|------|-----|--------|
| String to Integer | `int` | `df['col'].astype(int)` |
| String to Float | `float` | `df['col'].astype(float)` |
| Number to String | `str` | `df['col'].astype(str)` |
| String to Datetime | `datetime` | `pd.to_datetime(df['col'])` |
| String to Category | `category` | `df['col'].astype('category')` |

```{note}
`np.nan` is a float, so columns containing NaN values cannot be converted to `int` — use `float` instead, or fill the NaN values first.
```

## Practical Example: Cleaning Survey Data

Let's work through a realistic example. Imagine we have survey data about years of coding experience:

```python
# Simulated survey data
survey = pd.DataFrame({
    'respondent_id': range(1, 11),
    'years_coding': ['5', '10', 'Less than 1 year', '3', 'More than 50 years',
                     '8', np.nan, '15', '2', '20'],
    'salary': ['45000', '75000', '35000', np.nan, '120000',
               '55000', '48000', np.nan, '40000', '95000']
})

survey
```

```
   respondent_id          years_coding  salary
0              1                     5   45000
1              2                    10   75000
2              3      Less than 1 year   35000
3              4                     3     NaN
4              5    More than 50 years  120000
5              6                     8   55000
6              7                   NaN   48000
7              8                    15     NaN
8              9                     2   40000
9             10                    20   95000
```

### Step 1: Examine the Data

First, let's see what unique values we're dealing with:

```python
survey['years_coding'].unique()
```

```
array(['5', '10', 'Less than 1 year', '3', 'More than 50 years', '8',
       nan, '15', '2', '20'], dtype=object)
```

We have two non-numeric values: `'Less than 1 year'` and `'More than 50 years'`.

### Step 2: Replace Non-Numeric Values

```python
# Replace text values with appropriate numbers
survey['years_coding'] = survey['years_coding'].replace('Less than 1 year', '0')
survey['years_coding'] = survey['years_coding'].replace('More than 50 years', '51')

survey['years_coding'].unique()
```

```
array(['5', '10', '0', '3', '51', '8', nan, '15', '2', '20'], dtype=object)
```

### Step 3: Convert to Numeric

```python
survey['years_coding'] = survey['years_coding'].astype(float)
survey['salary'] = survey['salary'].astype(float)

survey.dtypes
```

```
respondent_id      int64
years_coding     float64
salary           float64
dtype: object
```

### Step 4: Calculate Statistics

Now we can analyse the data properly:

```python
print(f"Average years coding: {survey['years_coding'].mean():.1f}")
print(f"Median salary: £{survey['salary'].median():,.0f}")
```

```
Average years coding: 12.7
Median salary: £51,500
```

## Handling Duplicates

Duplicate rows can skew your analysis. Let's see how to detect and remove them.

```python
# Create data with duplicates
orders = pd.DataFrame({
    'order_id': [1, 2, 3, 2, 4, 3],
    'product': ['Widget', 'Gadget', 'Gizmo', 'Gadget', 'Widget', 'Gizmo'],
    'amount': [100, 200, 150, 200, 100, 150]
})

orders
```

```
   order_id product  amount
0         1  Widget     100
1         2  Gadget     200
2         3   Gizmo     150
3         2  Gadget     200
4         4  Widget     100
5         3   Gizmo     150
```

### Detecting Duplicates

```python
# Find duplicate rows
orders.duplicated()
```

```
0    False
1    False
2    False
3     True
4    False
5     True
dtype: bool
```

Rows 3 and 5 are duplicates of earlier rows.

```python
# Count duplicates
orders.duplicated().sum()
```

```
2
```

### Removing Duplicates

```python
orders.drop_duplicates()
```

```
   order_id product  amount
0         1  Widget     100
1         2  Gadget     200
2         3   Gizmo     150
4         4  Widget     100
```

### Check for Duplicates in Specific Columns

```python
# Check if order_id has duplicates (regardless of other columns)
orders.duplicated(subset=['order_id'])
```

```
0    False
1    False
2    False
3     True
4    False
5     True
dtype: bool
```

```python
# Keep only first occurrence of each order_id
orders.drop_duplicates(subset=['order_id'])
```

```
   order_id product  amount
0         1  Widget     100
1         2  Gadget     200
2         3   Gizmo     150
4         4  Widget     100
```

## String Cleaning

Text data often needs standardisation. Pandas provides string methods through the `.str` accessor.

```python
# Messy text data
customers = pd.DataFrame({
    'name': ['  Alice  ', 'BOB', 'charlie', 'DIANA jones'],
    'country': ['UK', 'united kingdom', 'U.K.', 'England']
})

customers
```

```
          name         country
0      Alice               UK
1          BOB  united kingdom
2      charlie            U.K.
3  DIANA jones         England
```

### Common String Cleaning Operations

```python
# Remove leading/trailing whitespace
customers['name'] = customers['name'].str.strip()

# Convert to title case (first letter capitalised)
customers['name'] = customers['name'].str.title()

# Standardise country names
customers['country'] = customers['country'].str.upper()
customers['country'] = customers['country'].replace({
    'UNITED KINGDOM': 'UK',
    'U.K.': 'UK',
    'ENGLAND': 'UK'
})

customers
```

```
          name country
0        Alice      UK
1          Bob      UK
2      Charlie      UK
3  Diana Jones      UK
```

### Useful String Methods

| Method | Description | Example |
|--------|-------------|---------|
| `.str.strip()` | Remove whitespace | `'  text  '` → `'text'` |
| `.str.lower()` | Convert to lowercase | `'TEXT'` → `'text'` |
| `.str.upper()` | Convert to uppercase | `'text'` → `'TEXT'` |
| `.str.title()` | Title case | `'text here'` → `'Text Here'` |
| `.str.replace('a', 'b')` | Replace characters | `'cat'` → `'cbt'` |
| `.str.contains('x')` | Check if contains | Returns `True`/`False` |
| `.str.split(',')` | Split by delimiter | Returns list |
| `.str.len()` | Get string length | `'text'` → `4` |

## The Data Cleaning Workflow

Here's a typical workflow for cleaning a new dataset:

```python
# 1. Load the data
df = pd.read_csv('messy_data.csv')

# 2. Examine the data
print(df.shape)           # How many rows and columns?
print(df.dtypes)          # What are the data types?
print(df.head())          # What do the first few rows look like?

# 3. Check for missing values
print(df.isna().sum())    # How many missing per column?

# 4. Check for unexpected values
for col in df.columns:
    print(f"\n{col}:")
    print(df[col].unique()[:10])  # First 10 unique values

# 5. Clean each column as needed
# - Replace non-standard missing values
# - Convert data types
# - Standardise text
# - Handle outliers

# 6. Verify the cleaning
print(df.dtypes)
print(df.isna().sum())
```

## Summary

Here's a quick reference for data cleaning operations:

| Task | Method |
|------|--------|
| Detect missing values | `df.isna()` |
| Count missing values | `df.isna().sum()` |
| Drop rows with missing values | `df.dropna()` |
| Drop rows with all values missing | `df.dropna(how='all')` |
| Fill missing values | `df.fillna(value)` |
| Fill with column mean | `df['col'].fillna(df['col'].mean())` |
| Replace specific values | `df.replace('old', 'new')` |
| Convert data type | `df['col'].astype(float)` |
| Check data types | `df.dtypes` |
| Find duplicates | `df.duplicated()` |
| Remove duplicates | `df.drop_duplicates()` |
| Strip whitespace | `df['col'].str.strip()` |
| Convert case | `df['col'].str.lower()` |

---

## Exercises

````{exercise}
:label: ex8-missing-values

**Exercise 1: Handling Missing Values**

Create the following DataFrame and perform the cleaning tasks:

```python
data = pd.DataFrame({
    'product': ['Apple', 'Banana', np.nan, 'Orange', 'Grape'],
    'price': [1.20, np.nan, 0.80, 1.50, np.nan],
    'quantity': [100, 150, np.nan, 80, 120]
})
```

1. Count the missing values in each column
2. Fill missing prices with the average price
3. Drop rows where product name is missing
4. Verify no missing values remain in the cleaned data
````

````{solution} ex8-missing-values
:class: dropdown

```python
import pandas as pd
import numpy as np

data = pd.DataFrame({
    'product': ['Apple', 'Banana', np.nan, 'Orange', 'Grape'],
    'price': [1.20, np.nan, 0.80, 1.50, np.nan],
    'quantity': [100, 150, np.nan, 80, 120]
})

# 1. Count missing values
print("Missing values per column:")
print(data.isna().sum())

# 2. Fill missing prices with average
avg_price = data['price'].mean()
data['price'] = data['price'].fillna(avg_price)
print(f"\nFilled missing prices with average: {avg_price:.2f}")

# 3. Drop rows where product is missing
data = data.dropna(subset=['product'])

# 4. Check for remaining quantity NaN and fill with median
data['quantity'] = data['quantity'].fillna(data['quantity'].median())

print("\nCleaned data:")
print(data)

print("\nRemaining missing values:")
print(data.isna().sum())
```
````

````{exercise}
:label: ex8-replace-values

**Exercise 2: Replacing and Converting Values**

You have survey data with non-standard values:

```python
survey = pd.DataFrame({
    'respondent': [1, 2, 3, 4, 5],
    'satisfaction': ['5', '4', 'N/A', '3', 'Missing'],
    'would_recommend': ['Yes', 'Yes', 'No', 'N/A', 'Yes']
})
```

1. Replace 'N/A' and 'Missing' with `np.nan`
2. Convert the satisfaction column to float
3. Calculate the average satisfaction score (ignoring missing values)
````

````{solution} ex8-replace-values
:class: dropdown

```python
import pandas as pd
import numpy as np

survey = pd.DataFrame({
    'respondent': [1, 2, 3, 4, 5],
    'satisfaction': ['5', '4', 'N/A', '3', 'Missing'],
    'would_recommend': ['Yes', 'Yes', 'No', 'N/A', 'Yes']
})

print("Original data:")
print(survey)

# 1. Replace N/A and Missing with np.nan
survey.replace(['N/A', 'Missing'], np.nan, inplace=True)

print("\nAfter replacing N/A and Missing:")
print(survey)

# 2. Convert satisfaction to float
survey['satisfaction'] = survey['satisfaction'].astype(float)

print("\nData types after conversion:")
print(survey.dtypes)

# 3. Calculate average satisfaction
avg_satisfaction = survey['satisfaction'].mean()
print(f"\nAverage satisfaction score: {avg_satisfaction:.2f}")
```
````

````{exercise}
:label: ex8-duplicates

**Exercise 3: Handling Duplicates**

You have transaction data that may contain duplicates:

```python
transactions = pd.DataFrame({
    'transaction_id': [101, 102, 103, 102, 104, 103, 105],
    'customer': ['Alice', 'Bob', 'Charlie', 'Bob', 'Diana', 'Charlie', 'Eve'],
    'amount': [50, 75, 100, 75, 60, 100, 80]
})
```

1. How many duplicate rows are there?
2. Which transaction_ids are duplicated?
3. Remove the duplicates, keeping the first occurrence
4. Verify the cleaned data has no duplicates
````

````{solution} ex8-duplicates
:class: dropdown

```python
import pandas as pd

transactions = pd.DataFrame({
    'transaction_id': [101, 102, 103, 102, 104, 103, 105],
    'customer': ['Alice', 'Bob', 'Charlie', 'Bob', 'Diana', 'Charlie', 'Eve'],
    'amount': [50, 75, 100, 75, 60, 100, 80]
})

print("Original data:")
print(transactions)

# 1. Count duplicate rows
num_duplicates = transactions.duplicated().sum()
print(f"\nNumber of duplicate rows: {num_duplicates}")

# 2. Find duplicated transaction_ids
duplicated_ids = transactions[transactions.duplicated(subset=['transaction_id'])]['transaction_id'].tolist()
print(f"Duplicated transaction IDs: {duplicated_ids}")

# 3. Remove duplicates
transactions_clean = transactions.drop_duplicates()
print("\nAfter removing duplicates:")
print(transactions_clean)

# 4. Verify no duplicates remain
remaining_duplicates = transactions_clean.duplicated().sum()
print(f"\nRemaining duplicates: {remaining_duplicates}")
```
````

````{exercise}
:label: ex8-full-cleaning

**Exercise 4: Complete Data Cleaning**

Clean the following messy employee dataset:

```python
employees = pd.DataFrame({
    'name': ['  john smith  ', 'JANE DOE', 'bob wilson', '  Alice Brown'],
    'department': ['Sales', 'sales', 'SALES', 'Marketing'],
    'salary': ['45000', '52000', 'N/A', '48000'],
    'years_employed': ['3', 'More than 10', '5', '2']
})
```

Perform the following cleaning steps:
1. Strip whitespace and convert names to title case
2. Standardise department names to title case
3. Replace 'N/A' with `np.nan` and convert salary to float
4. Replace 'More than 10' with '11' and convert years_employed to float
5. Calculate the average salary (excluding missing values)
````

````{solution} ex8-full-cleaning
:class: dropdown

```python
import pandas as pd
import numpy as np

employees = pd.DataFrame({
    'name': ['  john smith  ', 'JANE DOE', 'bob wilson', '  Alice Brown'],
    'department': ['Sales', 'sales', 'SALES', 'Marketing'],
    'salary': ['45000', '52000', 'N/A', '48000'],
    'years_employed': ['3', 'More than 10', '5', '2']
})

print("Original data:")
print(employees)
print("\nOriginal dtypes:")
print(employees.dtypes)

# 1. Clean names: strip whitespace and title case
employees['name'] = employees['name'].str.strip().str.title()

# 2. Standardise department names to title case
employees['department'] = employees['department'].str.title()

# 3. Replace N/A and convert salary to float
employees['salary'] = employees['salary'].replace('N/A', np.nan)
employees['salary'] = employees['salary'].astype(float)

# 4. Replace 'More than 10' and convert years_employed to float
employees['years_employed'] = employees['years_employed'].replace('More than 10', '11')
employees['years_employed'] = employees['years_employed'].astype(float)

print("\nCleaned data:")
print(employees)

print("\nNew dtypes:")
print(employees.dtypes)

# 5. Calculate average salary
avg_salary = employees['salary'].mean()
print(f"\nAverage salary: £{avg_salary:,.2f}")
```
````
