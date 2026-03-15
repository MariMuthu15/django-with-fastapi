import asyncio
import httpx
import websockets
import json

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

async def test_health():
    print("Testing Health Check...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/v1/fastapi/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")

async def test_chat():
    print("Testing Gemini Chat...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/fastapi/chat",
            json={"message": "Write a one sentence poem about a cat."},
            timeout=30.0
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")

async def test_llm_async():
    print("Testing Async LLM...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/api/v1/fastapi/llm/async?prompt=Say hi",
            timeout=30.0
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}\n")

async def test_websocket():
    print("Testing WebSocket...")
    try:
        async with websockets.connect(f"{WS_URL}/api/v1/fastapi/ws") as websocket:
            await websocket.send("Hello WS!")
            response = await websocket.recv()
            print(f"Received via WS: {response}\n")
    except Exception as e:
        print(f"WS Error: {e}\n")

async def test_django_admin():
    print("Testing Django Admin...")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/admin/")
        print(f"Status: {response.status_code} (Expect 200 or 302)\n")

async def main():
    await test_health()
    await test_chat()
    await test_llm_async()
    await test_websocket()
    await test_django_admin()

if __name__ == "__main__":
    asyncio.run(main())
