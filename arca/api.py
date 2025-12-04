# api.py
"""
ARCA System: FastAPI REST API (Phase 3)

TSD Requirements:
- Endpoint: POST /analyze_regulation
- Input: new_regulation_text (str, max 2000 words), date_of_law (str, optional)
- Output: TSD-compliant JSON report
- Framework: FastAPI (recommended) or Flask
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn

from arca_pipeline import ARCASystem

# ─────────────────────────────────────────────────────────
# API MODELS (Pydantic Schemas)
# ─────────────────────────────────────────────────────────

class RegulationAnalysisRequest(BaseModel):
    """
    TSD Section 3.1: Schéma d'Entrée
    
    Request body for POST /analyze_regulation
    """
    new_regulation_text: str = Field(
        ...,
        description="The complete text of the new regulation to analyze",
        min_length=10,
        max_length=20000  # ~2000 words * 10 chars average
    )
    
    date_of_law: Optional[str] = Field(
        None,
        description="Date when the regulation takes effect (format: YYYY-MM-DD)",
        example="2025-06-01"
    )
    
    regulation_title: Optional[str] = Field(
        "Untitled Regulation",
        description="Title or name of the regulation",
        max_length=500
    )
    
    @validator('date_of_law')
    def validate_date(cls, v):
        """Validate date format"""
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('date_of_law must be in YYYY-MM-DD format')
        return v
    
    @validator('new_regulation_text')
    def validate_word_count(cls, v):
        """Ensure text doesn't exceed 2000 words (TSD requirement)"""
        word_count = len(v.split())
        if word_count > 2000:
            raise ValueError(f'Regulation text exceeds 2000 words (found {word_count} words)')
        return v


class RiskObject(BaseModel):
    """
    TSD Section 4: Risk object schema
    """
    policy_id: str
    severity: str  # HIGH, MEDIUM, or LOW
    divergence_summary: str
    conflicting_policy_excerpt: str
    new_rule_excerpt: str
    recommendation: str


class RegulationAnalysisResponse(BaseModel):
    """
    TSD Section 3.2: Schéma de Sortie JSON
    
    Response body matching TSD requirements
    """
    regulation_id: str = Field(..., description="Unique ID generated from hash")
    regulation_title: str
    date_of_law: str
    date_processed: str = Field(..., description="Date when analysis was performed")
    total_risks_flagged: int = Field(..., description="Number of conflicts found")
    risks: List[RiskObject] = Field(..., description="Array of identified risks")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional analysis metadata")


class HealthCheckResponse(BaseModel):
    """Health check endpoint response"""
    status: str
    timestamp: str
    vectorstore_loaded: bool
    agents_initialized: bool


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: str
    timestamp: str


# ─────────────────────────────────────────────────────────
# FASTAPI APP INITIALIZATION
# ─────────────────────────────────────────────────────────

app = FastAPI(
    title="ARCA API",
    description="Agent de Conformité Réglementaire Agile - Automated regulatory compliance analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (allow all origins for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ARCA system instance (initialized on startup)
arca_system: Optional[ARCASystem] = None


# ─────────────────────────────────────────────────────────
# LIFECYCLE EVENTS
# ─────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup_event():
    """
    Initialize ARCA system on server startup
    """
    global arca_system
    
    print("\n" + "=" * 60)
    print("🚀 ARCA API SERVER STARTING")
    print("=" * 60)
    
    try:
        arca_system = ARCASystem()
        print("✅ ARCA system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ARCA system: {e}")
        print("⚠️  API will be unavailable")
        arca_system = None
    
    print("=" * 60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on server shutdown
    """
    print("\n🛑 ARCA API SERVER SHUTTING DOWN")


# ─────────────────────────────────────────────────────────
# API ENDPOINTS
# ─────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "ARCA API - Agent de Conformité Réglementaire Agile",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze_regulation (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["System"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Check if the ARCA system is ready to process requests
    """
    vectorstore_loaded = False
    agents_initialized = False
    
    if arca_system is not None:
        agents_initialized = True
        try:
            # Test if vectorstore is accessible
            arca_system.agent1.db.similarity_search("test", k=1)
            vectorstore_loaded = True
        except:
            pass
    
    status = "healthy" if (vectorstore_loaded and agents_initialized) else "unhealthy"
    
    return HealthCheckResponse(
        status=status,
        timestamp=datetime.now().isoformat(),
        vectorstore_loaded=vectorstore_loaded,
        agents_initialized=agents_initialized
    )


@app.post(
    "/analyze_regulation",
    response_model=RegulationAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Analysis completed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    },
    tags=["Analysis"],
    summary="Analyze a new regulation for compliance conflicts"
)
async def analyze_regulation(request: RegulationAnalysisRequest):
    """
    TSD Section 3.1: POST /analyze_regulation
    
    Analyze a new regulation against internal company policies and identify conflicts.
    
    **Sequential Processing Pipeline:**
    1. Policy Researcher → Retrieves Top 5 relevant policies from vectorstore
    2. Compliance Auditor → Analyzes each policy for conflicts
    3. Report Generator → Formats structured JSON report
    
    **Input Requirements:**
    - `new_regulation_text`: Complete regulation text (max 2000 words)
    - `date_of_law`: Optional effective date (YYYY-MM-DD format)
    - `regulation_title`: Optional regulation title
    
    **Output:**
    - Structured JSON report with identified conflicts
    - Each conflict includes severity (HIGH/MEDIUM/LOW) and recommendations
    
    **Processing Time:** Typically 10-30 seconds depending on regulation length
    """
    
    # Check if system is initialized
    if arca_system is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ARCA system not initialized. Check server logs."
        )
    
    try:
        # Run the complete ARCA pipeline
        result = arca_system.analyze_regulation(
            new_regulation_text=request.new_regulation_text,
            date_of_law=request.date_of_law,
            regulation_title=request.regulation_title,
            save_report=True  # Save all reports to disk
        )
        
        return RegulationAnalysisResponse(**result)
    
    except ValueError as e:
        # Validation errors (e.g., invalid input)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        # Internal errors
        print(f"❌ Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# ─────────────────────────────────────────────────────────
# DEVELOPMENT SERVER
# ─────────────────────────────────────────────────────────

def run_dev_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Run the FastAPI development server
    
    Usage:
        python api.py
    
    Then access:
        - API: http://localhost:8000
        - Swagger docs: http://localhost:8000/docs
        - ReDoc: http://localhost:8000/redoc
    """
    print("\n" + "=" * 60)
    print("🚀 STARTING ARCA API DEVELOPMENT SERVER")
    print("=" * 60)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )


if __name__ == "__main__":
    run_dev_server()