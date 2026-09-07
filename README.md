# ResearchMind — AI Multi-Agent Research Assistant

ResearchMind is an AI-powered web application that turns a single topic into a complete, fact-checked research report. It orchestrates four specialized AI agents — **Search**, **Reader**, **Writer**, and **Critic** — that work in sequence to gather live information from the web, extract deeper context, draft a structured report, and critically review the output before handing it back to the user.

Built for the 29–30 August Hackathon.

---

##  Problem Statement

Researching any topic thoroughly today means juggling multiple tabs, sifting through search results, reading full articles, and manually synthesizing everything into a coherent, well-structured write-up — a process that is slow, repetitive, and easy to get wrong.

**ResearchMind** solves this by automating the entire research workflow with a pipeline of cooperating AI agents, each responsible for one stage of the process, so a user can go from "a topic I want to understand" to "a structured, reviewed report" in a single click.

---

##  Features

- **Four-agent research pipeline**
  -  **Search Agent** — queries the live web (via Tavily) for recent, relevant sources on the topic.
  -  **Reader Agent** — scrapes and extracts clean, deep content from the most relevant source found.
  -  **Writer Chain** — synthesizes the gathered research into a structured report (Introduction, Key Findings, Conclusion, Sources).
  -  **Critic Chain** — independently reviews the report, scores it out of 10, and lists strengths and areas to improve.
- **Live pipeline visualization** — a real-time UI panel showing each agent's status (waiting / running / done) as the pipeline executes.
- **Clean, modern web interface** built with Streamlit, including example topic chips for quick testing.
- **Downloadable output** — export the final report as a Markdown (`.md`) file.
- **Actual AI agent usage** — powered by [LangChain](https://www.langchain.com/) agents and [GEMINI AI](https://gemini.google.com/) (`gemini-3.5-flash-lite`) for reasoning, tool use, and text generation.

### Why RAG Is Useful in ResearchMind

Without RAG, a simple pipeline may look like:

```text
Web Sources
    ↓
Scraped Content
    ↓
Entire Content → LLM
    ↓
Generated Report
```

As the number and size of sources increase, sending everything to the LLM becomes inefficient. It can also introduce irrelevant information into the generation step.

With RAG, the workflow becomes:

```text
Web Sources
    ↓
Reader Agent
    ↓
Research Documents
    ↓
Chunking + Embeddings
    ↓
Vector Store
    ↓
Relevant Retrieval
    ↓
Writer / Critic LLM
    ↓
Focused Research Report
```

RAG is useful in ResearchMind because it:

- **Reduces irrelevant context** — the LLM receives the passages most relevant to the research question.
- **Improves scalability** — larger collections of articles can be handled without passing every document to the model at once.
- **Improves evidence grounding** — generated content can be based on retrieved research passages rather than relying only on the model's internal knowledge.
- **Reduces context-window pressure** — only the most useful chunks need to be included in each generation request.
- **Makes multi-source research practical** — information from many scraped sources can be indexed and selectively retrieved.
- **Supports better citations** — retrieved chunks can retain source metadata such as title and URL, making claim-to-source linking easier.
- **Creates a reusable research knowledge base** — indexed research can potentially be searched again for follow-up questions or future reports.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | [Streamlit](https://streamlit.io/) |
| Agent Framework | [LangChain](https://www.langchain.com/) (`create_agent`) |
| Web Search | [Tavily API](https://tavily.com/) |
| Web Scraping | `requests` + `BeautifulSoup4` |
| RAG / Retrieval | Embeddings + Vector Store |
| Configuration | `python-dotenv` |
| Language | Python 3.10+ |

> **Note:** The RAG layer is designed to sit between the Reader stage and the Writer/Critic stages. The exact embedding model and vector store can be changed depending on the implementation.

---

##  Project Structure

```
multi_agent_news/
├── agents.py         # Agent + chain definitions (search, reader, writer, critic)
├── tools.py           # Tool implementations: web_search (Tavily), scrape_url (BeautifulSoup)
├── pipeline.py        # Orchestrates the 4-agent pipeline end-to-end (CLI runnable)
├── rag.py             # Vector Store, Chunking, Embedding
├── app.py             # Streamlit web application (UI + pipeline integration)
├── requirements.txt      # Python dependencies
├── .env             # API keys (not committed — see setup below)
├── .gitignore
└── README.md
```

---

## Steps

1. Enter a research topic in the input box, or select an example topic.
2. Click **Run research →**.
3. Watch the four-agent pipeline progress in real time.
4. The **Search Agent** finds relevant web sources.
5. The **Reader Agent** extracts deeper content from the sources.
6. The **RAG layer** can chunk, embed, index, and retrieve the most relevant research passages.
7. The **Writer Chain** generates a structured research report using the retrieved evidence.
8. The **Critic Chain** evaluates the report and provides a score and feedback.
9. Read the **Final Research Report** and **Critic Feedback**.

---

# ResearchMind Architecture

```text
                         USER TOPIC
                             │
                             ▼
                    ┌─────────────────┐
                    │  SEARCH AGENT   │
                    │     Tavily      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  READER AGENT   │
                    │ Web Scraping    │
                    └────────┬────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │     RAG PIPELINE     │
                  │                      │
                  │ Chunk → Embed →      │
                  │ Store → Retrieve     │
                  └──────────┬───────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   WRITER CHAIN  │
                    │ GEMINI AI LLM   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   CRITIC CHAIN  │
                    │ Score + Review  │
                    └────────┬────────┘
                             │
                             ▼
                 ┌──────────────────────┐
                 │ FINAL RESEARCH REPORT│
                 │   + CRITIC FEEDBACK  │
                 └──────────────────────┘
```

---

##  Setup / Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/multi_agent_news.git
cd multi_agent_news
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with the following keys:

```env
TAVILY_API_KEY=your_tavily_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```



## ▶️ Usage

### Run as a web app (recommended)

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`) in your browser:

1. Enter a research topic in the input box (or click one of the example chips).
2. Click **Run research →**.
3. Watch the four-agent pipeline progress in real time.
4. Read the generated **Final Research Report** and the **Critic Feedback** below it.
5. Optionally, click **Download Report (.md)** to save the report locally.

### Run from the command line

```bash
python pipeline.py
```

You'll be prompted to enter a topic, and the pipeline will print each stage's output (search results, scraped content, final report, and critic feedback) directly to the terminal.

---

## 🧠 How It Works

```
User Topic
    │
    ▼
1. Search Agent  ──► Tavily web search → titles, URLs, snippets
    │
    ▼
2. Reader Agent  ──► Scrapes the most relevant URL for deeper content
    │
    ▼
3. Writer Chain  ──► Synthesizes research into a structured report
    │
    ▼
4. Critic Chain  ──► Scores and critiques the report
    │
    ▼
Final Report + Feedback (displayed in UI, downloadable as .md)
```

---

## 🚀 Future Improvements

- Allow the Critic Agent's feedback to trigger an automatic re-draft loop.
- Add report history / session persistence across runs.

---



