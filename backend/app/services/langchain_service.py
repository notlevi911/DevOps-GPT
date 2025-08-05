import os
import tempfile
import shutil
from typing import List, Dict, Any
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from git import Repo
import google.generativeai as genai
from ..config import settings

class LangChainService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=settings.gemini_api_key,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        self.vector_store = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = None

    async def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """Clone and analyze a GitHub repository"""
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Clone repository
                repo = Repo.clone_from(repo_url, temp_dir)
                
                # Extract files
                documents = self._extract_files(temp_dir)
                
                # Add IDs to documents
                for i, doc in enumerate(documents):
                    doc.metadata["id"] = f"doc_{i}"
                
                # Create vector store
                if documents:  # Only create if we have documents
                    self.vector_store = Chroma.from_documents(
                        documents=documents,
                        embedding=self.embeddings,
                        persist_directory=settings.vector_db_path
                    )
                else:
                    raise Exception("No analyzable files found in repository")
                
                # Create QA chain
                self.qa_chain = ConversationalRetrievalChain.from_llm(
                    llm=self.llm,
                    retriever=self.vector_store.as_retriever(),
                    memory=self.memory,
                    return_source_documents=True
                )
                
                # Analyze codebase
                analysis = await self._analyze_codebase(documents)
                
                return {
                    "repository_url": repo_url,
                    "files_analyzed": [doc.metadata.get("source", "") for doc in documents],
                    "analysis": analysis,
                    "summary": await self._generate_summary(analysis)
                }
                
            except Exception as e:
                raise Exception(f"Failed to analyze repository: {str(e)}")

    def _extract_files(self, repo_path: str) -> List[Document]:
        """Extract and process files from repository"""
        documents = []
        
        # File patterns to include
        include_patterns = [
            "*.py", "*.js", "*.ts", "*.jsx", "*.tsx",
            "*.yaml", "*.yml", "*.json", "*.md",
            "Dockerfile*", "docker-compose*",
            "*.tf", "*.sh", "*.env*"
        ]
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv']]
            
            for file in files:
                if any(file.endswith(pattern.replace('*', '')) for pattern in include_patterns) or \
                   any(pattern.replace('*', '') in file for pattern in include_patterns):
                    
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, repo_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": relative_path,
                                "file_type": file.split('.')[-1] if '.' in file else 'unknown'
                            }
                        )
                        documents.append(doc)
                        
                    except (UnicodeDecodeError, PermissionError):
                        continue
        
        # Split documents
        split_docs = self.text_splitter.split_documents(documents)
        return split_docs

    async def _analyze_codebase(self, documents: List[Document]) -> Dict[str, List[str]]:
        """Analyze codebase for DevOps improvements"""
        analysis = {
            "dockerfile_suggestions": [],
            "kubernetes_suggestions": [],
            "cicd_suggestions": [],
            "monitoring_suggestions": []
        }
        
        # Find relevant files
        dockerfiles = [doc for doc in documents if "dockerfile" in doc.metadata.get("source", "").lower()]
        k8s_files = [doc for doc in documents if doc.metadata.get("source", "").endswith(('.yaml', '.yml'))]
        ci_files = [doc for doc in documents if ".github" in doc.metadata.get("source", "")]
        
        # Analyze Dockerfiles
        if dockerfiles:
            dockerfile_analysis = await self._analyze_dockerfiles(dockerfiles)
            analysis["dockerfile_suggestions"] = dockerfile_analysis
        
        # Analyze Kubernetes files
        if k8s_files:
            k8s_analysis = await self._analyze_kubernetes(k8s_files)
            analysis["kubernetes_suggestions"] = k8s_analysis
        
        # Analyze CI/CD files
        if ci_files:
            cicd_analysis = await self._analyze_cicd(ci_files)
            analysis["cicd_suggestions"] = cicd_analysis
        
        # General monitoring suggestions
        analysis["monitoring_suggestions"] = [
            "Add health check endpoints",
            "Implement Prometheus metrics",
            "Configure log aggregation",
            "Set up alerting rules"
        ]
        
        return analysis

    async def _analyze_dockerfiles(self, dockerfiles: List[Document]) -> List[str]:
        """Analyze Dockerfile for improvements"""
        suggestions = []
        
        for doc in dockerfiles:
            content = doc.page_content.lower()
            
            if "healthcheck" not in content:
                suggestions.append("Add HEALTHCHECK instruction to Dockerfile")
            
            if "user" not in content:
                suggestions.append("Run container as non-root user for security")
            
            if "multi-stage" not in content and "from" in content:
                suggestions.append("Consider using multi-stage builds to reduce image size")
            
            if ".dockerignore" not in content:
                suggestions.append("Create .dockerignore file to exclude unnecessary files")
        
        return suggestions

    async def _analyze_kubernetes(self, k8s_files: List[Document]) -> List[str]:
        """Analyze Kubernetes YAML files"""
        suggestions = []
        
        for doc in k8s_files:
            content = doc.page_content.lower()
            
            if "resources:" not in content:
                suggestions.append("Add resource limits and requests to prevent resource starvation")
            
            if "livenessprobe" not in content:
                suggestions.append("Configure liveness probe for health checking")
            
            if "readinessprobe" not in content:
                suggestions.append("Configure readiness probe for traffic routing")
            
            if "securitycontext" not in content:
                suggestions.append("Add security context to run containers securely")
        
        return suggestions

    async def _analyze_cicd(self, ci_files: List[Document]) -> List[str]:
        """Analyze CI/CD configuration"""
        suggestions = []
        
        for doc in ci_files:
            content = doc.page_content.lower()
            
            if "cache" not in content:
                suggestions.append("Add caching to speed up builds")
            
            if "test" not in content:
                suggestions.append("Include automated testing in CI pipeline")
            
            if "security" not in content and "scan" not in content:
                suggestions.append("Add security scanning to CI pipeline")
            
            if "artifact" not in content:
                suggestions.append("Configure build artifacts storage")
        
        return suggestions

    async def _generate_summary(self, analysis: Dict[str, List[str]]) -> str:
        """Generate summary of analysis"""
        total_suggestions = sum(len(suggestions) for suggestions in analysis.values())
        return f"Found {total_suggestions} improvement opportunities across Dockerfile, Kubernetes, CI/CD, and monitoring configurations."

    async def chat(self, message: str) -> str:
        """Chat with the AI about the codebase"""
        if not self.qa_chain:
            return "Please analyze a repository first before asking questions."
        
        try:
            result = await self.qa_chain.acall({"question": message})
            return result["answer"]
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

# Global service instance
langchain_service = LangChainService()