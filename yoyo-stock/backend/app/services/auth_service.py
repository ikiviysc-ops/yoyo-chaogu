import sqlite3
import os
import jwt
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")
SECRET_KEY = "your-secret-key"  # 实际项目中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def login(username: str, password: str):
    """用户登录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, username, password FROM user WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or user[2] != password:  # 实际项目中应该使用密码哈希
        raise Exception("用户名或密码错误")
    
    # 生成JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": str(user[0]),
        "username": user[1],
        "exp": datetime.utcnow() + access_token_expires
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token

def register(username: str, password: str, phone: str):
    """用户注册"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查用户名是否已存在
    cursor.execute('SELECT id FROM user WHERE username = ?', (username,))
    if cursor.fetchone():
        conn.close()
        raise Exception("用户名已存在")
    
    # 插入新用户
    cursor.execute('''
    INSERT INTO user (username, password, phone) VALUES (?, ?, ?)
    ''', (username, password, phone))
    user_id = cursor.lastrowid
    
    # 创建默认风控配置
    cursor.execute('''
    INSERT INTO risk_config (user_id, single_position, total_position, stop_loss_rate, consecutive_loss)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, 0.15, 0.3, 0.03, 3))
    
    conn.commit()
    conn.close()
    
    # 生成JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": str(user_id),
        "username": username,
        "exp": datetime.utcnow() + access_token_expires
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token