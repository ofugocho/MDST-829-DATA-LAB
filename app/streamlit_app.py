"""
Maize Yield Predictor - a Streamlit demo of the model trained on Day 2.

Run from the repository root:
    streamlit run app/streamlit_app.py

To demo YOUR OWN model: save it with src.modelling.save_model(...) and update
the feature lists in src/modelling.py. The input widgets are built
automatically from models/model_card.json.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.cleaning import clean_farm_data, load_processed  # noqa: E402
from src.modelling import FEATURES, MODEL_PATH, load_model, train_and_save  # noqa: E402

st.set_page_config(page_title="Maize Yield Predictor", page_icon="🌽", layout="wide")


@st.cache_resource
def get_model():
    return load_model()


@st.cache_data
def get_training_data():
    return load_processed()


st.title("🌽 Maize Yield Predictor")
st.caption(
    "Workshop demo · Nasarawa State University, Keffi · "
    "Trained on **synthetic** data for teaching, so do not use for real decisions."
)

if not MODEL_PATH.exists():
    st.warning("No trained model found. Run the Day 2 notebook, or train the default model now.")
    if st.button("Train default model"):
        with st.spinner("Training..."):
            train_and_save()
        st.cache_resource.clear()
        st.rerun()
    st.stop()

model, card = get_model()

tab_single, tab_batch, tab_about = st.tabs(["Predict one farm", "Predict from a CSV file", "About the model"])

# --- Single prediction -------------------------------------------------------
with tab_single:
    st.subheader("Describe the farm")
    inputs = {}
    with st.form("farm_inputs"):
        cols = st.columns(3)
        for i, col in enumerate(card["numeric_features"]):
            low, median, high = card["numeric_ranges"][col]
            step = 1.0 if high - low > 20 else 0.1
            inputs[col] = cols[i % 3].number_input(
                col.replace("_", " ").capitalize(), min_value=float(low), max_value=float(high),
                value=float(round(median, 1)), step=step,
            )
        cols = st.columns(3)
        for i, col in enumerate(card["categorical_features"]):
            inputs[col] = cols[i % 3].selectbox(col.replace("_", " ").capitalize(), card["categories"][col])
        submitted = st.form_submit_button("Predict yield", type="primary")

    if submitted:
        farm = pd.DataFrame([inputs])
        prediction = float(model.predict(farm)[0])
        average = float(get_training_data()[card["target"]].mean())

        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted yield", f"{prediction:,.0f} kg/ha", f"{prediction - average:+,.0f} vs average")
        c2.metric("Expected harvest for this farm", f"{prediction * inputs['farm_size_ha'] / 1000:,.2f} tonnes")
        c3.metric("Typical error (test MAE)", f"± {card['test_metrics']['MAE']:,.0f} kg/ha")

        st.markdown("#### What if this farm used a different amount of fertiliser?")
        low, _, high = card["numeric_ranges"]["fertilizer_kg_per_ha"]
        grid = pd.DataFrame([inputs] * 40)
        grid["fertilizer_kg_per_ha"] = pd.Series(range(40)) * (high - low) / 39 + low
        grid["predicted_yield"] = model.predict(grid[FEATURES])
        st.line_chart(grid, x="fertilizer_kg_per_ha", y="predicted_yield")
        st.caption("All other inputs are held fixed. This shows what the model learned. It does not prove cause and effect.")

# --- Batch prediction --------------------------------------------------------
with tab_batch:
    st.subheader("Upload farms to score")
    st.write(f"The CSV needs these columns: `{', '.join(FEATURES)}`. The same cleaning as Day 1 is applied first.")
    uploaded = st.file_uploader("CSV file", type="csv")
    if uploaded is not None:
        new = clean_farm_data(pd.read_csv(uploaded), require_target=False)
        missing = [c for c in FEATURES if c not in new.columns]
        if missing:
            st.error(f"These columns are missing: {missing}")
        else:
            new["predicted_yield_kg_per_ha"] = model.predict(new[FEATURES]).round(0)
            st.dataframe(new, width="stretch")
            st.download_button(
                "Download predictions", new.to_csv(index=False).encode(), "predictions.csv", "text/csv"
            )
    else:
        st.info("Tip: try uploading data/raw/nasarawa_maize_survey_synthetic.csv")

# --- Model card --------------------------------------------------------------
with tab_about:
    st.subheader("Model card")
    m = card["test_metrics"]
    c1, c2, c3 = st.columns(3)
    c1.metric("R² (test set)", f"{m['R2']:.2f}")
    c2.metric("MAE", f"{m['MAE']:,.0f} kg/ha")
    c3.metric("RMSE", f"{m['RMSE']:,.0f} kg/ha")
    st.write(
        f"**Model:** {card['model']} · **Trained on:** {card['n_training_rows']} farms · "
        f"**Trained at:** {card['trained_at']} · scikit-learn {card['scikit_learn']}"
    )
    st.warning(card["data_note"])
    with st.expander("Full model card (models/model_card.json)"):
        st.json(card)
