# 🎓 AI Student Career & Research Assistant

An AI-powered multi-tool assistant designed to help students and job seekers research careers, explore job opportunities, analyze companies, compare salaries, access real-time information, analyze documents, and build personalized learning roadmaps.

The application is built using **LangGraph**, **LangChain**, **Groq LLM**, **FastAPI**, **Streamlit**, and **SQLite**, with an **Orchestrator–Worker architecture** and both short-term and long-term memory.

---

## 📌 Project Overview

Students often need information from multiple sources when planning their careers, such as:

- Skills required for a career
- Current job opportunities
- Company information
- Salary information
- Learning roadmaps
- Financial information
- News and web research
- Document or resume analysis

Instead of using multiple applications separately, this project combines these capabilities into a single AI assistant.

The system receives a user query, breaks complex requests into smaller tasks, selects appropriate tools, collects the results, and generates a final response.

---

## ✨ Key Features

### 🤖 Multi-Agent Workflow

The application uses a LangGraph workflow based on an:

**Orchestrator → Worker → Collector**

architecture.

The Orchestrator analyzes complex user requests and breaks them into smaller tasks.

The Worker executes the tasks using appropriate tools.

The Collector combines the results into a clear final response.

---

### 🛠️ Multi-Tool Support

The assistant supports multiple tools, including:

- 🔎 Web Search
- 📚 Wikipedia
- 📰 News Search
- 💰 Finance / Stock Information
- 🌤️ Weather Information
- 🧮 Calculator
- 💱 Currency Converter
- 🐍 Python / Data Analysis
- 💼 Career Analysis
- 🔍 Job / Company Search
- 📄 PDF / Document Reader

These tools allow the assistant to handle both general questions and specialized research tasks.

---

## 🧠 Memory System

The project includes two types of memory.

### Short-Term Memory

Short-term memory maintains context within the current conversation.

This allows users to ask follow-up questions without repeating all previous information.

Example:

```text
User: I want to become a Data Scientist.

User: What skills should I learn first?
```

The assistant can understand that the second question refers to the Data Scientist career discussed earlier.

### Long-Term Memory

Long-term memory stores useful user preferences and career information across conversations.

Examples include:

- Career goal
- Learning preference
- Relevant persistent user preferences

This allows the assistant to provide more personalized responses.

---

## 💬 Persistent Recent Chats

The application stores conversation history using SQLite.

Users can:

- Start a new conversation
- View recent conversations
- Open previous conversations
- Continue previous chats
- Delete conversations
- Use automatically generated conversation titles

Conversation history remains available even when the Streamlit session changes.

---

## 📄 PDF / Document Analysis

Users can upload PDF documents through the Streamlit interface.

The assistant can use the document reader tool for tasks such as:

```text
Summarize the uploaded PDF in 5 bullet points.
```

Possible use cases include:

- Resume analysis
- Document summarization
- Extracting important information
- Career-related document review

---

## 🏗️ System Architecture

![System Architecture](assets/architecture.png)

The main application flow is:

```text
User
  │
  ▼
Streamlit Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
LangGraph Workflow
  │
  ├── Memory
  │     ├── Short-Term Memory
  │     └── Long-Term Memory
  │
  ▼
Orchestrator
  │
  ▼
Worker
  │
  ├── Web Search
  ├── Wikipedia
  ├── News Search
  ├── Finance / Stock
  ├── Weather
  ├── Calculator
  ├── Currency Converter
  ├── Python / Data Analysis
  ├── Career Analysis
  ├── Job / Company Search
  └── PDF Reader
  │
  ▼
Collector
  │
  ▼
Final Response
  │
  ▼
Streamlit User Interface
```

A visual architecture diagram can also be added to the repository.

---

## 🔄 LangGraph Workflow

A simplified workflow:

```text
START
  │
  ▼
Memory Processing
  │
  ▼
Orchestrator
  │
  ▼
Worker
  │
  ▼
Collector
  │
  ▼
END
```

### Orchestrator

Responsible for:

- Understanding the user query
- Breaking complex queries into subtasks
- Preparing tasks for execution

### Worker

Responsible for:

- Executing subtasks
- Selecting appropriate tools
- Collecting tool results

### Collector

Responsible for:

- Combining worker results
- Reducing duplicate information
- Formatting the final response
- Applying grounding rules to time-sensitive information

---

## 🛡️ Error Handling

The backend includes error handling for external AI API limitations.

For example, when the LLM provider reaches its usage limit, the application displays a user-friendly message instead of exposing an internal server error.

Example:

```text
⚠️ The AI service has temporarily reached its usage limit.
Please wait a few minutes and try again.
```

---

## 💻 Technology Stack

### AI / Agent Framework

- LangChain
- LangGraph
- Groq LLM

### Backend

- FastAPI
- Uvicorn
- Python

### Frontend

- Streamlit

### Storage

- SQLite

### External Tools / Data Sources

- Web search
- Wikipedia
- Finance / stock data
- Weather data
- Currency information
- Job / company search
- PDF document processing

---

## 📂 Project Structure

Example project structure:

```text
FINAL_PROJECT_AIML_9.9.2026/
│
├── backend/
│   └── app/
│       ├── graph/
│       │   ├── state.py
│       │   ├── orchestrator.py
│       │   ├── worker.py
│       │   ├── collector.py
│       │   └── workflow.py
│       │
│       ├── llm/
│       │   └── groq_llm.py
│       │
│       ├── memory/
│       │   ├── short_term_memory.py
│       │   ├── long_term_memory.py
│       │   └── chat_history.py
│       │
│       ├── tools/
│       │   └── ...
│       │
│       └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── uploads/
│
├── tests/
│   └── ...
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> The exact structure may vary slightly depending on the final implementation.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd FINAL_PROJECT_AIML_9.9.2026
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do **not** upload the real `.env` file or API keys to GitHub.

The repository `.gitignore` should exclude `.env`.

---

## ▶️ Running the Application

The application requires the FastAPI backend and Streamlit frontend to run.

### Terminal 1 — Start FastAPI

From the project root:

```bash
uvicorn backend.app.main:app --reload
```

The API will normally run at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2 — Start Streamlit

Open another terminal, activate the virtual environment, then run:

```bash
streamlit run frontend/app.py
```

The Streamlit application will normally open at:

```text
http://localhost:8501
```

---

## 💡 Example Prompts

### Career Research

```text
What skills do I need to become a Data Scientist in Malaysia?
```

### Multi-Tool Career Research

```text
Find Data Scientist jobs in Malaysia, identify the main skills required,
and give me a short learning roadmap.
```

### Career Comparison

```text
Compare the key skills required for a Data Scientist and AI Engineer.
```

### Finance

```text
What is the stock information for NVIDIA?
```

### Currency

```text
Convert 1000 USD to MYR.
```

### Weather

```text
What is the weather in Kuala Lumpur?
```

### Calculator

```text
Calculate 125 * 48.
```

### Document Analysis

```text
Summarize the uploaded PDF in 5 bullet points.
```

### Memory

```text
What do you know about my career goal and learning preference?
```

---

## 🧪 Testing

Individual tools and components can be tested from the `tests/` directory.

Example:

```bash
python -m tests.test_career_tools
```

Other tests can be added for:

- Memory
- Worker tools
- Job/company search
- PDF processing
- Conversation history
- LangGraph workflow

---

## 🔒 Security Notes

Sensitive information should never be committed to GitHub.

The following should remain excluded:

```text
.env
venv/
data/*.db
data/uploads/
__pycache__/
```

API keys must be stored using environment variables.

---

## 🚀 Future Improvements

Possible future enhancements include:

- Google Drive integration
- Gmail / Email integration
- Additional career APIs
- Improved job-search grounding
- Cloud deployment
- Authentication
- More advanced document analysis
- Additional memory management
- Improved observability and logging

---

## 🎯 Project Goal

The goal of this project is to demonstrate how Agentic AI can combine:

- LLM reasoning
- Tool usage
- Multi-step task orchestration
- External information retrieval
- Memory
- Document processing
- Backend APIs
- Persistent conversations
- Interactive user interfaces

into one practical AI application for student career and research assistance.

---

## 👩‍💻 Author

**Liyana Ishak**

AI/ML Final Project  
Yayasan Peneraju AI/ML Programme