# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 + Gemini-powered budget and recommendation assistant based on the supplied project documentation.

## Included
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image
- Register / Login / Logout
- JWT authentication
- Session information
- Recommendation history
- Gemini integration through the current Google Gen AI Python SDK
- Demo fallback mode when no Gemini API key is configured
- Responsive HTML/CSS/JavaScript frontend
- SQLite database
- Curated demo product/service catalog instead of pretending to scrape third-party sites

## Important model note
The supplied documentation names Gemini 1.5 Flash Pro. That model reference is historical. This implementation keeps the documented Gemini role but uses a configurable current Gemini model. The default is `gemini-2.5-flash`; change `GEMINI_MODEL` in `.env` if your account supports another model.

## Quick start

### Windows PowerShell

```powershell
cd PocketSmart_AI
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Open http://127.0.0.1:8000

### Gemini mode
Edit `.env` and set:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
DEMO_MODE=false
```

If `GEMINI_API_KEY` is empty, the application automatically uses local demo recommendations, so the complete UI can be tested without an API key.

## API endpoints

- `GET /`
- `GET /login`
- `GET /register`
- `GET /dashboard`
- `GET /planner/{planner}`
- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `GET /api/session-info`
- `GET /api/session-data`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`
- `GET /api/history`
- `GET /api/recommendations-details/{id}`
- `GET /health`

## Test

```powershell
python -m pytest
```

The tests verify the health endpoint, authentication flow, protected session endpoint, and planner fallback behavior.

## Security
Do not commit `.env`. Never put an API key directly in Python, HTML, JavaScript, or Git history. A real production deployment should use HTTPS, a managed database, secure cookie settings, rate limiting, and a secrets manager.
