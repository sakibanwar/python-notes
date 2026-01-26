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

```python
import pandas as pd
```

```python
pd.__version__
```

```
'2.0.0'
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

```python
pd.DataFrame({'Yup': [50, 21, 32], 'Nope': [131, 2, 200]})
```

```
   Yup  Nope
0   50   131
1   21     2
2   32   200
```

Notice what happened here:
- The dictionary **keys** became the **column names** (`Yup` and `Nope`)
- The dictionary **values** (lists) became the **data** in each column
- Pandas automatically added **row labels** (0, 1, 2) — these are called the **index**

DataFrame entries are not limited to integers. Here's a DataFrame with strings:

```python
pd.DataFrame({
    'Bob': ['I liked it.', 'It was awful.'],
    'Sue': ['Pretty good.', 'Bland.']
})
```

```
             Bob           Sue
0    I liked it.  Pretty good.
1  It was awful.        Bland.
```

### Custom Row Labels (Index)

The automatic numbering (0, 1, 2, ...) is fine for many purposes, but sometimes you want meaningful row labels. You can specify these using the `index` parameter:

```python
pd.DataFrame({
    'Bob': ['I liked it.', 'It was awful.'],
    'Sue': ['Pretty good.', 'Bland.']
}, index=['Product A', 'Product B'])
```

```
                     Bob           Sue
Product A    I liked it.  Pretty good.
Product B  It was awful.        Bland.
```

Now instead of 0 and 1, our rows are labelled 'Product A' and 'Product B'. This makes the data more readable and easier to reference.

## Series: A Single Column

A **Series** is a sequence of data values. If a DataFrame is a table, a Series is a single column (or row) of that table.

You can create a Series from a list:

```python
pd.Series([1, 2, 3, 4])
```

```
0    1
1    2
2    3
3    4
dtype: int64
```

Notice that a Series has:
- An **index** (0, 1, 2, 3) — just like DataFrame rows
- **Values** (1, 2, 3, 4)
- A **dtype** (data type) — here it's `int64` (64-bit integer)

You can also give a Series a name and custom index:

```python
pd.Series([30, 35, 40], index=['2020', '2021', '2022'], name='Sales')
```

```
2020    30
2021    35
2022    40
Name: Sales, dtype: int64
```

```{tip}
A Series is essentially a single column of a DataFrame. When you extract one column from a DataFrame, you get a Series!
```

## Loading Data from CSV Files

In the real world, you won't type your data manually. Instead, you'll load it from files. The most common format is **CSV** (Comma-Separated Values).

### Reading a CSV File

Use `pd.read_csv()` to load a CSV file:

```python
employee = pd.read_csv('employee_dataset.csv')
```

The argument can be:
- A **file path** on your computer: `'C:/Users/data/employees.csv'`
- A **URL** to a file online: `'https://example.com/data.csv'`

Let's look at the data:

```python
employee
```

```
    Employee_ID Department  Years_of_Experience  Full_Time Performance_Score   Salary First_Name  Last_Name
0             1    Finance                 1.82      False              Good  54550.0    Michael      Davis
1             2         IT                 2.09      False              Poor  55225.0      Karen      Brown
2             3         IT                13.24      False         Excellent  83100.0     Joseph    Johnson
3             4    Finance                 1.55      False         Excellent  53875.0      David     Garcia
4             5  Marketing                 4.16       True           Average  60400.0      Linda   Martinez
..          ...        ...                  ...        ...               ...      ...        ...        ...
45           46    Finance                14.65       True              Good  86625.0       John      Lopez
46           47         IT                 7.38       True           Average  68450.0      Susan    Johnson
47           48         IT                16.16       True         Excellent  90400.0     Thomas      Smith
48           49         IT                 5.72       True           Average  64300.0   Patricia     Thomas
49           50         IT                 4.32       True              Good  60800.0      Sarah      Jones

[50 rows x 8 columns]
```

Notice that pandas shows the first and last few rows, with `...` in between. This is helpful when your dataset is large.

## Exploring Your Data

Once you've loaded data, you'll want to explore it. Pandas provides several useful methods for this.

### Viewing the First/Last Rows

Use `.head()` to see the first few rows:

```python
employee.head()
```

```
   Employee_ID Department  Years_of_Experience  Full_Time Performance_Score   Salary First_Name Last_Name
0            1    Finance                 1.82      False              Good  54550.0    Michael     Davis
1            2         IT                 2.09      False              Poor  55225.0      Karen     Brown
2            3         IT                13.24      False         Excellent  83100.0     Joseph   Johnson
3            4    Finance                 1.55      False         Excellent  53875.0      David    Garcia
4            5  Marketing                 4.16       True           Average  60400.0      Linda  Martinez
```

By default, `.head()` shows 5 rows. You can specify a different number:

```python
employee.head(10)  # First 10 rows
```

Similarly, `.tail()` shows the last rows:

```python
employee.tail(10)  # Last 10 rows
```

### Checking the Shape

How big is your dataset? Use `.shape`:

```python
employee.shape
```

```
(50, 8)
```

This tells us we have **50 rows** and **8 columns**.

### Viewing Column Names

To see all column names:

```python
employee.columns
```

```
Index(['Employee_ID', 'Department', 'Years_of_Experience', 'Full_Time',
       'Performance_Score', 'Salary', 'First_Name', 'Last_Name'],
      dtype='object')
```

### Getting Summary Statistics

The `.describe()` method gives you summary statistics for numerical columns:

```python
employee.describe()
```

```
       Employee_ID  Years_of_Experience        Salary
count    50.000000            50.000000     50.000000
mean     25.500000            10.017600  75044.000000
std      14.577380             5.462507  13656.266372
min       1.000000             1.120000  52800.000000
25%      13.250000             5.277500  63193.750000
50%      25.500000            10.210000  75525.000000
75%      37.750000            14.607500  86518.750000
max      50.000000            19.420000  98550.000000
```

This shows you the count, mean, standard deviation, min, max, and quartiles (25%, 50%, 75%) for each numerical column. It's a quick way to understand the distribution of your data.

## Selecting Columns

To select a single column, use square brackets with the column name:

```python
employee['Salary']
```

```
0     54550.0
1     55225.0
2     83100.0
...
49    60800.0
Name: Salary, dtype: float64
```

Notice this returns a **Series** (a single column).

To select multiple columns, pass a **list** of column names:

```python
employee[['Performance_Score', 'Salary']]
```

```
   Performance_Score   Salary
0               Good  54550.0
1               Poor  55225.0
2          Excellent  83100.0
3          Excellent  53875.0
...
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

```python
employee.iloc[0]
```

```
Employee_ID                    1
Department               Finance
Years_of_Experience         1.82
Full_Time                  False
Performance_Score           Good
Salary                   54550.0
First_Name               Michael
Last_Name                  Davis
Name: 0, dtype: object
```

This returns a Series containing all columns for that row.

The **second row** (index 1):

```python
employee.iloc[1]
```

```
Employee_ID                  2
Department                  IT
Years_of_Experience       2.09
Full_Time                False
Performance_Score         Poor
Salary                 55225.0
First_Name               Karen
Last_Name                Brown
Name: 1, dtype: object
```

### Slicing Rows

You can select multiple rows using slicing:

```python
employee.iloc[0:3]  # Rows 0, 1, and 2
```

```
   Employee_ID Department  Years_of_Experience  Full_Time Performance_Score   Salary First_Name Last_Name
0            1    Finance                 1.82      False              Good  54550.0    Michael     Davis
1            2         IT                 2.09      False              Poor  55225.0      Karen     Brown
2            3         IT                13.24      False         Excellent  83100.0     Joseph   Johnson
```

Remember: slicing in Python is **exclusive** of the end index. `0:3` gives you indices 0, 1, 2 (not 3).

### Selecting Non-Consecutive Rows

What if you want specific rows that aren't in sequence? Pass a list of indices:

```python
employee.iloc[[1, 2, 39]]
```

```
   Employee_ID Department  Years_of_Experience  Full_Time Performance_Score   Salary First_Name Last_Name
1            2         IT                 2.09      False              Poor  55225.0      Karen     Brown
2            3         IT                13.24      False         Excellent  83100.0     Joseph   Johnson
39          40         HR                11.64       True         Excellent  79100.0      Karen  Martinez
```

### Selecting Rows and Columns

`.iloc` can select both rows and columns using `[row, column]`:

```python
employee.iloc[0, 0]  # First row, first column
```

```
1
```

```python
employee.iloc[0, 1]  # First row, second column
```

```
'Finance'
```

You can also use lists and slices for both:

```python
employee.iloc[[0, 1, 2], [0, 1, 2]]  # First 3 rows, first 3 columns
```

```
   Employee_ID Department  Years_of_Experience
0            1    Finance                 1.82
1            2         IT                 2.09
2            3         IT                13.24
```

Or with slicing:

```python
employee.iloc[0:3, 0:4]  # Rows 0-2, columns 0-3
```

```
   Employee_ID Department  Years_of_Experience  Full_Time
0            1    Finance                 1.82      False
1            2         IT                 2.09      False
2            3         IT                13.24      False
```

## Label-Based Selection with `.loc`

`.loc` selects data by **labels** (names) rather than positions. This is often more intuitive when you know your column names.

To see `.loc` in action clearly, let's create a DataFrame with meaningful row labels:

```python
df1 = pd.DataFrame(
    [[1, 2, 2], [4, 5, 2], [7, 5, 2], [232, 21, 24]],
    index=['cobra', 'viper', 'sidewinder', 'rattle_snake'],
    columns=['max_speed', 'shield', 'windy']
)
df1
```

```
              max_speed  shield  windy
cobra                 1       2      2
viper                 4       5      2
sidewinder            7       5      2
rattle_snake        232      21     24
```

### Selecting Rows by Label

```python
df1.loc['viper']
```

```
max_speed    4
shield       5
windy        2
Name: viper, dtype: int64
```

### Selecting Multiple Rows

Pass a list of labels:

```python
df1.loc[['viper', 'rattle_snake']]
```

```
              max_speed  shield  windy
viper                 4       5      2
rattle_snake        232      21     24
```

### Slicing with Labels

Unlike `.iloc`, `.loc` slicing is **inclusive** of the end label:

```python
df1.loc['viper':'rattle_snake']
```

```
              max_speed  shield  windy
viper                 4       5      2
sidewinder            7       5      2
rattle_snake        232      21     24
```

Notice this includes `rattle_snake`!

### Selecting Rows and Columns by Label

```python
df1.loc['viper':'rattle_snake', 'shield':'windy']
```

```
              shield  windy
viper              5      2
sidewinder         5      2
rattle_snake      21     24
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

```python
# Load the data
employee = pd.read_csv('employee_dataset.csv')

# Check the shape
print(f"Dataset has {employee.shape[0]} rows and {employee.shape[1]} columns")

# View first few rows
employee.head()

# Get summary statistics
employee.describe()

# Select specific columns
salaries = employee[['First_Name', 'Last_Name', 'Salary']]

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
