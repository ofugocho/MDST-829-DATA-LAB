"""
Build the workshop notebooks from the cell definitions below.

Facilitators: edit the text here, then run from the repository root:
    python scripts/build_notebooks.py
Participants: you do not need this file, just open the notebooks.
"""

from pathlib import Path
from textwrap import dedent

import nbformat as nbf

NOTEBOOK_DIR = Path(__file__).resolve().parents[1] / "notebooks"

SETUP_CODE = """
import sys
from pathlib import Path

# Make the project's src/ folder importable, whether the notebook runs from
# the repository root or from inside notebooks/
ROOT = Path.cwd() if (Path.cwd() / "src").exists() else Path.cwd().parent
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.plotting import set_publication_style, save_figure

set_publication_style()
pd.set_option("display.max_columns", 30)
print("Project root:", ROOT)
"""


def md(text):
    return nbf.v4.new_markdown_cell(dedent(text).strip())


def code(text):
    return nbf.v4.new_code_cell(dedent(text).strip())


# =============================================================================
# DAY 1
# =============================================================================
DAY1 = [
    md("""
    # Day 1: From messy data to clean insights
    **Python for Data Science in Academic Research, with AI, VS Code & GitHub**
    Nasarawa State University, Keffi · Friday 30 October 2026 · 10:00 am – 2:00 pm

    ### By the end of today you will be able to
    1. Run Python notebooks inside **VS Code** in a project's own environment
    2. Keep your research under **version control** with Git and GitHub
    3. **Audit** a dataset for quality problems and keep a cleaning log for your methods chapter
    4. **Clean** data with pandas and turn the steps into a reusable function
    5. **Explore** data visually and use an **AI assistant** *responsibly* along the way

    ### How to read this notebook
    | Symbol | Meaning |
    |---|---|
    | 🤖 | **AI exercise**: use ChatGPT, Claude, Gemini or GitHub Copilot, then **check** what it gives you |
    | ✍️ | **Your turn**: write your own code or notes |
    | 💾 | **Git checkpoint**: commit your work |

    Run a cell with **Shift + Enter**. If VS Code asks for a kernel, choose the `.venv` environment you created in `docs/SETUP.md`.
    """),

    md("## 0. Check your environment"),
    code("""
    import platform, importlib

    print("Python", platform.python_version())
    for pkg in ["pandas", "numpy", "matplotlib", "seaborn", "sklearn", "statsmodels", "scipy", "streamlit"]:
        try:
            print(f"  ✅ {pkg:12s} {importlib.import_module(pkg).__version__}")
        except ImportError:
            print(f"  ❌ {pkg:12s} NOT INSTALLED - run: pip install -r requirements.txt")
    """),

    md("""
    ## 1. A research project is a folder, not a single file

    ```
    nsuk-ds-workshop-starter/
    ├── data/raw/         ← original data, NEVER edited by hand
    ├── data/processed/   ← created by code (can always be re-created)
    ├── notebooks/        ← exploration and analysis, in order (01_, 02_ ...)
    ├── src/              ← reusable functions (cleaning, modelling, plotting)
    ├── figures/          ← figures for your thesis or paper (created by code)
    ├── results/          ← tables and outputs (created by code)
    ├── models/           ← saved trained models
    ├── app/              ← Streamlit app (Day 2)
    ├── prompts/          ← your AI prompt library
    └── docs/             ← setup guide, Git cheat sheet, checklists
    ```

    **Golden rule:** anything in `processed/`, `figures/`, `results/` and `models/` should be re-creatable by running your code on `raw/`. That is what *reproducible* means.

    ### 💾 Git checkpoint 1
    Open the VS Code terminal (**Ctrl + `**) and run:
    ```bash
    git status
    git add .
    git commit -m "Start Day 1 notebook"
    git push
    ```
    Or use the **Source Control** panel (Ctrl + Shift + G). See `docs/GIT_CHEATSHEET.md`.
    """),

    md("""
    ## 2. Load the raw data

    > ⚠️ **About this dataset.** `nasarawa_maize_survey_synthetic.csv` is **simulated** data that imitates a smallholder maize survey across the 13 LGAs of Nasarawa State. It was made for teaching and contains **deliberate errors**. Never cite it as real evidence.

    | Column | Meaning |
    |---|---|
    | `farm_id`, `survey_year`, `lga` | identifiers and location |
    | `farmer_age`, `gender`, `education_level`, `years_farming` | farmer characteristics |
    | `farm_size_ha`, `improved_seed`, `fertilizer_kg_per_ha`, `irrigation` | farm practices |
    | `rainfall_mm`, `avg_temp_c`, `soil_ph` | environment |
    | `extension_visits`, `cooperative_member`, `pest_incidence` | support and pests |
    | `harvest_sales_naira` | money earned from the harvest |
    | **`yield_kg_per_ha`** | **outcome we want to explain and predict** |
    """),
    code(SETUP_CODE),
    code("""
    RAW_PATH = ROOT / "data" / "raw" / "nasarawa_maize_survey_synthetic.csv"
    df_raw = pd.read_csv(RAW_PATH)

    print(df_raw.shape)
    df_raw.head()
    """),
    code("df_raw.info()"),
    code("df_raw.describe(include='all').T"),

    md("""
    ### 🤖 AI exercise 1: a second pair of eyes
    Copy the output of `df_raw.info()` and `describe()` (**not the raw data itself**) into your AI assistant with this prompt:

    > *"Act as a careful data science supervisor. Below is the `info()` and `describe()` output of a farm survey dataset. List the data-quality problems I should check before any analysis, and say which output line points to each one."*

    Then **check each claim with code** in the cells below. AI can be confidently wrong. Your thesis is your responsibility.

    🔒 **Never paste confidential, personal, or unpublished data into a public AI tool.** Summaries like `info()` are usually safe. Raw participant records are not.
    """),

    md("## 3. Data quality audit\n### 3.1 Missing values"),
    code("""
    missing = pd.DataFrame({
        "n_missing": df_raw.isna().sum(),
        "pct_missing": (df_raw.isna().mean() * 100).round(1),
    }).query("n_missing > 0").sort_values("pct_missing", ascending=False)
    missing
    """),
    md("### 3.2 Duplicates"),
    code("""
    print("Fully duplicated rows:", df_raw.duplicated().sum())
    print("Repeated farm IDs:    ", df_raw["farm_id"].duplicated().sum())
    """),
    md("### 3.3 Inconsistent categories\nThere are only **13** LGAs in Nasarawa State. How many does the data claim?"),
    code("""
    print(df_raw["lga"].nunique(), "distinct LGA values")
    df_raw["lga"].value_counts()
    """),
    code("""
    for col in ["improved_seed", "irrigation", "cooperative_member"]:
        print(col, df_raw[col].unique())
    """),
    md("### 3.4 Numbers stored as text\n`fertilizer_kg_per_ha` should be numeric, but `info()` says `object`. Why?"),
    code("""
    fert_as_number = pd.to_numeric(df_raw["fertilizer_kg_per_ha"], errors="coerce")
    df_raw.loc[fert_as_number.isna() & df_raw["fertilizer_kg_per_ha"].notna(), "fertilizer_kg_per_ha"].unique()
    """),
    md("### 3.5 Impossible values"),
    code("""
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))
    for ax, col in zip(axes, ["farmer_age", "farm_size_ha", "soil_ph"]):
        sns.boxplot(x=df_raw[col], ax=ax, color="#56B4E9")
        ax.set_title(col)
    plt.tight_layout()

    print("Ages outside 15-90:     ", (~df_raw["farmer_age"].between(15, 90) & df_raw["farmer_age"].notna()).sum())
    print("Farms larger than 50 ha:", (df_raw["farm_size_ha"] > 50).sum())
    """),
    md("""
    ### ✍️ Your turn: write a data cleaning log
    Examiners will ask *"what did you do to the data?"*. Write your answer **now**, while you remember. Edit this cell:

    | # | Problem found | How many rows | Decision | Reason |
    |---|---|---|---|---|
    | 1 | Duplicate rows | ? | Drop | Same farm entered twice |
    | 2 | LGA spelling variants | ? | Map to official names | ... |
    | 3 | ... | | | |
    """),

    md("## 4. Clean the data, one step at a time"),
    code("""
    df = df_raw.copy()          # never change df_raw, so you can always compare

    before = len(df)
    df = df.drop_duplicates()
    print(f"Removed {before - len(df)} duplicate rows")
    """),
    code("""
    lga_fixes = {"Nasarawa-Eggon": "Nasarawa Eggon", "N/Eggon": "Nasarawa Eggon", "Nassarawa": "Nasarawa"}
    df["lga"] = df["lga"].str.strip().str.title().replace(lga_fixes)

    print(df["lga"].nunique(), "LGAs now")
    sorted(df["lga"].unique())
    """),
    code("""
    yes_no = {"yes": "Yes", "y": "Yes", "no": "No", "n": "No"}
    for col in ["improved_seed", "irrigation", "cooperative_member"]:
        df[col] = df[col].astype("string").str.strip().str.lower().map(yes_no)
        print(col, df[col].unique())
    """),
    code("""
    df["fertilizer_kg_per_ha"] = pd.to_numeric(df["fertilizer_kg_per_ha"], errors="coerce")
    df["fertilizer_kg_per_ha"].dtype
    """),
    code("""
    valid_ranges = {"farmer_age": (15, 90), "farm_size_ha": (0.05, 50), "soil_ph": (3.5, 9.5)}

    for col, (low, high) in valid_ranges.items():
        bad = ~df[col].between(low, high) & df[col].notna()
        print(f"{col}: {bad.sum()} impossible values set to missing")
        df.loc[~df[col].between(low, high), col] = np.nan
    """),
    code("""
    before = len(df)
    df = df.dropna(subset=["yield_kg_per_ha"]).reset_index(drop=True)
    print(f"Dropped {before - len(df)} rows with no yield recorded. {len(df)} rows remain.")
    """),
    md("""
    > **Why don't we fill in (impute) the other missing values here?**
    > If we filled `soil_ph` with the average of the *whole* dataset now, tomorrow's test data would leak into training. Imputation belongs **inside the modelling pipeline**, learned from training data only. We'll do this on Day 2.
    """),

    md("""
    ## 5. From notebook steps to a reusable function
    Copy-pasting cleaning code between notebooks causes errors. The same steps live in **`src/cleaning.py`** as `clean_farm_data()`. Open that file in VS Code and compare it with what you did above.

    Then we **test** that the function gives exactly the same result as our step-by-step work:
    """),
    code("""
    from src.cleaning import clean_farm_data, save_processed

    df_clean = clean_farm_data(df_raw)
    pd.testing.assert_frame_equal(df.reset_index(drop=True), df_clean)
    print("✅ Function output matches the step-by-step cleaning")

    path = save_processed(df_clean)
    print("Saved:", path.relative_to(ROOT))
    """),
    md("""
    ### 💾 Git checkpoint 2
    ```bash
    git add notebooks/ src/
    git commit -m "Clean maize survey data; add cleaning log"
    git push
    ```
    Notice that `data/processed/` is listed in `.gitignore`, so it is **not** committed. Anyone can re-create it from the raw data and your code.
    """),

    md("## 6. Exploratory data analysis\n### 6.1 What does the outcome look like?"),
    code("""
    fig, ax = plt.subplots()
    sns.histplot(df_clean["yield_kg_per_ha"], bins=30, kde=True, ax=ax)
    ax.set(xlabel="Maize yield (kg/ha)", ylabel="Number of farms", title="Distribution of maize yield")
    df_clean["yield_kg_per_ha"].describe().round(0)
    """),
    md("### 6.2 Yield across LGAs"),
    code("""
    order = df_clean.groupby("lga")["yield_kg_per_ha"].median().sort_values().index

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=df_clean, y="lga", x="yield_kg_per_ha", order=order, color="#56B4E9", ax=ax)
    ax.set(xlabel="Maize yield (kg/ha)", ylabel="", title="Yield by Local Government Area")
    plt.show()
    """),
    md("### 6.3 Farm practices"),
    code("""
    summary = (df_clean
               .groupby(["improved_seed", "irrigation"])["yield_kg_per_ha"]
               .agg(n="count", mean="mean", median="median", sd="std")
               .round(0))
    summary
    """),
    code("""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    sns.scatterplot(data=df_clean, x="fertilizer_kg_per_ha", y="yield_kg_per_ha", hue="improved_seed", alpha=0.6, ax=axes[0])
    axes[0].set(xlabel="Fertiliser (kg/ha)", ylabel="Yield (kg/ha)", title="Fertiliser vs yield")
    sns.scatterplot(data=df_clean, x="rainfall_mm", y="yield_kg_per_ha", alpha=0.5, ax=axes[1])
    axes[1].set(xlabel="Seasonal rainfall (mm)", title="Rainfall vs yield")
    plt.tight_layout()
    """),
    md("### 6.4 Correlations between numeric variables"),
    code("""
    corr = df_clean.select_dtypes("number").drop(columns="survey_year").corr()

    fig, ax = plt.subplots(figsize=(8, 6.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1, ax=ax, annot_kws={"size": 8})
    ax.set_title("Correlation matrix")
    plt.show()
    """),
    md("""
    🔎 **Look closely:** `harvest_sales_naira` is strongly related to yield. Is it a useful *predictor*, or is it *calculated from* yield? Keep this in mind for Day 2.
    """),

    md("""
    ### 🤖 AI exercise 2: let AI write the code, and you check it
    1. Ask: *"Using pandas and seaborn, write code to plot mean maize yield by `pest_incidence` with 95% confidence intervals. Order the categories Absent, Low, Moderate, High. My DataFrame is `df_clean`."*
    2. Paste the code below and run it.
    3. Ask the AI: *"Explain this code line by line"*. Do you understand **every** line?
    4. Check the result: does the chart agree with `df_clean.groupby("pest_incidence")["yield_kg_per_ha"].mean()`?

    If you use VS Code with **GitHub Copilot**, try typing a comment such as `# plot mean yield by pest incidence` and pressing Enter.
    """),
    code("# 🤖 Paste and test the AI-generated code here\n"),

    md("""
    ## ✍️ Exercises
    1. Which LGA has the **highest median yield**? Is the difference large compared with the spread *within* LGAs?
    2. Do cooperative members get more `extension_visits`? Show it with a table **and** a chart.
    3. Save your best chart to `figures/` using `save_figure(fig, "my_chart_name")`.
    4. **Bonus:** what percentage of farms use *both* improved seed and irrigation?
    """),
    code("# 1.\n"),
    code("# 2.\n"),
    code("# 3.\n"),

    md("""
    ## Summary and homework
    Today you set up a reproducible project, audited and cleaned data, packaged the cleaning as a tested function, explored the data, and used AI with checking.

    ### 💾 Final commit for Day 1
    ```bash
    git add .
    git commit -m "Day 1: data audit, cleaning and EDA"
    git push
    ```
    Then open your repository on github.com and check that your work is there.

    **For tomorrow:** if you have your own research dataset (non-confidential), bring it as a CSV or Excel file. You will use it in the mini-project.
    """),
]

# =============================================================================
# DAY 2
# =============================================================================
DAY2 = [
    md("""
    # Day 2: Analysis, machine learning and a Streamlit app
    **Python for Data Science in Academic Research, with AI, VS Code & GitHub**
    Nasarawa State University, Keffi · Saturday 31 October 2026 · 10:00 am – 2:00 pm

    ### By the end of today you will be able to
    1. Test a hypothesis and report **effect sizes and confidence intervals**, not just p-values
    2. Fit and interpret a **regression model** with statsmodels and check its assumptions
    3. Build a **leak-free machine-learning pipeline** in scikit-learn and evaluate it honestly
    4. Produce **publication-ready figures and tables**
    5. Turn your model into an interactive **Streamlit app**
    6. Write an **AI-use statement** for your thesis or paper

    Symbols: 🤖 AI exercise · ✍️ your turn · 💾 Git checkpoint

    ### 💾 Start with a sync
    ```bash
    git pull
    ```
    """),
    code(SETUP_CODE),
    code("""
    from src.cleaning import load_processed, TARGET

    df = load_processed()          # re-creates the clean file from raw data if it's missing
    print(df.shape)
    df.head()
    """),

    md("""
    ## 1. Start from a research question
    > **RQ:** Which farm practices are associated with higher maize yield among smallholder farmers in Nasarawa State?
    >
    > **H1:** Farms that use improved seed have a higher mean yield than farms that do not.

    A clear question decides the method. *Explaining* (statistics) and *predicting* (machine learning) are different goals, and today we do both.
    """),

    md("## 2. Hypothesis test: improved seed vs local seed"),
    code("""
    from scipy import stats

    improved = df.loc[df["improved_seed"] == "Yes", TARGET]
    local = df.loc[df["improved_seed"] == "No", TARGET]

    t, p = stats.ttest_ind(improved, local, equal_var=False)       # Welch's t-test

    diff = improved.mean() - local.mean()
    se = np.sqrt(improved.var() / len(improved) + local.var() / len(local))
    ci_low, ci_high = diff - 1.96 * se, diff + 1.96 * se
    pooled_sd = np.sqrt((improved.var() + local.var()) / 2)
    cohens_d = diff / pooled_sd

    print(f"Improved seed: n = {len(improved)}, mean = {improved.mean():,.0f} kg/ha")
    print(f"Local seed:    n = {len(local)}, mean = {local.mean():,.0f} kg/ha")
    print(f"Difference = {diff:,.0f} kg/ha (95% CI {ci_low:,.0f} to {ci_high:,.0f}), "
          f"Welch t = {t:.2f}, p = {p:.3g}, Cohen's d = {cohens_d:.2f}")
    """),
    md("""
    **How to report it (APA style):**
    > Farms using improved seed had a higher mean yield than farms using local seed (difference = *X* kg/ha, 95% CI [*a*, *b*]), Welch's *t* = *…*, *p* < .001, Cohen's *d* = *…*.

    Reviewers want to know **how big** the effect is (effect size and CI), not only whether *p* < 0.05.

    ⚠️ This is an *association*. Farmers who buy improved seed may also differ in other ways, such as fertiliser use or cooperative membership. Regression helps us adjust for that.
    """),

    md("## 3. Multiple regression with statsmodels"),
    code("""
    import statsmodels.formula.api as smf

    formula = (
        "yield_kg_per_ha ~ fertilizer_kg_per_ha + rainfall_mm + soil_ph + extension_visits"
        " + C(improved_seed, Treatment('No')) + C(irrigation, Treatment('No'))"
        " + C(pest_incidence, Treatment('Absent')) + C(education_level, Treatment('No formal education'))"
    )
    ols = smf.ols(formula, data=df).fit()
    print(f"Rows used: {int(ols.nobs)} of {len(df)} (rows with missing values are dropped, so report this!)")
    ols.summary()
    """),
    md("### A tidy coefficient table for your thesis"),
    code("""
    coef_table = pd.DataFrame({
        "coef": ols.params,
        "ci_low": ols.conf_int()[0],
        "ci_high": ols.conf_int()[1],
        "p_value": ols.pvalues,
    }).round(3)

    RESULTS_DIR = ROOT / "results"
    RESULTS_DIR.mkdir(exist_ok=True)
    coef_table.to_csv(RESULTS_DIR / "table2_regression_coefficients.csv")
    coef_table
    """),
    md("### Check the assumptions before you believe the results"),
    code("""
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    axes[0].scatter(ols.fittedvalues, ols.resid, alpha=0.4)
    axes[0].axhline(0, color="black", lw=1)
    axes[0].set(xlabel="Fitted values", ylabel="Residuals", title="Residuals vs fitted")
    stats.probplot(ols.resid, dist="norm", plot=axes[1])
    axes[1].set_title("Normal Q-Q plot of residuals")
    plt.tight_layout()
    """),
    md("""
    Look for a **curve** in *residuals vs fitted*: it suggests a relationship that isn't a straight line. (Hint: is yield really a straight-line function of rainfall?)

    ### 🤖 AI exercise 3: interpret, then verify
    Paste the coefficient table (not the data) into your AI assistant:
    > *"Interpret this regression table for the results chapter of an MSc thesis in plain academic English. The outcome is maize yield in kg/ha. Mention the direction, size and confidence interval of each statistically significant effect, and state the limitations of observational data."*

    ✅ **Check every number** in the AI's paragraph against the table above. AI tools often get signs or units wrong and overstate causality.
    """),
    md("""
    ### ✍️ Your turn
    Add a squared rainfall term, `+ I((rainfall_mm - 1150)**2)`, to the formula. Does adjusted R² improve? Does the residual plot look better?
    """),
    code("# ✍️ Your improved model here\n"),

    md("""
    ## 4. Machine learning: can we *predict* yield for a new farm?
    ### 4.1 Hold out a test set first
    The test set is locked away until the very end. Every decision (model choice, settings) uses the training set only.
    """),
    code("""
    from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, KFold
    from sklearn.pipeline import Pipeline
    from sklearn.dummy import DummyRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor

    from src.modelling import (FEATURES, NUMERIC_FEATURES, CATEGORICAL_FEATURES, RANDOM_STATE,
                               build_preprocessor, regression_metrics, save_model)

    X, y = df[FEATURES], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)
    print(f"Train: {len(X_train)} farms   Test: {len(X_test)} farms")
    print("Numeric features:    ", NUMERIC_FEATURES)
    print("Categorical features:", CATEGORICAL_FEATURES)
    """),
    md("""
    ### 4.2 A *pipeline* keeps preprocessing inside cross-validation
    `build_preprocessor()` (in `src/modelling.py`) fills missing values, scales the numbers and one-hot encodes the categories. Because it sits **inside** the pipeline, those steps are re-learned on each training fold, so there is no leakage.
    """),
    code("""
    candidates = {
        "Baseline (predict the mean)": DummyRegressor(),
        "Linear regression": LinearRegression(),
        "Random forest": RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=RANDOM_STATE, n_jobs=-1),
        "Gradient boosting": HistGradientBoostingRegressor(random_state=RANDOM_STATE),
    }
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    rows = []
    for name, model in candidates.items():
        pipe = Pipeline([("preprocess", build_preprocessor()), ("model", model)])
        scores = cross_validate(pipe, X_train, y_train, cv=cv,
                                scoring=["r2", "neg_mean_absolute_error"])
        rows.append({"model": name,
                     "R2 (mean)": scores["test_r2"].mean(), "R2 (sd)": scores["test_r2"].std(),
                     "MAE (mean)": -scores["test_neg_mean_absolute_error"].mean()})

    cv_results = pd.DataFrame(rows).set_index("model").round(3)
    cv_results.to_csv(RESULTS_DIR / "table3_model_comparison_cv.csv")
    cv_results
    """),
    md("""
    Always include a **baseline**. A model is only useful if it clearly beats "just predict the average".

    ### 4.3 ⚠️ The leakage trap
    A colleague says: *"Add `harvest_sales_naira` divided by farm size, called sales per hectare. It makes the model much better!"* Let's see:
    """),
    code("""
    leaky = X_train.copy()
    leaky["sales_per_ha"] = df.loc[X_train.index, "harvest_sales_naira"] / df.loc[X_train.index, "farm_size_ha"]

    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder

    leaky_pipe = Pipeline([
        ("preprocess", ColumnTransformer([
            ("num", SimpleImputer(strategy="median"), NUMERIC_FEATURES + ["sales_per_ha"]),
            ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                              ("encode", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL_FEATURES),
        ])),
        ("model", RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=RANDOM_STATE, n_jobs=-1)),
    ])
    leaky_r2 = cross_val_score(leaky_pipe, leaky, y_train, cv=cv, scoring="r2").mean()
    print(f"R² WITH the leaky feature: {leaky_r2:.3f}   (looks amazing...)")
    print(f"R² without it:             {cv_results.loc['Random forest', 'R2 (mean)']:.3f}")
    """),
    md("""
    Sales are only known **after** harvest, and they are calculated from yield (sales = yield × area × price). The "amazing" model is useless for predicting a farm's yield in advance. **If a result looks too good to be true, check for leakage.** Common sources in research data are post-outcome variables, duplicate subjects across train and test, and scaling or imputing before splitting.

    ### 4.4 Final evaluation on the untouched test set
    """),
    code("""
    best_name = cv_results["R2 (mean)"].idxmax()
    final_pipeline = Pipeline([("preprocess", build_preprocessor()), ("model", candidates[best_name])])
    final_pipeline.fit(X_train, y_train)

    y_pred = final_pipeline.predict(X_test)
    test_metrics = regression_metrics(y_test, y_pred)
    print(f"Chosen model: {best_name}")
    print({k: round(v, 3) for k, v in test_metrics.items()})
    """),
    code("""
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(y_test, y_pred, alpha=0.6)
    lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
    ax.plot(lims, lims, color="black", lw=1, ls="--", label="Perfect prediction")
    ax.set(xlabel="Actual yield (kg/ha)", ylabel="Predicted yield (kg/ha)",
           title=f"{best_name}: test R² = {test_metrics['R2']:.2f}")
    ax.legend()
    save_figure(fig, "fig3_predicted_vs_actual")
    plt.show()
    """),
    md("### 4.5 Which features matter? (permutation importance)"),
    code("""
    from sklearn.inspection import permutation_importance

    perm = permutation_importance(final_pipeline, X_test, y_test, n_repeats=10, random_state=RANDOM_STATE, n_jobs=-1)
    importance = (pd.DataFrame({"feature": FEATURES, "importance": perm.importances_mean, "sd": perm.importances_std})
                  .sort_values("importance"))

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.barh(importance["feature"], importance["importance"], xerr=importance["sd"], color="#0072B2")
    ax.set(xlabel="Drop in R² when the feature is shuffled", title="Permutation feature importance (test set)")
    save_figure(fig, "fig4_feature_importance")
    plt.show()
    """),
    md("""
    ⚠️ *Important to the model* does **not** mean *causes yield*. Importance describes the model, not the world.
    """),

    md("""
    ## 5. A publication-ready figure
    A **coefficient (forest) plot** is often clearer than a long regression table. The code below uses the style from `src/plotting.py`: 300 dpi, a colour-blind-safe palette, labelled axes with units, and PNG for Word plus PDF for LaTeX.
    """),
    code("""
    plot_df = coef_table.drop(index="Intercept").copy()
    plot_df.index = (plot_df.index
                     .str.replace(r"C\\((\\w+), Treatment\\('\\w+'\\)\\)\\[T\\.(.+)\\]", r"\\1 = \\2", regex=True)
                     .str.replace("_", " "))
    plot_df = plot_df.sort_values("coef")

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.errorbar(plot_df["coef"], plot_df.index, xerr=[plot_df["coef"] - plot_df["ci_low"], plot_df["ci_high"] - plot_df["coef"]],
                fmt="o", color="#0072B2", ecolor="#56B4E9", capsize=3)
    ax.axvline(0, color="black", lw=1)
    ax.set(xlabel="Change in yield (kg/ha), 95% CI", title="Factors associated with maize yield")
    save_figure(fig, "fig2_regression_coefficients")
    plt.show()
    """),
    md("""
    > Note: continuous variables such as rainfall are "per 1 mm", so their bars look tiny. For your paper, consider rescaling (e.g. per 100 mm) so the effects can be compared.
    """),

    md("## 6. Save the model and its model card"),
    code("""
    save_model(final_pipeline, test_metrics, X_train, notes=f"Chosen by 5-fold CV in notebook 02 ({best_name})")
    print((ROOT / "models" / "model_card.json").read_text()[:600], "...")
    """),

    md("""
    ## 7. 🚀 Demo your model with Streamlit
    In the VS Code terminal, from the **repository root**, run:
    ```bash
    streamlit run app/streamlit_app.py
    ```
    Your browser opens the app. Try it:
    - **Predict one farm**: change the inputs and see the predicted yield and the fertiliser "what if" curve
    - **Predict from a CSV file**: upload `data/raw/nasarawa_maize_survey_synthetic.csv`
    - **About the model**: the model card, so users know what the model can and cannot do

    Open `app/streamlit_app.py`. It is about 120 lines of plain Python, and every `st.something(...)` call adds one element to the page.

    ### 🤖 AI exercise 4: extend the app
    Ask your AI assistant (or Copilot Chat in VS Code, with the file open):
    > *"In this Streamlit app, add a new tab called 'Explore data' that shows a bar chart of the average yield by LGA from `get_training_data()`, with a selectbox to choose between mean and median."*

    Save the file. Streamlit reloads automatically. Does it work? Do you understand the code it added?

    **Share it (optional):** push the repo to GitHub, then deploy for free at [share.streamlit.io](https://share.streamlit.io) (Community Cloud) and paste the link in your README.
    """),

    md("""
    ## 8. ✍️ Mini-project: your own data
    1. Put your dataset in `data/raw/` (non-confidential only, or add its file name to `.gitignore`)
    2. Copy `01_day1_clean_and_explore.ipynb` and adapt the audit and cleaning for your data
    3. State **one research question** and answer it with a test or regression **and** a figure
    4. *Stretch:* train a model, save it with `save_model(...)`, update the feature lists in `src/modelling.py` and run the app
    5. Update `README.md`: question, data source, how to run, key finding

    ## 9. Responsible AI and finishing your write-up
    - Fill in `docs/AI_USE_STATEMENT_TEMPLATE.md` and keep it with your thesis
    - Work through `docs/REPRODUCIBILITY_CHECKLIST.md`
    - **Never** let AI write citations for you without checking each one. AI tools invent references that look real.

    ### 💾 Final commit
    ```bash
    git add .
    git commit -m "Day 2: analysis, model and Streamlit app"
    git push
    ```
    🎓 **Optional:** connect the repository to [Zenodo](https://zenodo.org) and make a GitHub *release* to get a citable **DOI** for your code.
    """),
]


def write(cells, name):
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    NOTEBOOK_DIR.mkdir(exist_ok=True)
    path = NOTEBOOK_DIR / name
    nbf.write(nb, path)
    print("Wrote", path)


if __name__ == "__main__":
    write(DAY1, "01_day1_clean_and_explore.ipynb")
    write(DAY2, "02_day2_analyse_model_app.ipynb")
