import os
import django
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

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

@app.post("/fastapi/llm/async")
async def llm_placeholder(prompt: str):
    # Simulate an async LLM call
    await asyncio.sleep(2)
    return {"response": f"Processed prompt: {prompt}", "status": "completed"}
