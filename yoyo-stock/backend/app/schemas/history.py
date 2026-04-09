from pydantic import BaseModel

class TradeRecord(BaseModel):
    id: int
    stock_code: str
    buy_price: float
    sell_price: float
    profit_loss: float
    profit_rate: float
    trade_date: str

class TradeHistory(BaseModel):
    records: list[TradeRecord]
    total_profit: float
    success_rate: float