# Django & FastAPI Hybrid Backend

A powerful hybrid backend combining **Django** for authentication/user management and **FastAPI** for high-performance WebSockets and asynchronous LLM functions. All served via a unified ASGI entry point.

## Tech Stack
- **Frameworks**: Django 6.x, FastAPI
- **Environment Management**: `uv`
- **ASGI Server**: Uvicorn
- **ORM**: Django ORM (Shared)

## Project Structure
- `core/`: Django project settings and unified ASGI configuration.
- `api/`: FastAPI application logic.
- `manage.py`: Django management script.
- `pyproject.toml`: `uv` project definition.

## Setup Instructions

### 1. Prerequisites
Ensure you have `uv` installed. If not, install it via:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Initialize Environment
The project uses `uv` for lightning-fast dependency management.
```bash
# Install dependencies and create .venv
uv sync
```

### 3. Activate Virtual Environment
```bash
source .venv/bin/activate
```

### 4. Database Migrations
Initialize the Django models and authentication system.
```bash
uv run python manage.py migrate
```

### 5. Create Superuser (Optional)
To access the Django Admin panel:
```bash
uv run python manage.py createsuperuser
```

## Running the Server
Start the unified backend server:
```bash
uv run uvicorn core.asgi:application --reload --port 8000
```

## API Endpoints

### FastAPI (via `/api/v1`)
- **Health Check (with ORM integration)**: `GET http://localhost:8000/api/v1/fastapi/health`
- **Async LLM Placeholder**: `POST http://localhost:8000/api/v1/fastapi/llm/async?prompt=your_prompt`
- **WebSocket**: `ws://localhost:8000/api/v1/fastapi/ws`

### Django
- **Admin Panel**: `http://localhost:8000/admin/`
- **Auth URLs**: Integrated via standard Django patterns.

## Development Tips
- **FastAPI Docs**: Once the server is running, visit `http://localhost:8000/api/v1/docs` for interactive API documentation.
- **Shared ORM**: FastAPI is configured to use Django models. See `api/main.py` for usage examples.
