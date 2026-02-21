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

# Introduction to Pandas

In this chapter, we'll learn about **pandas** — a powerful library that makes working with data in Python much easier. If you've ever used Excel or Google Sheets, pandas will feel somewhat familiar. It gives you tables (called DataFrames) that you can sort, filter, and analyse with just a few lines of code.

## What is Pandas?

Pandas is a package built on top of NumPy, and provides an efficient implementation of a **DataFrame**. DataFrames are essentially multidimensional arrays with attached row and column labels, and often with heterogeneous types and/or missing data.

Think of it this way:
- A **list** stores a sequence of items
- A **dictionary** stores key-value pairs
- A **DataFrame** stores a whole table — rows, columns, and all!

## Installing and Importing Pandas

If you're using Google Colab or Anaconda, pandas is already installed. Otherwise, you can install it with:

```bash
pip install pandas
```

Once installed, we import pandas using a conventional alias:

```{code-cell} ipython3
import pandas as pd
```

```{code-cell} ipython3
pd.__version__
```

Notice we import pandas **as `pd`**. This is a widely-used convention — almost every pandas tutorial and documentation uses this alias. When you see `pd.something()`, you'll know it's a pandas function.

## The Two Core Data Structures

There are two core objects in pandas:

| Structure | Description | Analogy |
|-----------|-------------|---------|
| **Series** | A single column of data | Like a list with labels |
| **DataFrame** | A table with rows and columns | Like an Excel spreadsheet |

Let's explore both.

## DataFrame: Your Data Table

A **DataFrame** is a table. It contains an array of individual entries, each of which has a certain value. Each entry corresponds to a row (or record) and a column.

### Creating a DataFrame from a Dictionary

The simplest way to create a DataFrame is from a dictionary:

```{code-cell} ipython3
pd.DataFrame({'Yup': [50, 21, 32], 'Nope': [131, 2, 200]})
```

Notice what happened here:
- The dictionary **keys** became the **column names** (`Yup` and `Nope`)
- The dictionary **values** (lists) became the **data** in each column
- Pandas automatically added **row labels** (0, 1, 2) — these are called the **index**

DataFrame entries are not limited to integers. Here's a DataFrame with strings:

```{code-cell} ipython3
pd.DataFrame({
    'Bob': ['I liked it.', 'It was awful.'],
    'Sue': ['Pretty good.', 'Bland.']
})
```

### Custom Row Labels (Index)

The automatic numbering (0, 1, 2, ...) is fine for many purposes, but sometimes you want meaningful row labels. You can specify these using the `index` parameter:

```{code-cell} ipython3
pd.DataFrame({
    'Bob': ['I liked it.', 'It was awful.'],
    'Sue': ['Pretty good.', 'Bland.']
}, index=['Product A', 'Product B'])
```

Now instead of 0 and 1, our rows are labelled 'Product A' and 'Product B'. This makes the data more readable and easier to reference.

## Series: A Single Column

A **Series** is a sequence of data values. If a DataFrame is a table, a Series is a single column (or row) of that table.

You can create a Series from a list:

```{code-cell} ipython3
pd.Series([1, 2, 3, 4])
```

Notice that a Series has:
- An **index** (0, 1, 2, 3) — just like DataFrame rows
- **Values** (1, 2, 3, 4)
- A **dtype** (data type) — here it's `int64` (64-bit integer)

You can also give a Series a name and custom index:

```{code-cell} ipython3
pd.Series([30, 35, 40], index=['2020', '2021', '2022'], name='Sales')
```

```{tip}
A Series is essentially a single column of a DataFrame. When you extract one column from a DataFrame, you get a Series!
```

## Loading Data from CSV Files

In the real world, you won't type your data manually. Instead, you'll load it from files. The most common format is **CSV** (Comma-Separated Values).

### Reading a CSV File

Use `pd.read_csv()` to load a CSV file. You can load it directly from the book's GitHub repository:

```{code-cell} ipython3
employee = pd.read_csv('https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/employee_dataset.csv')
```

```{tip}
You can also download the CSV file from [GitHub](https://github.com/sakibanwar/python-notes/tree/main/data) and load it from your computer:

    employee = pd.read_csv('employee_dataset.csv')
```

The argument to `pd.read_csv()` can be:
- A **file path** on your computer: `'employee_dataset.csv'`
- A **URL** to a file online: `'https://raw.githubusercontent.com/...'`

Let's look at the data:

```{code-cell} ipython3
employee
```

Notice that pandas shows the first and last few rows, with `...` in between. This is helpful when your dataset is large.

## Exploring Your Data

Once you've loaded data, you'll want to explore it. Pandas provides several useful methods for this.

### Viewing the First/Last Rows

Use `.head()` to see the first few rows:

```{code-cell} ipython3
employee.head()
```

By default, `.head()` shows 5 rows. You can specify a different number:

```{code-cell} ipython3
employee.head(10)  # First 10 rows
```

Similarly, `.tail()` shows the last rows:

```{code-cell} ipython3
employee.tail(10)  # Last 10 rows
```

### Checking the Shape

How big is your dataset? Use `.shape`:

```{code-cell} ipython3
employee.shape
```

This tells us we have **50 rows** and **8 columns**.

### Viewing Column Names

To see all column names:

```{code-cell} ipython3
employee.columns
```

### Getting Summary Statistics

The `.describe()` method gives you summary statistics for numerical columns:

```{code-cell} ipython3
employee.describe()
```

This shows you the count, mean, standard deviation, min, max, and quartiles (25%, 50%, 75%) for each numerical column. It's a quick way to understand the distribution of your data.

## Selecting Columns

To select a single column, use square brackets with the column name:

```{code-cell} ipython3
employee['Salary']
```

Notice this returns a **Series** (a single column).

To select multiple columns, pass a **list** of column names:

```{code-cell} ipython3
employee[['Performance_Score', 'Salary']]
```

Notice the double brackets `[[...]]`. The outer brackets are for indexing the DataFrame; the inner brackets create a list of column names. This returns a **DataFrame** (not a Series).

## Indexing in Pandas

Pandas provides two main ways to select data:

| Method | Type | Description |
|--------|------|-------------|
| `.iloc[]` | **Index-based** | Select by position (0, 1, 2, ...) |
| `.loc[]` | **Label-based** | Select by label (row/column names) |

This is one of the most important concepts in pandas, so let's explore both carefully.

## Index-Based Selection with `.iloc`

`.iloc` stands for "integer location". It selects data based on **numerical position**, just like indexing a list.

### Selecting Rows

To select the **first row** (index 0):

```{code-cell} ipython3
employee.iloc[0]
```

This returns a Series containing all columns for that row.

The **second row** (index 1):

```{code-cell} ipython3
employee.iloc[1]
```

### Slicing Rows

You can select multiple rows using slicing:

```{code-cell} ipython3
employee.iloc[0:3]  # Rows 0, 1, and 2
```

Remember: slicing in Python is **exclusive** of the end index. `0:3` gives you indices 0, 1, 2 (not 3).

### Selecting Non-Consecutive Rows

What if you want specific rows that aren't in sequence? Pass a list of indices:

```{code-cell} ipython3
employee.iloc[[1, 2, 39]]
```

### Selecting Rows and Columns

`.iloc` can select both rows and columns using `[row, column]`:

```{code-cell} ipython3
employee.iloc[0, 0]  # First row, first column
```

```{code-cell} ipython3
employee.iloc[0, 1]  # First row, second column
```

You can also use lists and slices for both:

```{code-cell} ipython3
employee.iloc[[0, 1, 2], [0, 1, 2]]  # First 3 rows, first 3 columns
```

Or with slicing:

```{code-cell} ipython3
employee.iloc[0:3, 0:4]  # Rows 0-2, columns 0-3
```

## Label-Based Selection with `.loc`

`.loc` selects data by **labels** (names) rather than positions. This is often more intuitive when you know your column names.

To see `.loc` in action clearly, let's create a DataFrame with meaningful row labels:

```{code-cell} ipython3
df1 = pd.DataFrame(
    [[1, 2, 2], [4, 5, 2], [7, 5, 2], [232, 21, 24]],
    index=['cobra', 'viper', 'sidewinder', 'rattle_snake'],
    columns=['max_speed', 'shield', 'windy']
)
df1
```

### Selecting Rows by Label

```{code-cell} ipython3
df1.loc['viper']
```

### Selecting Multiple Rows

Pass a list of labels:

```{code-cell} ipython3
df1.loc[['viper', 'rattle_snake']]
```

### Slicing with Labels

Unlike `.iloc`, `.loc` slicing is **inclusive** of the end label:

```{code-cell} ipython3
df1.loc['viper':'rattle_snake']
```

Notice this includes `rattle_snake`!

### Selecting Rows and Columns by Label

```{code-cell} ipython3
df1.loc['viper':'rattle_snake', 'shield':'windy']
```

## The Difference Between `.loc` and `.iloc`

This is a crucial distinction:

| Feature | `.iloc` | `.loc` |
|---------|---------|--------|
| Selection type | By **position** (integer) | By **label** (name) |
| Slicing | **Exclusive** of end | **Inclusive** of end |
| Example | `df.iloc[0:3]` → rows 0, 1, 2 | `df.loc['a':'c']` → rows a, b, c |
| When to use | When you know the position | When you know the label |

```{warning}
Be careful! `df.iloc[0:3]` and `df.loc[0:3]` can give different results if your index labels are integers. `.iloc` always uses position; `.loc` always uses labels.
```

## Practical Example: Working with Real Data

Let's put it all together with our employee dataset:

```{code-cell} ipython3
# Check the shape
print(f"Dataset has {employee.shape[0]} rows and {employee.shape[1]} columns")
```

```{code-cell} ipython3
# View first few rows
employee.head()
```

```{code-cell} ipython3
# Get summary statistics
employee.describe()
```

```{code-cell} ipython3
# Select specific columns
salaries = employee[['First_Name', 'Last_Name', 'Salary']]
salaries.head()
```

```{code-cell} ipython3
# Select specific rows and columns
employee.iloc[0:5, [1, 5]]  # First 5 rows, columns 1 and 5
```

---

## Exercises

````{exercise}
:label: ex4-create-df

**Exercise 1: Create a DataFrame**

Create a DataFrame called `movies` with the following data:

| Title | Year | Rating |
|-------|------|--------|
| The Matrix | 1999 | 8.7 |
| Inception | 2010 | 8.8 |
| Interstellar | 2014 | 8.6 |

Then:
1. Print the DataFrame
2. Print only the 'Title' column
3. Print the shape of the DataFrame
````

````{solution} ex4-create-df
:class: dropdown

```python
import pandas as pd

movies = pd.DataFrame({
    'Title': ['The Matrix', 'Inception', 'Interstellar'],
    'Year': [1999, 2010, 2014],
    'Rating': [8.7, 8.8, 8.6]
})

# Print the DataFrame
print(movies)

# Print only the 'Title' column
print(movies['Title'])

# Print the shape
print(movies.shape)  # (3, 3)
```
````

````{exercise}
:label: ex4-iloc-practice

**Exercise 2: Index-Based Selection**

Using the `movies` DataFrame from Exercise 1:

1. Select the first row using `.iloc`
2. Select the last two rows using `.iloc`
3. Select the 'Title' and 'Rating' columns for all rows using `.iloc`
````

````{solution} ex4-iloc-practice
:class: dropdown

```python
# 1. First row
print(movies.iloc[0])

# 2. Last two rows
print(movies.iloc[-2:])
# Or: movies.iloc[1:3]

# 3. Title and Rating columns (columns 0 and 2)
print(movies.iloc[:, [0, 2]])
```
````

````{exercise}
:label: ex4-explore-data

**Exercise 3: Exploring a Dataset**

Load the built-in seaborn tips dataset and explore it:

```python
import seaborn as sns
tips = sns.load_dataset('tips')
```

Answer these questions:
1. How many rows and columns does the dataset have?
2. What are the column names?
3. What are the summary statistics for the numerical columns?
4. What do the first 10 rows look like?
````

````{solution} ex4-explore-data
:class: dropdown

```python
import seaborn as sns
tips = sns.load_dataset('tips')

# 1. Shape
print(f"Rows: {tips.shape[0]}, Columns: {tips.shape[1]}")
# Output: Rows: 244, Columns: 7

# 2. Column names
print(tips.columns)
# Output: Index(['total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size'], dtype='object')

# 3. Summary statistics
print(tips.describe())

# 4. First 10 rows
print(tips.head(10))
```
````

````{exercise}
:label: ex4-loc-vs-iloc

**Exercise 4: `.loc` vs `.iloc`**

Create this DataFrame:

```python
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8],
    'C': [9, 10, 11, 12]
}, index=['w', 'x', 'y', 'z'])
```

Then use both `.loc` and `.iloc` to:
1. Select the row with label 'x'
2. Select rows 'x' through 'z' and columns 'A' and 'B'
3. Select the value at row 'y', column 'C'
````

````{solution} ex4-loc-vs-iloc
:class: dropdown

```python
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8],
    'C': [9, 10, 11, 12]
}, index=['w', 'x', 'y', 'z'])

# 1. Select row 'x'
print(df.loc['x'])       # Using label
print(df.iloc[1])        # Using position

# 2. Rows 'x' through 'z', columns 'A' and 'B'
print(df.loc['x':'z', ['A', 'B']])     # Using labels
print(df.iloc[1:4, [0, 1]])            # Using positions

# 3. Value at row 'y', column 'C'
print(df.loc['y', 'C'])   # Output: 11
print(df.iloc[2, 2])      # Output: 11
```
````
