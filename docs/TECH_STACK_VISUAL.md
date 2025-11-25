# 🎨 Visual Tech Stack

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph Input
        USER[👤 User Input<br/>Test Scenario]
    end

    subgraph Processing
        PLAN[🧠 Planner<br/>Explore & Document]
        GEN[⚙️ Generator<br/>Create Test Code]
        HEAL[🔧 Healer<br/>Fix & Validate]
    end

    subgraph Storage
        RAG[(📚 ChromaDB<br/>Knowledge Base)]
        FILES[📁 Test Files<br/>& Plans]
    end

    subgraph Output
        RESULT[✅ Working Test<br/>Ready to Run]
    end

    USER --> PLAN
    PLAN -->|Test Plan| GEN
    PLAN -.->|Store Knowledge| RAG
    RAG -.->|Query Knowledge| PLAN
    GEN -->|Test File| HEAL
    GEN -->|Save| FILES
    RAG -.->|Code Patterns| GEN
    HEAL -->|Fixed Test| RESULT
    RAG -.->|Known Fixes| HEAL
    HEAL -.->|Store Fix| RAG

    style USER fill:#61dafb,stroke:#333,stroke-width:3px
    style PLAN fill:#ff6b6b,stroke:#333,stroke-width:2px
    style GEN fill:#4ecdc4,stroke:#333,stroke-width:2px
    style HEAL fill:#95e1d3,stroke:#333,stroke-width:2px
    style RAG fill:#f38181,stroke:#333,stroke-width:3px
    style RESULT fill:#51cf66,stroke:#333,stroke-width:3px
```

---

## Tech Stack Layers

```mermaid
graph TB
    subgraph "Layer 1: Presentation"
        L1A[React UI]
        L1B[TypeScript]
        L1C[CSS]
    end

    subgraph "Layer 2: API"
        L2A[FastAPI]
        L2B[SSE Streaming]
        L2C[REST Endpoints]
    end

    subgraph "Layer 3: Orchestration"
        L3A[CrewAI Framework]
        L3B[Multi-Agent System]
        L3C[Task Management]
    end

    subgraph "Layer 4: Intelligence"
        L4A[OpenAI GPT-4o-mini]
        L4B[CrewAI Framework]
        L4C[Prompt Engineering]
    end

    subgraph "Layer 5: Knowledge"
        L5A[ChromaDB Vectors]
        L5B[RAG Retrieval]
        L5C[Semantic Search]
    end

    subgraph "Layer 6: Automation"
        L6A[Playwright]
        L6B[MCP Protocol]
        L6C[Browser Control]
    end

    subgraph "Layer 7: Storage"
        L7A[Filesystem]
        L7B[Vector DB]
        L7C[JSON State]
    end

    L1A --> L2A
    L1B --> L2B
    L1C --> L2C
    
    L2A --> L3A
    L2B --> L3B
    L2C --> L3C
    
    L3A --> L4A
    L3B --> L4B
    L3C --> L4C
    
    L4A --> L5A
    L4B --> L5B
    L4C --> L5C
    
    L5A --> L6A
    L5B --> L6B
    L5C --> L6C
    
    L6A --> L7A
    L6B --> L7B
    L6C --> L7C

    style L1A fill:#61dafb
    style L2A fill:#009688
    style L3A fill:#673ab7
    style L4A fill:#ff9800
    style L5A fill:#f38181
    style L6A fill:#e74c3c
    style L7A fill:#34495e
```

---

## 📸 How to Use

### View in GitHub
GitHub automatically renders Mermaid diagrams when you view this file in your repository.

### Export as Image
1. **Using Mermaid Live Editor:**
   - Go to https://mermaid.live
   - Copy any diagram code above
   - Click "Export" → PNG/SVG
   - Use for presentations or LinkedIn posts

2. **Using VS Code:**
   - Install "Markdown Preview Mermaid Support" extension
   - Open this file and preview (Cmd+Shift+V)
   - Right-click diagram → Copy as image

### For LinkedIn Posts

**Example Post:**
```
🚀 Built an AI-powered Test Automation Platform with multi-agent orchestration!

🏗️ Tech Stack:
• React + TypeScript (Frontend)
• FastAPI + Python (Backend)  
• CrewAI + GPT-4o-mini (AI Agents)
• ChromaDB (Vector RAG)
• Playwright (Browser Automation)
• MCP Protocol (Tool Integration)

💡 How it works:
1️⃣ Planner Agent explores your app
2️⃣ Generator Agent creates test code
3️⃣ Healer Agent fixes failing tests automatically

✅ Self-healing tests
✅ RAG prevents redundant work
✅ Real-time workflow updates

[Include diagram image]

#AI #TestAutomation #Python #React #CrewAI #Playwright
```

---

*Ready to showcase! 🚀*
