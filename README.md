# Python for Data Science in Academic Research
### using AI, VS Code & GitHub: starter repository

**Workshop for MSc, MPhil & PhD researchers · Nasarawa State University, Keffi**
📅 Friday 30 & Saturday 31 October 2026 · 🕙 10:00 am – 2:00 pm (WAT)

You will build this repository into a **reproducible research project**: cleaned data, statistical analysis, a machine-learning model, publication-ready figures, and a **Streamlit app** that demonstrates your model, all under version control on GitHub.

---

## 🚀 Quick start

> **New here? Follow [`docs/SETUP.md`](docs/SETUP.md) step by step before the workshop.**

```bash
# 1. Click "Use this template" on GitHub to make your own copy, then clone it in VS Code
# 2. Create and activate the environment (Windows PowerShell shown)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. Check that everything works
streamlit run app/streamlit_app.py
```

## 🗂️ What's inside

```
├── data/
│   ├── raw/nasarawa_maize_survey_synthetic.csv   synthetic practice dataset (see data/README.md)
│   └── processed/                                created by the notebooks
├── notebooks/
│   ├── 01_day1_clean_and_explore.ipynb           Day 1: audit, cleaning, EDA, AI-assisted coding
│   └── 02_day2_analyse_model_app.ipynb           Day 2: statistics, ML, figures, Streamlit
├── src/
│   ├── cleaning.py      reusable, tested cleaning function
│   ├── modelling.py     leak-free ML pipeline, metrics, model saving
│   └── plotting.py      publication-ready figure style (300 dpi, colour-blind-safe)
├── app/streamlit_app.py interactive demo of your trained model
├── prompts/PROMPT_LIBRARY.md        AI prompts for research coding, writing and debugging
├── docs/
│   ├── SETUP.md                     installation and troubleshooting
│   ├── GIT_CHEATSHEET.md            Git and GitHub for researchers, plus getting a DOI
│   ├── AI_USE_STATEMENT_TEMPLATE.md disclose AI use in your thesis or paper
│   └── REPRODUCIBILITY_CHECKLIST.md before you submit
├── figures/  results/  models/      outputs created by code
└── scripts/                         facilitator tools (data and notebook generators)
```

## 📋 Programme

### Day 1, Friday 30 October: Setup, version control and AI-assisted data work
| Time | Session | Notebook |
|---|---|---|
| 10:00 – 10:30 | Welcome, goals, interest poll, setup check | §0 |
| 10:30 – 11:15 | VS Code and Python for research: environments, notebooks, extensions | §0–1 |
| 11:15 – 12:15 | Git and GitHub for researchers: project structure, commit, push, `.gitignore` | §1 |
| 12:15 – 12:35 | ☕ Break | |
| 12:35 – 1:45 | Data audit, cleaning and EDA with an AI assistant (prompt, then verify) | §2–6 |
| 1:45 – 2:00 | Exercise review, commit and push, homework | |

### Day 2, Saturday 31 October: Analysis, machine learning and Streamlit
| Time | Session | Notebook |
|---|---|---|
| 10:00 – 10:10 | Recap and `git pull` | |
| 10:10 – 11:05 | Hypothesis testing and regression: effect sizes, CIs, assumptions | §1–3 |
| 11:05 – 11:50 | Machine learning: pipelines, cross-validation, the leakage trap, honest evaluation | §4 |
| 11:50 – 12:05 | ☕ Break | |
| 12:05 – 12:25 | Publication-ready figures and tables; saving the model | §5–6 |
| 12:25 – 1:05 | **Streamlit:** demo your model as a web app, and extend it with AI | §7 |
| 1:05 – 1:35 | Mini-project on your own data | §8 |
| 1:35 – 1:50 | Responsible AI in research: disclosure, invented citations, data privacy | §9 |
| 1:50 – 2:00 | Showcase, next steps, certificates | |

## 🎒 What you leave with
- ✅ A GitHub repository showing a complete, reproducible analysis workflow
- ✅ A project template to reuse for your thesis chapters
- ✅ A working Streamlit app for your model
- ✅ A prompt library for AI-assisted research coding
- ✅ An AI-use statement and a reproducibility checklist for your thesis

## ⚠️ About the sample data
`data/raw/nasarawa_maize_survey_synthetic.csv` is **simulated** for teaching, with deliberate errors to practise cleaning. It is not real survey data and must not be cited as evidence. See [`data/README.md`](data/README.md).

---

## 🧑‍🏫 Facilitator notes

- **Make this a template repo:** on GitHub, go to Settings → tick **Template repository**. Participants then use **Use this template**.
- **Regenerate the dataset:** `python scripts/make_sample_data.py` (fixed seed, so the output is identical every time).
- **Edit the notebooks:** change `scripts/build_notebooks.py`, then run `python scripts/build_notebooks.py`.
- **Offline package folder** for a flash drive (build it on a Windows machine with the same Python version as participants):
  ```bash
  pip download -r requirements.txt -d wheelhouse
  # participants then run:
  pip install --no-index --find-links=wheelhouse -r requirements.txt
  ```
- **Smoke test before the workshop:** delete `data/processed/` and `models/`, then run both notebooks top to bottom and start the app.
