import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")

def get_trade_history(start_date: str = None, end_date: str = None):
    """获取交易历史"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT id, stock_code, buy_price, sell_price, profit_loss, profit_rate, trade_date FROM trade_record"
    params = []
    
    if start_date and end_date:
        query += " WHERE trade_date BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    elif start_date:
        query += " WHERE trade_date >= ?"
        params.append(start_date)
    elif end_date:
        query += " WHERE trade_date <= ?"
        params.append(end_date)
    
    cursor.execute(query, params)
    trades = cursor.fetchall()
    conn.close()
    
    result = []
    for trade in trades:
        result.append({
            "id": trade[0],
            "stock_code": trade[1],
            "buy_price": trade[2],
            "sell_price": trade[3],
            "profit_loss": trade[4],
            "profit_rate": trade[5],
            "trade_date": trade[6]
        })
    
    return result

def add_trade_record(record):
    """添加交易记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 计算盈亏
    profit_loss = record.sell_price - record.buy_price
    profit_rate = (profit_loss / record.buy_price) * 100
    
    # 插入交易记录
    cursor.execute('''
    INSERT INTO trade_record (stock_code, buy_price, sell_price, profit_loss, profit_rate, trade_date)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        record.stock_code,
        record.buy_price,
        record.sell_price,
        profit_loss,
        profit_rate,
        record.trade_date or datetime.now().strftime("%Y-%m-%d")
    ))
    
    trade_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": trade_id,
        "stock_code": record.stock_code,
        "buy_price": record.buy_price,
        "sell_price": record.sell_price,
        "profit_loss": profit_loss,
        "profit_rate": profit_rate,
        "trade_date": record.trade_date or datetime.now().strftime("%Y-%m-%d")
    }