import React, { useState } from 'react'
import { Send, Upload, Github, MessageSquare, Settings, Zap, Shield, Activity } from 'lucide-react'
import './App.css'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

interface Tab {
  id: string
  name: string
  icon: React.ReactNode
}

const tabs: Tab[] = [
  { id: 'chat', name: 'Chat', icon: <MessageSquare size={20} /> },
  { id: 'suggestions', name: 'Suggestions', icon: <Zap size={20} /> },
  { id: 'monitoring', name: 'Monitoring', icon: <Activity size={20} /> },
  { id: 'testing', name: 'Testing', icon: <Shield size={20} /> },
  { id: 'settings', name: 'Settings', icon: <Settings size={20} /> }
]

function App() {
  const [activeTab, setActiveTab] = useState('chat')
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello! I'm your DevOps GPT assistant. I can help you analyze your codebase, suggest improvements, and answer questions about your infrastructure. Upload a repository or ask me anything!",
      sender: 'bot',
      timestamp: new Date()
    }
  ])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [repoUrl, setRepoUrl] = useState('')

  const handleSendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm analyzing your request. This is a demo response - in the real app, this would connect to your LangChain backend.",
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, botMessage])
      setIsLoading(false)
    }, 1000)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // Handle file upload logic here
      console.log('File uploaded:', file.name)
    }
  }

  const handleRepoSubmit = () => {
    if (repoUrl.trim()) {
      // Handle repository URL submission
      console.log('Repository URL:', repoUrl)
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        text: `Analyzing repository: ${repoUrl}`,
        sender: 'bot',
        timestamp: new Date()
      }])
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="container">
          <div className="header-content">
            <h1 className="logo">
              <Zap size={32} />
              DevOps GPT
            </h1>
            <p className="subtitle">AI-powered DevOps assistant</p>
          </div>
        </div>
      </header>

      <div className="main-content">
        <div className="container">
          <div className="app-layout">
            {/* Sidebar */}
            <aside className="sidebar">
              <nav className="nav-tabs">
                {tabs.map(tab => (
                  <button
                    key={tab.id}
                    className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
                    onClick={() => setActiveTab(tab.id)}
                  >
                    {tab.icon}
                    {tab.name}
                  </button>
                ))}
              </nav>

              {/* Upload Section */}
              <div className="upload-section">
                <h3>Connect Repository</h3>
                
                {/* GitHub URL Input */}
                <div className="input-group">
                  <Github size={20} />
                  <input
                    type="text"
                    placeholder="Enter GitHub repository URL"
                    value={repoUrl}
                    onChange={(e) => setRepoUrl(e.target.value)}
                    className="input"
                  />
                  <button 
                    onClick={handleRepoSubmit}
                    className="btn btn-primary"
                    disabled={!repoUrl.trim()}
                  >
                    Connect
                  </button>
                </div>

                {/* File Upload */}
                <div className="upload-area">
                  <Upload size={32} />
                  <p>Or upload files directly</p>
                  <input
                    type="file"
                    id="file-upload"
                    onChange={handleFileUpload}
                    multiple
                    accept=".zip,.tar.gz"
                    style={{ display: 'none' }}
                  />
                  <label htmlFor="file-upload" className="btn btn-secondary">
                    Choose Files
                  </label>
                </div>
              </div>
            </aside>

            {/* Main Content Area */}
            <main className="main-area">
              {activeTab === 'chat' && (
                <div className="chat-container">
                  {/* Messages */}
                  <div className="messages">
                    {messages.map(message => (
                      <div key={message.id} className={`message ${message.sender}`}>
                        <div className="message-content">
                          {message.text}
                        </div>
                        <div className="message-time">
                          {message.timestamp.toLocaleTimeString()}
                        </div>
                      </div>
                    ))}
                    {isLoading && (
                      <div className="message bot">
                        <div className="message-content">
                          <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Input Area */}
                  <div className="input-area">
                    <div className="input-container">
                      <textarea
                        value={inputText}
                        onChange={(e) => setInputText(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Ask me about your Dockerfile, Kubernetes configs, CI/CD pipeline, or anything DevOps related..."
                        className="input message-input"
                        rows={3}
                      />
                      <button
                        onClick={handleSendMessage}
                        disabled={!inputText.trim() || isLoading}
                        className="btn btn-primary send-btn"
                      >
                        <Send size={20} />
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'suggestions' && (
                <div className="tab-content">
                  <h2>AI Suggestions</h2>
                  <div className="suggestions-grid">
                    <div className="card suggestion-card">
                      <h3>Dockerfile Optimization</h3>
                      <p>Multi-stage builds, layer caching, and security best practices</p>
                    </div>
                    <div className="card suggestion-card">
                      <h3>Kubernetes Configs</h3>
                      <p>Resource limits, health checks, and scaling policies</p>
                    </div>
                    <div className="card suggestion-card">
                      <h3>CI/CD Pipeline</h3>
                      <p>GitHub Actions optimization and deployment strategies</p>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'monitoring' && (
                <div className="tab-content">
                  <h2>Monitoring & Alerts</h2>
                  <div className="monitoring-grid">
                    <div className="card monitoring-card">
                      <h3>Prometheus Alerts</h3>
                      <p>Custom alert rules for your infrastructure</p>
                    </div>
                    <div className="card monitoring-card">
                      <h3>Grafana Dashboards</h3>
                      <p>Pre-built dashboard configurations</p>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'testing' && (
                <div className="tab-content">
                  <h2>Testing & Quality</h2>
                  <div className="testing-grid">
                    <div className="card testing-card">
                      <h3>Unit Tests</h3>
                      <p>Automated test generation for your codebase</p>
                    </div>
                    <div className="card testing-card">
                      <h3>Integration Tests</h3>
                      <p>End-to-end testing scenarios</p>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'settings' && (
                <div className="tab-content">
                  <h2>Settings</h2>
                  <div className="settings-grid">
                    <div className="card">
                      <h3>API Configuration</h3>
                      <p>Configure your backend API endpoints</p>
                    </div>
                    <div className="card">
                      <h3>Preferences</h3>
                      <p>Customize your experience</p>
                    </div>
                  </div>
                </div>
              )}
            </main>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
