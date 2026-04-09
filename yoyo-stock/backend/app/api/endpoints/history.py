from fastapi import APIRouter, HTTPException
from app.services.history_service import get_trade_history, add_trade_record
from app.schemas.history import TradeRecord, TradeHistory

router = APIRouter()

@router.get("/trades", response_model=list[TradeRecord])
async def get_trades(start_date: str = None, end_date: str = None):
    """获取交易历史"""
    try:
        trades = await get_trade_history(start_date, end_date)
        return trades
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trades", response_model=TradeRecord)
async def add_trade(record: TradeRecord):
    """添加交易记录"""
    try:
        new_record = await add_trade_record(record)
        return new_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))