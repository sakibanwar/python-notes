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
