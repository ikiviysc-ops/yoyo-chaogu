import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")

def get_market_analysis(date: str = None):
    """获取市场分析"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟市场分析数据
    # 实际项目中应该从API获取真实数据
    analysis = {
        "date": date,
        "market_sentiment": "中性",
        "position_advice": "保守",
        "risk_level": "中等",
        "market_summary": "今日大盘震荡整理，成交量萎缩，建议控制仓位，关注业绩优良的蓝筹股。"
    }
    
    return analysis

def get_strategy_log(start_date: str = None, end_date: str = None):
    """获取策略执行日志"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT id, log_date, success_rate, total_profit, update_param, execution_status FROM strategy_log"
    params = []
    
    if start_date and end_date:
        query += " WHERE log_date BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    elif start_date:
        query += " WHERE log_date >= ?"
        params.append(start_date)
    elif end_date:
        query += " WHERE log_date <= ?"
        params.append(end_date)
    
    cursor.execute(query, params)
    logs = cursor.fetchall()
    conn.close()
    
    result = []
    for log in logs:
        result.append({
            "id": log[0],
            "log_date": log[1],
            "success_rate": log[2],
            "total_profit": log[3],
            "update_param": log[4],
            "execution_status": log[5]
        })
    
    return result

def generate_strategy_log():
    """生成策略执行日志"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 统计今日选股结果
    cursor.execute('SELECT COUNT(*) FROM daily_selection WHERE select_date = ?', (today,))
    total_count = cursor.fetchone()[0]
    
    # 模拟成功率和总盈亏
    # 实际项目中应该基于真实交易数据计算
    success_rate = 0.65  # 65%成功率
    total_profit = 2.5  # 2.5%总盈利
    
    # 策略更新参数
    update_param = "调整选股条件：将量比阈值从1.2调整为1.1"
    
    # 执行状态
    execution_status = "成功"
    
    # 插入策略日志
    cursor.execute('''
    INSERT INTO strategy_log (log_date, success_rate, total_profit, update_param, execution_status)
    VALUES (?, ?, ?, ?, ?)
    ''', (today, success_rate, total_profit, update_param, execution_status))
    
    conn.commit()
    conn.close()
    
    return {
        "log_date": today,
        "success_rate": success_rate,
        "total_profit": total_profit,
        "update_param": update_param,
        "execution_status": execution_status
    }