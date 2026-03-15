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
from api.models import ChatSession, ChatMessage
from typing import List, Optional

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

class MessageSchema(BaseModel):
    id: int
    role: str
    content: str
    timestamp: str

class SessionSchema(BaseModel):
    id: int
    title: str
    created_at: str

@app.get("/fastapi/sessions", response_model=List[SessionSchema])
async def get_sessions():
    sessions = await asyncio.to_thread(list, ChatSession.objects.all().order_by('-updated_at'))
    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": s.created_at.isoformat()
        } for s in sessions
    ]

@app.post("/fastapi/sessions", response_model=SessionSchema)
async def create_session():
    session = await asyncio.to_thread(ChatSession.objects.create)
    return {
        "id": session.id,
        "title": session.title,
        "created_at": session.created_at.isoformat()
    }

@app.get("/fastapi/sessions/{session_id}/messages", response_model=List[MessageSchema])
async def get_messages(session_id: int):
    messages = await asyncio.to_thread(list, ChatMessage.objects.filter(session_id=session_id).order_by('timestamp'))
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp.isoformat()
        } for m in messages
    ]

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
    session_id: Optional[int] = None

@app.post("/fastapi/chat")
async def chat_with_gemini(request: ChatRequest):
    """
    General chat endpoint for Gemini with persistence.
    """
    session_id = request.session_id
    
    # 1. Ensure session exists
    if not session_id:
        session = await asyncio.to_thread(ChatSession.objects.create)
        session_id = session.id
    else:
        session = await asyncio.to_thread(ChatSession.objects.get, id=session_id)

    # 2. Save User Message
    await asyncio.to_thread(ChatMessage.objects.create, session=session, role='user', content=request.message)

    # 3. Get Gemini Response
    response_text = await gemini_service.get_response(request.message)

    # 4. Save Assistant Message
    await asyncio.to_thread(ChatMessage.objects.create, session=session, role='assistant', content=response_text)

    # 5. Update Session Title if it's "New Chat"
    if session.title == "New Chat":
        # Simple title generation: first 30 chars of the message
        session.title = request.message[:30] + ("..." if len(request.message) > 30 else "")
        await asyncio.to_thread(session.save)

    return {
        "response": response_text,
        "session_id": session_id,
        "status": "completed"
    }

@app.post("/fastapi/llm/async")
async def chat_with_gemini_async(prompt: str):
    response_text = await gemini_service.get_response(prompt)
    return {"response": response_text}

