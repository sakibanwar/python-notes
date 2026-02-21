# Python for Business, Economics & Finance

An online textbook for learning Python for data analysis, designed for courses at the University of Winchester.

## View Online

This textbook is published in two versions:

| Version | Course | Link |
|---------|--------|------|
| **Data Analysis** | Data Analytics / Data Analysis | [Read the DA book](https://sakibanwar.github.io/python-notes/) |
| **Statistics & Quantitative Methods** | Quantitative Methods and Statistics | [Read the Stats book](https://sakibanwar.github.io/python-notes/stats/) |

Both versions share the same Python fundamentals (Chapters 1-4, 7-8, 10, 12). The Stats version has expanded content on data visualisation, filtering, statistical inference, and regression.

## Features

- **Step-by-step tutorials** from Python basics to data analysis
- **Executable code cells** — real output rendered in every chapter
- **Exercises with solutions** — try them yourself, then check the dropdown
- **Real-world examples** using economic and business datasets

## Contents

| Ch | Data Analysis | Stats & QM |
|----|--------------|------------|
| 1 | Getting Started with Python | Getting Started with Python |
| 2 | Conditionals | Conditionals |
| 3 | Data Structures and Loops | Data Structures and Loops |
| 4 | Introduction to Pandas | Introduction to Pandas |
| 5 | Data Visualisation with Seaborn | Data Visualisation with Seaborn *(expanded)* |
| 6 | Filtering Data | Filtering Data *(expanded)* |
| 7 | Grouping and Aggregating | Grouping and Aggregating |
| 8 | Data Cleaning | Data Cleaning |
| 9 | Hypothesis Testing | Statistical Inference *(rewritten)* |
| 10 | Exploratory Analysis | Exploratory Analysis |
| 11 | Introduction to Regression | Introduction to Regression *(expanded)* |
| 12 | Creating Dashboards with Streamlit | Creating Dashboards with Streamlit |

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
