# Filtering Data

In this chapter, we'll learn how to filter DataFrames to extract exactly the rows we need. Filtering is one of the most fundamental and frequently used operations in data analysis — you'll use it constantly to answer questions like "Which customers spent more than £100?" or "What were the sales in the North region?"

## Why Filter Data?

Real-world datasets are often large and contain much more information than you need for a specific analysis. Filtering allows you to:

- **Focus** on a specific subset (e.g., only female customers, only sales from 2024)
- **Remove** irrelevant or problematic data
- **Compare** different groups by filtering to each separately
- **Answer questions** that require looking at specific conditions

Let's start by loading pandas and creating a sample dataset to work with:

```python
import pandas as pd

# Create a sample dataset of employees
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'city': ['London', 'Manchester', 'London', 'Birmingham', 'London', 'Manchester', 'Birmingham', 'London']
})

employees
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
1      Bob         IT   55000                 7  Manchester
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
4      Eve         IT   62000                 9      London
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
7    Henry         IT   58000                 6      London
```

## Boolean Indexing: The Foundation

The key to filtering in pandas is **boolean indexing**. This might sound complicated, but the idea is simple:

1. Create a condition that produces `True` or `False` for each row
2. Use that condition to select only the rows where it's `True`

### Step 1: Create a Condition

Let's find employees who earn more than £50,000. First, let's see what the condition looks like:

```python
employees['salary'] > 50000
```

```
0    False
1     True
2    False
3    False
4     True
5     True
6    False
7     True
Name: salary, dtype: bool
```

Notice what happened — pandas compared each value in the `salary` column to 50000 and returned `True` or `False` for each row. This is called a **boolean Series**.

### Step 2: Use the Condition to Filter

Now we put this condition inside square brackets to filter the DataFrame:

```python
employees[employees['salary'] > 50000]
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
5  Frank      Sales   51000                 5  Manchester
7  Henry         IT   58000                 6      London
```

Only the rows where the condition is `True` are returned. The original DataFrame is unchanged — we've created a **view** of the data that matches our criteria.

```{tip}
The syntax `df[condition]` reads as "give me the rows of df where condition is True". You'll use this pattern constantly.
```

## Comparison Operators

You can use all the standard comparison operators to create conditions:

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `df['city'] == 'London'` |
| `!=` | Not equal to | `df['city'] != 'London'` |
| `>` | Greater than | `df['salary'] > 50000` |
| `<` | Less than | `df['salary'] < 50000` |
| `>=` | Greater than or equal | `df['years_experience'] >= 5` |
| `<=` | Less than or equal | `df['years_experience'] <= 3` |

```{warning}
For equality, use `==` (double equals), not `=` (single equals). A single `=` is for assignment, not comparison!
```

### Examples with Different Operators

```python
# Employees in the IT department
employees[employees['department'] == 'IT']
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
7  Henry         IT   58000                 6      London
```

```python
# Employees NOT in London
employees[employees['city'] != 'London']
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
3  Diana         HR   42000                 2  Birmingham
5  Frank      Sales   51000                 5  Manchester
6  Grace         HR   44000                 3  Birmingham
```

```python
# Employees with 5 or more years of experience
employees[employees['years_experience'] >= 5]
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
5  Frank      Sales   51000                 5  Manchester
7  Henry         IT   58000                 6      London
```

## Combining Multiple Conditions

Often you'll need to filter on more than one condition. For example, "employees in IT who earn more than £55,000" or "employees in London OR Manchester".

### AND Conditions (Both Must Be True)

Use the `&` operator to combine conditions where **both** must be true:

```python
# IT employees earning more than £55,000
employees[(employees['department'] == 'IT') & (employees['salary'] > 55000)]
```

```
    name department  salary  years_experience    city
4    Eve         IT   62000                 9  London
7  Henry         IT   58000                 6  London
```

```{warning}
**Critical:** You MUST wrap each condition in parentheses when using `&` or `|`. This is a common source of errors!

Wrong: `employees[employees['department'] == 'IT' & employees['salary'] > 55000]`

Right: `employees[(employees['department'] == 'IT') & (employees['salary'] > 55000)]`
```

### OR Conditions (At Least One Must Be True)

Use the `|` operator (pipe) to combine conditions where **at least one** must be true:

```python
# Employees in Sales OR HR
employees[(employees['department'] == 'Sales') | (employees['department'] == 'HR')]
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
```

### NOT Conditions (Inverting)

Use the `~` operator (tilde) to invert a condition:

```python
# Everyone NOT in IT
employees[~(employees['department'] == 'IT')]
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
```

### Complex Combinations

You can combine as many conditions as you need:

```python
# IT employees in London earning more than £55,000
employees[
    (employees['department'] == 'IT') &
    (employees['city'] == 'London') &
    (employees['salary'] > 55000)
]
```

```
    name department  salary  years_experience    city
4    Eve         IT   62000                 9  London
7  Henry         IT   58000                 6  London
```

```python
# Employees in London earning > £50k OR in Manchester with > 5 years experience
employees[
    ((employees['city'] == 'London') & (employees['salary'] > 50000)) |
    ((employees['city'] == 'Manchester') & (employees['years_experience'] > 5))
]
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
7  Henry         IT   58000                 6      London
```

## The `isin()` Method

When you want to check if a value is one of several options, use `isin()` instead of multiple `|` conditions:

```python
# Instead of this (long and repetitive):
employees[(employees['department'] == 'Sales') | (employees['department'] == 'HR')]

# Use this (cleaner):
employees[employees['department'].isin(['Sales', 'HR'])]
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
```

```python
# Employees in London, Manchester, or Birmingham
employees[employees['city'].isin(['London', 'Manchester'])]
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
1      Bob         IT   55000                 7  Manchester
2  Charlie      Sales   48000                 4      London
4      Eve         IT   62000                 9      London
5    Frank      Sales   51000                 5  Manchester
7    Henry         IT   58000                 6      London
```

You can also negate `isin()` with `~`:

```python
# Employees NOT in Sales or HR
employees[~employees['department'].isin(['Sales', 'HR'])]
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
7  Henry         IT   58000                 6      London
```

## The `query()` Method

For complex filtering, pandas provides the `query()` method which lets you write conditions as strings. Many people find this more readable:

```python
# Basic query
employees.query('salary > 50000')
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
5  Frank      Sales   51000                 5  Manchester
7  Henry         IT   58000                 6      London
```

```python
# Using 'and' instead of '&'
employees.query('department == "IT" and salary > 55000')
```

```
    name department  salary  years_experience    city
4    Eve         IT   62000                 9  London
7  Henry         IT   58000                 6  London
```

```python
# Using 'or' instead of '|'
employees.query('department == "Sales" or department == "HR"')
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
```

```{note}
In `query()`, you can use either `and`/`or` or `&`/`|`. The string-based syntax is often cleaner for complex conditions.
```

### Using Variables in Queries

To use a Python variable in a query, prefix it with `@`:

```python
min_salary = 50000
employees.query('salary > @min_salary')
```

```
    name department  salary  years_experience        city
1    Bob         IT   55000                 7  Manchester
4    Eve         IT   62000                 9      London
5  Frank      Sales   51000                 5  Manchester
7  Henry         IT   58000                 6      London
```

```python
target_departments = ['IT', 'Sales']
employees.query('department in @target_departments')
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
1      Bob         IT   55000                 7  Manchester
2  Charlie      Sales   48000                 4      London
4      Eve         IT   62000                 9      London
5    Frank      Sales   51000                 5  Manchester
7    Henry         IT   58000                 6      London
```

## Filtering with String Methods

When working with text data, you often need to filter based on patterns rather than exact matches. Pandas provides powerful string methods through the `.str` accessor.

### Checking if a String Contains Something

```python
# Employees with names containing 'a' (case-sensitive)
employees[employees['name'].str.contains('a')]
```

```
      name department  salary  years_experience        city
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
```

```python
# Case-insensitive search
employees[employees['name'].str.contains('a', case=False)]
```

```
      name department  salary  years_experience        city
0    Alice      Sales   45000                 3      London
2  Charlie      Sales   48000                 4      London
3    Diana         HR   42000                 2  Birmingham
5    Frank      Sales   51000                 5  Manchester
6    Grace         HR   44000                 3  Birmingham
```

### Starts With and Ends With

```python
# Cities starting with 'L'
employees[employees['city'].str.startswith('L')]
```

```
      name department  salary  years_experience    city
0    Alice      Sales   45000                 3  London
2  Charlie      Sales   48000                 4  London
4      Eve         IT   62000                 9  London
7    Henry         IT   58000                 6  London
```

```python
# Cities ending with 'ham'
employees[employees['city'].str.endswith('ham')]
```

```
    name department  salary  years_experience        city
3  Diana         HR   42000                 2  Birmingham
6  Grace         HR   44000                 3  Birmingham
```

### Common String Methods for Filtering

| Method | Description | Example |
|--------|-------------|---------|
| `.str.contains('x')` | Contains substring | `df['col'].str.contains('abc')` |
| `.str.startswith('x')` | Starts with | `df['col'].str.startswith('A')` |
| `.str.endswith('x')` | Ends with | `df['col'].str.endswith('ing')` |
| `.str.len()` | Length of string | `df['col'].str.len() > 5` |
| `.str.isupper()` | All uppercase | `df['col'].str.isupper()` |
| `.str.islower()` | All lowercase | `df['col'].str.islower()` |

## Filtering with Missing Values

Real datasets often contain missing values (shown as `NaN` in pandas). Let's add some to our dataset:

```python
# Create a dataset with some missing values
employees_with_na = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'department': ['Sales', None, 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, None, 42000, 62000],
    'bonus': [2000, None, 1500, None, 3000]
})

employees_with_na
```

```
      name department   salary   bonus
0    Alice      Sales  45000.0  2000.0
1      Bob       None  55000.0     NaN
2  Charlie      Sales      NaN  1500.0
3    Diana         HR  42000.0     NaN
4      Eve         IT  62000.0  3000.0
```

### Finding Missing Values

Use `isna()` or `isnull()` to find missing values:

```python
# Rows where department is missing
employees_with_na[employees_with_na['department'].isna()]
```

```
  name department   salary  bonus
1  Bob       None  55000.0    NaN
```

```python
# Rows where salary is NOT missing
employees_with_na[employees_with_na['salary'].notna()]
```

```
    name department   salary   bonus
0  Alice      Sales  45000.0  2000.0
1    Bob       None  55000.0     NaN
3  Diana         HR  42000.0     NaN
4    Eve         IT  62000.0  3000.0
```

### Finding Rows with Any Missing Values

```python
# Rows with at least one missing value
employees_with_na[employees_with_na.isna().any(axis=1)]
```

```
      name department   salary   bonus
1      Bob       None  55000.0     NaN
2  Charlie      Sales      NaN  1500.0
3    Diana         HR  42000.0     NaN
```

```python
# Rows with NO missing values (complete cases)
employees_with_na[employees_with_na.notna().all(axis=1)]
```

```
    name department   salary   bonus
0  Alice      Sales  45000.0  2000.0
4    Eve         IT  62000.0  3000.0
```

## Modifying Data Based on Conditions

Sometimes you don't just want to view filtered data — you want to change values that meet certain conditions. Use `.loc` for this:

```python
# Create a copy to modify
emp = employees.copy()

# Give a 10% raise to IT employees
emp.loc[emp['department'] == 'IT', 'salary'] = emp.loc[emp['department'] == 'IT', 'salary'] * 1.10

emp
```

```
      name department   salary  years_experience        city
0    Alice      Sales  45000.0                 3      London
1      Bob         IT  60500.0                 7  Manchester
2  Charlie      Sales  48000.0                 4      London
3    Diana         HR  42000.0                 2  Birmingham
4      Eve         IT  68200.0                 9      London
5    Frank      Sales  51000.0                 5  Manchester
6    Grace         HR  44000.0                 3  Birmingham
7    Henry         IT  63800.0                 6      London
```

```python
# Add a 'senior' column based on experience
emp['senior'] = False
emp.loc[emp['years_experience'] >= 5, 'senior'] = True

emp
```

```
      name department   salary  years_experience        city  senior
0    Alice      Sales  45000.0                 3      London   False
1      Bob         IT  60500.0                 7  Manchester    True
2  Charlie      Sales  48000.0                 4      London   False
3    Diana         HR  42000.0                 2  Birmingham   False
4      Eve         IT  68200.0                 9      London    True
5    Frank      Sales  51000.0                 5  Manchester    True
6    Grace         HR  44000.0                 3  Birmingham   False
7    Henry         IT  63800.0                 6      London    True
```

```{warning}
Always use `.loc` when modifying data based on conditions. Using chained indexing (like `df[condition]['column'] = value`) can cause unexpected behaviour and will generate a warning.
```

## Creating New Columns from Existing Data

So far we've been filtering data — selecting rows that match a condition. But what if you need to **create a new variable** from existing ones? This comes up constantly in data analysis. For example:

- "I have price and quantity — I need total revenue."
- "I have gestation weeks — I need a column that says 'premature' or 'full term'."
- "I have a continuous variable — I need to bin it into categories."

Let's work through each of these, starting simple and building up.

### Arithmetic Operations

The simplest case: creating a new column from a calculation on existing columns.

```python
# Create a sample dataset
orders = pd.DataFrame({
    'product': ['Widget', 'Gadget', 'Gizmo', 'Widget', 'Gadget'],
    'price': [10.00, 25.00, 15.00, 10.00, 25.00],
    'quantity': [5, 2, 8, 3, 6],
    'discount_pct': [0, 10, 5, 0, 15]
})

# Create a total column
orders['total'] = orders['price'] * orders['quantity']

# Create a discount amount column
orders['discount_amount'] = orders['total'] * orders['discount_pct'] / 100

# Create a final price column
orders['final_price'] = orders['total'] - orders['discount_amount']

orders
```

```
  product  price  quantity  discount_pct  total  discount_amount  final_price
0  Widget  10.00         5             0   50.0              0.0         50.0
1  Gadget  25.00         2            10   50.0              5.0         45.0
2   Gizmo  15.00         8             5  120.0              6.0        114.0
3  Widget  10.00         3             0   30.0              0.0         30.0
4  Gadget  25.00         6            15  150.0             22.5        127.5
```

Notice how each new column is calculated **row by row** automatically — pandas handles the whole column at once without you writing a loop. This is one of the things that makes pandas so powerful.

### Creating Binary Columns from Conditions

Here's where it gets interesting. Remember the boolean conditions we used for filtering? We can store those results as a new column!

Let's say we have birth data and need to flag premature births (less than 37 weeks):

```python
# Create a dataset of patients
patients = pd.DataFrame({
    'patient_id': range(1, 9),
    'weeks_gestation': [39, 36, 41, 34, 38, 40, 35, 37],
    'weight_lbs': [7.5, 5.8, 8.2, 5.1, 7.0, 8.0, 5.5, 6.8]
})

# Create a 'premature' column: True if born before 37 weeks
patients['premature'] = patients['weeks_gestation'] < 37

patients
```

```
   patient_id  weeks_gestation  weight_lbs  premature
0           1               39         7.5      False
1           2               36         5.8       True
2           3               41         8.2      False
3           4               34         5.1       True
4           5               38         7.0      False
5           6               40         8.0      False
6           7               35         5.5       True
7           8               37         6.8      False
```

Notice this is the exact same boolean logic we used for filtering! The condition `patients['weeks_gestation'] < 37` returns `True` or `False` for each row — but instead of using it inside `df[...]` to filter, we're storing it as a new column.

### Creating Categorical Columns with `np.where()`

But what if you don't want `True`/`False` — you want descriptive labels like `'premature'` and `'full term'`? That's where `np.where()` comes in:

```python
import numpy as np

# Label as 'premature' or 'full term' (string labels instead of True/False)
patients['term_status'] = np.where(
    patients['weeks_gestation'] < 37,
    'premature',     # Value if condition is True
    'full term'      # Value if condition is False
)

patients[['patient_id', 'weeks_gestation', 'term_status']]
```

```
   patient_id  weeks_gestation term_status
0           1               39   full term
1           2               36   premature
2           3               41   full term
3           4               34   premature
4           5               38   full term
5           6               40   full term
6           7               35   premature
7           8               37   full term
```

Let's break down what `np.where()` does:

1. It evaluates the condition (`weeks_gestation < 37`) for every row
2. Where the condition is `True`, it assigns `'premature'`
3. Where the condition is `False`, it assigns `'full term'`

Think of it like an if-else that runs on an entire column at once.

```{tip}
`np.where(condition, value_if_true, value_if_false)` is much more efficient than looping through rows one at a time. Always prefer it over writing a `for` loop when you have a simple two-way condition.
```

### Using `.apply()` for More Complex Logic

What if you need **more than two categories**? `np.where()` only handles two outcomes (if/else). For three or more, use `.apply()` with a custom function:

```python
def categorise_weight(weight):
    if weight < 5.5:
        return 'low'
    elif weight < 7.5:
        return 'normal'
    else:
        return 'high'

patients['weight_category'] = patients['weight_lbs'].apply(categorise_weight)
patients[['patient_id', 'weight_lbs', 'weight_category']]
```

```
   patient_id  weight_lbs weight_category
0           1         7.5            high
1           2         5.8          normal
2           3         8.2            high
3           4         5.1             low
4           5         7.0          normal
5           6         8.0            high
6           7         5.5          normal
7           8         6.8          normal
```

Here's what's happening:

1. We define a function `categorise_weight()` that takes a single weight value and returns a category
2. `.apply()` calls this function **once for each row** in the column
3. The results are collected into a new column

```{warning}
A common mistake is trying to use `np.where()` for three categories by nesting it: `np.where(cond1, 'A', np.where(cond2, 'B', 'C'))`. This works but gets messy fast. Use `.apply()` instead — it's much more readable.
```

### Quick Summary: Which Method to Use?

| Scenario | Method | Example |
|----------|--------|---------|
| Arithmetic on columns | Direct operation | `df['total'] = df['price'] * df['qty']` |
| Two outcomes (True/False) | Boolean condition | `df['flag'] = df['age'] >= 18` |
| Two outcomes (custom labels) | `np.where()` | `np.where(df['age'] >= 18, 'adult', 'minor')` |
| Three or more categories | `.apply()` | Define a function, then `.apply()` it |

## Cross-Tabulation with `pd.crosstab()`

We've seen how to create new columns and filter data. But what if you want to summarise the **relationship between two categorical variables**? For example: "Do smokers have higher rates of premature birth?" or "Is there a difference in pass rates between departments?"

This is where **cross-tabulation** (also called a contingency table) comes in. It counts how many observations fall into each combination of two categories.

### Basic Cross-Tabulation

Let's create a dataset of students and their results:

```python
students = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank',
             'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Leo'],
    'department': ['Business', 'Business', 'Economics', 'Economics',
                   'Business', 'Economics', 'Business', 'Economics',
                   'Business', 'Economics', 'Business', 'Economics'],
    'result': ['Pass', 'Fail', 'Pass', 'Pass', 'Pass', 'Fail',
               'Pass', 'Pass', 'Fail', 'Pass', 'Pass', 'Fail']
})

# Create a cross-tabulation
pd.crosstab(students['department'], students['result'])
```

```
result      Fail  Pass
department
Business       2     4
Economics      2     4
```

Notice how this gives us a compact summary: 2 Business students failed and 4 passed, and the same for Economics. You could figure this out by filtering repeatedly, but `crosstab` does it in one line.

### Adding Row and Column Totals

What if you also want the totals? Use the `margins` parameter:

```python
pd.crosstab(students['department'], students['result'], margins=True)
```

```
result      Fail  Pass  All
department
Business       2     4    6
Economics      2     4    6
All            4     8   12
```

The `All` row and column show the totals. This is the same table format you'll see in probability and statistics textbooks.

### Showing Proportions Instead of Counts

Raw counts are useful, but proportions are often more informative — especially when comparing groups of different sizes. Use the `normalize` parameter:

```python
# Proportions across each row (each row sums to 1)
pd.crosstab(students['department'], students['result'], normalize='index')
```

```
result          Fail      Pass
department
Business    0.333333  0.666667
Economics   0.333333  0.666667
```

This shows that 33.3% of students in each department failed. But which `normalize` option should you use? Here's a quick guide:

| `normalize` value | What it does | When to use it |
|-------------------|-------------|----------------|
| `'index'` | Each **row** sums to 1 | "What proportion of Business students passed?" |
| `'columns'` | Each **column** sums to 1 | "Of those who failed, what proportion were Business?" |
| `'all'` | Entire **table** sums to 1 | "What proportion of all students are Business + Pass?" |

```{warning}
A common mistake is using the wrong normalisation. If you want to compare rates **across groups** (e.g., "Is the failure rate higher in Economics?"), use `normalize='index'` — this ensures you're comparing like with like, even if the groups have different sizes.
```

### Putting It Together: A Realistic Example

Let's see how cross-tabulation works with a health dataset. Suppose we want to know: *Is there a relationship between smoking and premature birth?*

First, we need to create the premature variable (using `np.where()` from earlier), then cross-tabulate:

```python
# Simulated birth data
births = pd.DataFrame({
    'habit': ['nonsmoker'] * 8 + ['smoker'] * 4,
    'weeks': [39, 40, 38, 41, 36, 40, 39, 37, 35, 38, 34, 39]
})

# Create the premature variable
births['premature'] = np.where(births['weeks'] < 37, 'premie', 'full term')

# Cross-tabulate habit vs premature status
pd.crosstab(births['habit'], births['premature'])
```

```
premature  full term  premie
habit
nonsmoker          6       2
smoker             2       2
```

Now let's compare the **rates** rather than just the counts:

```python
# Show row proportions to compare rates
pd.crosstab(births['habit'], births['premature'], normalize='index').round(3)
```

```
premature  full term  premie
habit
nonsmoker      0.750   0.250
smoker         0.500   0.500
```

This reveals that 25% of nonsmokers had premature births compared to 50% of smokers — a notable difference. But is this difference *statistically significant* or could it just be due to chance? That's what we'll learn to test in the chapter on statistical inference.

```{note}
`pd.crosstab()` is especially useful for preparing data for statistical tests. In later chapters, we'll use cross-tabulations to calculate proportions, standard errors, and run hypothesis tests to determine whether differences between groups are real.
```

## Practical Example: Analysing Sales Data

Let's apply what we've learned to a more realistic dataset:

```python
# Create sales data
sales = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=10, freq='D'),
    'product': ['Widget', 'Gadget', 'Widget', 'Gizmo', 'Gadget',
                'Widget', 'Gizmo', 'Gadget', 'Widget', 'Gizmo'],
    'region': ['North', 'South', 'North', 'East', 'South',
               'East', 'North', 'East', 'South', 'North'],
    'units': [100, 150, 80, 200, 175, 90, 220, 160, 110, 180],
    'revenue': [1000, 2250, 800, 3000, 2625, 900, 3300, 2400, 1100, 2700]
})

sales
```

```
        date product region  units  revenue
0 2024-01-01  Widget  North    100     1000
1 2024-01-02  Gadget  South    150     2250
2 2024-01-03  Widget  North     80      800
3 2024-01-04   Gizmo   East    200     3000
4 2024-01-05  Gadget  South    175     2625
5 2024-01-06  Widget   East     90      900
6 2024-01-07   Gizmo  North    220     3300
7 2024-01-08  Gadget   East    160     2400
8 2024-01-09  Widget  South    110     1100
9 2024-01-10   Gizmo  North    180     2700
```

Now let's answer some business questions using filtering:

```python
# Q1: What were the Widget sales?
sales[sales['product'] == 'Widget']
```

```
        date product region  units  revenue
0 2024-01-01  Widget  North    100     1000
2 2024-01-03  Widget  North     80      800
5 2024-01-06  Widget   East     90      900
8 2024-01-09  Widget  South    110     1100
```

```python
# Q2: Which sales had revenue over £2000?
sales[sales['revenue'] > 2000]
```

```
        date product region  units  revenue
1 2024-01-02  Gadget  South    150     2250
3 2024-01-04   Gizmo   East    200     3000
4 2024-01-05  Gadget  South    175     2625
6 2024-01-07   Gizmo  North    220     3300
7 2024-01-08  Gadget   East    160     2400
9 2024-01-10   Gizmo  North    180     2700
```

```python
# Q3: What was the total revenue for the North region?
north_sales = sales[sales['region'] == 'North']
north_sales['revenue'].sum()
```

```
7800
```

```python
# Q4: How many high-value sales (>£2500) were Gizmos?
high_value_gizmos = sales[(sales['revenue'] > 2500) & (sales['product'] == 'Gizmo')]
len(high_value_gizmos)
```

```
3
```

```python
# Q5: What's the average units sold for Gadgets and Gizmos combined?
gadgets_gizmos = sales[sales['product'].isin(['Gadget', 'Gizmo'])]
gadgets_gizmos['units'].mean()
```

```
180.83333333333334
```

## Summary

Here's a quick reference for filtering in pandas:

| Task | Syntax |
|------|--------|
| Basic filter | `df[df['col'] > value]` |
| AND conditions | `df[(cond1) & (cond2)]` |
| OR conditions | `df[(cond1) \| (cond2)]` |
| NOT condition | `df[~condition]` |
| Multiple values | `df[df['col'].isin([val1, val2])]` |
| Query method | `df.query('col > value')` |
| Contains string | `df[df['col'].str.contains('x')]` |
| Missing values | `df[df['col'].isna()]` |
| Not missing | `df[df['col'].notna()]` |
| Modify based on condition | `df.loc[condition, 'col'] = value` |

---

## Exercises

````{exercise}
:label: ex6-basic-filter

**Exercise 1: Basic Filtering**

Using the employees DataFrame from this chapter:

```python
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'city': ['London', 'Manchester', 'London', 'Birmingham', 'London', 'Manchester', 'Birmingham', 'London']
})
```

1. Find all employees in the Sales department
2. Find all employees earning less than £50,000
3. Find all employees in London with more than 3 years of experience
````

````{solution} ex6-basic-filter
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'city': ['London', 'Manchester', 'London', 'Birmingham', 'London', 'Manchester', 'Birmingham', 'London']
})

# 1. Sales department employees
print("Sales employees:")
print(employees[employees['department'] == 'Sales'])

# 2. Employees earning less than £50,000
print("\nEmployees earning < £50,000:")
print(employees[employees['salary'] < 50000])

# 3. London employees with more than 3 years experience
print("\nLondon employees with > 3 years experience:")
print(employees[(employees['city'] == 'London') & (employees['years_experience'] > 3)])
```
````

````{exercise}
:label: ex6-multiple-conditions

**Exercise 2: Complex Conditions**

Using the same employees DataFrame:

1. Find employees who are in IT OR HR departments
2. Find employees in Sales who earn more than £48,000
3. Find employees who are NOT in Manchester and have less than 5 years experience
4. Use `isin()` to find employees in London or Birmingham
````

````{solution} ex6-multiple-conditions
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'city': ['London', 'Manchester', 'London', 'Birmingham', 'London', 'Manchester', 'Birmingham', 'London']
})

# 1. IT or HR employees
print("IT or HR employees:")
print(employees[(employees['department'] == 'IT') | (employees['department'] == 'HR')])

# 2. Sales employees earning > £48,000
print("\nSales employees earning > £48,000:")
print(employees[(employees['department'] == 'Sales') & (employees['salary'] > 48000)])

# 3. Not in Manchester with < 5 years experience
print("\nNot Manchester and < 5 years experience:")
print(employees[(employees['city'] != 'Manchester') & (employees['years_experience'] < 5)])

# 4. Using isin() for London or Birmingham
print("\nLondon or Birmingham (using isin):")
print(employees[employees['city'].isin(['London', 'Birmingham'])])
```
````

````{exercise}
:label: ex6-query-method

**Exercise 3: Using the Query Method**

Rewrite the following filters using the `.query()` method:

1. `employees[employees['salary'] > 50000]`
2. `employees[(employees['department'] == 'IT') & (employees['city'] == 'London')]`
3. `employees[(employees['department'] == 'Sales') | (employees['department'] == 'HR')]`
````

````{solution} ex6-query-method
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'city': ['London', 'Manchester', 'London', 'Birmingham', 'London', 'Manchester', 'Birmingham', 'London']
})

# 1. Salary > 50000
print("Salary > 50000:")
print(employees.query('salary > 50000'))

# 2. IT department AND London
print("\nIT department in London:")
print(employees.query('department == "IT" and city == "London"'))

# 3. Sales OR HR
print("\nSales or HR:")
print(employees.query('department == "Sales" or department == "HR"'))
# Alternative using 'in':
# employees.query('department in ["Sales", "HR"]')
```
````

````{exercise}
:label: ex6-practical

**Exercise 4: Practical Analysis**

A retail company has the following transaction data:

```python
transactions = pd.DataFrame({
    'transaction_id': range(1, 11),
    'customer_type': ['Regular', 'Premium', 'Regular', 'Premium', 'Regular',
                      'Premium', 'Regular', 'Premium', 'Regular', 'Premium'],
    'amount': [150, 450, 75, 320, 200, 550, 90, 280, 180, 420],
    'category': ['Electronics', 'Clothing', 'Food', 'Electronics', 'Clothing',
                 'Electronics', 'Food', 'Clothing', 'Electronics', 'Food'],
    'returned': [False, False, True, False, False, False, True, False, False, False]
})
```

Answer these questions using filtering:

1. How many transactions were returned?
2. What is the total amount spent by Premium customers?
3. What is the average transaction amount for Electronics that were NOT returned?
4. Find all Regular customers who spent more than £100 on Clothing or Electronics
````

````{solution} ex6-practical
:class: dropdown

```python
import pandas as pd

transactions = pd.DataFrame({
    'transaction_id': range(1, 11),
    'customer_type': ['Regular', 'Premium', 'Regular', 'Premium', 'Regular',
                      'Premium', 'Regular', 'Premium', 'Regular', 'Premium'],
    'amount': [150, 450, 75, 320, 200, 550, 90, 280, 180, 420],
    'category': ['Electronics', 'Clothing', 'Food', 'Electronics', 'Clothing',
                 'Electronics', 'Food', 'Clothing', 'Electronics', 'Food'],
    'returned': [False, False, True, False, False, False, True, False, False, False]
})

# 1. How many transactions were returned?
returned_count = len(transactions[transactions['returned'] == True])
print(f"Number of returned transactions: {returned_count}")

# 2. Total amount spent by Premium customers
premium_total = transactions[transactions['customer_type'] == 'Premium']['amount'].sum()
print(f"Total spent by Premium customers: £{premium_total}")

# 3. Average for Electronics NOT returned
electronics_not_returned = transactions[
    (transactions['category'] == 'Electronics') &
    (transactions['returned'] == False)
]
avg_electronics = electronics_not_returned['amount'].mean()
print(f"Average Electronics (not returned): £{avg_electronics:.2f}")

# 4. Regular customers spending > £100 on Clothing or Electronics
regular_high_spend = transactions[
    (transactions['customer_type'] == 'Regular') &
    (transactions['amount'] > 100) &
    (transactions['category'].isin(['Clothing', 'Electronics']))
]
print("\nRegular customers spending > £100 on Clothing/Electronics:")
print(regular_high_spend)
```
````
