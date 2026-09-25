import json
from typing import Optional
from backend.config import settings
from backend.services.recommendation_service import home_demo, party_demo, jewelry_demo


def _json_from_text(text: str):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    try:
        return json.loads(text)
    except Exception:
        return None


def _prompt(planner: str, data: dict) -> str:
    base = f"""
You are PocketSmart AI, a budget-aware recommendation assistant.
Planner: {planner}
User input: {json.dumps(data, ensure_ascii=False)}
Return ONLY valid JSON with this exact top-level shape:
{{
  "planner": "{planner}",
  "summary": "short summary",
  "budget_allocation": [{{"category":"string","amount":0}}],
  "recommendations": [
    {{"name":"string","category":"string","price":0,"platform":"string","url":"string"}}
  ],
  "tips": ["string"],
  "mode": "gemini"
}}
Rules:
- Currency is INR.
- Respect the user's budget.
- Never claim that you checked a live store unless the URL is a general platform/search URL.
- If exact live product data is unavailable, describe the item as a suggestion rather than verified inventory.
- Keep the answer concise and useful.
"""
    return base


def generate(planner: str, data: dict, image_bytes: Optional[bytes] = None, image_mime: Optional[str] = None):
    if settings.DEMO_MODE or not settings.GEMINI_API_KEY:
        return {"home": home_demo, "party": party_demo, "jewelry": jewelry_demo}[planner](data)

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        contents = [_prompt(planner, data)]

        if image_bytes and image_mime:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime))

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=2500,
            ),
        )
        parsed = _json_from_text(response.text or "")
        if parsed and isinstance(parsed, dict):
            parsed["mode"] = "gemini"
            return parsed
    except Exception:
        pass

    fallback = {"home": home_demo, "party": party_demo, "jewelry": jewelry_demo}[planner](data)
    fallback["mode"] = "demo-fallback"
    return fallback
