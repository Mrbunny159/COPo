from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from typing import Optional

from app.excel_processing.reader import read_excel_file
from app.excel_processing.validator import validate_marksheet
from app.assessment.calculator import calculate_attainment

router = APIRouter(prefix="/api/v1/assessment", tags=["Student Marks Assessment"])

@router.post("/process")
async def process_student_assessment(
    academic_year: str = Form(...),
    exam_month: str = Form(...),
    subject_code: str = Form(...),
    subject_name: str = Form(...),
    internal_file: Optional[UploadFile] = File(None),
    external_file: Optional[UploadFile] = File(None)
):
    """
    Processes Student Marks Assessment independently for Internal and/or External marksheets.
    Internal and External marks are NEVER merged or combined.
    """
    if not internal_file and not external_file:
        raise HTTPException(
            status_code=400,
            detail="At least one marksheet (Internal or External) must be uploaded."
        )

    internal_report = None
    external_report = None

    # Process Internal file if provided
    if internal_file and internal_file.filename:
        try:
            df_internal = read_excel_file(internal_file)
            df_internal_clean = validate_marksheet(df_internal, "Internal Exam Marksheet")
            internal_report = calculate_attainment(df_internal_clean, internal_file.filename)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing Internal file: {str(e)}")

    # Process External file if provided
    if external_file and external_file.filename:
        try:
            df_external = read_excel_file(external_file)
            df_external_clean = validate_marksheet(df_external, "External Exam Marksheet")
            external_report = calculate_attainment(df_external_clean, external_file.filename)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing External file: {str(e)}")

    return {
        "status": "success",
        "academicDetails": {
            "academicYear": academic_year,
            "examMonth": exam_month,
            "subjectCode": subject_code,
            "subjectName": subject_name
        },
        "internalReport": internal_report,
        "externalReport": external_report
    }
