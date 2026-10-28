# Reproducibility checklist

Could another researcher, your examiner, or *you in two years*, get the same results from your repository? Tick each item.

## Project & data
- [ ] Raw data is in `data/raw/` and has **never been edited by hand**
- [ ] Every change to the data is done in code (`src/` or a notebook)
- [ ] `data/README.md` describes the source, collection date, licence/permissions and every column
- [ ] Confidential data is in `.gitignore`, and the README explains how authorised people can get it
- [ ] Ethical approval reference is recorded (if applicable)

## Code
- [ ] `requirements.txt` lists every package. Run `pip freeze > requirements-lock.txt` for exact versions
- [ ] Notebooks are numbered in the order they run (`01_`, `02_` …)
- [ ] **Restart kernel & Run All** works from top to bottom without errors
- [ ] Repeated code has been moved into functions in `src/`
- [ ] Random seeds are fixed (`random_state=42`) so results don't change between runs
- [ ] No hard-coded personal paths like `C:\Users\Musa\Desktop\...`. Use paths relative to the project

## Analysis
- [ ] The research question and hypotheses are written down **before** the main analysis
- [ ] Assumptions of each statistical test were checked
- [ ] Effect sizes and confidence intervals are reported, not just p-values
- [ ] For ML: a baseline model, a held-out test set, preprocessing inside a pipeline, and no leaky features
- [ ] The number of rows used in each analysis is reported (missing data!)

## Outputs
- [ ] Every figure and table in the thesis is produced by code and saved in `figures/` or `results/`
- [ ] Figures are 300 dpi with labelled axes, units and colour-blind-safe colours

## Sharing
- [ ] `README.md` explains what the project is, how to install and how to run it
- [ ] AI use is disclosed (`docs/AI_USE_STATEMENT_TEMPLATE.md`)
- [ ] A licence is chosen (e.g. MIT for code, CC BY 4.0 for data you own), agreed with your supervisor
- [ ] A release is archived on Zenodo with a DOI, and the DOI is cited in the thesis
