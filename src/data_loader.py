from pathlib import Path
import pandas as pd


def load_raw_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load the original cyclone preheater dataset.

    Parameters
    ----------
    file_path : str or Path
        Location of the raw CSV file.

    Returns
    -------
    pd.DataFrame
        Raw dataset.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    return df

