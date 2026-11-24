"""
Emails router – LLM generation, preview, send, CSV report.
"""
import os, io, csv, asyncio
from datetime import datetime, timezone
from typing import Any

import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, SessionLocal
from models import User, EmailLog
from security import get_current_user
from llm import generate_email

router = APIRouter()

class GenerateRequest(BaseModel):
    context:   str
    rows:      list[dict[str, Any]]
    email_col: str

class SendRequest(BaseModel):
    logs: list[dict[str, Any]]

class RegenerateRequest(BaseModel):
    context: str
    row:     dict[str, Any]

@router.post("/generate")
async def generate_emails_endpoint(
    req: GenerateRequest,
    user: User = Depends(get_current_user),
    db:   Session = Depends(get_db),
):
    results = []
    for row in req.rows:
        if row.get("_issues") and "missing_email" in row["_issues"]:
            results.append({**row, "subject": "", "body": "", "skipped": True})
            continue
        subject, body = await generate_email(req.context, row)
        log = EmailLog(
            user_id=user.id,
            recipient_name=str(row.get("Name", row.get("name", ""))),
            recipient_email=str(row.get(req.email_col, "")),
            subject=subject,
            body=body,
            status="queued",
        )
        db.add(log)
        db.flush()
        results.append({
            **row,
            "subject":  subject,
            "body":     body,
            "log_id":   log.id,
            "skipped":  False,
        })
    db.commit()
    return {"emails": results}

@router.post("/regenerate")
async def regenerate_one(
    req: RegenerateRequest,
    _user: User = Depends(get_current_user),
):
    subject, body = await generate_email(req.context, req.row)
    return {"subject": subject, "body": body}

async def _send_one(log_id: int, to_email: str, subject: str, body: str):
    # Separate session for background task
    db = SessionLocal()
    try:
        log = db.query(EmailLog).filter(EmailLog.id == log_id).first()

        mock_smtp = os.getenv("MOCK_SMTP", "false").lower() in ("true", "1", "yes")
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASSWORD", "")

        # If mock mode or credentials are dummy/empty, simulate successful delivery
        if mock_smtp or not smtp_user or "your_email" in smtp_user or "mock" in smtp_pass or not smtp_pass:
            await asyncio.sleep(0.8) # simulate network latency
            if log:
                log.status = "sent"
                log.sent_at = datetime.now(timezone.utc)
                log.error_msg = "[Simulated delivery - MOCK_SMTP is enabled]"
            db.commit()
            return

        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        from_name = os.getenv("SMTP_FROM_NAME", "AI Mail Automation")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{from_name} <{smtp_user}>"
        msg["To"]      = to_email
        msg.attach(MIMEText(body, "plain"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=smtp_host,
                port=smtp_port,
                username=smtp_user,
                password=smtp_pass,
                start_tls=True,
            )
            if log:
                log.status  = "sent"
                log.sent_at = datetime.now(timezone.utc)
        except Exception as e:
            if log:
                log.status    = "failed"
                log.error_msg = str(e)
        db.commit()
    finally:
        db.close()

@router.post("/send")
async def send_emails(
    req:        SendRequest,
    bg:         BackgroundTasks,
    _user:      User = Depends(get_current_user),
):
    for item in req.logs:
        log_id = item.get("log_id")
        if not log_id:
            continue
        bg.add_task(
            _send_one,
            log_id=log_id,
            to_email=item["recipient_email"],
            subject=item["subject"],
            body=item["body"],
        )
    return {"queued": len(req.logs), "message": "Emails are being sent in the background"}

@router.get("/status")
def get_status(
    user: User = Depends(get_current_user),
    db:   Session = Depends(get_db),
):
    logs = db.query(EmailLog).filter(EmailLog.user_id == user.id).order_by(EmailLog.created_at.desc()).all()
    return {
        "logs": [
            {
                "id":               l.id,
                "recipient_name":   l.recipient_name,
                "recipient_email":  l.recipient_email,
                "subject":          l.subject,
                "status":           l.status,
                "error_msg":        l.error_msg,
                "created_at":       str(l.created_at),
                "sent_at":          str(l.sent_at) if l.sent_at else None,
            }
            for l in logs
        ]
    }

@router.get("/report")
def download_report(
    user: User = Depends(get_current_user),
    db:   Session = Depends(get_db),
):
    logs = db.query(EmailLog).filter(EmailLog.user_id == user.id).order_by(EmailLog.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Recipient Name", "Email", "Subject", "Status", "Error", "Sent At"])
    for l in logs:
        writer.writerow([l.id, l.recipient_name, l.recipient_email, l.subject, l.status, l.error_msg or "", l.sent_at or ""])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=email_report.csv"},
    )
