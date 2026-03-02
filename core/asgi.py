"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from api.main import app as fastapi_app
from starlette.routing import Mount
from starlette.applications import Starlette

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_app = get_asgi_application()

# Combine Django and FastAPI
application = Starlette(routes=[
    Mount("/api/v1", fastapi_app), # FastAPI endpoints
    Mount("/", django_asgi_app),   # Django endpoints (Admin, etc)
])

