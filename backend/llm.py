"""
LLM abstraction – supports OpenAI, Claude (Anthropic), Gemini.
Reads LLM_PROVIDER from env (default: openai).
"""
import os
import json
from typing import Any

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

SYSTEM_PROMPT = """You are an expert email copywriter.
Given a context (purpose, tone, sender name/signature, call-to-action) and a row of contact data,
write a highly personalised email.

RULES:
- Use {{Name}} placeholder where the contact name appears (it will be substituted).
- Keep subject under 60 characters.
- Body should be 100-200 words, professional, warm, and action-oriented.
- Respond ONLY with valid JSON: {"subject": "...", "body": "..."}
"""

def _build_user_msg(context: str, row: dict[str, Any]) -> str:
    row_clean = {k: v for k, v in row.items() if not k.startswith("_")}
    return f"""Context: {context}

Contact data: {json.dumps(row_clean, default=str)}

Write a personalised email."""

# ── OpenAI ───────────────────────────────────────────────────────────────────
async def _openai(context: str, row: dict) -> tuple[str, str]:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": _build_user_msg(context, row)},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    data = json.loads(resp.choices[0].message.content)
    return data["subject"], data["body"]

# ── Claude ───────────────────────────────────────────────────────────────────
async def _claude(context: str, row: dict) -> tuple[str, str]:
    import anthropic
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    msg = await client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_msg(context, row)}],
    )
    data = json.loads(msg.content[0].text)
    return data["subject"], data["body"]

# ── Gemini ───────────────────────────────────────────────────────────────────
async def _gemini(context: str, row: dict) -> tuple[str, str]:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    model = genai.GenerativeModel(model_name, system_instruction=SYSTEM_PROMPT)
    resp = await model.generate_content_async(
        _build_user_msg(context, row),
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.7,
        ),
    )
    data = json.loads(resp.text)
    return data["subject"], data["body"]

# ── Dispatcher ───────────────────────────────────────────────────────────────
async def generate_email(context: str, row: dict[str, Any]) -> tuple[str, str]:
    try:
        if LLM_PROVIDER == "claude":
            return await _claude(context, row)
        elif LLM_PROVIDER == "gemini":
            return await _gemini(context, row)
        else:
            return await _openai(context, row)
    except Exception as e:
        # Graceful fallback – return a template so the app doesn't crash
        name = row.get("Name", row.get("name", "there"))
        subject = f"Hello {name} – {context[:40]}"
        body = (
            f"Dear {name},\n\n"
            f"{context}\n\n"
            "We look forward to hearing from you.\n\nBest regards"
        )
        return subject, body

