"""
Credang – AI Mail Automation  |  FastAPI backend
"""
import os
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path, override=True)
except Exception:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from database import init_db
from routers import auth, contacts, emails

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Credang AI Mail Automation", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import HTMLResponse

try:
    from static_html import INDEX_HTML
except ImportError:
    try:
        from backend.static_html import INDEX_HTML
    except ImportError:
        INDEX_HTML = "<h1>Credang AI Mail Automation Live</h1>"

app.include_router(auth.router,     prefix="/auth",     tags=["auth"])
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(emails.router,   prefix="/emails",   tags=["emails"])

@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def serve_index():
    return HTMLResponse(content=INDEX_HTML)

