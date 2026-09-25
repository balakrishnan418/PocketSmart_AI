import json
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Request
from backend.database import execute, fetch_all, fetch_one
from backend.schemas import RegisterRequest, LoginRequest, HomeRequest, PartyRequest, JewelryRequest
from backend.security import hash_password, verify_password, create_token, get_current_user
from backend.services.gemini_service import generate



router = APIRouter()


@router.delete("/recommendations/{recommendation_id}")
def delete_recommendation(
    recommendation_id: int,
    request: Request
):
    user = get_current_user(request)

    if not user:
        raise HTTPException(status_code=401, detail="Not logged in")

    recommendation = fetch_one(
        "SELECT id FROM recommendations WHERE id = ? AND user_id = ?",
        (recommendation_id, user["id"])
    )

    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    execute(
        "DELETE FROM recommendations WHERE id = ? AND user_id = ?",
        (recommendation_id, user["id"])
    )

    return {"message": "Recommendation deleted successfully"}


@router.post("/register")
def register(payload: RegisterRequest):
    if fetch_one("SELECT id FROM users WHERE email = ?", (payload.email.lower(),)):
        raise HTTPException(409, "Email already registered")
    user_id = execute(
        "INSERT INTO users(name,email,password_hash) VALUES(?,?,?)",
        (payload.name.strip(), payload.email.lower(), hash_password(payload.password)),
    )
    return {"message": "Registered successfully", "user_id": user_id}


@router.post("/login")
def login(payload: LoginRequest, request: Request):
    user = fetch_one("SELECT * FROM users WHERE email = ?", (payload.email.lower(),))
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    token = create_token(user["id"])
    response = {"message": "Login successful", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}
    from fastapi.responses import JSONResponse
    r = JSONResponse(response)
    r.set_cookie("access_token", token, httponly=True, samesite="lax", secure=False, max_age=43200)
    return r


@router.post("/logout")
def logout():
    from fastapi.responses import JSONResponse
    r = JSONResponse({"message": "Logged out"})
    r.delete_cookie("access_token")
    return r


@router.get("/session-info")
def session_info(request: Request):
    try:
        user = get_current_user(request)
        return {"logged_in": True, "user": user}
    except HTTPException:
        return {"logged_in": False}


@router.get("/session-data")
def session_data(request: Request):
    user = get_current_user(request)
    count = fetch_one("SELECT COUNT(*) AS c FROM recommendations WHERE user_id = ?", (user["id"],))["c"]
    return {"user": user, "recommendation_count": count}


@router.post("/generate-home")
def generate_home(payload: HomeRequest, request: Request):
    user = get_current_user(request)
    data = payload.model_dump()
    result = generate("home", data)
    rec_id = execute(
        "INSERT INTO recommendations(user_id,planner,input_json,result_json) VALUES(?,?,?,?)",
        (user["id"], "home", json.dumps(data), json.dumps(result)),
    )
    result["id"] = rec_id
    return result


@router.post("/generate-party")
def generate_party(payload: PartyRequest, request: Request):
    user = get_current_user(request)
    data = payload.model_dump()
    result = generate("party", data)
    rec_id = execute(
        "INSERT INTO recommendations(user_id,planner,input_json,result_json) VALUES(?,?,?,?)",
        (user["id"], "party", json.dumps(data), json.dumps(result)),
    )
    result["id"] = rec_id
    return result


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form("Casual"),
    style: str = Form("Elegant"),
    outfit_color: str = Form(""),
    notes: str = Form(""),
    image: UploadFile | None = File(None),
):
    user = get_current_user(request)
    if budget <= 0:
        raise HTTPException(422, "Budget must be positive")
    image_bytes = None
    image_mime = None
    if image:
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(400, "Outfit file must be an image")
        image_bytes = await image.read()
        if len(image_bytes) > 5 * 1024 * 1024:
            raise HTTPException(413, "Image must be 5 MB or smaller")
        image_mime = image.content_type

    data = JewelryRequest(
        budget=budget, occasion=occasion, style=style,
        outfit_color=outfit_color, notes=notes
    ).model_dump()
    result = generate("jewelry", data, image_bytes, image_mime)
    rec_id = execute(
        "INSERT INTO recommendations(user_id,planner,input_json,result_json) VALUES(?,?,?,?)",
        (user["id"], "jewelry", json.dumps(data), json.dumps(result)),
    )
    result["id"] = rec_id
    return result


@router.get("/history")
def history(request: Request):
    user = get_current_user(request)
    return fetch_all(
        "SELECT id, planner, input_json, result_json, created_at FROM recommendations WHERE user_id = ? ORDER BY id DESC LIMIT 30",
        (user["id"],),
    )


@router.get("/recommendations-details/{rec_id}")
def recommendation_details(rec_id: int, request: Request):
    user = get_current_user(request)
    row = fetch_one(
        "SELECT id, planner, input_json, result_json, created_at FROM recommendations WHERE id = ? AND user_id = ?",
        (rec_id, user["id"]),
    )
    if not row:
        raise HTTPException(404, "Recommendation not found")
    row["input_json"] = json.loads(row["input_json"])
    row["result_json"] = json.loads(row["result_json"])
    return row

