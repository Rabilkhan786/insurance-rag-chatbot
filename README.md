# AI Insurance Assistant

## Live App
🔗 https://insurance-rag-chatbot-hgr3.onrender.com

A high-performance Retrieval-Augmented Generation (RAG) AI assistant designed to answer complex insurance policy queries instantly.

Built with FastAPI, LangChain, and Docker, this assistant retrieves accurate information from a FAISS vector database and uses the Groq (Llama-3) LLM to generate natural, context-aware responses.

---

##  Features

* **RAG Architecture:** retrieves precise context from indexed insurance PDF documents.
* **FastAPI Backend:** Lightweight, asynchronous API handling.
* **Vector Search:** Uses **FAISS** (Facebook AI Similarity Search) for millisecond-latency retrievals.
* **Conversational Memory:** Remembers previous turns of the conversation for a fluid chat experience.
* **Dockerized:** Fully containerized with a highly optimized, lightweight image (CPU-only PyTorch).
* **Deployment Ready:** Configured for seamless deployment on Render/AWS.

---

##  Tech Stack

* **Language:** Python 3.10
* **LLM:** Llama-3-8b (via Groq API)
* **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2`)
* **Vector DB:** FAISS (CPU)
* **Orchestration:** LangChain
* **API Framework:** FastAPI & Uvicorn
* **Containerization:** Docker
* **Cloud-Server:**Render

---

##  Project Structure

```bash
├── src/
│   ├── llm/
│   ├── memory/
│   ├── audio/
│   └── rag/
├── faiss_insurance_index/
├── app.py
├── Dockerfile
├── requirements.txt
└── .env.example
                
```

---

# How to run Locally?
### STEP-01 Clone the repository:

```bash
git clone https://github.com/Rabilkhan786/insurance-rag-chatbot.git
cd insurance-rag-chatbot
```

### Step-02 Create a virtual environment: :

# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### STEP-03- install the requirements

```bash
pip install -r requirements.txt
```


### STEP-04 Create a .env file::

```ini
GROQ_API_KEY=your_groq_api_key_here
# OPENAI_API_KEY=your_key (If using OpenAI)
```

### STEP-05 Run the App:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Run with Docker:

### Step-01:
```bash
docker build -t insurance-rag-agent .
```

###  Run The Docker Container:


```bash
docker run -p 8001:8000 --env-file .env insurance-rag-agent
```

### Open in Browser:
```bash
http://localhost:8001
http://localhost:8001/docs
```


## API Documentation
Once the app is running, open your browser to access the interactive Swagger UI:

http://localhost:8000/docs (or port 8001 if using Docker)

## Key Endpoints
POST /chat: Chat with the RAG agent.

GET /health: Health check to ensure the API is running.

## Deployment

This project is configured for Render.

1. Push code to GitHub.

2. Create a new Web Service on Render.

3. Connect your repository.

4. Add Environment Variables (GROQ_API_KEY) in the Render dashboard.

5. Render will automatically build using the Dockerfile
