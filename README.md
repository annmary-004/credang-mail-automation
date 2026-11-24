# Credang – AI Mail Automation 🚀

> **Full-stack web app** · Excel Upload → LLM Personalisation → Bulk Email Send → CSV Report

---

## Architecture

```
credang-mail-automation/
├── backend/          FastAPI (Python 3.11)
│   ├── main.py       App entrypoint + CORS
│   ├── routers/
│   │   ├── auth.py        Sign-up / Login / Google OAuth
│   │   ├── contacts.py    Excel/CSV upload, preview, column detection
│   │   └── emails.py      LLM generate, re-generate, send, status, CSV report
│   ├── llm.py        LLM abstraction (OpenAI / Claude / Gemini)
│   ├── models.py     SQLAlchemy models (User, EmailLog)
│   ├── security.py   JWT auth, bcrypt passwords
│   ├── database.py   SQLite (async)
│   └── requirements.txt
├── frontend/         React + Vite + Tailwind CSS
│   └── src/
│       ├── pages/    Login, Register, Dashboard, OAuthCallback
│       └── components/ UploadStep, ContextStep, EmailsPreview, SendStatus
├── docker-compose.yml
└── README.md
```

---

## Quick Start (Local — no Docker)

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env     # fill in your keys
uvicorn main:app --reload
# → http://localhost:8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

---

## Quick Start (Docker)

```bash
cp backend/.env.example backend/.env   # fill in your keys
docker compose up --build
# Frontend → http://localhost:3000
# API docs  → http://localhost:8000/docs
```

---

## Environment Variables (`backend/.env`)

| Variable | Description |
|---|---|
| `SECRET_KEY` | Long random string for JWT signing |
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID (optional) |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret (optional) |
| `LLM_PROVIDER` | `openai` (default) \| `claude` \| `gemini` |
| `OPENAI_API_KEY` | OpenAI API key |
| `ANTHROPIC_API_KEY` | Anthropic (Claude) API key |
| `GEMINI_API_KEY` | Google Gemini API key |
| `SMTP_HOST` | SMTP server (default: `smtp.gmail.com`) |
| `SMTP_PORT` | SMTP port (default: `587`) |
| `SMTP_USER` | Your email address |
| `SMTP_PASSWORD` | Gmail App Password (not your login password!) |

### Gmail App Password Setup
1. Enable 2FA on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Create password for "Mail" → use that as `SMTP_PASSWORD`

---

## Application Flow

```
Sign Up / Login (email+password or Google OAuth)
        ↓
Upload Excel / CSV (.xlsx, .xls, .csv)
  • Auto-detect Email column
  • Flag missing / invalid / duplicate emails
  • Manual column selection if needed
        ↓
Enter Context (purpose, tone, sender, CTA)
        ↓
LLM generates Subject + Body per row
  • Preview table with expand / edit / re-generate
        ↓
Send  (async SMTP, retries on failure)
  • Live status: Queued → Sent / Failed
        ↓
Download CSV Report
```

---

## Edge Cases Handled

- ✅ Missing Email column → user manually selects
- ✅ Empty rows → skipped
- ✅ Duplicate emails → flagged
- ✅ Invalid email format → flagged
- ✅ LLM timeout / error → graceful fallback template
- ✅ SMTP failure → logged as `failed`, shown in report
- ✅ Double-click Send → no duplicate sends (background task per log_id)

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Register with email+password |
| POST | `/auth/login` | Login → JWT token |
| GET  | `/auth/google` | Redirect to Google OAuth |
| GET  | `/auth/google/callback` | Google OAuth callback |
| POST | `/contacts/upload` | Upload Excel/CSV |
| POST | `/emails/generate` | LLM generate all emails |
| POST | `/emails/regenerate` | Re-generate single email |
| POST | `/emails/send` | Send all (async) |
| GET  | `/emails/status` | Live send status |
| GET  | `/emails/report` | Download CSV report |

Interactive Swagger docs: **http://localhost:8000/docs**

---

## Sample contacts.xlsx format

| Name | Email | Company |
|---|---|---|
| Manoj Rajendran | manoj_rajendran@credang.com | Credang |
| Your Name | your@email.com | Your Company |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy (async), aiosqlite |
| Auth | JWT (python-jose), bcrypt, Google OAuth (authlib) |
| LLM | OpenAI GPT-4o-mini / Claude 3 Haiku / Gemini 1.5 Flash |
| Email | aiosmtplib (SMTP with STARTTLS) |
| Frontend | React 18, Vite, Tailwind CSS, React Router |
| File parsing | pandas, openpyxl |
| Containerisation | Docker, docker-compose |

