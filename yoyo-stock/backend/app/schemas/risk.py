from pydantic import BaseModel

class RiskConfig(BaseModel):
    id: int
    user_id: int
    single_position: float
    total_position: float
    stop_loss_rate: float
    consecutive_loss: int