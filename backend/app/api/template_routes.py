from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.utils.sample_generator import generate_sample_excel

router = APIRouter(prefix="/api/v1/templates", tags=["Sample Excel Templates"])

@router.get("/download/{template_type}")
async def download_template(template_type: str):
    """
    Downloads sample Excel template file (.xlsx) for: internal, external, co, or po.
    """
    try:
        excel_stream = generate_sample_excel(template_type)
        filename = f"Sample_{template_type.upper()}_Template.xlsx"
        
        return StreamingResponse(
            excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sample template: {str(e)}")
