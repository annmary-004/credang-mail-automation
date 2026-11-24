import os
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    load_dotenv(env_path, override=True)
except Exception:
    pass

# Allow HTTP for local OAuth development
os.environ["AUTHLIB_INSECURE_TRANSPORT"] = "true"

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from authlib.integrations.httpx_client import AsyncOAuth2Client

from database import get_db
from models import User
from security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

def get_oauth_config():
    client_id     = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
    redirect_uri  = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback").strip()
    return client_id, client_secret, redirect_uri

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    email: str

@router.post("/register", response_model=TokenOut, status_code=201)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    user = User(email=data.email, name=data.name, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": user.email})
    return TokenOut(access_token=token, name=user.name or "", email=user.email)

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not user.hashed_password or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = create_access_token({"sub": user.email})
    return TokenOut(access_token=token, name=user.name or "", email=user.email)

@router.get("/google")
async def google_login(db: Session = Depends(get_db)):
    client_id, client_secret, redirect_uri = get_oauth_config()
    if not client_id:
        user = db.query(User).filter(User.email == "google.user@credang.com").first()
        if not user:
            user = User(
                email="google.user@credang.com",
                name="Google User (Credang)",
                google_id="google-mock-id-12345"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        access_token = create_access_token({"sub": user.email})
        return RedirectResponse(
            f"http://localhost:8000/?token={access_token}&name={user.name}&email={user.email}"
        )

    client = AsyncOAuth2Client(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    uri, _ = client.create_authorization_url(
        "https://accounts.google.com/o/oauth2/v2/auth",
        scope="openid email profile",
        access_type="offline",
        prompt="select_account",
    )
    return RedirectResponse(uri)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    client_id, client_secret, redirect_uri = get_oauth_config()
    client = AsyncOAuth2Client(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    token = await client.fetch_token(
        "https://oauth2.googleapis.com/token",
        authorization_response=str(request.url),
    )
    userinfo = await client.get("https://www.googleapis.com/oauth2/v3/userinfo")
    info = userinfo.json()

    user = db.query(User).filter(User.email == info["email"]).first()
    if not user:
        user = User(email=info["email"], name=info.get("name", ""), google_id=info.get("sub"))
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    return RedirectResponse(
        f"http://localhost:8000/?token={access_token}&name={user.name}&email={user.email}"
    )

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"email": user.email, "name": user.name}
