import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")

def init_db():
    """初始化数据库，创建所有必要的表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建用户信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建股票基础信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stock_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_code TEXT UNIQUE NOT NULL,
        stock_name TEXT NOT NULL,
        market TEXT,
        float_capital REAL,
        is_st INTEGER DEFAULT 0,
        is_delist INTEGER DEFAULT 0
    )
    ''')
    
    # 创建每日选股结果表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_selection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        select_date TEXT NOT NULL,
        stock_code TEXT NOT NULL,
        stock_name TEXT NOT NULL,
        rise_rate REAL,
        volume_ratio REAL,
        turnover_rate REAL,
        select_reason TEXT,
        risk_tip TEXT,
        FOREIGN KEY (stock_code) REFERENCES stock_info(stock_code)
    )
    ''')
    
    # 创建风控配置表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS risk_config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        single_position REAL DEFAULT 0.15,
        total_position REAL DEFAULT 0.3,
        stop_loss_rate REAL DEFAULT 0.03,
        consecutive_loss INTEGER DEFAULT 3,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    ''')
    
    # 创建历史交易记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trade_record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_code TEXT NOT NULL,
        buy_price REAL,
        sell_price REAL,
        profit_loss REAL,
        profit_rate REAL,
        trade_date TEXT,
        FOREIGN KEY (stock_code) REFERENCES stock_info(stock_code)
    )
    ''')
    
    # 创建策略日志表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS strategy_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_date TEXT NOT NULL,
        success_rate REAL,
        total_profit REAL,
        update_param TEXT,
        execution_status TEXT
    )
    ''')
    
    # 创建消息表
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
    
    # 创建默认用户
    cursor.execute('''
    INSERT OR IGNORE INTO user (username, password, phone) VALUES (?, ?, ?)
    ''', ('admin', 'admin123', '13800138000'))
    
    # 创建默认风控配置
    cursor.execute('''
    INSERT OR IGNORE INTO risk_config (user_id, single_position, total_position, stop_loss_rate, consecutive_loss) 
    VALUES (?, ?, ?, ?, ?)
    ''', (1, 0.15, 0.3, 0.03, 3))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("数据库初始化完成")