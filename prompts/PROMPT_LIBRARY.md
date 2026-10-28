# 🤖 AI Prompt Library for Research Coding

Ready-made prompts for ChatGPT, Claude, Gemini or GitHub Copilot Chat. Copy one, replace the `[brackets]`, and **always verify the answer**.

> **The three rules**
> 1. **Protect data.** Share column names, `df.info()`, `df.describe()` or a few *fake* rows, never confidential or personal records.
> 2. **Verify everything.** Run the code, check the numbers, and look up every citation yourself.
> 3. **Understand before you use.** If you can't explain a line to your supervisor, don't put it in your thesis.

Add your own prompts that work well to the end of this file. This library is part of your toolkit.

---

## 1. Getting unstuck with code

**Explain an error**
```
I'm running Python [3.x] with pandas in a Jupyter notebook in VS Code.
This code:
[paste code]
gives this error:
[paste the FULL traceback]
Explain in simple terms what the error means, why it happened, and give the corrected code.
```

**Explain code line by line**
```
Explain this Python code line by line for a researcher who knows basic Python.
For each line, say what it does and why it is needed:
[paste code]
```

**Write code from a description**
```
I have a pandas DataFrame `df` with these columns and dtypes:
[paste df.dtypes]
Write code to [task, e.g. "compute the mean and 95% CI of yield for each LGA and sort descending"].
Use clear variable names and add short comments. Do not invent columns that are not listed.
```

**Make code cleaner / reusable**
```
Refactor this notebook code into a well-named Python function with a docstring,
type hints and no global variables. Keep the behaviour exactly the same:
[paste code]
```

**Write a test**
```
Write a simple pytest test for this function that checks [expected behaviour],
including one edge case such as missing values:
[paste function]
```

## 2. Data cleaning & exploration

**Data quality audit**
```
Act as a careful data science supervisor. Below is df.info() and df.describe() for a
[type of] dataset with [n] rows. List the data-quality problems I should investigate
before analysis, and for each one give the pandas code to check it.
[paste output]
```

**Missing data strategy**
```
My dataset on [topic] has these missing-value percentages:
[paste table]
For each variable, suggest whether to drop, impute (and how), or model the missingness,
and explain the assumptions (MCAR / MAR / MNAR) behind each choice. I am going to train
a model later, so tell me how to avoid data leakage.
```

**Exploration plan**
```
My research question is: [question]. My variables are: [list with types].
Suggest 5 exploratory plots or tables that would help answer it, why each is useful,
and the seaborn/pandas code for each.
```

## 3. Choosing & running the analysis

**Which statistical test?**
```
I want to compare [outcome, with its type and distribution] between [groups / variables].
Sample size: [n]. Design: [independent / paired / repeated measures].
Which statistical test is appropriate? What are its assumptions, how do I check them in
Python, and what is the non-parametric alternative if they fail?
```

**Check my regression**
```
Here is my statsmodels regression summary:
[paste summary]
1) Interpret the significant coefficients in plain language with units.
2) What assumptions should I check, and how in Python?
3) What warnings in this output should worry me?
```

**Machine learning set-up review**
```
Review this scikit-learn workflow for data leakage, an incorrect train/test split,
and misleading evaluation. Explain any problem and show the fix:
[paste code]
```

**Pick evaluation metrics**
```
I am predicting [target] for [purpose]. The data is [balanced/imbalanced, n rows].
Which evaluation metrics should I report in my thesis and why? What is a sensible baseline?
```

## 4. Figures & tables for publication

```
Improve this matplotlib/seaborn figure so it meets journal standards: readable font
sizes, axis labels with units, colour-blind-safe colours, no chart junk, 300 dpi export
as PNG and PDF. Keep the same data:
[paste code]
```

```
Convert this pandas DataFrame into a publication-style table (APA 7) and give me code to
export it as CSV and as a Word-friendly HTML table:
[paste df.head() or the table]
```

## 5. Writing (use with great care)

**Interpret results, then verify them**
```
Here are my results: [paste table/statistics].
Draft a results paragraph in formal academic English for an [MSc/PhD] thesis in [field].
Report effect sizes and 95% CIs, avoid causal language, and do not add any numbers
that are not in the table.
```
✅ *Check every number against your output. Watch for words like "caused", "proved" or "significant" used loosely.*

**Methods section from code**
```
Here is my analysis code. Write a methods paragraph describing the data cleaning,
statistical tests and model evaluation so another researcher could reproduce it.
Mention software and package versions: [paste versions].
[paste code]
```

**Critique my argument**
```
Act as a critical external examiner. Read this paragraph from my thesis and list the
weaknesses in the argument, unsupported claims, and questions you would ask in my defence:
[paste paragraph]
```

⛔ **Do not** ask AI to *"give me references on X"* and paste them in. AI tools invent realistic-looking citations. Use Google Scholar, Scopus, Semantic Scholar or your library, and read what you cite.

## 6. Git, GitHub & VS Code

```
Explain what this Git message means and what I should do next, step by step
(I am using VS Code on Windows):
[paste message]
```

```
Write a clear README.md for my research repository. Project: [title]. Research question:
[question]. Data: [source and licence]. Folder structure: [paste tree]. How to run:
[steps]. Include a "How to cite" section.
```

## 7. Streamlit apps

```
Here is my Streamlit app:
[paste code]
Add [feature, e.g. "a sidebar filter by LGA" / "a tab with a downloadable summary table"].
Keep the existing structure and explain what you changed.
```

```
My Streamlit app fails with this error:
[paste error]
It loads a model with joblib from models/. Explain the cause and fix it.
```

---

## ✍️ My own prompts that worked
| Task | Prompt | Tool | Notes |
|---|---|---|---|
| | | | |
