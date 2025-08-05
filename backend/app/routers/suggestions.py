from fastapi import APIRouter, HTTPException
from typing import List

from ..models.schemas import (
    Suggestion, SuggestionType, Priority,
    TestGenerationRequest, MonitoringGenerationRequest, GenerationResponse
)

router = APIRouter(prefix="/suggestions", tags=["suggestions"])

# Import current analysis from repository router
from .repository import current_analysis

@router.get("", response_model=List[Suggestion])
async def get_suggestions():
    if not current_analysis:
        return []
    
    suggestions = []
    
    # Convert analysis to structured suggestions
    for suggestion_text in current_analysis.analysis.get("dockerfile_suggestions", []):
        suggestions.append(Suggestion(
            type=SuggestionType.DOCKERFILE,
            title="Dockerfile Optimization",
            description=suggestion_text,
            priority=Priority.MEDIUM
        ))
    
    for suggestion_text in current_analysis.analysis.get("kubernetes_suggestions", []):
        suggestions.append(Suggestion(
            type=SuggestionType.KUBERNETES,
            title="Kubernetes Configuration",
            description=suggestion_text,
            priority=Priority.HIGH
        ))
    
    for suggestion_text in current_analysis.analysis.get("cicd_suggestions", []):
        suggestions.append(Suggestion(
            type=SuggestionType.CICD,
            title="CI/CD Pipeline",
            description=suggestion_text,
            priority=Priority.MEDIUM
        ))
    
    for suggestion_text in current_analysis.analysis.get("monitoring_suggestions", []):
        suggestions.append(Suggestion(
            type=SuggestionType.MONITORING,
            title="Monitoring & Observability",
            description=suggestion_text,
            priority=Priority.LOW
        ))
    
    return suggestions

@router.post("/generate-tests", response_model=GenerationResponse)
async def generate_test_scripts(request: TestGenerationRequest):
    try:
        test_type = request.type.lower()
        
        templates = {
            "selenium": {
                "content": '''from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class DevOpsGPTUITests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5173")
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_page_loads(self):
        title = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        self.assertIn("DevOps GPT", title.text)
    
    def test_chat_functionality(self):
        chat_input = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea")))
        send_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        
        chat_input.send_keys("Hello, test message")
        send_button.click()
        
        # Wait for response
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "message")))
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()''',
                "filename": "test_ui_selenium.py",
                "description": "Selenium UI tests for DevOps GPT frontend"
            },
            
            "pytest": {
                "content": '''import pytest
import requests
import json

BASE_URL = "http://localhost:8000"

@pytest.fixture
def api_client():
    return requests.Session()

def test_health_endpoint(api_client):
    response = api_client.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint(api_client):
    payload = {"message": "test message"}
    response = api_client.post(f"{BASE_URL}/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert data["sender"] == "bot"
    assert "timestamp" in data

def test_repository_analyze(api_client):
    payload = {"repository_url": "https://github.com/test/repo"}
    response = api_client.post(f"{BASE_URL}/repository/analyze", json=payload)
    
    # This might fail in real test, but shows the structure
    assert response.status_code in [200, 500]  # 500 expected for invalid repo

def test_suggestions_endpoint(api_client):
    response = api_client.get(f"{BASE_URL}/suggestions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)''',
                "filename": "test_api_pytest.py",
                "description": "Pytest API tests for DevOps GPT backend"
            },
            
            "testng": {
                "content": '''package com.devopsgpt.tests;

import org.testng.annotations.Test;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.AfterClass;
import org.testng.Assert;
import io.restassured.RestAssured;
import io.restassured.response.Response;
import static io.restassured.RestAssured.*;

public class DevOpsGPTApiTests {
    
    @BeforeClass
    public void setUp() {
        RestAssured.baseURI = "http://localhost:8000";
    }
    
    @Test
    public void testHealthEndpoint() {
        Response response = get("/health");
        Assert.assertEquals(response.getStatusCode(), 200);
        Assert.assertEquals(response.jsonPath().getString("status"), "healthy");
    }
    
    @Test
    public void testChatEndpoint() {
        String requestBody = "{\\"message\\": \\"test message\\"}";
        
        Response response = given()
            .header("Content-Type", "application/json")
            .body(requestBody)
            .post("/chat");
            
        Assert.assertEquals(response.getStatusCode(), 200);
        Assert.assertTrue(response.jsonPath().getString("text").length() > 0);
        Assert.assertEquals(response.jsonPath().getString("sender"), "bot");
    }
    
    @Test
    public void testSuggestionsEndpoint() {
        Response response = get("/suggestions");
        Assert.assertEquals(response.getStatusCode(), 200);
    }
}''',
                "filename": "DevOpsGPTApiTests.java",
                "description": "TestNG API tests for DevOps GPT backend"
            }
        }
        
        if test_type not in templates:
            raise HTTPException(status_code=400, detail=f"Unsupported test type: {test_type}")
        
        return GenerationResponse(**templates[test_type])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")

@router.post("/generate-monitoring", response_model=GenerationResponse)
async def generate_monitoring_config(request: MonitoringGenerationRequest):
    try:
        config_type = request.type.lower()
        
        templates = {
            "prometheus": {
                "content": '''global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "devops_gpt_alerts.yml"

scrape_configs:
  - job_name: 'devops-gpt-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: /metrics
    scrape_interval: 5s
    
  - job_name: 'devops-gpt-frontend'
    static_configs:
      - targets: ['localhost:5173']
    metrics_path: /metrics
    scrape_interval: 10s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093''',
                "filename": "prometheus.yml",
                "description": "Prometheus configuration for DevOps GPT monitoring"
            },
            
            "grafana": {
                "content": '''{
  "dashboard": {
    "id": null,
    "title": "DevOps GPT Dashboard",
    "tags": ["devops", "gpt", "monitoring"],
    "style": "dark",
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "API Response Time",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile",
            "refId": "A"
          },
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile",
            "refId": "B"
          }
        ]
      },
      {
        "id": 2,
        "title": "Request Rate",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "id": 3,
        "title": "Chat Messages",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 18, "y": 0},
        "targets": [
          {
            "expr": "increase(chat_messages_total[1h])",
            "legendFormat": "Messages/hour"
          }
        ]
      }
    ]
  }
}''',
                "filename": "devops_gpt_dashboard.json",
                "description": "Grafana dashboard for DevOps GPT metrics"
            }
        }
        
        if config_type not in templates:
            raise HTTPException(status_code=400, detail=f"Unsupported monitoring type: {config_type}")
        
        return GenerationResponse(**templates[config_type])
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Monitoring config generation failed: {str(e)}")