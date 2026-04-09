from fastapi import APIRouter, HTTPException
from app.services.strategy_service import get_market_analysis, get_strategy_log
from app.schemas.strategy import MarketAnalysis, StrategyLog

router = APIRouter()

@router.get("/market-analysis", response_model=MarketAnalysis)
async def get_analysis(date: str = None):
    """获取市场分析"""
    try:
        analysis = await get_market_analysis(date)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs", response_model=list[StrategyLog])
async def get_logs(start_date: str = None, end_date: str = None):
    """获取策略执行日志"""
    try:
        logs = await get_strategy_log(start_date, end_date)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))