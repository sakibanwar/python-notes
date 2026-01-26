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

# Data Visualisation with Seaborn

In this chapter, we'll learn how to create beautiful and informative visualisations using **seaborn**. Data visualisation is one of the most important skills in data analysis — a good chart can reveal patterns that are invisible in raw numbers.

## Why Visualise Data?

Consider this: you have a dataset with 10,000 rows of sales data. You could:
- Scroll through thousands of numbers (tedious and ineffective)
- Calculate summary statistics (helpful but limited)
- Create a chart that shows the pattern instantly (this is what we want!)

Visualisations help you:
- **Explore** your data to find patterns
- **Communicate** findings to others
- **Identify** outliers and anomalies
- **Compare** groups or categories

## Python Visualisation Libraries

There are several libraries for data visualisation in Python:

| Library | Description |
|---------|-------------|
| **Matplotlib** | The most versatile and customisable — but verbose |
| **Seaborn** | Built on matplotlib, easier for beginners, beautiful defaults |
| **Plotnine** | Library that is very close to R's ggplot2 (probably not updated regularly) |
| **Lets-plot** | Another library that is very close to ggplot2 (it is maintained regularly) |

We'll focus on **seaborn** because it's easy to learn and produces publication-quality plots with minimal code. I would suggest you learn Matplotlib later at some point.

## Setting Up

Let's import the libraries we need:

```{code-cell} ipython3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Apply seaborn's default theme for nicer-looking plots
sns.set_theme()
```

```{note}
We import matplotlib as `plt` because seaborn is built on top of it. We'll use `plt.show()` to display our plots.
```

## Loading Example Data

Seaborn comes with several built-in datasets that are perfect for learning. Let's load the famous "tips" dataset:

```{code-cell} ipython3
df_tips = sns.load_dataset('tips')
df_tips.head()
```

This dataset contains information about restaurant bills and tips. Let's explore it:

```{code-cell} ipython3
df_tips.describe()
```

## Scatter Plots

A **scatter plot** shows the relationship between two numerical variables. Each point represents one observation.

### Basic Scatter Plot

Let's see if there's a relationship between the total bill and the tip:

```{code-cell} ipython3
sns.scatterplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['tip'])
plt.show()
```

Notice the syntax:
- `data=df_tips` — the DataFrame to use
- `x=df_tips['total_bill']` — the column for the x-axis
- `y=df_tips['tip']` — the column for the y-axis

The plot shows a **positive relationship**: higher bills tend to have higher tips. This makes intuitive sense!

### Adding Colour (Hue)

We can add a third variable using colour. Let's see if the pattern differs by gender:

```{code-cell} ipython3
sns.scatterplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['tip'], hue=df_tips['sex'])
plt.show()
```

The `hue` parameter colours the points by the 'sex' column. Seaborn automatically:
- Assigns different colours to each category
- Adds a legend

Now we can compare the tipping patterns of male and female customers at a glance.

```{tip}
The `hue` parameter works with most seaborn plots. It's a powerful way to add a categorical dimension to your visualisation.
```

## Histograms

A **histogram** shows the distribution of a single numerical variable. It divides the data into bins and counts how many values fall into each bin.

### Basic Histogram

Let's see how total bills are distributed:

```{code-cell} ipython3
sns.histplot(data=df_tips, x=df_tips['total_bill'])
plt.show()
```

Most bills are between $10 and $25, with fewer very low or very high bills.

### Adjusting the Number of Bins

The `bins` parameter controls how many bars the histogram has:

```{code-cell} ipython3
sns.histplot(data=df_tips, x=df_tips['total_bill'], bins=40)
plt.show()
```

More bins show more detail, but can look noisy. Fewer bins show the overall shape but hide detail. Experiment to find the right balance.

### Different Statistics

By default, histograms show counts. You can change this with the `stat` parameter:

```{code-cell} ipython3
# Show percentages instead of counts
sns.histplot(data=df_tips, x=df_tips['total_bill'], bins=40, stat='percent')
plt.show()
```

```{code-cell} ipython3
# Show frequency (same as count)
sns.histplot(data=df_tips, x=df_tips['total_bill'], bins=30, stat='frequency')
plt.show()
```

```{code-cell} ipython3
# Show density (area under curve = 1)
sns.histplot(data=df_tips, x=df_tips['total_bill'], bins=30, stat='density')
plt.show()
```

| Stat | Description |
|------|-------------|
| `'count'` | Number of observations in each bin (default) |
| `'frequency'` | Same as count |
| `'percent'` | Percentage of total observations |
| `'density'` | Normalised so the area equals 1 |

### Adding a Density Curve (KDE)

You can overlay a smooth density curve using `kde=True`:

```{code-cell} ipython3
sns.histplot(data=df_tips, x=df_tips['total_bill'], kde=True)
plt.show()
```

The KDE (Kernel Density Estimate) curve shows a smoothed version of the distribution.

## Bar Plots

A **bar plot** shows the relationship between a categorical variable and a numerical variable. By default, it shows the **mean** of the numerical variable for each category.

### Basic Bar Plot

Let's compare average total bills for lunch vs dinner:

```{code-cell} ipython3
sns.barplot(data=df_tips, x=df_tips['time'], y=df_tips['total_bill'])
plt.show()
```

Dinner bills are higher on average than lunch bills.

### Grouped Bar Plot

Add `hue` to compare across another category:

```{code-cell} ipython3
sns.barplot(data=df_tips, x=df_tips['time'], y=df_tips['total_bill'], hue=df_tips['sex'], errorbar=None)
plt.show()
```

Now we can see that male customers have slightly higher bills on average, for both lunch and dinner.

```{note}
The `errorbar=None` removes the error bars. By default, seaborn shows 95% confidence intervals, which can be useful but also cluttered.
```

## Box Plots

A **box plot** (or box-and-whisker plot) shows the distribution of a numerical variable. It displays:
- The **median** (middle line)
- The **interquartile range** or IQR (the box — middle 50% of data)
- **Whiskers** extending to 1.5 × IQR
- **Outliers** as individual points beyond the whiskers

### Basic Box Plot

```{code-cell} ipython3
sns.boxplot(data=df_tips, x=df_tips['total_bill'])
plt.show()
```

This shows the distribution of total bills. The box shows that 50% of bills are roughly between $13 and $24, with a few high outliers.

### Comparing Groups

Box plots are excellent for comparing distributions across categories:

```{code-cell} ipython3
sns.boxplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['sex'])
plt.show()
```

This shows the distribution of total bills separately for males and females. We can see that:
- Male customers have a slightly higher median bill
- Both groups have outliers at the high end

### Adding a Title and Labels

You can customise the plot using the `.set()` method:

```{code-cell} ipython3
sns.boxplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['sex']).set(
    title='Distribution of Bills by Gender',
    xlabel='Total Bill ($)',
    ylabel='Gender'
)
plt.show()
```

## Line Plots

A **line plot** shows how a numerical variable changes over time or another ordered variable. It's particularly useful for time series data.

### Loading Time Series Data

Let's use the flights dataset, which shows monthly airline passenger numbers:

```{code-cell} ipython3
df_flights = sns.load_dataset('flights')
df_flights.head()
```

### Basic Line Plot

```{code-cell} ipython3
sns.lineplot(data=df_flights, x='year', y='passengers', errorbar=None)
plt.show()
```

This shows the average number of passengers per year. The clear upward trend shows that air travel grew significantly from 1949 to 1960.

### Multiple Lines

Use `hue` to show separate lines for each category:

```{code-cell} ipython3
sns.lineplot(data=df_flights, x='year', y='passengers', hue='month')
plt.show()
```

Now we can see the trend for each month. Notice that:
- All months show an upward trend
- Summer months (especially July and August) consistently have more passengers
- The seasonal pattern is clear

## Faceted Plots with displot

Sometimes you want to create separate plots for different categories. The `displot` function (distribution plot) makes this easy:

```{code-cell} ipython3
sns.displot(data=df_tips, x='total_bill', col='time', kde=True)
plt.show()
```

This creates two histograms side by side — one for Lunch and one for Dinner. The `col='time'` parameter creates a separate column for each value of 'time'.

## Choosing the Right Chart

Here's a quick guide to choosing the right visualisation:

| Data Type | Question | Chart Type |
|-----------|----------|------------|
| 1 numerical | What's the distribution? | Histogram, Box plot |
| 2 numerical | What's the relationship? | Scatter plot |
| 1 categorical + 1 numerical | How do groups compare? | Bar plot, Box plot |
| Time series | How does it change over time? | Line plot |
| 1 categorical | What are the frequencies? | Count plot (bar chart) |

## Saving Your Plots

To save a plot as an image file, use matplotlib's `savefig`:

```python
sns.histplot(data=df_tips, x=df_tips['total_bill'], bins=30)
plt.savefig('my_histogram.png')
plt.show()
```

You can save in various formats: `.png`, `.jpg`, `.pdf`, `.svg`.

```{tip}
Call `plt.savefig()` **before** `plt.show()`. Once `show()` is called, the figure is cleared.
```

## Common Customisations

### Changing Figure Size

```{code-cell} ipython3
plt.figure(figsize=(10, 6))  # Width, Height in inches
sns.histplot(data=df_tips, x=df_tips['total_bill'])
plt.show()
```

### Adding Titles and Labels

```{code-cell} ipython3
sns.scatterplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['tip'])
plt.title('Relationship Between Bill and Tip')
plt.xlabel('Total Bill ($)')
plt.ylabel('Tip ($)')
plt.show()
```

### Changing Colours

Seaborn has many built-in colour palettes:

```{code-cell} ipython3
sns.scatterplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['tip'], hue=df_tips['day'], palette='Set2')
plt.show()
```

Popular palettes include: `'Set1'`, `'Set2'`, `'deep'`, `'muted'`, `'pastel'`, `'bright'`.

---

## Exercises

````{exercise}
:label: ex5-scatter

**Exercise 1: Create a Scatter Plot**

Using the tips dataset:
1. Create a scatter plot with `total_bill` on the x-axis and `tip` on the y-axis
2. Colour the points by the `day` column
3. Add a title: "Tips by Total Bill and Day"
````

````{solution} ex5-scatter
:class: dropdown

```python
import seaborn as sns
import matplotlib.pyplot as plt

df_tips = sns.load_dataset('tips')

sns.scatterplot(data=df_tips, x=df_tips['total_bill'], y=df_tips['tip'], hue=df_tips['day'])
plt.title('Tips by Total Bill and Day')
plt.show()
```
````

````{exercise}
:label: ex5-histogram

**Exercise 2: Create Histograms**

Using the tips dataset:
1. Create a histogram of the `tip` column
2. Use 20 bins
3. Add a KDE curve
4. Change the stat to show percentages
````

````{solution} ex5-histogram
:class: dropdown

```python
import seaborn as sns
import matplotlib.pyplot as plt

df_tips = sns.load_dataset('tips')

sns.histplot(data=df_tips, x=df_tips['tip'], bins=20, kde=True, stat='percent')
plt.title('Distribution of Tips')
plt.xlabel('Tip ($)')
plt.show()
```
````

````{exercise}
:label: ex5-boxplot

**Exercise 3: Compare Distributions**

Using the tips dataset:
1. Create a box plot comparing `total_bill` across different days (`day` column)
2. Add appropriate title and labels
3. What day has the highest median bill?
````

````{solution} ex5-boxplot
:class: dropdown

```python
import seaborn as sns
import matplotlib.pyplot as plt

df_tips = sns.load_dataset('tips')

sns.boxplot(data=df_tips, x=df_tips['day'], y=df_tips['total_bill'])
plt.title('Total Bill Distribution by Day')
plt.xlabel('Day of Week')
plt.ylabel('Total Bill ($)')
plt.show()

# Answer: Sunday has the highest median bill
```
````

````{exercise}
:label: ex5-complete-viz

**Exercise 4: Complete Visualisation**

Load the 'penguins' dataset from seaborn:

```python
penguins = sns.load_dataset('penguins')
```

Create the following visualisations:
1. A scatter plot of `flipper_length_mm` vs `body_mass_g`, coloured by `species`
2. A histogram of `bill_length_mm` with separate colours for each species
3. A box plot comparing `body_mass_g` across species

What patterns do you notice?
````

````{solution} ex5-complete-viz
:class: dropdown

```python
import seaborn as sns
import matplotlib.pyplot as plt

penguins = sns.load_dataset('penguins')

# 1. Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=penguins, x=penguins['flipper_length_mm'], y=penguins['body_mass_g'], hue=penguins['species'])
plt.title('Penguin Size by Species')
plt.xlabel('Flipper Length (mm)')
plt.ylabel('Body Mass (g)')
plt.show()

# 2. Histogram
plt.figure(figsize=(10, 6))
sns.histplot(data=penguins, x=penguins['bill_length_mm'], hue=penguins['species'], bins=20)
plt.title('Bill Length Distribution by Species')
plt.xlabel('Bill Length (mm)')
plt.show()

# 3. Box plot
plt.figure(figsize=(10, 6))
sns.boxplot(data=penguins, x=penguins['species'], y=penguins['body_mass_g'])
plt.title('Body Mass by Species')
plt.xlabel('Species')
plt.ylabel('Body Mass (g)')
plt.show()

# Patterns:
# - Gentoo penguins are the largest (highest body mass)
# - Adelie penguins have shorter bills
# - There's a clear relationship between flipper length and body mass
# - The three species form distinct clusters in the scatter plot
```
````
