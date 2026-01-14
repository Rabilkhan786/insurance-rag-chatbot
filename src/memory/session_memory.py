import uuid
from langchain_core.chat_history import InMemoryChatMessageHistory

SESSION_STORE = {}
MAX_MESSAGES = 6

def get_or_create_session_id(session_id: str | None):
    if session_id and session_id.strip():
        return session_id          
    return str(uuid.uuid4())  


def get_session_history(session_id: str):
    if session_id not in SESSION_STORE:
        SESSION_STORE[session_id] = InMemoryChatMessageHistory()

    history = SESSION_STORE[session_id]

    # limit past history to control tokens
    
    if len(history.messages) > MAX_MESSAGES:
        history.messages = history.messages[-MAX_MESSAGES:]

    return history