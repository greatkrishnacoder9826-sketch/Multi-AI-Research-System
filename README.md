# 🔬 Astavakara — Multi-Agent AI Research System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-0A0A0F?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge"/>
</p>

<p align="center">
  A powerful <strong>Multi-Agent AI Research System</strong> that automatically searches the web, scrapes content, writes detailed research reports, and critiques them — all in one pipeline.
</p>

---

## ✨ Features

- 🔍 **Search Agent** — Finds recent & reliable sources using Tavily Search API
- 📖 **Reader Agent** — Scrapes and extracts deep content from top URLs
- ✍️ **Writer Chain** — Generates structured, professional research reports
- 🧠 **Critic Chain** — Reviews and scores the report with constructive feedback
- 🎨 **Clean Streamlit UI** — Dark themed, step-by-step visual pipeline
- ⬇️ **Download Report** — Export your research as a `.txt` file

---

## 🖥️ Demo

> Enter any topic → Hit Research → Watch 4 agents work in real-time!

```
Topic: "Future of Quantum Computing"
→ Step 1: Search Agent finds 5 sources
→ Step 2: Reader Agent scrapes best URL  
→ Step 3: Writer drafts full report
→ Step 4: Critic scores & reviews
```

---

## 🏗️ Project Structure

```
Multi_agent_system/
│
├── app.py              # Streamlit UI (main entry point)
├── agents.py           # LLM agents + writer/critic chains
├── tools.py            # web_search & scrape_url tools
├── pipeline.py         # CLI pipeline runner
├── .env                # API keys (not committed)
├── requirements.txt    # All dependencies
└── README.md           # This file
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Multi_agent_system.git
cd Multi_agent_system
```

### 2. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Keys

Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your free API keys:
- 🔑 **Groq** (Free) → [console.groq.com](https://console.groq.com)
- 🔑 **Tavily** (Free) → [tavily.com](https://tavily.com)

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🤖 Agent Architecture

```
User Input (Topic)
       │
       ▼
┌─────────────────┐
│  Search Agent   │  ← Tavily Search API + LLM
│  (LangGraph)    │
└────────┬────────┘
         │ search_results
         ▼
┌─────────────────┐
│  Reader Agent   │  ← BeautifulSoup Scraper + LLM
│  (LangGraph)    │
└────────┬────────┘
         │ scraped_content
         ▼
┌─────────────────┐
│  Writer Chain   │  ← LCEL Chain (Prompt → LLM → Parser)
│  (LangChain)    │
└────────┬────────┘
         │ report
         ▼
┌─────────────────┐
│  Critic Chain   │  ← LCEL Chain (Score + Feedback)
│  (LangChain)    │
└─────────────────┘
         │
         ▼
    Final Output
  (Report + Score)
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core language |
| **Streamlit** | Web UI |
| **LangChain** | LLM chains & tools |
| **LangGraph** | ReAct Agents |
| **Groq + LLaMA 3.3** | Free LLM (llama-3.3-70b-versatile) |
| **Tavily** | Web search API |
| **BeautifulSoup4** | Web scraping |
| **Python-dotenv** | Environment variables |

---

## 📦 Requirements

```
langchain
langchain-core
langchain-community
langchain-openai
langchain-groq
langgraph
tavily-python
beautifulsoup4
requests
streamlit
python-dotenv
rich
openai
```

---

## 🚀 Usage

### Via Streamlit UI (Recommended)
```bash
streamlit run app.py
```

### Via CLI
```bash
python pipeline.py
# Enter a research topic when prompted
```

---

## 📄 Output Format

The Writer Agent produces a structured report:

```
- Introduction
- Key Findings (minimum 3 points)
- Conclusion  
- Sources (all URLs)
```

The Critic Agent evaluates:
```
Score: X/10
Strengths: ...
Areas to Improve: ...
One line verdict: ...
```

---

## 🔐 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLaMA model | ✅ Yes |
| `TAVILY_API_KEY` | Tavily search API key | ✅ Yes |

---

## 👨‍💻 Author

**Krishna Great**  
Data Science & ML Student  

---

## ⭐ Support

Agar yeh project helpful laga toh **Star ⭐** zaroor karo!

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).
