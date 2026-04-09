from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.services.scheduler import init_scheduler
import uvicorn

app = FastAPI(
    title="YOYO炒股系统API",
    description="基于杨永兴尾盘买入策略的智能选股系统",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)

# 启动时初始化定时任务
@app.on_event("startup")
async def startup_event():
    init_scheduler()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)