# 💸 Financial AI Assistant

An intelligent, multi-agent system that delivers spoken market briefs by aggregating data from financial APIs, scraping filings, retrieving relevant documents via RAG, and synthesizing responses using LLMs — all orchestrated through a Streamlit UI with voice and text capabilities.

---

## 🧠 Use Case: Morning Market Brief

Every trading day at 8 AM, a portfolio manager asks:

> “What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?”

The assistant responds:

> “Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday.  
> TSMC beat estimates by 4%, Samsung missed by 2%.  
> Regional sentiment is neutral with a cautionary tilt due to rising yields.”

---

## 📐 Architecture Overview

![Architecture Diagram](docs/architecture.png) <!-- Replace with your actual path -->

- Microservices using FastAPI for each agent
- Retrieval-Augmented Generation (RAG) with FAISS
- Streamlit frontend with voice + text I/O
- Dockerized deployment of all services

---

## 🧩 Agent Overview

| Agent             | Role                                                                 |
|------------------|----------------------------------------------------------------------|
| 📈 Market API Agent | Pulls real-time/historical data via AlphaVantage (stock, earnings)  |
| 🔍 Scraper Agent     | Extracts earnings data and SEC filings from Yahoo Finance & EDGAR  |
| 📚 Retrieval Agent   | Embeds and indexes documents using FAISS and SentenceTransformer   |
| 💬 LLM Agent         | Uses OpenAI GPT model to generate concise market briefs             |
| 🎤 Voice Agent       | Whisper for STT, pyttsx3 for TTS (audio responses)                  |
| 🧭 Orchestrator      | Central logic hub for routing between agents                        |

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/yourusername/financial-ai-assistant.git
cd financial-ai-assistant/docker
2. Environment Variables
Create a .env file in the docker/ directory:

env
Copy
Edit
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
OPENAI_API_KEY=your_openai_key
3. Build and Run with Docker Compose
bash
Copy
Edit
docker-compose up --build
4. Launch the Streamlit App
bash
Copy
Edit
cd ../streamlit_app
streamlit run app.py
Then open http://localhost:8501 in your browser.
