from src.data_loader import load_raw_data
from src.data_cleaning import (
    standardize_timestamp,
    sort_by_timestamp,
    calculate_time_gaps,
    find_time_gaps
)
from src.data_cleaning import (
    standardize_timestamp,
    sort_by_timestamp,
    calculate_time_gaps,
    find_time_gaps,
    identify_non_numeric_values,
    get_non_numeric_values
)


# Load raw data
df = load_raw_data(
    "data/raw/Data (4).csv"
)

print("Raw shape:", df.shape)


# Standardize timestamp
df = standardize_timestamp(df)

print(
    "Unparseable timestamps:",
    df["timestamp"].isna().sum()
)


# Sort chronologically
df = sort_by_timestamp(df)

print(
    "Chronologically sorted:",
    df["timestamp"].is_monotonic_increasing
)


# Calculate intervals
df = calculate_time_gaps(df)

print("\nMost common intervals:")
print(
    df["time_diff"]
    .value_counts()
    .head(10)
)


# Find gaps
gaps = find_time_gaps(df)

print("\nDetected gaps:")
print(gaps)

SENSOR_COLS = [
    "Cyclone_Inlet_Gas_Temp",
    "Cyclone_Material_Temp",
    "Cyclone_Outlet_Gas_draft",
    "Cyclone_cone_draft",
    "Cyclone_Gas_Outlet_Temp",
    "Cyclone_Inlet_Draft"
]

print("\nNon-numeric summary:")
print(
    identify_non_numeric_values(
        df,
        SENSOR_COLS
    )
)

print("\nActual non-numeric values:")

non_numeric_values = get_non_numeric_values(
    df,
    SENSOR_COLS
)

for column, values in non_numeric_values.items():
    print(f"\n{column}:")
    print(values)

print("\nComplete non-numeric summary:")
summary = identify_non_numeric_values(
    df,
    SENSOR_COLS
)

print(summary.to_string(index=False))

from src.data_cleaning import (
    standardize_timestamp,
    sort_by_timestamp,
    calculate_time_gaps,
    find_time_gaps,
    identify_non_numeric_values,
    get_non_numeric_values,
    convert_sensor_columns_to_numeric,
    get_invalid_sensor_mask,
)

df_numeric = convert_sensor_columns_to_numeric(
    df,
    SENSOR_COLS
)

print("\nData types after conversion:")
print(df_numeric[SENSOR_COLS].dtypes)

print("\nMissing values after conversion:")
print(df_numeric[SENSOR_COLS].isna().sum())

invalid_mask = get_invalid_sensor_mask(df, SENSOR_COLS)

print("\nRows with at least one invalid sensor:", invalid_mask.sum())
print("Percentage of rows:", invalid_mask.mean() * 100)