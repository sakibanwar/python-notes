# Grouping and Aggregating

In this chapter, we'll learn how to summarise data by groups — one of the most powerful techniques in data analysis. When you have questions like "What's the average salary by department?" or "How many sales did each region make?", grouping and aggregating is the answer.

## The Split-Apply-Combine Pattern

The fundamental concept behind grouping operations is called **split-apply-combine**:

1. **Split**: Divide the data into groups based on some criteria
2. **Apply**: Apply a function to each group independently (like calculating the mean)
3. **Combine**: Combine the results back into a single data structure

This pattern is incredibly powerful and forms the basis of most data summarisation tasks.

```{figure} https://pandas.pydata.org/docs/_images/06_groupby1.svg
:alt: Split-Apply-Combine diagram
:width: 80%

The split-apply-combine pattern: data is split into groups, a function is applied to each group, and the results are combined.
```

Let's start with a practical example. First, we'll create a sample employee dataset:

```python
import pandas as pd

# Create employee data
employees = pd.DataFrame({
    'employee_id': range(1, 13),
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank',
             'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Leo'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales',
                   'HR', 'IT', 'Sales', 'HR', 'IT', 'Sales'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000,
               44000, 58000, 47000, 46000, 60000, 52000],
    'years_experience': [2, 5, 3, 1, 8, 4, 2, 6, 3, 4, 7, 5],
    'performance_score': ['Good', 'Excellent', 'Average', 'Good', 'Excellent', 'Good',
                          'Average', 'Good', 'Good', 'Excellent', 'Good', 'Average']
})

employees
```

```
    employee_id     name department  salary  years_experience performance_score
0             1    Alice      Sales   45000                 2              Good
1             2      Bob         IT   55000                 5         Excellent
2             3  Charlie      Sales   48000                 3           Average
3             4    Diana         HR   42000                 1              Good
4             5      Eve         IT   62000                 8         Excellent
5             6    Frank      Sales   51000                 4              Good
6             7    Grace         HR   44000                 2           Average
7             8    Henry         IT   58000                 6              Good
8             9      Ivy      Sales   47000                 3              Good
9            10     Jack         HR   46000                 4         Excellent
10           11     Kate         IT   60000                 7              Good
11           12      Leo      Sales   52000                 5           Average
```

## Basic Grouping with `groupby()`

The `groupby()` method is your gateway to grouped operations. Let's group our employees by department:

```python
grouped = employees.groupby('Department')
grouped
```

```
<pandas.core.groupby.generic.DataFrameGroupBy object at 0x...>
```

Notice that `groupby()` doesn't immediately compute anything — it returns a **GroupBy object**. Think of it as a "waiting room" where the data is organised into groups, ready for you to tell it what calculation to perform.

### Applying an Aggregation Function

Now let's calculate the average salary for each department:

```python
employees.groupby('department')['salary'].mean()
```

```
department
HR        44000.0
IT        58750.0
Sales     48600.0
Name: salary, dtype: float64
```

Let's break down what happened:

1. `employees.groupby('department')` — Split the data by department
2. `['salary']` — Select just the salary column from each group
3. `.mean()` — Calculate the mean of each group's salaries

The result is a **Series** where the index contains the department names and the values are the average salaries.

```{tip}
The result of a groupby operation is often a Series with the grouping column as the index. Use `.reset_index()` to convert it back to a regular DataFrame.
```

### Converting the Result to a DataFrame

If you want a proper DataFrame with columns instead of a Series with an index:

```python
avg_salary = employees.groupby('department')['salary'].mean()
avg_salary.reset_index()
```

```
  department   salary
0         HR  44000.0
1         IT  58750.0
2      Sales  48600.0
```

Now we have a DataFrame with 'department' as a regular column. This is often more useful for further analysis or merging with other data.

## Common Aggregation Functions

Pandas provides many built-in aggregation functions you can use with groups:

| Function | Description |
|----------|-------------|
| `.mean()` | Average of the group |
| `.sum()` | Sum of all values |
| `.count()` | Number of values (excludes NaN) |
| `.size()` | Number of rows (includes NaN) |
| `.min()` | Minimum value |
| `.max()` | Maximum value |
| `.std()` | Standard deviation |
| `.var()` | Variance |
| `.median()` | Median value |
| `.first()` | First value in the group |
| `.last()` | Last value in the group |

### Examples

```python
# Total salary per department
employees.groupby('department')['salary'].sum()
```

```
department
HR        132000
IT        235000
Sales     243000
Name: salary, dtype: int64
```

```python
# Number of employees per department
employees.groupby('department')['employee_id'].count()
```

```
department
HR       3
IT       4
Sales    5
Name: employee_id, dtype: int64
```

```python
# Maximum years of experience per department
employees.groupby('department')['years_experience'].max()
```

```
department
HR       4
IT       8
Sales    5
Name: years_experience, dtype: int64
```

## Grouping by Multiple Columns

You can group by more than one column to get more granular summaries. Simply pass a list of column names to `groupby()`:

```python
# Average salary by department AND performance score
avg_by_dept_perf = employees.groupby(['department', 'performance_score'])['salary'].mean()
avg_by_dept_perf
```

```
department  performance_score
HR          Average              44000.0
            Excellent            46000.0
            Good                 42000.0
IT          Excellent            58500.0
            Good                 59000.0
Sales       Average              50000.0
            Good                 47666.666667
Name: salary, dtype: float64
```

Notice the result has a **MultiIndex** — a hierarchical index with two levels. This can be useful, but it's often easier to work with a flat DataFrame.

### Using `reset_index()` with Multiple Groups

```python
avg_by_dept_perf.reset_index()
```

```
  department performance_score        salary
0         HR           Average  44000.000000
1         HR         Excellent  46000.000000
2         HR              Good  42000.000000
3         IT         Excellent  58500.000000
4         IT              Good  59000.000000
5      Sales           Average  50000.000000
6      Sales              Good  47666.666667
```

### Using `unstack()` for Pivot-Table Style

The `unstack()` method pivots one level of the index to columns, creating a pivot table-like structure:

```python
avg_by_dept_perf.unstack()
```

```
performance_score  Average  Excellent          Good
department
HR                 44000.0    46000.0  42000.000000
IT                     NaN    58500.0  59000.000000
Sales              50000.0        NaN  47666.666667
```

This makes it easy to compare values across one dimension. Notice that `NaN` appears where there are no employees matching that combination (e.g., no IT employees with 'Average' performance in our data).

```{note}
The difference between `reset_index()` and `unstack()`:
- `reset_index()` gives you a "long" format with each combination as a row
- `unstack()` gives you a "wide" format with one grouping variable as columns
```

## Multiple Aggregations with `agg()`

Often you want to calculate several statistics at once. The `agg()` method (short for aggregate) lets you do this:

### Single Column, Multiple Functions

```python
# Multiple statistics for salary by department
employees.groupby('department')['salary'].agg(['mean', 'min', 'max', 'count'])
```

```
                mean    min    max  count
department
HR          44000.0  42000  46000      3
IT          58750.0  55000  62000      4
Sales       48600.0  45000  52000      5
```

### Multiple Columns, Multiple Functions

```python
# Different aggregations for different columns
employees.groupby('department').agg({
    'salary': ['mean', 'sum'],
    'years_experience': ['mean', 'max'],
    'employee_id': 'count'
})
```

```
             salary              years_experience      employee_id
               mean     sum                 mean max        count
department
HR          44000.0  132000             2.333333   4            3
IT          58750.0  235000             6.500000   8            4
Sales       48600.0  243000             3.400000   5            5
```

The result has a MultiIndex for columns. You can flatten it:

```python
summary = employees.groupby('department').agg({
    'salary': ['mean', 'sum'],
    'years_experience': ['mean', 'max'],
    'employee_id': 'count'
})

# Flatten the column names
summary.columns = ['_'.join(col) for col in summary.columns]
summary.reset_index()
```

```
  department  salary_mean  salary_sum  years_experience_mean  years_experience_max  employee_id_count
0         HR      44000.0      132000               2.333333                     4                  3
1         IT      58750.0      235000               6.500000                     8                  4
2      Sales      48600.0      243000               3.400000                     5                  5
```

### Named Aggregations (Cleaner Syntax)

Pandas also supports a cleaner syntax for naming your aggregated columns:

```python
employees.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    total_salary=('salary', 'sum'),
    num_employees=('employee_id', 'count'),
    max_experience=('years_experience', 'max')
).reset_index()
```

```
  department  avg_salary  total_salary  num_employees  max_experience
0         HR     44000.0        132000              3               4
1         IT     58750.0        235000              4               8
2      Sales     48600.0        243000              5               5
```

This syntax is often preferred because it produces clean, single-level column names directly.

## Applying Custom Functions with `apply()`

Sometimes the built-in aggregation functions aren't enough. The `apply()` method lets you use custom functions.

### Creating Categories from Continuous Data

Let's categorise employees by their years of experience:

```python
def categorise_experience(years):
    if years < 3:
        return 'Junior'
    elif years < 6:
        return 'Mid-Level'
    else:
        return 'Senior'

# Apply the function to create a new column
employees['experience_level'] = employees['years_experience'].apply(categorise_experience)
employees[['name', 'years_experience', 'experience_level']]
```

```
       name  years_experience experience_level
0     Alice                 2           Junior
1       Bob                 5        Mid-Level
2   Charlie                 3        Mid-Level
3     Diana                 1           Junior
4       Eve                 8           Senior
5     Frank                 4        Mid-Level
6     Grace                 2           Junior
7     Henry                 6           Senior
8       Ivy                 3        Mid-Level
9      Jack                 4        Mid-Level
10     Kate                 7           Senior
11      Leo                 5        Mid-Level
```

### Applying Functions to Groups

You can also apply custom functions to entire groups:

```python
# Custom function to get the salary range within each department
def salary_range(group):
    return group['salary'].max() - group['salary'].min()

employees.groupby('department').apply(salary_range)
```

```
department
HR        4000
IT        7000
Sales     7000
dtype: int64
```

### Lambda Functions for Quick Operations

For simple operations, lambda functions provide a compact syntax:

```python
# Calculate the proportion of total salary that each department represents
total_salary = employees['salary'].sum()
employees.groupby('department')['salary'].sum().apply(lambda x: x / total_salary * 100)
```

```
department
HR        21.639344
IT        38.524590
Sales     39.836066
Name: salary, dtype: float64
```

## Practical Example: Sales Analysis

Let's work through a more realistic example with sales data:

```python
# Create sales data
sales = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=20, freq='D'),
    'region': ['North', 'South', 'East', 'West'] * 5,
    'product': ['Widget', 'Gadget', 'Widget', 'Gizmo', 'Gadget',
                'Widget', 'Gizmo', 'Gadget', 'Widget', 'Gizmo',
                'Gadget', 'Widget', 'Gizmo', 'Gadget', 'Widget',
                'Gizmo', 'Widget', 'Gadget', 'Widget', 'Gizmo'],
    'quantity': [10, 15, 8, 20, 12, 18, 25, 14, 9, 22,
                 16, 11, 19, 13, 7, 24, 10, 17, 12, 21],
    'revenue': [100, 225, 80, 400, 180, 180, 500, 210, 90, 440,
                240, 110, 380, 195, 70, 480, 100, 255, 120, 420]
})

sales.head(10)
```

```
        date region product  quantity  revenue
0 2024-01-01  North  Widget        10      100
1 2024-01-02  South  Gadget        15      225
2 2024-01-03   East  Widget         8       80
3 2024-01-04   West   Gizmo        20      400
4 2024-01-05  North  Gadget        12      180
5 2024-01-06  South  Widget        18      180
6 2024-01-07   East   Gizmo        25      500
7 2024-01-08   West  Gadget        14      210
8 2024-01-09  North  Widget         9       90
9 2024-01-10  South   Gizmo        22      440
```

### Business Question 1: Total Revenue by Region

```python
revenue_by_region = sales.groupby('region')['revenue'].sum().reset_index()
revenue_by_region.columns = ['region', 'total_revenue']
revenue_by_region.sort_values('total_revenue', ascending=False)
```

```
  region  total_revenue
0   East            960
2  South           1100
3   West           1030
1  North            470
```

### Business Question 2: Best-Selling Products by Quantity

```python
sales.groupby('product')['quantity'].sum().sort_values(ascending=False)
```

```
product
Gizmo     132
Widget     67
Gadget     87
Name: quantity, dtype: int64
```

### Business Question 3: Average Revenue per Sale by Product and Region

```python
sales.groupby(['product', 'region'])['revenue'].mean().unstack().round(2)
```

```
region    East   North  South   West
product
Gadget   240.0   180.0  225.0  210.0
Gizmo    500.0     NaN  440.0  400.0
Widget    80.0    95.0  180.0  120.0
```

### Business Question 4: Comprehensive Summary

```python
summary = sales.groupby('region').agg(
    total_sales=('revenue', 'sum'),
    avg_sale=('revenue', 'mean'),
    num_transactions=('revenue', 'count'),
    total_quantity=('quantity', 'sum')
).reset_index()

summary['avg_price_per_unit'] = summary['total_sales'] / summary['total_quantity']
summary.round(2)
```

```
  region  total_sales  avg_sale  num_transactions  total_quantity  avg_price_per_unit
0   East          960     192.0                 5              57               16.84
1  North          470      94.0                 5              48                9.79
2  South         1100     220.0                 5              75               14.67
3   West         1030     206.0                 5             112                9.20
```

## Transform: Returning Data in Original Shape

Sometimes you want to perform a group calculation but keep the result aligned with the original data. The `transform()` method does exactly this.

### Adding Group Statistics to Each Row

```python
# Add department average salary to each employee row
employees['dept_avg_salary'] = employees.groupby('department')['salary'].transform('mean')
employees[['name', 'department', 'salary', 'dept_avg_salary']]
```

```
       name department  salary  dept_avg_salary
0     Alice      Sales   45000          48600.0
1       Bob         IT   55000          58750.0
2   Charlie      Sales   48000          48600.0
3     Diana         HR   42000          44000.0
4       Eve         IT   62000          58750.0
5     Frank      Sales   51000          48600.0
6     Grace         HR   44000          44000.0
7     Henry         IT   58000          58750.0
8       Ivy      Sales   47000          48600.0
9      Jack         HR   46000          44000.0
10     Kate         IT   60000          58750.0
11      Leo      Sales   52000          48600.0
```

### Calculating Difference from Group Mean

```python
# How much does each employee earn above/below their department average?
employees['salary_vs_dept_avg'] = employees['salary'] - employees['dept_avg_salary']
employees[['name', 'department', 'salary', 'dept_avg_salary', 'salary_vs_dept_avg']]
```

```
       name department  salary  dept_avg_salary  salary_vs_dept_avg
0     Alice      Sales   45000          48600.0             -3600.0
1       Bob         IT   55000          58750.0             -3750.0
2   Charlie      Sales   48000          48600.0              -600.0
3     Diana         HR   42000          44000.0             -2000.0
4       Eve         IT   62000          58750.0              3250.0
5     Frank      Sales   51000          48600.0              2400.0
6     Grace         HR   44000          44000.0                 0.0
7     Henry         IT   58000          58750.0              -750.0
8       Ivy      Sales   47000          48600.0             -1600.0
9      Jack         HR   46000          44000.0              2000.0
10     Kate         IT   60000          58750.0              1250.0
11      Leo      Sales   52000          48600.0              3400.0
```

This is incredibly useful for normalisation or comparing individual values to group benchmarks.

## Working with Real Data: String Splitting

Often real-world data needs cleaning before grouping. A common task is splitting columns:

```python
# Data with location as "City, Country"
locations = pd.DataFrame({
    'employee': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'location': ['London, England', 'Glasgow, Scotland', 'Belfast, Northern Ireland', 'Cardiff, Wales'],
    'salary': [50000, 48000, 52000, 47000]
})

locations
```

```
  employee                   location  salary
0    Alice            London, England   50000
1      Bob          Glasgow, Scotland   48000
2  Charlie  Belfast, Northern Ireland   52000
3    Diana             Cardiff, Wales   47000
```

### Splitting into Separate Columns

```python
# Split location into city and country
locations[['city', 'country']] = locations['location'].str.split(', ', expand=True)
locations
```

```
  employee                   location  salary      city          country
0    Alice            London, England   50000    London          England
1      Bob          Glasgow, Scotland   48000   Glasgow         Scotland
2  Charlie  Belfast, Northern Ireland   52000   Belfast  Northern Ireland
3    Diana             Cardiff, Wales   47000   Cardiff            Wales
```

Now we can group by country:

```python
locations.groupby('country')['salary'].mean()
```

```
country
England             50000.0
Northern Ireland    52000.0
Scotland            48000.0
Wales               47000.0
Name: salary, dtype: float64
```

## Summary

Here's a quick reference for grouping and aggregating:

| Task | Syntax |
|------|--------|
| Group by one column | `df.groupby('col')` |
| Group by multiple columns | `df.groupby(['col1', 'col2'])` |
| Single aggregation | `df.groupby('col')['value'].mean()` |
| Multiple aggregations | `df.groupby('col')['value'].agg(['mean', 'sum'])` |
| Named aggregations | `df.groupby('col').agg(new_name=('col', 'func'))` |
| Different aggregations per column | `df.groupby('col').agg({'col1': 'mean', 'col2': 'sum'})` |
| Reset the index | `grouped.reset_index()` |
| Pivot to columns | `grouped.unstack()` |
| Transform (keep original shape) | `df.groupby('col')['value'].transform('mean')` |
| Apply custom function | `df.groupby('col').apply(custom_func)` |

---

## Exercises

````{exercise}
:label: ex7-basic-groupby

**Exercise 1: Basic Grouping**

Using the employees DataFrame:

```python
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'bonus': [2000, 3000, 2500, 1500, 4000, 2800, 1800, 3200]
})
```

1. Calculate the average salary for each department
2. Find the total bonus paid to each department
3. Count how many employees are in each department
````

````{solution} ex7-basic-groupby
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'bonus': [2000, 3000, 2500, 1500, 4000, 2800, 1800, 3200]
})

# 1. Average salary per department
print("Average salary by department:")
print(employees.groupby('department')['salary'].mean())

# 2. Total bonus per department
print("\nTotal bonus by department:")
print(employees.groupby('department')['bonus'].sum())

# 3. Employee count per department
print("\nEmployee count by department:")
print(employees.groupby('department')['name'].count())
```
````

````{exercise}
:label: ex7-multiple-agg

**Exercise 2: Multiple Aggregations**

Using the same employees DataFrame:

1. Create a summary table showing for each department:
   - Average salary
   - Maximum salary
   - Total years of experience
   - Number of employees

2. Use the named aggregation syntax to give meaningful column names
````

````{solution} ex7-multiple-agg
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'bonus': [2000, 3000, 2500, 1500, 4000, 2800, 1800, 3200]
})

# Using named aggregations
summary = employees.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    max_salary=('salary', 'max'),
    total_experience=('years_experience', 'sum'),
    num_employees=('name', 'count')
).reset_index()

print(summary)
```
````

````{exercise}
:label: ex7-custom-function

**Exercise 3: Using Custom Functions**

Create a function that categorises salaries into bands:
- 'Low': salary < 45000
- 'Medium': 45000 <= salary < 55000
- 'High': salary >= 55000

1. Apply this function to create a new 'salary_band' column
2. Count how many employees fall into each salary band
3. Calculate the average years of experience for each salary band
````

````{solution} ex7-custom-function
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'bonus': [2000, 3000, 2500, 1500, 4000, 2800, 1800, 3200]
})

# Define the categorisation function
def categorise_salary(salary):
    if salary < 45000:
        return 'Low'
    elif salary < 55000:
        return 'Medium'
    else:
        return 'High'

# 1. Apply function to create salary_band column
employees['salary_band'] = employees['salary'].apply(categorise_salary)
print("Employees with salary bands:")
print(employees[['name', 'salary', 'salary_band']])

# 2. Count employees in each band
print("\nCount by salary band:")
print(employees.groupby('salary_band')['name'].count())

# 3. Average experience by salary band
print("\nAverage experience by salary band:")
print(employees.groupby('salary_band')['years_experience'].mean())
```
````

````{exercise}
:label: ex7-transform

**Exercise 4: Using Transform**

Using the employees DataFrame:

1. Add a new column 'dept_avg_salary' containing each employee's department average salary
2. Add a new column 'salary_pct_of_dept' showing each employee's salary as a percentage of their department's total salary
3. Identify which employees earn above their department average
````

````{solution} ex7-transform
:class: dropdown

```python
import pandas as pd

employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry'],
    'department': ['Sales', 'IT', 'Sales', 'HR', 'IT', 'Sales', 'HR', 'IT'],
    'salary': [45000, 55000, 48000, 42000, 62000, 51000, 44000, 58000],
    'years_experience': [3, 7, 4, 2, 9, 5, 3, 6],
    'bonus': [2000, 3000, 2500, 1500, 4000, 2800, 1800, 3200]
})

# 1. Department average salary
employees['dept_avg_salary'] = employees.groupby('department')['salary'].transform('mean')

# 2. Salary as percentage of department total
employees['dept_total_salary'] = employees.groupby('department')['salary'].transform('sum')
employees['salary_pct_of_dept'] = (employees['salary'] / employees['dept_total_salary'] * 100).round(2)

print("Employees with department statistics:")
print(employees[['name', 'department', 'salary', 'dept_avg_salary', 'salary_pct_of_dept']])

# 3. Employees earning above department average
print("\nEmployees earning above their department average:")
above_avg = employees[employees['salary'] > employees['dept_avg_salary']]
print(above_avg[['name', 'department', 'salary', 'dept_avg_salary']])
```
````
