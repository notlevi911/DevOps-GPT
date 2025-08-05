from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config import settings
from .routers import chat, repository, suggestions

app = FastAPI(
    title="DevOps GPT API", 
    version="1.0.0",
    description="AI-powered DevOps assistant with repository analysis and suggestions"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(repository.router)
app.include_router(suggestions.router)

# Health endpoints
@app.get("/")
async def root():
    return {
        "message": "DevOps GPT API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "devops-gpt-api"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )