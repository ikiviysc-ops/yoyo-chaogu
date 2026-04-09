import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")

def get_risk_config(user_id: int = 1):
    """获取风控配置"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, user_id, single_position, total_position, stop_loss_rate, consecutive_loss 
    FROM risk_config WHERE user_id = ?
    ''', (user_id,))
    
    config = cursor.fetchone()
    conn.close()
    
    if config:
        return {
            "id": config[0],
            "user_id": config[1],
            "single_position": config[2],
            "total_position": config[3],
            "stop_loss_rate": config[4],
            "consecutive_loss": config[5]
        }
    
    # 如果没有配置，返回默认值
    return {
        "id": 0,
        "user_id": user_id,
        "single_position": 0.15,
        "total_position": 0.3,
        "stop_loss_rate": 0.03,
        "consecutive_loss": 3
    }

def update_risk_config(user_id: int, config):
    """更新风控配置"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查是否已有配置
    cursor.execute('SELECT id FROM risk_config WHERE user_id = ?', (user_id,))
    existing = cursor.fetchone()
    
    if existing:
        # 更新现有配置
        cursor.execute('''
        UPDATE risk_config SET 
            single_position = ?, 
            total_position = ?, 
            stop_loss_rate = ?, 
            consecutive_loss = ? 
        WHERE user_id = ?
        ''', (
            config.single_position,
            config.total_position,
            config.stop_loss_rate,
            config.consecutive_loss,
            user_id
        ))
        config_id = existing[0]
    else:
        # 插入新配置
        cursor.execute('''
        INSERT INTO risk_config (user_id, single_position, total_position, stop_loss_rate, consecutive_loss)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            user_id,
            config.single_position,
            config.total_position,
            config.stop_loss_rate,
            config.consecutive_loss
        ))
        config_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return {
        "id": config_id,
        "user_id": user_id,
        "single_position": config.single_position,
        "total_position": config.total_position,
        "stop_loss_rate": config.stop_loss_rate,
        "consecutive_loss": config.consecutive_loss
    }