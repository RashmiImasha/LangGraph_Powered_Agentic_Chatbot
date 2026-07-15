# LangGraph powered Multi-Tool Agentic Chatbot with Human-in-the-Loop Approval

A conversational AI agent built with **LangGraph** and **Google Gemini**, capable of reasoning about which tool to use, retrieving answers from uploaded PDFs, searching the web, checking live weather and stock prices, performing mathematical calculations, and **pausing for human approval** before executing a simulated stock purchase.

The application features **persistent multi-thread conversations**, allowing users to switch between previous chat sessions while maintaining conversation state using LangGraph's SQLite checkpointer.

---

## ✨ Features

- 🤖 **Tool-Routing AI Agent**
  - Uses LangGraph to determine whether to answer directly or invoke an appropriate tool.
  - Routes execution through `tools_condition`.

- 📄 **Retrieval-Augmented Generation (RAG)**
  - Upload PDF documents directly from the chat interface.
  - Documents are chunked using `RecursiveCharacterTextSplitter`.
  - Embedded with **Google Gemini Embeddings**.
  - Stored locally in **FAISS** for semantic retrieval.

- 🌐 **Web Search**
  - Retrieves up-to-date information using **Tavily Search**.

- 🧮 **Calculator**
  - Performs mathematical calculations using a sandboxed evaluator.

- 🌦️ **Live Weather**
  - Fetches current weather conditions using the OpenWeatherMap API.

- 📈 **Stock Price Lookup**
  - Retrieves live stock prices through Alpha Vantage.

- 👤 **Human-in-the-Loop Approval**
  - Simulated stock purchases require explicit human approval.
  - Uses LangGraph's `interrupt()` mechanism.
  - Streamlit displays **Approve** and **Reject** buttons.
  - Workflow resumes using `Command(resume=...)`.

- 💾 **Persistent Conversations**
  - Every conversation is assigned a unique thread ID.
  - Chat history is stored in SQLite using `SqliteSaver`.
  - Previous conversations can be reopened from the sidebar.

- ⚡ **Streaming Responses**
  - Assistant responses stream token-by-token.
  - Tool execution is displayed with live status updates.

---

## 🏗️ Architecture

```text
User (Streamlit)
        │
        ▼
 chat_node (Gemini + Tools)
        │
        ▼
 tools_condition
        │
   ┌────┴────┐
   │         │
 Tool Node   END
   │
   ├── Web Search
   ├── Calculator
   ├── Weather
   ├── Stock Price
   ├── PDF RAG
   └── Purchase Stock
          │
          ▼
     interrupt()
          │
          ▼
 Human Approval
 (Approve / Reject)
          │
          ▼
 Command(resume)
          │
          ▼
      chat_node
```

---

## 🛠️ Tech Stack

Agent Framework : LangGraph 
LLM : Google Gemini 2.5 Flash 
Embeddings : Google Gemini Embeddings 
Vector Database : FAISS 
Web Search : Tavily 
Weather API : OpenWeatherMap 
Stock API : Alpha Vantage 
Frontend : Streamlit 
Persistence : SQLite (`langgraph-checkpoint-sqlite`) 

---

## 📁 Project Structure

```text
.
├── backend.py          # LangGraph graph, tools, state management
├── main.py             # Streamlit application
├── requirements.txt
├── pyproject.toml
├── Dockerfile
└── chatbot.db          # Generated automatically
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/RashmiImasha/LangGraph_Powered_Agentic_Chatbot.git

cd LangGraph_Powered_Agentic_Chatbot
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
```

---

### 4. Run the Application

```bash
streamlit run main.py
```

Open your browser and navigate to:

```
https://langgraph-powered-agentic-chatbot.onrender.com/
```

---

## 💡 Usage

### General Chat

Simply type a message. The AI agent determines whether to answer directly or invoke one of its available tools.

---

### Upload a PDF

1. Upload a PDF using the chat input.
2. The document is indexed into a FAISS vector store.
3. Ask questions about the uploaded document.

Example:

```
Summarize this report.

What was Tesla's net income in 2024?

Who is the CEO mentioned in this document?
```

---

### Search the Web

Ask questions requiring current information.

Example:

```
Latest AI news

Who won today's cricket match?

Current Bitcoin price
```

---

### Weather Information

Example:

```
What's the weather in Colombo?

Current weather in Tokyo
```

---

### Stock Information

Example:

```
Price of AAPL

Current TSLA stock price
```

---

### Human-in-the-Loop Purchase

Example:

```
Buy 10 shares of AAPL
```

The workflow will:

1. Pause execution.
2. Display **Approve** and **Reject** buttons.
3. Resume only after user approval.

---

### Conversation History

- Start a new conversation.
- Switch between previous chats using the sidebar.
- Conversation state is restored automatically.

---


**Rashmi Imasha**

GitHub: https://github.com/RashmiImasha
