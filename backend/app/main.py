from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import uuid

app = FastAPI(title="DevOps GPT API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    id: str
    text: str
    sender: str
    timestamp: datetime

class RepositoryRequest(BaseModel):
    repository_url: str

class RepositoryAnalysis(BaseModel):
    repository_url: str
    analysis: dict

class Suggestion(BaseModel):
    type: str
    title: str
    description: str
    code: Optional[str] = None
    priority: str

class TestGenerationRequest(BaseModel):
    type: str  # 'selenium', 'pytest', 'testng'

class MonitoringRequest(BaseModel):
    type: str  # 'prometheus', 'grafana'

# In-memory storage (replace with DB later)
chat_history: List[ChatResponse] = []
current_analysis: Optional[RepositoryAnalysis] = None

@app.get("/")
async def root():
    return {"message": "DevOps GPT API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Chat endpoints
@app.post("/chat", response_model=ChatResponse)
async def send_message(message: ChatMessage):
    # Add user message to history
    user_msg = ChatResponse(
        id=str(uuid.uuid4()),
        text=message.message,
        sender="user",
        timestamp=datetime.now()
    )
    chat_history.append(user_msg)
    
    # Generate bot response (placeholder for now)
    bot_response = f"I received your message: '{message.message}'. This is a placeholder response. In the full implementation, this will use LangChain and Gemini API."
    
    bot_msg = ChatResponse(
        id=str(uuid.uuid4()),
        text=bot_response,
        sender="bot",
        timestamp=datetime.now()
    )
    chat_history.append(bot_msg)
    
    return bot_msg

@app.get("/chat/history", response_model=List[ChatResponse])
async def get_chat_history():
    return chat_history

# Repository endpoints
@app.post("/repository/analyze", response_model=RepositoryAnalysis)
async def analyze_repository(request: RepositoryRequest):
    # Placeholder analysis
    analysis = RepositoryAnalysis(
        repository_url=request.repository_url,
        analysis={
            "dockerfile_suggestions": [
                "Add health check to Dockerfile",
                "Use multi-stage build for smaller image"
            ],
            "kubernetes_suggestions": [
                "Add resource limits to deployments",
                "Configure liveness and readiness probes"
            ],
            "cicd_suggestions": [
                "Add caching to GitHub Actions",
                "Include security scanning step"
            ],
            "monitoring_suggestions": [
                "Add Prometheus metrics endpoint",
                "Configure basic alerts"
            ]
        }
    )
    
    global current_analysis
    current_analysis = analysis
    return analysis

@app.post("/repository/upload", response_model=RepositoryAnalysis)
async def upload_files(files: List[UploadFile] = File(...)):
    # Process uploaded files (placeholder)
    filenames = [file.filename for file in files]
    
    analysis = RepositoryAnalysis(
        repository_url=f"uploaded_files: {', '.join(filenames)}",
        analysis={
            "dockerfile_suggestions": ["Analyzing uploaded files..."],
            "kubernetes_suggestions": ["Processing YAML files..."],
            "cicd_suggestions": ["Checking CI/CD configurations..."],
            "monitoring_suggestions": ["Evaluating monitoring setup..."]
        }
    )
    
    global current_analysis
    current_analysis = analysis
    return analysis

# Suggestions endpoints
@app.get("/suggestions", response_model=List[Suggestion])
async def get_suggestions():
    if not current_analysis:
        return []
    
    suggestions = []
    
    # Convert analysis to suggestions
    for suggestion_text in current_analysis.analysis.get("dockerfile_suggestions", []):
        suggestions.append(Suggestion(
            type="dockerfile",
            title="Dockerfile Optimization",
            description=suggestion_text,
            priority="medium"
        ))
    
    for suggestion_text in current_analysis.analysis.get("kubernetes_suggestions", []):
        suggestions.append(Suggestion(
            type="kubernetes",
            title="Kubernetes Configuration",
            description=suggestion_text,
            priority="high"
        ))
    
    return suggestions

@app.post("/suggestions/generate-tests")
async def generate_test_scripts(request: TestGenerationRequest):
    test_type = request.type
    
    if test_type == "selenium":
        script = """
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class BasicUITest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000")
    
    def test_page_loads(self):
        self.assertIn("DevOps GPT", self.driver.title)
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
        """
    elif test_type == "pytest":
        script = """
import pytest
import requests

def test_api_health():
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint():
    response = requests.post(
        "http://localhost:8000/chat",
        json={"message": "test message"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["sender"] == "bot"
        """
    else:
        script = "# Test script generation for other types coming soon..."
    
    return {"script": script}

@app.post("/suggestions/generate-monitoring")
async def generate_monitoring_config(request: MonitoringRequest):
    config_type = request.type
    
    if config_type == "prometheus":
        config = """
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'devops-gpt-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    scrape_interval: 5s
    
rule_files:
  - "alerts.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
        """
    elif config_type == "grafana":
        config = """{
  "dashboard": {
    "title": "DevOps GPT Monitoring",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "http_request_duration_seconds",
            "legendFormat": "Response Time"
          }
        ]
      },
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      }
    ]
  }
}"""
    else:
        config = "# Configuration for other monitoring types coming soon..."
    
    return {"config": config}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)