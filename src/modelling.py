"""
Model building and saving, shared by the Day 2 notebook and the Streamlit app.

Train and save the default model from the command line (repository root):
    python -m src.modelling
"""

import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.cleaning import TARGET, load_processed

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "yield_model.joblib"
MODEL_CARD_PATH = ROOT / "models" / "model_card.json"

RANDOM_STATE = 42

NUMERIC_FEATURES = [
    "farmer_age", "years_farming", "farm_size_ha", "fertilizer_kg_per_ha",
    "rainfall_mm", "avg_temp_c", "soil_ph", "extension_visits",
]
CATEGORICAL_FEATURES = [
    "lga", "gender", "education_level", "improved_seed", "irrigation",
    "pest_incidence", "cooperative_member",
]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# harvest_sales_naira is calculated FROM the yield, so it must never be a feature
LEAKY_COLUMNS = ["harvest_sales_naira"]


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    categorical = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ])
    return ColumnTransformer([
        ("num", numeric, NUMERIC_FEATURES),
        ("cat", categorical, CATEGORICAL_FEATURES),
    ])


def build_pipeline(model=None) -> Pipeline:
    if model is None:
        model = RandomForestRegressor(n_estimators=300, min_samples_leaf=3, random_state=RANDOM_STATE, n_jobs=-1)
    return Pipeline([("preprocess", build_preprocessor()), ("model", model)])


def regression_metrics(y_true, y_pred) -> dict:
    return {
        "MAE": float(mean_absolute_error(y_true, y_pred)),
        "RMSE": float(root_mean_squared_error(y_true, y_pred)),
        "R2": float(r2_score(y_true, y_pred)),
    }


def save_model(pipeline: Pipeline, metrics: dict, training_data, notes: str = "") -> None:
    """Save the fitted pipeline plus a small 'model card' describing it."""
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    card = {
        "model": type(pipeline.named_steps["model"]).__name__,
        "target": TARGET,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "test_metrics": metrics,
        "n_training_rows": int(len(training_data)),
        # Ranges and categories seen in training, used to build the app's input widgets
        "numeric_ranges": {
            col: [float(np.nanmin(training_data[col])), float(np.nanmedian(training_data[col])),
                  float(np.nanmax(training_data[col]))]
            for col in NUMERIC_FEATURES
        },
        "categories": {
            col: sorted(training_data[col].dropna().astype(str).unique().tolist())
            for col in CATEGORICAL_FEATURES
        },
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "scikit_learn": sklearn.__version__,
        "data_note": "Trained on SYNTHETIC workshop data - for teaching only.",
        "notes": notes,
    }
    MODEL_CARD_PATH.write_text(json.dumps(card, indent=2))


def load_model():
    return joblib.load(MODEL_PATH), json.loads(MODEL_CARD_PATH.read_text())


def train_and_save() -> dict:
    df = load_processed()
    X, y = df[FEATURES], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE)

    pipeline = build_pipeline().fit(X_train, y_train)
    metrics = regression_metrics(y_test, pipeline.predict(X_test))
    save_model(pipeline, metrics, X_train, notes="Default model trained by src/modelling.py")
    return metrics


if __name__ == "__main__":
    print("Test-set metrics:", train_and_save())
