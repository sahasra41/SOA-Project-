from pathlib import Path
import pandas as pd


# ============================================================
# DATASET PATH
# ============================================================

DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "ai4i.csv"
)


# ============================================================
# MACHINE INPUT FEATURES
# ============================================================

FEATURE_COLUMNS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]


# ============================================================
# TARGET
# ============================================================

TARGET_COLUMN = "Machine failure"


# ============================================================
# DATASET COLUMNS REQUIRED
# ============================================================

REQUIRED_COLUMNS = [
    "UDI",
    "Product ID",
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "Machine failure",
    "TWF",
    "HDF",
    "PWF",
    "OSF",
    "RNF",
]


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset(csv_path=DATASET_PATH):

    path = Path(csv_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"AI4I dataset not found: {path}"
        )

    df = pd.read_csv(path)

    # Remove accidental spaces from column names
    df.columns = df.columns.str.strip()

    # Check required columns
    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Dataset is missing columns: "
            + ", ".join(missing)
        )

    if df.empty:
        raise ValueError("AI4I dataset is empty")

    # Convert machine features to numeric
    for column in FEATURE_COLUMNS:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Convert target to numeric
    df[TARGET_COLUMN] = pd.to_numeric(
        df[TARGET_COLUMN],
        errors="coerce"
    )

    # Check invalid feature values
    if df[FEATURE_COLUMNS].isna().any().any():
        raise ValueError(
            "Dataset contains invalid numeric values "
            "in machine feature columns."
        )

    # Check invalid target values
    if df[TARGET_COLUMN].isna().any():
        raise ValueError(
            "Dataset contains missing Machine failure values."
        )

    # Target should be 0 or 1
    invalid_targets = set(df[TARGET_COLUMN].unique()) - {0, 1}

    if invalid_targets:
        raise ValueError(
            f"Unexpected Machine failure values: "
            f"{sorted(invalid_targets)}"
        )

    return df


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    data = load_dataset()

    print("\nAI4I DATASET LOADED SUCCESSFULLY")
    print("-" * 50)

    print(f"Dataset shape: {data.shape}")

    print("\nMachine input features:")
    for feature in FEATURE_COLUMNS:
        print(f"  - {feature}")

    print(f"\nTarget: {TARGET_COLUMN}")

    print("\nMachine failure counts:")
    print(data[TARGET_COLUMN].value_counts())

    print("\nFirst 5 rows:")
    print(
        data[
            FEATURE_COLUMNS + [TARGET_COLUMN]
        ].head()
    )