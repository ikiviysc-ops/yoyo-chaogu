import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")

def create_message_table():
    """创建消息表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL,
        user_id INTEGER DEFAULT 1,
        read INTEGER DEFAULT 0,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def send_message(title: str, message: str, message_type: str = "info", user_id: int = 1):
    """发送消息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO message (title, message, type, user_id)
    VALUES (?, ?, ?, ?)
    ''', (title, message, message_type, user_id))
    
    message_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "id": message_id,
        "title": title,
        "message": message,
        "type": message_type,
        "user_id": user_id,
        "read": 0,
        "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_messages(user_id: int = 1, limit: int = 10):
    """获取用户消息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, title, message, type, read, create_time 
    FROM message 
    WHERE user_id = ? 
    ORDER BY create_time DESC 
    LIMIT ?
    ''', (user_id, limit))
    
    messages = cursor.fetchall()
    conn.close()
    
    result = []
    for msg in messages:
        result.append({
            "id": msg[0],
            "title": msg[1],
            "message": msg[2],
            "type": msg[3],
            "read": msg[4],
            "create_time": msg[5]
        })
    
    return result

def mark_message_as_read(message_id: int):
    """标记消息为已读"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE message SET read = 1 WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()
    
    return True