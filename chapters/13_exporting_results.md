# Exporting Results to Word and Excel

You've just run a regression. The output is there, in your notebook, full of useful coefficients, p-values, and R-squareds. But your dissertation isn't going to write itself, and your supervisor doesn't want a screenshot — they want a properly formatted table they can print and read.

This chapter is about closing that gap: getting your Python output **out of the notebook** and **into Word** (or Excel, or LaTeX) in a way that:

- looks professional,
- updates automatically when your data changes,
- and doesn't require you to retype a single number.

We'll start with the **headline tool — Stargazer** — because it's what produces the kind of regression tables you've actually seen in journal articles and economics textbooks. Then we'll cover a simpler built-in alternative (`summary_col`), how to export descriptive statistics to Excel, and the copy-paste workflow into Word.

We'll keep using the `wage1` dataset from Chapter 12, so the regressions will feel familiar.

```{warning}
**Why not just take a screenshot?** Because the moment you fix a typo, drop an outlier, or update the data, your screenshot is wrong — and so is your dissertation. The whole point of these tools is **reproducibility**: if the data changes, you regenerate the file with one line of code, and your tables update automatically. No retyping, no copy-paste errors, no late-night panic the day before submission.
```

---

## Setting Up

We'll need a couple of extra packages for this chapter. If you're working in **Google Colab** or a Jupyter notebook (which is what most students will use), run this **in a code cell**:

```bash
!pip install stargazer openpyxl
```

The leading `!` tells Jupyter/Colab to execute the command as a shell command rather than as Python. You only need to run it once per session — `stargazer` isn't pre-installed in Colab, but it'll stay loaded for the rest of your session.

```{note}
**Running from a terminal instead?** If you're installing from your computer's command line (outside a notebook), drop the `!` and run `pip install stargazer openpyxl` directly.
```

- **`stargazer`** is a Python port of the much-loved R package of the same name. It produces the kind of regression tables you've seen in journal articles.
- **`openpyxl`** is what pandas uses behind the scenes to write `.xlsx` files.

Now let's load our libraries, the data, and fit a few regressions we'll reuse throughout:

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
from stargazer.stargazer import Stargazer

# Load wage1
url = "https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv"
df = pd.read_csv(url)

# Three regressions to compare
m1 = smf.ols("wage ~ educ", data=df).fit()
m2 = smf.ols("wage ~ educ + exper + tenure", data=df).fit()
m3 = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit()
```

These three models should look familiar from Chapter 12 — a simple regression, a multiple regression, and a model with a gender dummy. The whole chapter will treat these as the headline results we want to communicate.

---

## Stargazer: Publication-Quality Regression Tables

Stargazer is by far the most popular tool for producing regression tables that look ready for a journal article or thesis. Rather than throwing every option at you at once, let's build it up step by step — starting with the simplest possible case and adding polish as we go.

### Step 1: One Model, No Customisation

The minimum you need is a single fitted regression. Just hand it to `Stargazer`:

```python
star = Stargazer([m1])
star
```

When you put `star` on the last line of a Jupyter cell, it renders the table directly. Here's what it looks like:

```{raw} html
<table style="text-align:center"><tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left"></td><td colspan="1"><em>Dependent variable: wage</em></td></tr><tr><td style="text-align:left"></td><tr><td style="text-align:left"></td><td>(1)</td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left">Intercept</td><td>-0.905<sup></sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.685)</td></tr>
<tr><td style="text-align:left">educ</td><td>0.541<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.053)</td></tr>
<td colspan="2" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align: left">Observations</td><td>526</td></tr><tr><td style="text-align: left">R<sup>2</sup></td><td>0.165</td></tr><tr><td style="text-align: left">Adjusted R<sup>2</sup></td><td>0.163</td></tr><tr><td style="text-align: left">Residual Std. Error</td><td>3.378 (df=524)</td></tr><tr><td style="text-align: left">F Statistic</td><td>103.363<sup>***</sup> (df=1; 524)</td></tr>
<tr><td colspan="2" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align: left">Note:</td><td colspan="1" style="text-align: right"><sup>*</sup>p&lt;0.1; <sup>**</sup>p&lt;0.05; <sup>***</sup>p&lt;0.01</td></tr></table>
```

Even with zero customisation, the table is already publication-style. Let's go through what each part shows:

- **`Dependent variable: wage`** at the top tells the reader what the regression is explaining. By default Stargazer just uses the column name from your DataFrame.
- **`(1)`** below it numbers the model. With one column there's only `(1)`; with multiple models you'd get `(1)`, `(2)`, `(3)`, etc. — exactly how journal tables number their specifications.
- The **coefficient table** in the middle shows each variable's estimate with the standard error in parentheses underneath. Significance stars (`*`, `**`, `***`) flag p-values below 0.1, 0.05, and 0.01 respectively.
- The **fit statistics** block at the bottom reports `Observations`, `R²`, `Adjusted R²`, `Residual Std. Error`, and the `F Statistic`. This is what most journal tables include as a "footer".
- The **note** at the very bottom defines what the stars mean.

So with one line of code you've got something that looks remarkably like the regression tables you've seen in published papers. That's the whole appeal of Stargazer.

### Step 2: Add More Models

Comparing models side-by-side is the bread and butter of empirical economics — you want to show how a coefficient changes as you add controls, or how different specifications fit the same data. Adding more models to the table is as simple as putting them all in the list:

```python
star = Stargazer([m1, m2, m3])
star
```

```{raw} html
<table style="text-align:center"><tr><td colspan="4" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left"></td><td colspan="3"><em>Dependent variable: wage</em></td></tr><tr><td style="text-align:left"></td><tr><td style="text-align:left"></td><td>(1)</td><td>(2)</td><td>(3)</td></tr>
<tr><td colspan="4" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left">Intercept</td><td>-0.905<sup></sup></td><td>-2.873<sup>***</sup></td><td>-1.568<sup>**</sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.685)</td><td>(0.729)</td><td>(0.725)</td></tr>
<tr><td style="text-align:left">educ</td><td>0.541<sup>***</sup></td><td>0.599<sup>***</sup></td><td>0.572<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.053)</td><td>(0.051)</td><td>(0.049)</td></tr>
<tr><td style="text-align:left">exper</td><td></td><td>0.022<sup>*</sup></td><td>0.025<sup>**</sup></td></tr>
<tr><td style="text-align:left"></td><td></td><td>(0.012)</td><td>(0.012)</td></tr>
<tr><td style="text-align:left">female</td><td></td><td></td><td>-1.811<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td></td><td></td><td>(0.265)</td></tr>
<tr><td style="text-align:left">tenure</td><td></td><td>0.169<sup>***</sup></td><td>0.141<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td></td><td>(0.022)</td><td>(0.021)</td></tr>
<td colspan="4" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align: left">Observations</td><td>526</td><td>526</td><td>526</td></tr><tr><td style="text-align: left">R<sup>2</sup></td><td>0.165</td><td>0.306</td><td>0.364</td></tr><tr><td style="text-align: left">Adjusted R<sup>2</sup></td><td>0.163</td><td>0.302</td><td>0.359</td></tr><tr><td style="text-align: left">Residual Std. Error</td><td>3.378 (df=524)</td><td>3.084 (df=522)</td><td>2.958 (df=521)</td></tr><tr><td style="text-align: left">F Statistic</td><td>103.363<sup>***</sup> (df=1; 524)</td><td>76.873<sup>***</sup> (df=3; 522)</td><td>74.398<sup>***</sup> (df=4; 521)</td></tr>
<tr><td colspan="4" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align: left">Note:</td><td colspan="3" style="text-align: right"><sup>*</sup>p&lt;0.1; <sup>**</sup>p&lt;0.05; <sup>***</sup>p&lt;0.01</td></tr></table>
```

Three things to notice:

1. **Three model columns** now — `(1)`, `(2)`, `(3)` — one per model, in the order you passed them.
2. **Blank cells** where a variable doesn't appear in a particular model. `exper` is absent from model (1), so the (1) column for `exper` is empty. This is exactly how journal tables handle it.
3. **The fit statistics** at the bottom (R², adjusted R², F-statistic, etc.) get a value for each column. Comparing R² across columns is the whole point — you can immediately see how much extra variation each new variable explains.

This is already enough for a working draft of a results table. But it could read better — `educ` and `tenure` aren't very informative as labels, and there's no overall title. That's where customisation comes in.

### Step 3: Customise the Labels

A journal-quality table needs more than the raw variable names. You'll want to:

1. Give the table a **title** so the reader knows what it's about.
2. Add **friendly column headers** above the model numbers, summarising what each specification does.
3. **Rename the covariates** from variable-name shorthand to readable phrases (e.g., `educ` → "Years of education").
4. Replace the **dependent variable label** with something more descriptive than `wage`.

Stargazer has a method for each of these, and they all attach to the same `star` object:

```python
star = Stargazer([m1, m2, m3])

# 1. Overall table title
star.title("Wage Equation: OLS Estimates")

# 2. Friendly column headers — labels and how many columns each spans
star.custom_columns(["Simple", "Multiple", "With gender"], [1, 1, 1])

# 3. Rename variables (left = raw name, right = display label)
star.rename_covariates({
    "educ":      "Years of education",
    "exper":     "Years of experience",
    "tenure":    "Years of tenure",
    "female":    "Female (=1)",
    "Intercept": "Constant",
})

# 4. Better label for the y-variable
star.dependent_variable_name("Hourly wage ($)")

star
```

```{raw} html
Wage Equation: OLS Estimates<br><table style="text-align:center"><tr><td colspan="4" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left"></td><td colspan="3"><em>Dependent variable: Hourly wage ($)</em></td></tr><tr><td style="text-align:left"></td><tr><td></td><td colspan="1">Simple</td><td colspan="1">Multiple</td><td colspan="1">With gender</td></tr><tr><td style="text-align:left"></td><td>(1)</td><td>(2)</td><td>(3)</td></tr>
<tr><td colspan="4" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left">Constant</td><td>-0.905<sup></sup></td><td>-2.873<sup>***</sup></td><td>-1.568<sup>**</sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.685)</td><td>(0.729)</td><td>(0.725)</td></tr>
<tr><td style="text-align:left">Years of education</td><td>0.541<sup>***</sup></td><td>0.599<sup>***</sup></td><td>0.572<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.053)</td><td>(0.051)</td><td>(0.049)</td></tr>
<tr><td style="text-align:left">Years of experience</td><td></td><td>0.022<sup>*</sup></td><td>0.025<sup>**</sup></td></tr>
<tr><td style="text-align:left"></td><td></td><td>(0.012)</td><td>(0.012)</td></tr>
<tr><td style="text-align:left">Female (=1)</td><td></td><td></td><td>-1.811<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td></td><td></td><td>(0.265)</td></tr>
<tr><td style="text-align:left">Years of tenure</td><td></td><td>0.169<sup>***</sup></td><td>0.141<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td></td><td>(0.022)</td><td>(0.021)</td></tr>
<td colspan="4" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align: left">Observations</td><td>526</td><td>526</td><td>526</td></tr><tr><td style="text-align: left">R<sup>2</sup></td><td>0.165</td><td>0.306</td><td>0.364</td></tr><tr><td style="text-align: left">Adjusted R<sup>2</sup></td><td>0.163</td><td>0.302</td><td>0.359</td></tr><tr><td style="text-align: left">Residual Std. Error</td><td>3.378 (df=524)</td><td>3.084 (df=522)</td><td>2.958 (df=521)</td></tr><tr><td style="text-align: left">F Statistic</td><td>103.363<sup>***</sup> (df=1; 524)</td><td>76.873<sup>***</sup> (df=3; 522)</td><td>74.398<sup>***</sup> (df=4; 521)</td></tr>
<tr><td colspan="4" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align: left">Note:</td><td colspan="3" style="text-align: right"><sup>*</sup>p&lt;0.1; <sup>**</sup>p&lt;0.05; <sup>***</sup>p&lt;0.01</td></tr></table>
```

That's much closer to a real journal table. Each customisation is doing useful work:

- **`title()`** — every paper-style table has a title above it. Without one, the reader has to guess what they're looking at.
- **`custom_columns()`** — readers shouldn't have to look up what specifications (1), (2), and (3) mean. The labels "Simple", "Multiple", and "With gender" tell them at a glance. The second list (`[1, 1, 1]`) tells Stargazer how many model columns each label should span — useful when you have, say, four models split into two groups, where you'd write `[2, 2]`.
- **`rename_covariates()`** — `educ` is a Python column name, not English. Readers don't need to know that. The raw name (left of the colon) maps to the display label (right). Notice we also renamed `Intercept` to `Constant`, which is the standard journal convention.
- **`dependent_variable_name()`** — replaces the bare `wage` with the more descriptive "Hourly wage ($)". You'd also use this for things like "log of GDP per capita" or "Probability of voting".

You don't have to do all of these every time — at minimum, `rename_covariates` and `dependent_variable_name` make a huge readability difference. Add the others when you're polishing a final draft.

### Step 4: Save the Table to a File

Rendering the table inside a notebook is great for checking it looks right, but to get it into Word we need to write it to disk. The simplest version is one line:

```python
with open("regression_table.html", "w") as f:
    f.write(star.render_html())
```

That's it. A file called `regression_table.html` now sits in your working directory containing the table HTML. Double-click it and it opens in your default browser, ready to copy into Word.

```{tip}
**The two-line workflow.** Once the file is saved, the rest is the standard copy-paste workflow:

1. Double-click `regression_table.html` to open it in your browser.
2. Click into the table, press <kbd>Cmd</kbd>+<kbd>A</kbd> (Mac) / <kbd>Ctrl</kbd>+<kbd>A</kbd> (Windows) to select all, then copy.
3. In Word, right-click → **Paste Special** → **HTML Format** (or use "Keep Source Formatting" from the paste options popup).

The borders, italics, and significance stars all come across.
```

#### A More Robust Version: Wrap in `<html><body>...</body></html>`

You'll sometimes see a slightly fancier version that wraps the rendered HTML in proper document tags:

```python
with open("regression_table.html", "w") as f:
    f.write("<html><body>" + star.render_html() + "</body></html>")
```

What's the difference? Stargazer's `render_html()` only produces the `<table>` element on its own — it isn't a complete HTML document. Browsers are forgiving and will display the table fine either way, but **Word's clipboard handling can be picky**, especially older versions on Windows. Wrapping the table in `<html><body>...</body></html>` makes it a proper, standalone HTML document, which tends to paste more reliably across different Word versions and operating systems.

If the simple version works for you, stick with it. If you ever find that Word strips your formatting on paste, switch to the wrapped version — it's a one-character change for an extra layer of safety.

### LaTeX Output

If you're writing your thesis in LaTeX, Stargazer can produce a `.tex` file directly:

```python
with open("regression_table.tex", "w") as f:
    f.write(star.render_latex())
```

You can then `\input{regression_table.tex}` from your main document. No more retyping numbers; if your data updates, re-run the Python and the LaTeX table updates with it.

---

## A Simpler Alternative: `summary_col`

Stargazer is the polished tool you'd use for a final report. But there's a built-in alternative that comes with `statsmodels` and needs no extra package: `summary_col`. It produces a plain-text comparison table that's perfect for quick checks while you're still iterating on a model.

```python
from statsmodels.iolib.summary2 import summary_col

table = summary_col(
    [m1, m2, m3],
    stars=True,
    float_format='%.3f',
    model_names=['(1) Simple', '(2) Multiple', '(3) With gender'],
    info_dict={'N': lambda x: f"{int(x.nobs)}"}
)
print(table)
```

```
======================================================
               (1) Simple (2) Multiple (3) With gender
------------------------------------------------------
Intercept      -0.905     -2.873***    -1.568**
               (0.685)    (0.729)      (0.725)
educ           0.541***   0.599***     0.572***
               (0.053)    (0.051)      (0.049)
exper                     0.022*       0.025**
                          (0.012)      (0.012)
tenure                    0.169***     0.141***
                          (0.022)      (0.021)
female                                 -1.811***
                                       (0.265)
R-squared      0.165      0.306        0.364
R-squared Adj. 0.163      0.302        0.359
N              526        526          526
======================================================
Standard errors in parentheses.
* p<.1, ** p<.05, ***p<.01
```

The information is all there — same coefficients, same SEs, same significance stars — just in plain text rather than fancy HTML. The arguments worth knowing:

- **`stars=True`** turns on the significance stars (off by default).
- **`float_format='%.3f'`** formats numbers to 3 decimal places.
- **`model_names=[...]`** labels the columns.
- **`info_dict={...}`** lets you add custom rows at the bottom — here we've added `N` (number of observations).

You can also save the table as text or LaTeX:

```python
with open("regression_table.txt", "w") as f:
    f.write(str(table))

with open("regression_table.tex", "w") as f:
    f.write(table.as_latex())
```

```{tip}
**When to use `summary_col` vs Stargazer:**

- **Use `summary_col`** for quick sanity checks while you're still fitting and tweaking models. No customisation overhead, no extra package.
- **Use Stargazer** for the final tables that go into your dissertation, term paper, or journal submission.

Both produce the same numerical content; Stargazer just makes them look nicer.
```

---

## Excel: Exporting Descriptive Statistics

Regression tables are the headline output of empirical work, but a typical results section also has descriptive statistics — means, standard deviations, group counts, correlations. These are just regular DataFrames, so the easiest export is a one-liner: `.to_excel()`.

### A Single DataFrame

`describe()` gives us a quick summary table. To send it to Excel, just call `.to_excel()`:

```python
summary = df[["wage", "educ", "exper", "tenure", "female"]].describe().round(2)
summary.to_excel("summary_stats.xlsx")
```

That's it. A file called `summary_stats.xlsx` now sits in your working directory. Open it in Excel and you'll see the same table you saw in Python.

```{tip}
The `.round(2)` is doing something important here: it's making sure the numbers in your Excel file are presented at the same level of precision that you want in your report. Floats with 14 decimal places look ugly. Round before you export.
```

### Tidying the Output

You'll often want descriptives in a more report-friendly shape — variables down the rows, statistics across the columns. The `.T` (transpose) attribute does exactly that:

```python
tidy = summary.T.reset_index().rename(columns={"index": "Variable"})
tidy.to_excel("summary_stats_clean.xlsx", index=False)
tidy
```

```
  Variable  count   mean    std   min    25%    50%    75%    max
0     wage  526.0   5.90   3.69  0.53   3.33   4.65   6.88  24.98
1     educ  526.0  12.56   2.77  0.00  12.00  12.00  14.00  18.00
2    exper  526.0  17.02  13.57  1.00   5.00  13.50  26.00  51.00
3   tenure  526.0   5.10   7.22  0.00   0.00   2.00   7.00  44.00
4   female  526.0   0.48   0.50  0.00   0.00   0.00   1.00   1.00
```

Three small but useful tweaks:

1. `.T` flips the table so each variable is a row.
2. `.reset_index()` turns the row labels into a normal column.
3. `.rename(columns={"index": "Variable"})` gives that column a proper header.
4. `index=False` in `to_excel()` tells pandas not to add another row-number column to the Excel file.

### Multiple Sheets in One Workbook

Often you want a single Excel file containing several tables — descriptives on one sheet, group means on another, your raw data sample on a third. The `pd.ExcelWriter` context manager makes this easy:

```python
with pd.ExcelWriter("results_full.xlsx") as writer:
    summary.to_excel(writer, sheet_name="Descriptives")
    df.head(10).to_excel(writer, sheet_name="Data sample", index=False)
    df.groupby("female")["wage"].agg(["mean", "count"]).to_excel(writer, sheet_name="By gender")
```

Open `results_full.xlsx` in Excel and you'll find three tabs along the bottom — one for each sheet. Use this any time you have related tables that belong together.

---

## Going Further: `python-docx` (Advanced)

The HTML copy-paste workflow above is what most students will use — it's quick, it works, and it preserves the formatting. But if you find yourself building a really long report — say, a quarterly regression update where you regenerate dozens of tables every month — there's a more automated route.

The [`python-docx`](https://python-docx.readthedocs.io/) library lets you write directly to `.docx` files:

```python
# In Colab/Jupyter: !pip install python-docx
# From a terminal:  pip install python-docx
from docx import Document

doc = Document()
doc.add_heading("Regression Results", level=1)
doc.add_paragraph("This document was generated automatically.")
# ... add tables, paragraphs, images ...
doc.save("report.docx")
```

You can build entire Word documents with paragraphs, headings, embedded tables, and images — all from Python. It's a steeper learning curve and overkill for most coursework, but if you ever need a fully reproducible Word report (no copy-paste), that's where to look.

---

## Putting It All Together

Here's a complete, end-to-end script that produces both a polished HTML regression table **and** a multi-sheet Excel workbook of descriptive statistics, ready to drop into a dissertation:

```python
import pandas as pd
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer

# 1. Load and prepare
url = "https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv"
df = pd.read_csv(url)

# 2. Fit the models
m1 = smf.ols("wage ~ educ", data=df).fit()
m2 = smf.ols("wage ~ educ + exper + tenure", data=df).fit()
m3 = smf.ols("wage ~ educ + exper + tenure + female", data=df).fit()

# 3. Polished HTML regression table for Word
star = Stargazer([m1, m2, m3])
star.title("Wage Equation: OLS Estimates")
star.custom_columns(["Simple", "Multiple", "With gender"], [1, 1, 1])
star.rename_covariates({
    "educ":      "Years of education",
    "exper":     "Years of experience",
    "tenure":    "Years of tenure",
    "female":    "Female (=1)",
    "Intercept": "Constant",
})
star.dependent_variable_name("Hourly wage ($)")
with open("regression_table.html", "w") as f:
    f.write("<html><body>" + star.render_html() + "</body></html>")

# 4. Excel workbook with descriptives + group means
with pd.ExcelWriter("results.xlsx") as writer:
    df[["wage", "educ", "exper", "tenure", "female"]].describe().round(2)\
      .to_excel(writer, sheet_name="Descriptives")
    df.groupby("female")["wage"].agg(["mean", "count"])\
      .to_excel(writer, sheet_name="By gender")

print("All done — you should now have:")
print("  regression_table.html  — open this in a browser, copy, paste into Word")
print("  results.xlsx           — descriptive statistics workbook")
```

Run that script once. Then if your data updates — say, you find an error and re-clean the file — you re-run the script, re-open the HTML, and re-paste. The numbers update everywhere automatically. **That's reproducibility.**

---

## Summary: When to Use Which Tool

| Tool | Best for | File format | Effort |
|------|----------|-------------|--------|
| `Stargazer` | Publication-quality regression tables for reports | HTML / LaTeX | A few lines for full customisation |
| `summary_col` | Quick side-by-side comparison while iterating | Text / LaTeX | Three lines |
| `df.to_excel()` | Descriptive statistics, group means, cleaned data | `.xlsx` | One line |
| `python-docx` | Fully automated Word documents (advanced) | `.docx` | Steeper learning curve |

For a typical dissertation chapter, the combination is:

- `Stargazer` for the regression tables — copy-paste from the HTML into Word.
- `to_excel()` for descriptive statistics.
- Save the script that generates everything so re-running is a one-button operation.

That's everything you need.

---

## Exercises

````{exercise}
:label: ex12-stargazer-simple

**Exercise 1: Your First Stargazer Table**

Using `wage1`:

1. Fit a simple regression `lwage ~ educ` and save it as `m_simple`.
2. Pass it to `Stargazer` and display the table in your notebook.
3. From the table alone (without printing `model.summary()`), what's the coefficient on `educ`? What's its significance level?
4. What does the `R²` row tell you?
````

````{solution} ex12-stargazer-simple
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer

url = "https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv"
df = pd.read_csv(url)

m_simple = smf.ols("lwage ~ educ", data=df).fit()
star = Stargazer([m_simple])
star
```

The table will show the coefficient on `educ` as roughly **0.083** with three stars (p < 0.01) — i.e., highly significant. The R² row reports about **0.186**, meaning education alone explains roughly 18.6% of the variation in log-wage in this sample.
````

````{exercise}
:label: ex12-stargazer-multi

**Exercise 2: Building a Side-by-Side Comparison**

Using `wage1`, fit three models predicting `lwage`:

- **A**: `lwage ~ educ`
- **B**: `lwage ~ educ + exper + tenure`
- **C**: `lwage ~ educ + exper + tenure + female`

1. Pass all three to `Stargazer` to produce a side-by-side table.
2. By how much does the coefficient on `educ` change as you add controls? Why might that be?
3. Save the table as `lwage_table.html` (the simple version, without the `<html><body>` wrapper).
````

````{solution} ex12-stargazer-multi
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer

url = "https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv"
df = pd.read_csv(url)

A = smf.ols("lwage ~ educ", data=df).fit()
B = smf.ols("lwage ~ educ + exper + tenure", data=df).fit()
C = smf.ols("lwage ~ educ + exper + tenure + female", data=df).fit()

star = Stargazer([A, B, C])
star  # display in notebook

with open("lwage_table.html", "w") as f:
    f.write(star.render_html())
```

The coefficient on `educ` typically rises from about 0.083 in column (A) to around 0.087 in column (C). It rises because in the simple model, `educ` was implicitly carrying part of the effect of variables correlated with it (less-educated workers tend to have *more* experience, which masks the schooling return). Adding controls separates the effects.
````

````{exercise}
:label: ex12-stargazer-polish

**Exercise 3: A Polished Stargazer Table**

Building on Exercise 2, polish the table:

1. Set the **title** to `"Log Wage Equation"`.
2. Use **`custom_columns`** to label the three columns "Simple", "+ Exp/Tenure", "+ Gender".
3. **Rename the covariates** so they read in plain English (e.g., `educ` → "Years of education", `Intercept` → "Constant").
4. Set the **dependent variable label** to `"ln(Hourly wage)"`.
5. Save the result as `lwage_table.html` using the **wrapped `<html><body>...</body></html>` version**.
6. Open the file in your browser and confirm it looks ready to paste into Word.
````

````{solution} ex12-stargazer-polish
:class: dropdown

```python
import pandas as pd
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer

url = "https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv"
df = pd.read_csv(url)

A = smf.ols("lwage ~ educ", data=df).fit()
B = smf.ols("lwage ~ educ + exper + tenure", data=df).fit()
C = smf.ols("lwage ~ educ + exper + tenure + female", data=df).fit()

star = Stargazer([A, B, C])
star.title("Log Wage Equation")
star.custom_columns(["Simple", "+ Exp/Tenure", "+ Gender"], [1, 1, 1])
star.rename_covariates({
    "educ":      "Years of education",
    "exper":     "Years of experience",
    "tenure":    "Years of tenure",
    "female":    "Female (=1)",
    "Intercept": "Constant",
})
star.dependent_variable_name("ln(Hourly wage)")

with open("lwage_table.html", "w") as f:
    f.write("<html><body>" + star.render_html() + "</body></html>")

print("Wrote lwage_table.html — open it in your browser, copy the table, paste into Word.")
```
````

````{exercise}
:label: ex12-excel

**Exercise 4: Tidy Descriptives to Excel**

Using `wage1`:

1. Compute the summary statistics for the variables `wage`, `educ`, `exper`, and `tenure` rounded to 2 decimal places.
2. Transpose the result so that variables are in rows and statistics are in columns.
3. Save the tidied table to a file called `descriptives.xlsx` without the row-number column.
4. Open the file in Excel (or just open it from your file browser) and confirm the columns and numbers look as expected.
````

````{solution} ex12-excel
:class: dropdown

```python
import pandas as pd

url = "https://raw.githubusercontent.com/sakibanwar/python-notes/main/data/wage1.csv"
df = pd.read_csv(url)

tidy = (
    df[["wage", "educ", "exper", "tenure"]]
      .describe()
      .round(2)
      .T
      .reset_index()
      .rename(columns={"index": "Variable"})
)

tidy.to_excel("descriptives.xlsx", index=False)
print(tidy)
```

```
  Variable  count   mean    std   min    25%    50%    75%    max
0     wage  526.0   5.90   3.69  0.53   3.33   4.65   6.88  24.98
1     educ  526.0  12.56   2.77  0.00  12.00  12.00  14.00  18.00
2    exper  526.0  17.02  13.57  1.00   5.00  13.50  26.00  51.00
3   tenure  526.0   5.10   7.22  0.00   0.00   2.00   7.00  44.00
```
````
