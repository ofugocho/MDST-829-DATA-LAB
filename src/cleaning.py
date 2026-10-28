"""
Reusable cleaning steps for the Nasarawa maize survey data.

On Day 1 we clean the data step by step in a notebook. Once the steps work,
we move them here as a function, so that the Day 2 notebook and the Streamlit
app all use exactly the same cleaning. That makes the work reproducible.

Usage:
    from src.cleaning import load_raw, clean_farm_data
    df = clean_farm_data(load_raw())
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "nasarawa_maize_survey_synthetic.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "maize_survey_clean.csv"

TARGET = "yield_kg_per_ha"
YES_NO_COLUMNS = ["improved_seed", "irrigation", "cooperative_member"]

# Spelling variants found in the raw data -> the official LGA name
LGA_FIXES = {
    "Nasarawa-Eggon": "Nasarawa Eggon",
    "N/Eggon": "Nasarawa Eggon",
    "Nassarawa": "Nasarawa",
}

# Values outside these ranges are data-entry errors, not real observations
VALID_RANGES = {
    "farmer_age": (15, 90),
    "farm_size_ha": (0.05, 50),
    "soil_ph": (3.5, 9.5),
}


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def standardise_yes_no(series: pd.Series) -> pd.Series:
    mapping = {"yes": "Yes", "y": "Yes", "no": "No", "n": "No"}
    return series.astype("string").str.strip().str.lower().map(mapping)


def clean_farm_data(df: pd.DataFrame, require_target: bool = True) -> pd.DataFrame:
    """Fix errors in the raw survey. Does NOT fill in missing values.

    Imputation is left to the modelling pipeline on Day 2, so that it is
    learned from the training data only (filling in values using the whole
    dataset before splitting leaks information from the test set).

    Set require_target=False for new data that has no yield yet (e.g. a CSV
    uploaded to the Streamlit app for prediction).
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    df = df.drop_duplicates()

    df["lga"] = df["lga"].str.strip().str.title().replace(LGA_FIXES)

    for col in YES_NO_COLUMNS:
        if col in df:
            df[col] = standardise_yes_no(df[col])

    if "fertilizer_kg_per_ha" in df:
        df["fertilizer_kg_per_ha"] = pd.to_numeric(df["fertilizer_kg_per_ha"], errors="coerce")

    for col, (low, high) in VALID_RANGES.items():
        if col in df:
            df.loc[~df[col].between(low, high), col] = np.nan

    # Rows without the outcome cannot be used for analysis
    if require_target:
        df = df.dropna(subset=[TARGET])

    return df.reset_index(drop=True)


def save_processed(df: pd.DataFrame, path: Path = PROCESSED_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def load_processed() -> pd.DataFrame:
    """Load the cleaned data, creating it from the raw file if needed."""
    if not PROCESSED_PATH.exists():
        save_processed(clean_farm_data(load_raw()))
    return pd.read_csv(PROCESSED_PATH)
