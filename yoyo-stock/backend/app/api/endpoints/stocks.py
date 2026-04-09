from fastapi import APIRouter, HTTPException
from app.services.stock_service import get_stock_info, get_daily_selection
from app.schemas.stock import StockInfo, StockSelection

router = APIRouter()

@router.get("/info/{stock_code}", response_model=StockInfo)
async def get_stock(stock_code: str):
    """获取单个股票信息"""
    try:
        stock = await get_stock_info(stock_code)
        if not stock:
            raise HTTPException(status_code=404, detail="股票不存在")
        return stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/selection", response_model=list[StockSelection])
async def get_selection(date: str = None):
    """获取选股结果"""
    try:
        selections = await get_daily_selection(date)
        return selections
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))