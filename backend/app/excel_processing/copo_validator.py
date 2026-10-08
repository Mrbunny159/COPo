import pandas as pd
from typing import Tuple

def validate_co_sheet(df: pd.DataFrame, file_label: str = "CO Sheet") -> pd.DataFrame:
    """
    Validates Course Outcomes (CO) DataFrame for Module 2.
    Required columns: 'CO Number', 'Statement'
    """
    if df.empty:
        raise ValueError(f"{file_label}: Excel sheet is empty.")

    col_mapping = {}
    for col in df.columns:
        clean_col = str(col).strip()
        if clean_col.lower() in ["co number", "co_number", "co #", "conumber", "co"]:
            col_mapping[col] = "CO Number"
        elif clean_col.lower() in ["statement", "co statement", "description", "details"]:
            col_mapping[col] = "Statement"

    df = df.rename(columns=col_mapping)

    required_cols = ["CO Number", "Statement"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"{file_label}: Missing required columns: {', '.join(missing)}. "
            f"Expected columns are 'CO Number' and 'Statement'."
        )

    df = df.dropna(subset=["CO Number", "Statement"])
    if df.empty:
        raise ValueError(f"{file_label}: No valid CO rows found after dropping empty entries.")

    df["CO Number"] = df["CO Number"].astype(str).str.strip()
    df["Statement"] = df["Statement"].astype(str).str.strip()

    return df


def validate_po_sheet(df: pd.DataFrame, file_label: str = "PO Sheet") -> pd.DataFrame:
    """
    Validates Program Outcomes (PO) DataFrame for Module 2.
    Required columns: 'PO Number', 'Statement'
    """
    if df.empty:
        raise ValueError(f"{file_label}: Excel sheet is empty.")

    col_mapping = {}
    for col in df.columns:
        clean_col = str(col).strip()
        if clean_col.lower() in ["po number", "po_number", "po #", "ponumber", "po"]:
            col_mapping[col] = "PO Number"
        elif clean_col.lower() in ["statement", "po statement", "description", "details"]:
            col_mapping[col] = "Statement"

    df = df.rename(columns=col_mapping)

    required_cols = ["PO Number", "Statement"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"{file_label}: Missing required columns: {', '.join(missing)}. "
            f"Expected columns are 'PO Number' and 'Statement'."
        )

    df = df.dropna(subset=["PO Number", "Statement"])
    if df.empty:
        raise ValueError(f"{file_label}: No valid PO rows found after dropping empty entries.")

    df["PO Number"] = df["PO Number"].astype(str).str.strip()
    df["Statement"] = df["Statement"].astype(str).str.strip()

    return df
