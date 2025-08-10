import os
import uuid
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure the Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
logger.info(f"API Key loaded: {'Yes' if GOOGLE_API_KEY else 'No'}")

if not GOOGLE_API_KEY:
    logger.error("No Google API Key found. Make sure to set GOOGLE_API_KEY in your .env file.")

# Initialize FastAPI app
app = FastAPI(title="Heart Health Chatbot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Default credentials (hardcoded as requested)
DEFAULT_USERNAME = "linsija"
DEFAULT_PASSWORD = "linsi123"

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

# Define a system prompt for heart health context
SYSTEM_PROMPT = """
You are a compassionate and knowledgeable doctor specializing in heart health. Keep responses **short, clear, and informative** while maintaining a professional tone.  

- **Acknowledge the concern.**  
- **Provide a brief, evidence-based explanation.**  
- **Give simple, actionable advice.**  

Keep it **under 3-4 sentences if requried add more but should be easy to understand by the patient**, avoiding unnecessary details. Always remind users that they should consult a doctor for medical advice.
"""

# Define request and response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    history: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Store chat histories
chat_histories = {}

# Configure the model
def configure_genai():
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("Gemini API configured successfully")
    except Exception as e:
        logger.error(f"Error configuring Gemini API: {str(e)}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Redirect to login page
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    # You might want to add authentication check here in a real application
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/login")
async def login(request: LoginRequest):
    if request.username == DEFAULT_USERNAME and request.password == DEFAULT_PASSWORD:
        return {"success": True}
    return {"success": False, "message": "Incorrect username or password"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": str(type(exc).__name__)},
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    user_message = chat_request.message
    logger.info(f"Received message: {user_message[:30]}...")

    # Generate a new session ID if not provided
    session_id = chat_request.session_id or str(uuid.uuid4())
    logger.info(f"Using session: {session_id}")

    # Configure the Gemini API
    configure_genai()

    # Retrieve or initialize chat history
    history = chat_histories.get(session_id, [])

    # Prepare context-aware prompt
    conversation_history = "\n".join(
        [f"User: {entry['parts'][0]}" if entry["role"] == "user" else f"Doctor: {entry['parts'][0]}" for entry in history]
    )

    # Create the new prompt
    prompt = f"{SYSTEM_PROMPT}\n\n{conversation_history}\nUser: {user_message}\nDoctor (keep it brief and direct):"

    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-1.5-pro')

        # Generate the response
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Update the chat history
        history.append({"role": "user", "parts": [user_message]})
        history.append({"role": "model", "parts": [response_text]})
        chat_histories[session_id] = history  # Store updated history

        logger.info(f"Generated response: {response_text[:30]}...")

        return ChatResponse(response=response_text, session_id=session_id)

    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Test endpoint to verify API key
@app.get("/api/test-key")
async def test_key():
    if not GOOGLE_API_KEY:
        return {"status": "error", "message": "No API key configured"}
    
    try:
        # Configure the Gemini API
        configure_genai()
        
        # Quick model test
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content("Hello, this is a test. i have heart pain")
        return {
            "status": "success", 
            "message": "API key is valid",
            "test_response": response.text[:50] + "..."
        }
    except Exception as e:
        return {"status": "error", "message": f"Error with API key: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)