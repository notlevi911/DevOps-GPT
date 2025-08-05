import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface ChatMessage {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

export interface RepositoryAnalysis {
  repository_url: string
  analysis: {
    dockerfile_suggestions: string[]
    kubernetes_suggestions: string[]
    cicd_suggestions: string[]
    monitoring_suggestions: string[]
  }
}

export interface Suggestion {
  type: 'dockerfile' | 'kubernetes' | 'cicd' | 'monitoring' | 'testing'
  title: string
  description: string
  code?: string
  priority: 'low' | 'medium' | 'high'
}

// Chat API
export const chatAPI = {
  sendMessage: async (message: string): Promise<ChatMessage> => {
    const response = await api.post('/chat', { message })
    return response.data
  },

  getHistory: async (): Promise<ChatMessage[]> => {
    const response = await api.get('/chat/history')
    return response.data
  },
}

// Repository API
export const repositoryAPI = {
  analyzeRepository: async (repoUrl: string): Promise<RepositoryAnalysis> => {
    const response = await api.post('/repository/analyze', { repository_url: repoUrl })
    return response.data
  },

  uploadFiles: async (files: File[]): Promise<RepositoryAnalysis> => {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    
    const response = await api.post('/repository/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}

// Suggestions API
export const suggestionsAPI = {
  getSuggestions: async (): Promise<Suggestion[]> => {
    const response = await api.get('/suggestions')
    return response.data
  },

  generateTestScripts: async (type: 'selenium' | 'pytest' | 'testng'): Promise<string> => {
    const response = await api.post('/suggestions/generate-tests', { type })
    return response.data.script
  },

  generateMonitoringConfig: async (type: 'prometheus' | 'grafana'): Promise<string> => {
    const response = await api.post('/suggestions/generate-monitoring', { type })
    return response.data.config
  },
}

// Error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    throw error
  }
)

export default api 