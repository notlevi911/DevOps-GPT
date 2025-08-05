from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageSender(str, Enum):
    USER = "user"
    BOT = "bot"

class SuggestionType(str, Enum):
    DOCKERFILE = "dockerfile"
    KUBERNETES = "kubernetes"
    CICD = "cicd"
    MONITORING = "monitoring"
    TESTING = "testing"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Chat Models
class ChatMessageRequest(BaseModel):
    message: str

class ChatMessageResponse(BaseModel):
    id: str
    text: str
    sender: MessageSender
    timestamp: datetime

# Repository Models
class RepositoryRequest(BaseModel):
    repository_url: HttpUrl

class FileAnalysis(BaseModel):
    filename: str
    file_type: str
    issues: List[str]
    suggestions: List[str]

class RepositoryAnalysis(BaseModel):
    repository_url: str
    files_analyzed: List[str]
    analysis: Dict[str, List[str]]
    files_details: List[FileAnalysis]
    summary: str

# Suggestion Models
class Suggestion(BaseModel):
    type: SuggestionType
    title: str
    description: str
    code: Optional[str] = None
    priority: Priority
    file_path: Optional[str] = None

# Generation Models
class TestGenerationRequest(BaseModel):
    type: str  # selenium, pytest, testng

class MonitoringGenerationRequest(BaseModel):
    type: str  # prometheus, grafana

class GenerationResponse(BaseModel):
    content: str
    filename: str
    description: str