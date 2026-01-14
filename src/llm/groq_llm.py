import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def groq_model():
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")            
    
    if not GROQ_API_KEY:
         raise ValueError("GROQ_API_KEY not found. Check your .env file")   

    model = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant", # or  You can use  "llama-3.3-70b versatile" for better reasoning 
    temperature=0.2
    )
    return model