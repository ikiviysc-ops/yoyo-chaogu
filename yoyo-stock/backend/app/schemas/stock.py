from pydantic import BaseModel

class StockInfo(BaseModel):
    id: int
    stock_code: str
    stock_name: str
    market: str = None
    float_capital: float = None
    is_st: int = 0
    is_delist: int = 0

class StockSelection(BaseModel):
    id: int
    select_date: str
    stock_code: str
    stock_name: str
    rise_rate: float
    volume_ratio: float
    turnover_rate: float
    select_reason: str
    risk_tip: str