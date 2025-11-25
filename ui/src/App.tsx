import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

interface RAGStats {
  total_items: number;
  test_fixes: number;
  code_patterns: number;
  test_plans: number;
  application_knowledge: number;
}

interface AgentEvent {
  agent: string;
  status: string;
  message: string;
  progress?: number;
}

interface TestPlan {
  filename: string;
  path: string;
  relative_path: string;
  created: string;
  size: number;
}

interface TestFile {
  filename: string;
  path: string;
  relative_path: string;
  created: string;
  modified: string;
  size: number;
}

function App() {
  const [scenario, setScenario] = useState('Create a new account in Salesforce');
  const [selectedAgent, setSelectedAgent] = useState('full');
  const [testFile, setTestFile] = useState('');
  const [selectedTestFiles, setSelectedTestFiles] = useState<string[]>([]);
  const [testPlans, setTestPlans] = useState<TestPlan[]>([]);
  const [testFiles, setTestFiles] = useState<TestFile[]>([]);
  const [workflowId, setWorkflowId] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [ragStats, setRagStats] = useState<RAGStats | null>(null);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [currentEvent, setCurrentEvent] = useState<AgentEvent | null>(null);
  const [apiMode, setApiMode] = useState<string>('demo');
  const [apiKeyConfigured, setApiKeyConfigured] = useState<boolean | null>(null);
  const [agentStates, setAgentStates] = useState({
    planner: { status: 'idle', progress: 0, message: '' },
    generator: { status: 'idle', progress: 0, message: '' },
    healer: { status: 'idle', progress: 0, message: '' }
  });

  // Fetch RAG stats, health, test plans, and test files on mount
  useEffect(() => {
    fetchRAGStats();
    fetchHealth();
    fetchTestPlans();
    fetchTestFiles();
  }, []);

  const fetchRAGStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/rag/stats`);
      setRagStats(response.data);
    } catch (error) {
      console.error('Error fetching RAG stats:', error);
    }
  };

  const fetchHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/health`);
      setApiMode(response.data.mode || 'demo');
      setApiKeyConfigured(response.data.api_key_configured);
    } catch (error) {
      console.error('Error fetching health:', error);
    }
  };

  const fetchTestPlans = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/test-plans`);
      setTestPlans(response.data.test_plans || []);
    } catch (error) {
      console.error('Error fetching test plans:', error);
    }
  };

  const fetchTestFiles = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/test-files`);
      setTestFiles(response.data.test_files || []);
    } catch (error) {
      console.error('Error fetching test files:', error);
    }
  };

  const handleTestFileToggle = (filePath: string) => {
    setSelectedTestFiles(prev => {
      if (prev.includes(filePath)) {
        return prev.filter(f => f !== filePath);
      } else {
        return [...prev, filePath];
      }
    });
  };

  const startWorkflow = async () => {
    if (!scenario.trim()) return;

    setIsRunning(true);
    setEvents([]);
    setCurrentEvent(null);

    try {
      // Start workflow
      const response = await axios.post(`${API_BASE}/api/workflow/start`, {
        scenario: scenario,
        agent: selectedAgent,
        test_file: selectedAgent === 'healer' 
          ? (selectedTestFiles.length > 0 ? selectedTestFiles.join(',') : null)
          : (testFile || null)
      });

      const wfId = response.data.workflow_id;
      setWorkflowId(wfId);

      // Connect to SSE stream
      const eventSource = new EventSource(`${API_BASE}/api/workflow/${wfId}/stream`);

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setCurrentEvent(data);
        setEvents(prev => [...prev, data]);

        // Update agent states
        if (data.agent && data.agent !== 'workflow') {
          setAgentStates(prev => ({
            ...prev,
            [data.agent]: {
              status: data.status,
              progress: data.progress || 0,
              message: data.message
            }
          }));
        }

        // If workflow completed, close connection
        if (data.status === 'completed' && data.agent === 'workflow') {
          eventSource.close();
          setIsRunning(false);
          fetchRAGStats(); // Refresh stats
        }
      };

      eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        eventSource.close();
        setIsRunning(false);
      };

    } catch (error) {
      console.error('Error starting workflow:', error);
      setIsRunning(false);
    }
  };

  const getStatusEmoji = (status: string) => {
    switch (status) {
      case 'started': return '🟢';
      case 'thinking': return '🤔';
      case 'progress': return '⚙️';
      case 'completed': return '✅';
      case 'error': return '❌';
      default: return '⏸️';
    }
  };

  const getAgentColor = (agent: string) => {
    switch (agent) {
      case 'planner': return '#8b5cf6'; // purple
      case 'generator': return '#3b82f6'; // blue
      case 'healer': return '#10b981'; // green
      default: return '#6b7280'; // gray
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 Test Automation Agents</h1>
        <p className="subtitle">    Next-Gen Test Automation</p>
      </header>

      <div className="container">
        {/* RAG Stats Panel */}
        {ragStats && (
          <div className="rag-stats">
            <h3>🧠 Knowledge Base</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-value">{ragStats.total_items}</div>
                <div className="stat-label">Total Items</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{ragStats.test_fixes}</div>
                <div className="stat-label">Test Fixes</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{ragStats.code_patterns}</div>
                <div className="stat-label">Code Patterns</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{ragStats.test_plans}</div>
                <div className="stat-label">Test Plans</div>
              </div>
              <div className="stat-item">
                <div className="stat-value">{ragStats.application_knowledge}</div>
                <div className="stat-label">App Knowledge</div>
              </div>
            </div>
          </div>
        )}

        {/* API Mode Indicator */}
        <div className={`mode-indicator ${apiMode === 'real' ? 'mode-real' : 'mode-demo'}`}>
          <div className="mode-badge">
            {apiMode === 'real' ? '🚀 LIVE MODE' : '🎭 DEMO MODE'}
          </div>
          <div className="mode-info">
            {apiMode === 'real' ? (
              apiKeyConfigured ? 
                'Using actual AI agents' : 
                '⚠️ API key not configured'
            ) : (
              'Simulated agent execution'
            )}
          </div>
        </div>

        {/* Input Section */}
        <div className="input-section">
          <h3>💬 What should I test?</h3>
          <div className="input-group">
            <input
              type="text"
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              placeholder="Enter test scenario..."
              disabled={isRunning}
              className="scenario-input"
            />
            <select
              value={selectedAgent}
              onChange={(e) => setSelectedAgent(e.target.value)}
              disabled={isRunning}
              className="agent-select"
            >
              <option value="full">🤖 Full Workflow (All Agents)</option>
              <option value="planner">🧠 Planner Only</option>
              <option value="generator">⚙️ Generator Only</option>
              <option value="healer">🔧 Healer Only</option>
            </select>
            {selectedAgent === 'generator' && (
              <select
                value={testFile}
                onChange={(e) => setTestFile(e.target.value)}
                disabled={isRunning}
                className="file-input"
              >
                <option value="">Select a test plan...</option>
                {testPlans.map((plan) => (
                  <option key={plan.filename} value={plan.relative_path}>
                    {plan.filename} ({new Date(plan.created).toLocaleString()})
                  </option>
                ))}
              </select>
            )}
            {selectedAgent === 'healer' && (
              <div className="test-files-selector">
                <div className="test-files-header">
                  Select test files to fix ({selectedTestFiles.length} selected):
                </div>
                <div className="test-files-list">
                  {testFiles.length === 0 ? (
                    <div className="no-files">No test files found</div>
                  ) : (
                    testFiles.map((file) => (
                      <label key={file.relative_path} className="test-file-item">
                        <input
                          type="checkbox"
                          checked={selectedTestFiles.includes(file.relative_path)}
                          onChange={() => handleTestFileToggle(file.relative_path)}
                          disabled={isRunning}
                        />
                        <span className="test-file-name">{file.filename}</span>
                        <span className="test-file-meta">
                          Modified: {new Date(file.modified).toLocaleString()}
                        </span>
                      </label>
                    ))
                  )}
                </div>
              </div>
            )}
            <button
              onClick={startWorkflow}
              disabled={isRunning || !scenario.trim()}
              className="start-button"
            >
              {isRunning ? '⏳ Running...' : '▶️ Start'}
            </button>
          </div>
        </div>

        {/* Agent Cards - Show all 3 agents as robots */}
        <div className="agents-container">
          {/* Planner Agent */}
          <div className={`robot-card ${agentStates.planner.status !== 'idle' ? 'active' : ''}`}>
            <div className={`robot-icon ${agentStates.planner.status === 'thinking' || agentStates.planner.status === 'progress' ? 'working' : ''}`}>
              🧠
            </div>
            <h4>Planner</h4>
            <div className="robot-progress-bar">
              <div 
                className="robot-progress-fill" 
                style={{ 
                  width: `${agentStates.planner.progress}%`,
                  backgroundColor: '#8b5cf6'
                }}
              />
            </div>
            <p className="robot-status">{agentStates.planner.status !== 'idle' ? agentStates.planner.message : 'Ready'}</p>
          </div>

          {/* Generator Agent */}
          <div className={`robot-card ${agentStates.generator.status !== 'idle' ? 'active' : ''}`}>
            <div className={`robot-icon ${agentStates.generator.status === 'thinking' || agentStates.generator.status === 'progress' ? 'working' : ''}`}>
              ⚙️
            </div>
            <h4>Generator</h4>
            <div className="robot-progress-bar">
              <div 
                className="robot-progress-fill" 
                style={{ 
                  width: `${agentStates.generator.progress}%`,
                  backgroundColor: '#3b82f6'
                }}
              />
            </div>
            <p className="robot-status">{agentStates.generator.status !== 'idle' ? agentStates.generator.message : 'Ready'}</p>
          </div>

          {/* Healer Agent */}
          <div className={`robot-card ${agentStates.healer.status !== 'idle' ? 'active' : ''}`}>
            <div className={`robot-icon ${agentStates.healer.status === 'thinking' || agentStates.healer.status === 'progress' ? 'working' : ''}`}>
              🔧
            </div>
            <h4>Healer</h4>
            <div className="robot-progress-bar">
              <div 
                className="robot-progress-fill" 
                style={{ 
                  width: `${agentStates.healer.progress}%`,
                  backgroundColor: '#10b981'
                }}
              />
            </div>
            <p className="robot-status">{agentStates.healer.status !== 'idle' ? agentStates.healer.message : 'Ready'}</p>
          </div>
        </div>

        {/* Activity Log */}
        {events.length > 0 && (
          <div className="activity-log">
            <h3>📡 Activity Log</h3>
            <div className="log-container">
              {events.slice().reverse().map((event, idx) => (
                <div key={idx} className="log-item">
                  <span className="log-agent" style={{ color: getAgentColor(event.agent) }}>
                    {event.agent}:
                  </span>
                  <span className="log-message">{event.message}</span>
                  <span className="log-status">{getStatusEmoji(event.status)}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Completion Message */}
        {workflowId && !isRunning && events.length > 0 && (
          <div className="completion-message">
            <h2>✅ Workflow Complete!</h2>
            <p>Workflow ID: <code>{workflowId}</code></p>
            <button onClick={() => {
              setEvents([]);
              setCurrentEvent(null);
              setWorkflowId(null);
            }} className="reset-button">
              Run Another Test
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
