"""
Generate the workshop's SYNTHETIC sample dataset.

The data imitates a smallholder maize farm survey across the 13 LGAs of
Nasarawa State. It is NOT real survey data - every value is simulated - so it
must never be cited as evidence about real farms.

Problems are injected on purpose so participants can practise cleaning:
  * inconsistent text (lowercase, trailing spaces, spelling variants)
  * Yes/No columns written several different ways
  * a numeric column stored as text, with "not recorded" entries
  * missing values, impossible values (age 150, 250 ha farms) and duplicates
  * a "leaky" column (harvest_sales_naira) that is computed from the target

Run from the repository root:
    python scripts/make_sample_data.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026
N_FARMS = 640
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "nasarawa_maize_survey_synthetic.csv"

LGAS = [
    "Akwanga", "Awe", "Doma", "Karu", "Keana", "Keffi", "Kokona",
    "Lafia", "Nasarawa", "Nasarawa Eggon", "Obi", "Toto", "Wamba",
]


def simulate(rng: np.random.Generator) -> pd.DataFrame:
    n = N_FARMS
    lga = rng.choice(LGAS, size=n)
    lga_effect = dict(zip(LGAS, rng.normal(0, 180, size=len(LGAS))))

    farmer_age = rng.normal(43, 11, n).clip(18, 80).round()
    years_farming = (farmer_age - 18 - rng.integers(0, 15, n)).clip(1, None)
    education = rng.choice(["No formal education", "Primary", "Secondary", "Tertiary"], n, p=[0.18, 0.32, 0.35, 0.15])
    gender = rng.choice(["Male", "Female"], n, p=[0.68, 0.32])
    farm_size = rng.lognormal(mean=0.6, sigma=0.55, size=n).round(2)
    improved_seed = rng.random(n) < 0.48
    irrigation = rng.random(n) < 0.17
    cooperative = rng.random(n) < 0.41
    extension_visits = rng.poisson(1.0 + 1.6 * cooperative, n)
    fertilizer = (rng.gamma(4, 28, n) + 35 * cooperative).round(1)
    rainfall = rng.normal(1180, 190, n).round(1)
    avg_temp = rng.normal(27.4, 1.1, n).round(1)
    soil_ph = rng.normal(6.1, 0.55, n).round(2)
    pest = rng.choice(["Absent", "Low", "Moderate", "High"], n, p=[0.25, 0.4, 0.25, 0.1])
    year = rng.choice([2022, 2023, 2024], n)

    pest_penalty = pd.Series(pest).map({"Absent": 0, "Low": 120, "Moderate": 380, "High": 750}).to_numpy()
    edu_bonus = pd.Series(education).map({"No formal education": 0, "Primary": 60, "Secondary": 120, "Tertiary": 170}).to_numpy()

    yield_kg = (
        1500
        + 6.5 * np.minimum(fertilizer, 220)            # diminishing returns above 220 kg/ha
        - 0.0035 * (rainfall - 1150) ** 2              # too little or too much rain hurts
        + 520 * improved_seed
        + 310 * irrigation
        + 65 * extension_visits
        - 420 * (soil_ph - 6.3) ** 2
        - 55 * (avg_temp - 27) ** 2
        + 4 * np.minimum(years_farming, 25)
        + edu_bonus
        - pest_penalty
        + np.array([lga_effect[x] for x in lga])
        + rng.normal(0, 340, n)
    ).clip(250).round(0)

    price_per_kg = rng.normal(420, 35, n)  # naira per kg, varies by market
    harvest_sales = (yield_kg * farm_size * price_per_kg).round(-2)

    return pd.DataFrame({
        "farm_id": [f"NSW-{i:04d}" for i in range(1, n + 1)],
        "survey_year": year,
        "lga": lga,
        "farmer_age": farmer_age,
        "gender": gender,
        "education_level": education,
        "years_farming": years_farming,
        "farm_size_ha": farm_size,
        "improved_seed": np.where(improved_seed, "Yes", "No"),
        "fertilizer_kg_per_ha": fertilizer,
        "irrigation": np.where(irrigation, "Yes", "No"),
        "rainfall_mm": rainfall,
        "avg_temp_c": avg_temp,
        "soil_ph": soil_ph,
        "extension_visits": extension_visits,
        "pest_incidence": pest,
        "cooperative_member": np.where(cooperative, "Yes", "No"),
        "harvest_sales_naira": harvest_sales,
        "yield_kg_per_ha": yield_kg,
    })


def make_messy(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    df = df.copy()
    n = len(df)

    def pick(frac):
        return rng.choice(n, size=int(frac * n), replace=False)

    # Inconsistent LGA spellings
    for i in pick(0.06):
        df.loc[i, "lga"] = df.loc[i, "lga"].lower()
    for i in pick(0.04):
        df.loc[i, "lga"] = df.loc[i, "lga"] + " "
    df.loc[df["lga"] == "Nasarawa Eggon", "lga"] = rng.choice(
        ["Nasarawa Eggon", "Nasarawa-Eggon", "N/Eggon"], size=(df["lga"] == "Nasarawa Eggon").sum(), p=[0.7, 0.2, 0.1]
    )
    df.loc[df["lga"] == "Nasarawa", "lga"] = rng.choice(
        ["Nasarawa", "Nassarawa"], size=(df["lga"] == "Nasarawa").sum(), p=[0.85, 0.15]
    )

    # Yes/No written many ways
    variants = {"Yes": ["Yes", "yes", "Y", "YES"], "No": ["No", "no", "N", "NO"]}
    for col in ["improved_seed", "irrigation", "cooperative_member"]:
        for i in pick(0.15):
            df.loc[i, col] = rng.choice(variants[df.loc[i, col]])

    # Numbers stored as text
    df["fertilizer_kg_per_ha"] = df["fertilizer_kg_per_ha"].astype(object)
    for i in pick(0.03):
        df.loc[i, "fertilizer_kg_per_ha"] = "not recorded"

    # Missing values
    for col, frac in [("soil_ph", 0.07), ("rainfall_mm", 0.04), ("farmer_age", 0.03),
                      ("extension_visits", 0.05), ("education_level", 0.02), ("yield_kg_per_ha", 0.015)]:
        df.loc[pick(frac), col] = np.nan

    # Impossible values (data-entry errors)
    df.loc[pick(0.004), "farmer_age"] = 150
    df.loc[pick(0.003), "farmer_age"] = 7
    for i in pick(0.006):
        df.loc[i, "farm_size_ha"] = df.loc[i, "farm_size_ha"] * 100  # decimal point slipped

    # Duplicated survey entries
    dupes = df.sample(10, random_state=SEED)
    df = pd.concat([df, dupes], ignore_index=True)
    return df.sample(frac=1, random_state=SEED).reset_index(drop=True)


def main() -> None:
    rng = np.random.default_rng(SEED)
    df = make_messy(simulate(rng), rng)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print(f"Wrote {len(df)} rows x {df.shape[1]} columns to {OUT_PATH}")


if __name__ == "__main__":
    main()
