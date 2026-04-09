from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import login, register
from app.schemas.auth import LoginRequest, RegisterRequest, AuthResponse

router = APIRouter()

@router.post("/login", response_model=AuthResponse)
async def user_login(request: LoginRequest):
    """用户登录"""
    try:
        token = await login(request.username, request.password)
        return AuthResponse(token=token, message="登录成功")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/register", response_model=AuthResponse)
async def user_register(request: RegisterRequest):
    """用户注册"""
    try:
        token = await register(request.username, request.password, request.phone)
        return AuthResponse(token=token, message="注册成功")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))