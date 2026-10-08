import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from app.excel_processing.validator import validate_marksheet
from app.assessment.calculator import calculate_attainment
from app.excel_processing.copo_validator import validate_co_sheet, validate_po_sheet
from app.nlp.copo_mapper import map_similarity_to_score

def test_marksheet_validation_valid():
    data = {"Roll No": [1, 2, 3], "Marks": [45, 60, 75]}
    df = pd.DataFrame(data)
    clean_df = validate_marksheet(df, "Test")
    assert len(clean_df) == 3
    assert "Roll No" in clean_df.columns
    assert "Marks" in clean_df.columns

def test_marksheet_validation_duplicate_roll():
    data = {"Roll No": [1, 1, 2], "Marks": [45, 60, 75]}
    df = pd.DataFrame(data)
    try:
        validate_marksheet(df, "Test")
        assert False, "Should have raised ValueError for duplicate roll numbers"
    except ValueError as ve:
        assert "Duplicate Roll Numbers detected" in str(ve)

def test_attainment_calculation_level3():
    data = {"Roll No": [1, 2, 3, 4], "Marks": [75, 80, 85, 90]}
    df = pd.DataFrame(data)
    report = calculate_attainment(df, "test.xlsx")
    assert report["totalStudents"] == 4
    assert report["passed"] == 4
    assert report["passPercentage"] == 100.0
    assert "Level 3" in report["attainmentLevel"]

def test_copo_validation():
    co_df = pd.DataFrame({"CO Number": ["CO1"], "Statement": ["Programming basic logic"]})
    po_df = pd.DataFrame({"PO Number": ["PO1"], "Statement": ["Engineering knowledge application"]})
    
    clean_co = validate_co_sheet(co_df)
    clean_po = validate_po_sheet(po_df)
    
    assert len(clean_co) == 1
    assert len(clean_po) == 1

def test_similarity_score_mapping():
    assert map_similarity_to_score(0.65) == 3
    assert map_similarity_to_score(0.40) == 2
    assert map_similarity_to_score(0.10) == 1

if __name__ == "__main__":
    test_marksheet_validation_valid()
    test_marksheet_validation_duplicate_roll()
    test_attainment_calculation_level3()
    test_copo_validation()
    test_similarity_score_mapping()
    print("ALL 5 UNIT TESTS PASSED SUCCESSFULLY!")
