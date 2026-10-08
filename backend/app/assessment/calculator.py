import pandas as pd
from typing import Dict, Any

def calculate_attainment(df: pd.DataFrame, filename: str, pass_threshold_pct: float = 50.0) -> Dict[str, Any]:
    """
    Calculates independent student marks attainment report.
    - df: Validated DataFrame with 'Roll No' and 'Marks'
    - filename: Name of the uploaded file
    - pass_threshold_pct: Percentage threshold to consider a student passed (default 50%)
    """
    total_students = len(df)
    if total_students == 0:
        raise ValueError(f"No valid student records found in '{filename}'.")

    max_mark = float(df["Marks"].max())
    # If max mark is 0, avoid division by zero
    if max_mark <= 0:
        max_mark = 100.0
    
    # Standardize to percentage scale (0-100)
    # If marks are already out of 100 or another scale, compute percentage
    if max_mark > 100:
        df["Percentage"] = (df["Marks"] / max_mark) * 100.0
    elif max_mark <= 100 and max_mark > 0:
        # If scale is <= 100, calculate relative percentage against max_mark or 100
        df["Percentage"] = (df["Marks"] / max_mark) * 100.0
    else:
        df["Percentage"] = df["Marks"]

    df["Passed"] = df["Percentage"] >= pass_threshold_pct
    passed_count = int(df["Passed"].sum())
    pass_percentage = round((passed_count / total_students) * 100.0, 2)

    # Distribution Brackets
    range_high = df[df["Percentage"] >= 70.0]
    range_mid = df[(df["Percentage"] >= 60.0) & (df["Percentage"] < 70.0)]
    range_low = df[df["Percentage"] < 60.0]

    count_high = len(range_high)
    count_mid = len(range_mid)
    count_low = len(range_low)

    pct_high = round((count_high / total_students) * 100.0, 2)
    pct_mid = round((count_mid / total_students) * 100.0, 2)
    pct_low = round((count_low / total_students) * 100.0, 2)

    # Attainment Level Determination (OBE Rules)
    if pass_percentage >= 70.0:
        attainment_level = "Level 3 (Substantial Attainment - >= 70% Passed)"
    elif pass_percentage >= 60.0:
        attainment_level = "Level 2 (Moderate Attainment - 60% to 69% Passed)"
    else:
        attainment_level = "Level 1 (Slight Attainment - < 60% Passed)"

    return {
        "filename": filename,
        "totalStudents": total_students,
        "appeared": total_students,
        "passed": passed_count,
        "passPercentage": pass_percentage,
        "attainmentLevel": attainment_level,
        "maxMarksDetected": max_mark,
        "distribution": [
            {"range": ">= 70% (High)", "count": count_high, "percentage": pct_high},
            {"range": "60% - 69% (Moderate)", "count": count_mid, "percentage": pct_mid},
            {"range": "< 60% (Low)", "count": count_low, "percentage": pct_low}
        ]
    }
