from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
import tempfile
import os

from ..models.schemas import RepositoryRequest, RepositoryAnalysis
from ..services.langchain_service import langchain_service

router = APIRouter(prefix="/repository", tags=["repository"])

# Store current analysis
current_analysis: RepositoryAnalysis = None

@router.post("/analyze", response_model=RepositoryAnalysis)
async def analyze_repository(request: RepositoryRequest):
    try:
        result = await langchain_service.analyze_repository(str(request.repository_url))
        
        global current_analysis
        current_analysis = RepositoryAnalysis(**result)
        
        return current_analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Repository analysis failed: {str(e)}")

@router.post("/upload", response_model=RepositoryAnalysis)
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save uploaded files
            for file in files:
                file_path = os.path.join(temp_dir, file.filename)
                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)
            
            # Analyze uploaded files (simplified version)
            # In a real implementation, you'd process these files similar to repository analysis
            analysis_result = {
                "repository_url": f"uploaded_files_{len(files)}_files",
                "files_analyzed": [file.filename for file in files],
                "analysis": {
                    "dockerfile_suggestions": ["Check uploaded Dockerfiles for optimization"],
                    "kubernetes_suggestions": ["Validate Kubernetes manifests"],
                    "cicd_suggestions": ["Review CI/CD pipeline configurations"],
                    "monitoring_suggestions": ["Add monitoring to your services"]
                },
                "summary": f"Analyzed {len(files)} uploaded files"
            }
            
            global current_analysis
            current_analysis = RepositoryAnalysis(**analysis_result)
            
            return current_analysis
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload analysis failed: {str(e)}")

@router.get("/current", response_model=RepositoryAnalysis)
async def get_current_analysis():
    if not current_analysis:
        raise HTTPException(status_code=404, detail="No repository analysis available")
    return current_analysis