import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "yoyo_stock.db")

def insert_test_data():
    """向数据库中插入测试数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 先删除今日已有的选股结果
    cursor.execute('DELETE FROM daily_selection WHERE select_date = ?', (today,))
    
    # 插入测试数据
    test_data = [
        {
            "select_date": today,
            "stock_code": "600519",
            "stock_name": "贵州茅台",
            "rise_rate": 3.25,
            "volume_ratio": 1.5,
            "turnover_rate": 6.8,
            "select_reason": "符合杨永兴尾盘买入策略：当日涨幅3.25%，20日内有涨停，量比1.5，换手率6.8%，股价在20日均线上方",
            "risk_tip": "风险提示：暂无明显风险"
        },
        {
            "select_date": today,
            "stock_code": "000858",
            "stock_name": "五粮液",
            "rise_rate": 4.12,
            "volume_ratio": 1.8,
            "turnover_rate": 5.2,
            "select_reason": "符合杨永兴尾盘买入策略：当日涨幅4.12%，20日内有涨停，量比1.8，换手率5.2%，股价在20日均线上方",
            "risk_tip": "风险提示：量比异常"
        },
        {
            "select_date": today,
            "stock_code": "601318",
            "stock_name": "中国平安",
            "rise_rate": 2.88,
            "volume_ratio": 1.3,
            "turnover_rate": 4.5,
            "select_reason": "符合杨永兴尾盘买入策略：当日涨幅2.88%，20日内有涨停，量比1.3，换手率4.5%，股价在20日均线上方",
            "risk_tip": "风险提示：暂无明显风险"
        }
    ]
    
    for stock in test_data:
        cursor.execute('''
        INSERT INTO daily_selection (select_date, stock_code, stock_name, rise_rate, volume_ratio, turnover_rate, select_reason, risk_tip)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            stock["select_date"],
            stock["stock_code"],
            stock["stock_name"],
            stock["rise_rate"],
            stock["volume_ratio"],
            stock["turnover_rate"],
            stock["select_reason"],
            stock["risk_tip"]
        ))
    
    # 提交更改
    conn.commit()
    conn.close()
    
    print("测试数据插入成功！")

if __name__ == "__main__":
    insert_test_data()