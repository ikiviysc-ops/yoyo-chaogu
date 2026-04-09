from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.stock_service import filter_stocks
from app.services.strategy_service import get_market_analysis, generate_strategy_log
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def init_scheduler():
    """初始化定时任务"""
    # 每日09:00执行盘前市场分析
    scheduler.add_job(
        func=market_analysis_job,
        trigger=CronTrigger(hour=9, minute=0),
        id='market_analysis',
        name='盘前市场分析',
        replace_existing=True
    )
    
    # 每日09:35执行低估超跌选股
    scheduler.add_job(
        func=value_stock_selection_job,
        trigger=CronTrigger(hour=9, minute=35),
        id='value_stock_selection',
        name='低估超跌选股',
        replace_existing=True
    )
    
    # 每日14:30执行隔夜套利核心选股
    scheduler.add_job(
        func=core_stock_selection_job,
        trigger=CronTrigger(hour=14, minute=30),
        id='core_stock_selection',
        name='隔夜套利核心选股',
        replace_existing=True
    )
    
    # 每日15:10执行收盘复盘统计
    scheduler.add_job(
        func=market_summary_job,
        trigger=CronTrigger(hour=15, minute=10),
        id='market_summary',
        name='收盘复盘统计',
        replace_existing=True
    )
    
    # 启动调度器
    scheduler.start()
    logger.info("定时任务调度器已启动")

def market_analysis_job():
    """盘前市场分析任务"""
    try:
        logger.info("开始执行盘前市场分析...")
        analysis = get_market_analysis()
        logger.info(f"盘前市场分析完成: {analysis['market_summary']}")
    except Exception as e:
        logger.error(f"盘前市场分析任务失败: {str(e)}")

def value_stock_selection_job():
    """低估超跌选股任务"""
    try:
        logger.info("开始执行低估超跌选股...")
        # 这里可以实现低估超跌选股逻辑
        # 暂时复用核心选股逻辑
        stocks = filter_stocks()
        logger.info(f"低估超跌选股完成，选出{len(stocks)}只股票")
    except Exception as e:
        logger.error(f"低估超跌选股任务失败: {str(e)}")

def core_stock_selection_job():
    """隔夜套利核心选股任务"""
    try:
        logger.info("开始执行隔夜套利核心选股...")
        stocks = filter_stocks()
        logger.info(f"隔夜套利核心选股完成，选出{len(stocks)}只股票")
    except Exception as e:
        logger.error(f"隔夜套利核心选股任务失败: {str(e)}")

def market_summary_job():
    """收盘复盘统计任务"""
    try:
        logger.info("开始执行收盘复盘统计...")
        log = generate_strategy_log()
        logger.info(f"收盘复盘统计完成，成功率: {log['success_rate']}, 总盈利: {log['total_profit']}%")
    except Exception as e:
        logger.error(f"收盘复盘统计任务失败: {str(e)}")