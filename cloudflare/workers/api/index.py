from fastapi import FastAPI
import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from app.main import app as main_app

app = FastAPI()

# Copy routes from main app
app.include_router(main_app.router)

# Configure CORS for Cloudflare Pages
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this more strictly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudflare Workers entry point
def handle_request(request):
    return app(request)

