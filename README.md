# Python for Business, Economics & Finance

An online textbook for learning Python for data analysis, designed for courses at the University of Winchester.

## View Online

This textbook is published in two versions:

| Version | Course | Link |
|---------|--------|------|
| **Data Analysis** | Data Analytics / Data Analysis | [Read the DA book](https://sakibanwar.github.io/python-notes/) |
| **Statistics & Quantitative Methods** | Quantitative Methods and Statistics | [Read the Stats book](https://sakibanwar.github.io/python-notes/stats/) |

Both versions share most chapters. The Stats version has expanded content in **data visualisation** (Ch 5), **filtering** (Ch 6), and a **different regression case study** (Ch 14); everything else is identical.

## Features

- **Step-by-step tutorials** from Python basics to data analysis
- **Executable code cells** — real output rendered in every chapter
- **Exercises with solutions** — try them yourself, then check the dropdown
- **Real-world examples** using economic and business datasets

## Contents

| Ch | Topic | Notes |
|----|-------|-------|
| 1  | Getting Started with Python | shared |
| 2  | Conditionals and Loops | shared |
| 3  | Data Structures: Lists and Dictionaries | shared |
| 4  | Introduction to Pandas | shared |
| 5  | Data Visualisation with Seaborn | Stats version expanded |
| 6  | Filtering Data | Stats version expanded |
| 7  | Grouping and Aggregating | shared |
| 8  | Data Cleaning | shared |
| 9  | Statistical Inference: Foundation (Normal, CLT, CIs) | shared |
| 10 | Statistical Inference: Hypothesis Testing | shared |
| 11 | Exploratory Analysis | shared |
| 12 | Introduction to Regression (Wooldridge `wage1`) | shared |
| 13 | Exporting Results to Word and Excel (Stargazer) | shared |
| 14 | Regression Analysis: A Case Study (Vienna hotels) | DA and Stats variants |
| 15 | Creating Dashboards with Streamlit | shared |

## Building Locally

```bash
# Clone the repository
git clone https://github.com/sakibanwar/python-notes.git
cd python-notes

# Install dependencies
pip install -r requirements.txt

# Build the DA version
jupyter-book build .

# Build the Stats version
jupyter-book build . --toc _toc_stats.yml --config _config_stats.yml --path-output _build_stats

# Open in browser
open _build/html/index.html
open _build_stats/_build/html/index.html
```

## Course Reference

These notes accompany lectures based on:

> Békés, G., & Kézdi, G. (2021). *Data analysis for business, economics, and policy*. Cambridge University Press.
> [gabors-data-analysis.com](https://gabors-data-analysis.com/)

> Diez, D. M., Çetinkaya-Rundel, M., & Barr, C. D. (2019). *OpenIntro Statistics* (4th ed.). OpenIntro, Inc.
> [openintro.org](https://www.openintro.org/)

## Contributing

Found an error or have a suggestion? Please [open an issue](https://github.com/sakibanwar/python-notes/issues) or submit a pull request.

## License

This work is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
