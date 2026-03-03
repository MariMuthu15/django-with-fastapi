import os
import django
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from api.services import gemini_service
from pydantic import BaseModel

# Setup Django environment to use ORM in FastAPI
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User

app = FastAPI(title="FastAPI LLM & WebSocket Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fastapi/health")
async def health_check():
    # Example of using Django ORM
    user_count = await asyncio.to_thread(User.objects.count)
    return {"status": "ok", "service": "fastapi", "django_user_count": user_count}

@app.websocket("/fastapi/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("WebSocket client disconnected")

class ChatRequest(BaseModel):
    message: str

@app.post("/fastapi/chat")
async def chat_with_gemini(request: ChatRequest):
    """
    General chat endpoint for Gemini.
    """
    response = await gemini_service.get_response(request.message)
    return {"response": response, "status": "completed"}

@app.post("/fastapi/llm/async")
async def llm_gemini_async(prompt: str):
    """
    Updated placeholder to use actual Gemini API.
    """
    response = await gemini_service.get_response(prompt)
    return {"response": response, "status": "completed"}
