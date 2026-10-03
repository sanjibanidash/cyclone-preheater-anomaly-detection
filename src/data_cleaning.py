import pandas as pd


def standardize_timestamp(
    df: pd.DataFrame,
    time_col: str = "time"
) -> pd.DataFrame:
    """
    Convert the raw timestamp column into a standardized datetime column.
    """

    df = df.copy()

    df["timestamp"] = pd.to_datetime(
        df[time_col],
        format="mixed",
        errors="coerce"
    )

    return df


def sort_by_timestamp(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp"
) -> pd.DataFrame:
    """
    Sort observations chronologically.
    """

    df = df.copy()

    df = (
        df.sort_values(timestamp_col)
        .reset_index(drop=True)
    )

    return df


def calculate_time_gaps(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp"
) -> pd.DataFrame:
    """
    Calculate the time difference between consecutive observations.
    """

    df = df.copy()

    df["time_diff"] = df[timestamp_col].diff()

    return df


def find_time_gaps(
    df: pd.DataFrame,
    expected_minutes: int = 5,
    timestamp_col: str = "timestamp"
) -> pd.DataFrame:
    """
    Identify intervals larger than the expected sampling interval.
    """

    expected_interval = pd.Timedelta(
        minutes=expected_minutes
    )

    time_diff = df[timestamp_col].diff()

    gap_mask = time_diff > expected_interval

    gaps = df.loc[
        gap_mask,
        [timestamp_col]
    ].copy()

    gaps["previous_timestamp"] = (
        df[timestamp_col].shift(1)[gap_mask].values
    )

    gaps["gap_duration"] = (
        gaps[timestamp_col]
        - gaps["previous_timestamp"]
    )

    return gaps.reset_index(drop=True)

def identify_non_numeric_values(
    df: pd.DataFrame,
    sensor_cols: list[str]
) -> pd.DataFrame:
    """
    Identify non-numeric sensor observations.

    Returns a summary containing the number of values
    that cannot be converted to numeric for each sensor.
    """

    results = []

    for col in sensor_cols:
        converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        results.append({
            "column": col,
            "non_numeric_count": converted.isna().sum(),
            "non_numeric_percentage": (
                converted.isna().mean() * 100
            )
        })

    return pd.DataFrame(results)

def get_non_numeric_values(
    df: pd.DataFrame,
    sensor_cols: list[str]
) -> dict:
    """
    Return the unique non-numeric values found in each sensor.
    """

    non_numeric_values = {}

    for col in sensor_cols:
        converted = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        mask = converted.isna()

        non_numeric_values[col] = (
            df.loc[mask, col]
            .value_counts()
            .to_dict()
        )

    return non_numeric_values

def convert_sensor_columns_to_numeric(
    df: pd.DataFrame,
    sensor_cols: list[str]
) -> pd.DataFrame:
    """
    Convert sensor columns to numeric values.

    Non-numeric status strings are converted to NaN.
    The original dataframe is not modified.
    """

    df = df.copy()

    for col in sensor_cols:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    return df

def get_invalid_sensor_mask(
    df: pd.DataFrame,
    sensor_cols: list[str]
) -> pd.Series:
    """
    Identify rows where at least one sensor value
    is unavailable/non-numeric.
    """
    numeric_data = df[sensor_cols].apply(
        pd.to_numeric,
        errors="coerce"
    )

    return numeric_data.isna().any(axis=1)