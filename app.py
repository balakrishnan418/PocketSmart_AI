from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from backend.config import settings
from backend.database import init_db
from backend.routes.api import router as api_router

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title=settings.APP_NAME, version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "frontend" / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"page": "home"}
    )


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"page": "login"}
    )


@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"page": "register"}
    )


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"page": "dashboard"}
    )


@app.get("/planner/{planner}")
def planner_page(request: Request, planner: str):
    return templates.TemplateResponse(
        request=request,
        name="planner.html",
        context={
            "page": planner,
            "planner": planner
        }
    )

@app.get("/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)

