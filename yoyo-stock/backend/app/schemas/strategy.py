from pydantic import BaseModel

class MarketAnalysis(BaseModel):
    date: str
    market_sentiment: str
    position_advice: str
    risk_level: str
    market_summary: str

class StrategyLog(BaseModel):
    id: int
    log_date: str
    success_rate: float
    total_profit: float
    update_param: str
    execution_status: str