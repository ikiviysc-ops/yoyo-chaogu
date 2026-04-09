from fastapi import APIRouter, HTTPException
from app.services.risk_service import get_risk_config, update_risk_config
from app.schemas.risk import RiskConfig

router = APIRouter()

@router.get("/config", response_model=RiskConfig)
async def get_config(user_id: int = 1):
    """获取风控配置"""
    try:
        config = await get_risk_config(user_id)
        return config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/config", response_model=RiskConfig)
async def update_config(config: RiskConfig, user_id: int = 1):
    """更新风控配置"""
    try:
        updated_config = await update_risk_config(user_id, config)
        return updated_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))