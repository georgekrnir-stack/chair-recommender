from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Response, Request
from pydantic import BaseModel
from jose import jwt

from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24


class LoginRequest(BaseModel):
    password: str


def create_token() -> str:
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode({"exp": expire, "role": "admin"}, settings.session_secret, algorithm=ALGORITHM)


def verify_admin(request: Request) -> bool:
    token = request.cookies.get("session")
    if not token:
        return False
    try:
        payload = jwt.decode(token, settings.session_secret, algorithms=[ALGORITHM])
        return payload.get("role") == "admin"
    except Exception:
        return False


def require_admin(request: Request):
    if not verify_admin(request):
        raise HTTPException(status_code=401, detail="管理者ログインが必要です")


@router.post("/login")
def login(body: LoginRequest, response: Response):
    if body.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="パスワードが正しくありません")
    token = create_token()
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=TOKEN_EXPIRE_HOURS * 3600,
    )
    return {"message": "ログインしました"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("session")
    return {"message": "ログアウトしました"}


@router.get("/me")
def me(request: Request):
    is_admin = verify_admin(request)
    return {"is_admin": is_admin}
