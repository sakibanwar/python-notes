# Python Notes — Claude Code Instructions

## Project Overview

This is an **online Python textbook** for the AN7914 Data Analytics and Modelling course at the University of Winchester. It uses **Jupyter Book** to generate a static website with interactive code execution, hosted on GitHub Pages.

## Source Materials

The original Python session PDFs are in a separate local folder. These are the authoritative source for:
- Content topics and progression
- Teaching style and tone
- Code examples and explanations

## Writing Style — CRITICAL

Match the original notes exactly. The style is:

### Tone
- Conversational and direct — speak TO the student
- Friendly but professional
- Use "you" and "we" frequently
- Ask rhetorical questions to engage: "Why might this be?", "What happens if...?"

### Structure
- **Step-by-step progression** — show simple code first, then improve it iteratively
- Use "Notice..." to highlight key observations
- Show code blocks followed immediately by their output
- Include tables for comparisons and summaries
- Add warnings/tips for common pitfalls

### Code Style
- Include comments explaining what code does
- Show both the wrong way and right way when teaching concepts
- Use realistic examples (Harry Potter characters, everyday scenarios)
- Always show the output after code blocks

### What NOT to do
- Don't be overly academic or formal
- Don't skip steps — show the full progression
- Don't assume prior knowledge without explanation
- Don't use jargon without defining it first

## File Structure

```
python-notes/
├── _config.yml              # DA Jupyter Book config
├── _config_stats.yml        # Stats Jupyter Book config
├── _toc.yml                 # DA table of contents
├── _toc_stats.yml           # Stats table of contents
├── intro.md                 # DA welcome page
├── intro_stats.md           # Stats welcome page
├── chapters/
│   ├── 01_getting_started.md
│   ├── 02_conditionals.md
│   ├── 03_data_structures.md
│   ├── 04_intro_pandas.md
│   ├── 05_data_viz.md / 05_data_viz_stats.md
│   ├── 06_filtering.md / 06_filtering_stats.md
│   ├── 07_grouping.md
│   ├── 08_data_cleaning.md
│   ├── 09_statistical_inference.md                  # Shared (was DA-only Hypothesis Testing)
│   ├── 10_exploratory_analysis.md
│   ├── 11_regression.md                              # Intro to regression (wage1, shared)
│   ├── 12_exporting_results.md                       # Stargazer / Excel (shared)
│   ├── 13_regression_case_study.md /
│   │   13_regression_case_study_stats.md             # Vienna hotels case study
│   └── 14_dashboards.md                              # Streamlit (shared)
├── data/
│   ├── wage1.csv                                     # Wooldridge wage equation data
│   ├── vienna_hotels.csv                             # for the case study
│   └── ... (other course datasets)
├── _scripts/
│   └── build_data.py                                 # Regenerates Wooldridge CSVs
├── _static/
│   ├── css/custom.css
│   └── js/exercises.js
└── requirements.txt
```

## Chapter Mapping (PDF → Book)

The book is published in two versions sharing most chapters: the **DA** version (Data Analytics / Data Analysis) and the **Stats** version (Quantitative Methods and Statistics). Stats-only files have a `_stats` suffix.

| Ch | Topic | Chapter File(s) |
|----|-------|-----------------|
| 1 | Functions and Variables | `01_getting_started.md` |
| 2 | Conditionals | `02_conditionals.md` |
| 3 | Data Structures and Loops | `03_data_structures.md` |
| 4 | Intro to Pandas | `04_intro_pandas.md` |
| 5 | Data Viz with Seaborn | `05_data_viz.md` (DA) / `05_data_viz_stats.md` (Stats) |
| 6 | Filtering Data | `06_filtering.md` (DA) / `06_filtering_stats.md` (Stats) |
| 7 | Grouping and Aggregating | `07_grouping.md` |
| 8 | Data Cleaning | `08_data_cleaning.md` |
| 9 | Statistical Inference | `09_statistical_inference.md` (shared) |
| 10 | Exploratory Analysis | `10_exploratory_analysis.md` |
| 11 | Intro to Regression (wage1) | `11_regression.md` (shared) |
| 12 | Exporting Results to Word and Excel | `12_exporting_results.md` (shared) |
| 13 | Regression Analysis: A Case Study (Vienna hotels) | `13_regression_case_study.md` (DA) / `13_regression_case_study_stats.md` (Stats) |
| 14 | Streamlit Dashboards | `14_dashboards.md` (shared) |

## Exercise Format

Each chapter ends with 2-4 exercises using this format:

````markdown
````{exercise}
:label: ex1-name

**Exercise 1: Title**

Description of the exercise...
````

````{solution} ex1-name
:class: dropdown

```python
# Solution code here
```
````
````

Exercises should:
- Build directly on chapter content
- Start simple, increase in difficulty
- Have clear success criteria
- Include hints when appropriate

## Building the Book

```bash
# Install dependencies
pip install -r requirements.txt

# Build HTML
jupyter-book build .

# Deploy to GitHub Pages
ghp-import -n -p -f _build/html
```

## When Expanding Chapters

1. Read the corresponding PDF first
2. Expand explanations where the PDF is brief
3. Add more examples and edge cases
4. Include practical "why this matters" context
5. Add 2-4 exercises per chapter
6. Keep the iterative improvement pattern (show basic → show improved)

## Common Patterns to Follow

### Introducing a new concept:
```markdown
## Concept Name

Brief intro sentence explaining what this is and why it matters.

```python
simple_example_code()
```

```
output
```

Notice [key observation]. This works because [explanation].

[More detailed explanation with context]

```python
more_advanced_example()
```
```

### Showing common mistakes:
```markdown
What happens if we try this?

```python
wrong_approach()
```

```
ErrorMessage: explanation
```

This doesn't work because [reason]. Instead, we need to [correct approach]:

```python
correct_approach()
```

```
expected output
```
```

### Tables for comparison:
```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Syntax  | `x`      | `y`      |
| When to use | ... | ... |
```

## Important Notes

- The target audience is **postgraduate business/economics students**, not CS majors
- Prioritise clarity and understanding over efficiency
- The textbook reference is Békés & Kézdi (2021) — align econometric examples with their approach
- For pandas/seaborn chapters, use real-world economic datasets where possible
