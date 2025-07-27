import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
API_BASE_URL = "http://localhost:8000"

# RAG Configuration
VECTOR_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chatbot responses
BOT_RESPONSES = {
    "greeting": "Hello! I'm here to help you with your grievances. How can I assist you today?",
    "complaint_registration": "I can help you register a complaint. I'll need some information from you.",
    "status_inquiry": "I can help you check the status of your complaint.",
    "unknown": "I'm sorry, I didn't understand that. I can help you register a complaint or check complaint status."
} 