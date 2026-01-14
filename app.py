import uvicorn
from fastapi import FastAPI, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os

# IMPORT CUSTOM MODULES
from src.rag.chain import build_chat_chain
from src.utlis.safe_invoke import safe_chat_invoke
from src.memory.session_memory import get_or_create_session_id

# LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG AI Insurance Agent",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# STATIC FILES (safe check)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# GLOBAL CHAIN
chat_chain = None

@app.on_event("startup")
async def startup_event():
    global chat_chain
    try:
        logger.info("Loading RAG Chain...")
        chat_chain = build_chat_chain()
        logger.info("RAG Chain loaded successfully!")
    except Exception as e:
        logger.exception("Critical Error loading RAG Chain")

# DATA MODELS
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    session_id: str
    error: Optional[str] = None

# ROOT
@app.get("/")
async def read_root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "RAG AI Insurance Agent is running"}

# HEALTH CHECK (RENDER REQUIRED)
@app.get("/health")
async def health():
    return {"status": "ok"}

# CHAT ENDPOINT
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    x_session_id: Optional[str] = Header(None)
):
    global chat_chain

    if chat_chain is None:
        return ChatResponse(
            answer="System is initializing. Please try again shortly.",
            session_id="init",
            error="System Not Ready"
        )

    user_session_id = x_session_id or request.session_id
    clean_session_id = get_or_create_session_id(user_session_id)

    logger.info(f"Session: {clean_session_id} | Question: {request.question}")

    result = safe_chat_invoke(
        chat_chain,
        request.question,
        clean_session_id
    )

    return ChatResponse(
        answer=result.get("answer") or "I couldn't generate an answer.",
        session_id=clean_session_id,
        error=result.get("error")
    )

# ENTRY POINT (Docker & Render safe)
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        workers=1
    )
