# Data

## `raw/nasarawa_maize_survey_synthetic.csv`

> ⚠️ **Synthetic data, for teaching only.** Every value is simulated by
> `scripts/make_sample_data.py` (fixed random seed 2026). It imitates a smallholder
> maize survey across the 13 LGAs of Nasarawa State. It is **not** real survey
> data and must not be cited as evidence about real farms.

The file contains **deliberate data-quality problems** for the Day 1 cleaning exercises:
duplicate rows, LGA spelling variants, Yes/No values written several ways, a numeric
column stored as text (`"not recorded"`), missing values, and impossible values such as an age of 150
or a 250 ha "smallholder" farm.

| Column | Type | Description |
|---|---|---|
| `farm_id` | text | Farm identifier |
| `survey_year` | integer | Season surveyed (2022–2024) |
| `lga` | category | Local Government Area |
| `farmer_age` | number | Age of the farmer (years) |
| `gender` | category | Male / Female |
| `education_level` | category | No formal education / Primary / Secondary / Tertiary |
| `years_farming` | number | Farming experience (years) |
| `farm_size_ha` | number | Maize area (hectares) |
| `improved_seed` | Yes/No | Used improved maize seed |
| `fertilizer_kg_per_ha` | number | Fertiliser applied (kg/ha) |
| `irrigation` | Yes/No | Any irrigation used |
| `rainfall_mm` | number | Seasonal rainfall (mm) |
| `avg_temp_c` | number | Mean growing-season temperature (°C) |
| `soil_ph` | number | Soil pH |
| `extension_visits` | integer | Visits from extension officers this season |
| `pest_incidence` | category | Absent / Low / Moderate / High |
| `cooperative_member` | Yes/No | Member of a farmers' cooperative |
| `harvest_sales_naira` | number | Money from the harvest (₦). **Calculated from yield, so it leaks the outcome** |
| `yield_kg_per_ha` | number | **Outcome**: maize yield (kg/ha) |

To regenerate the file: `python scripts/make_sample_data.py`

## `processed/`

Created by the notebooks (`src/cleaning.py`). It is not committed to Git because it can always be re-created.

## Using your own data

Put it in `raw/` and **never edit raw files by hand**. Do every change in code so it can be repeated.
If the data is confidential, add its file name to `.gitignore` **before** your next commit.
