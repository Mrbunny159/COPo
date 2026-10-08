from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import Optional

from app.excel_processing.reader import read_excel_file
from app.excel_processing.copo_validator import validate_co_sheet, validate_po_sheet
from app.nlp.copo_mapper import generate_copo_matrix

router = APIRouter(prefix="/api/v1/copo", tags=["CO-PO Mapping"])

@router.post("/map")
async def map_co_po_matrix(
    academic_year: str = Form(...),
    exam_month: str = Form(...),
    subject_code: str = Form(...),
    subject_name: str = Form(...),
    co_file: Optional[UploadFile] = File(None),
    po_file: Optional[UploadFile] = File(None)
):
    """
    Generates an automated CO-PO correlation matrix using NLP embeddings.
    Both CO Sheet and PO Sheet are mandatory.
    """
    # Validation: Missing files check
    missing = []
    if not co_file or not co_file.filename:
        missing.append("CO Sheet")
    if not po_file or not po_file.filename:
        missing.append("PO Sheet")

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Validation Error: {' and '.join(missing)} {'is' if len(missing) == 1 else 'are'} required for CO-PO Mapping."
        )

    try:
        # Read Excel Files
        df_co_raw = read_excel_file(co_file)
        df_po_raw = read_excel_file(po_file)

        # Validate Schema and Clean Data
        df_co = validate_co_sheet(df_co_raw, "CO Sheet")
        df_po = validate_po_sheet(df_po_raw, "PO Sheet")

        # Extract Records
        co_records = df_co.to_dict(orient="records")
        po_records = df_po.to_dict(orient="records")

        # Generate CO-PO Matrix via NLP Engine
        matrix_result = generate_copo_matrix(co_records, po_records)

        return {
            "status": "success",
            "academicDetails": {
                "academicYear": academic_year,
                "examMonth": exam_month,
                "subjectCode": subject_code,
                "subjectName": subject_name
            },
            "poList": matrix_result["poList"],
            "matrix": matrix_result["matrix"]
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CO-PO matrix: {str(e)}")
