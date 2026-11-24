"""
Contacts router – Excel / CSV upload, preview, column detection.
Uses openpyxl and standard csv module (zero pandas dependency).
"""
import io
import csv
from typing import Any
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
import openpyxl
from models import User
from security import get_current_user

router = APIRouter()

ALLOWED_EXT = {".xlsx", ".xls", ".csv"}

def _parse_csv(file_bytes: bytes) -> tuple[list[str], list[dict[str, Any]]]:
    text = file_bytes.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    columns = reader.fieldnames or []
    rows = [row for row in reader if any(v.strip() for v in row.values())]
    return columns, rows

def _parse_excel(file_bytes: bytes) -> tuple[list[str], list[dict[str, Any]]]:
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
    ws = wb.active
    rows_iter = ws.iter_rows(values_only=True)
    try:
        header = next(rows_iter)
    except StopIteration:
        return [], []
    columns = [str(col).strip() for col in header if col is not None]
    rows = []
    for row in rows_iter:
        if not any(v is not None and str(v).strip() for v in row):
            continue
        row_dict = {}
        for idx, col_name in enumerate(columns):
            val = row[idx] if idx < len(row) else ""
            row_dict[col_name] = str(val).strip() if val is not None else ""
        rows.append(row_dict)
    return columns, rows

def _detect_email_col(columns: list[str]) -> str | None:
    for col in columns:
        c_low = col.lower()
        if "email" in c_low or "mail" in c_low:
            return col
    return columns[0] if columns else None

def _flag_issues(rows: list[dict], email_col: str | None) -> list[dict]:
    seen_emails = set()
    result = []
    for i, row in enumerate(rows):
        r = dict(row)
        issues = []
        val = str(r.get(email_col, "")).strip() if email_col else ""
        if not val:
            issues.append("missing_email")
        elif "@" not in val or "." not in val:
            issues.append("invalid_email")
        elif val.lower() in seen_emails:
            issues.append("duplicate")
        else:
            seen_emails.add(val.lower())
        r["_issues"] = issues
        r["_row_idx"] = i
        result.append(r)
    return result

@router.post("/upload")
async def upload_contacts(
    file: UploadFile = File(...),
    _user: User = Depends(get_current_user),
):
    content = await file.read()
    ext = "." + (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, f"Unsupported file type: {ext}. Upload .xlsx, .xls or .csv")

    if ext == ".csv":
        columns, rows = _parse_csv(content)
    else:
        columns, rows = _parse_excel(content)

    email_col = _detect_email_col(columns)
    flagged = _flag_issues(rows, email_col)

    return {
        "columns": columns,
        "email_col": email_col,
        "rows": flagged,
        "total": len(flagged),
        "issues_count": sum(1 for r in flagged if r["_issues"]),
    }

@router.post("/set-email-col")
async def set_email_col(
    columns: list[str],
    email_col: str = Form(...),
    _user: User = Depends(get_current_user),
):
    if email_col not in columns:
        raise HTTPException(400, "Column not in dataset")
    return {"email_col": email_col}
