from fastapi import APIRouter
from app.api.endpoints import stocks, strategy, risk, auth, history

router = APIRouter()

# 注册各个模块的路由
router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
router.include_router(risk.router, prefix="/risk", tags=["risk"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(history.router, prefix="/history", tags=["history"])