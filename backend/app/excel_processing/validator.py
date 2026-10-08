import pandas as pd

def validate_marksheet(df: pd.DataFrame, file_label: str = "Marksheet") -> pd.DataFrame:
    """
    Validates a student marksheet DataFrame for Module 1.
    Required columns: 'Roll No', 'Marks'
    Checks:
    - Empty DataFrame
    - Column presence
    - Duplicate Roll Numbers
    - Non-numeric or negative marks
    Returns cleaned DataFrame with standardized types.
    """
    if df.empty:
        raise ValueError(f"{file_label}: Excel sheet is empty.")

    # Standardize column headers case-insensitively if needed
    col_mapping = {}
    for col in df.columns:
        clean_col = str(col).strip()
        if clean_col.lower() in ["roll no", "rollno", "roll_no"]:
            col_mapping[col] = "Roll No"
        elif clean_col.lower() in ["marks", "mark", "score"]:
            col_mapping[col] = "Marks"
    
    df = df.rename(columns=col_mapping)

    required_cols = ["Roll No", "Marks"]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"{file_label}: Missing required columns: {', '.join(missing_cols)}. "
            f"Expected columns are 'Roll No' and 'Marks'."
        )

    # Drop fully empty rows
    df = df.dropna(how="all", subset=["Roll No", "Marks"])

    # Check for missing values in required columns
    if df["Roll No"].isnull().any():
        raise ValueError(f"{file_label}: Contains missing/empty 'Roll No' entries.")
    if df["Marks"].isnull().any():
        raise ValueError(f"{file_label}: Contains missing/empty 'Marks' entries.")

    # Check duplicate Roll Numbers
    duplicates = df[df.duplicated(subset=["Roll No"], keep=False)]
    if not duplicates.empty:
        dup_rolls = duplicates["Roll No"].unique().tolist()
        raise ValueError(
            f"{file_label}: Duplicate Roll Numbers detected: {dup_rolls[:5]}. "
            f"Each student Roll No must be unique."
        )

    # Validate numeric Marks
    try:
        df["Marks"] = pd.to_numeric(df["Marks"])
    except Exception:
        raise ValueError(f"{file_label}: All entries in 'Marks' column must be valid numeric values.")

    # Check for negative marks
    if (df["Marks"] < 0).any():
        raise ValueError(f"{file_label}: Negative mark values are not allowed.")

    return df
