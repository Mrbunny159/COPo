from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.assessment_routes import router as assessment_router
from app.api.copo_routes import router as copo_router
from app.api.template_routes import router as template_router

app = FastAPI(
    title="Outcome Based Education (OBE) Assessment API",
    description="FastAPI Backend for Student Marks Assessment and Semantic CO-PO Mapping",
    version="1.0.0"
)

# Configure CORS for local frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(assessment_router)
app.include_router(copo_router)
app.include_router(template_router)

@app.get("/api/v1/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint to verify backend status."""
    return {
        "status": "healthy",
        "service": "OBE Assessment Backend API",
        "version": "1.0.0"
    }

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    """Custom exception handler for validation errors."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "Validation Exception"}
    )
