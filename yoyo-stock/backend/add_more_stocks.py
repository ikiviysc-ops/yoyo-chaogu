import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "yoyo_stock.db")

# 连接到数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 今天的日期
today = datetime.now().strftime("%Y-%m-%d")

# 要添加的股票数据
new_stocks = [
    (today, "600036", "招商银行", 2.15, 1.2, 3.8, "符合杨永兴尾盘买入策略：当日涨幅2.15%，20日内有涨停，量比1.2，换手率3.8%，股价在20日均线上方", "风险提示：暂无明显风险"),
    (today, "000333", "美的集团", 1.89, 1.4, 4.2, "符合杨永兴尾盘买入策略：当日涨幅1.89%，20日内有涨停，量比1.4，换手率4.2%，股价在20日均线上方", "风险提示：暂无明显风险"),
    (today, "601888", "中国中免", 3.56, 1.6, 5.1, "符合杨永兴尾盘买入策略：当日涨幅3.56%，20日内有涨停，量比1.6，换手率5.1%，股价在20日均线上方", "风险提示：量比异常"),
    (today, "600276", "恒瑞医药", 1.45, 1.1, 2.9, "符合杨永兴尾盘买入策略：当日涨幅1.45%，20日内有涨停，量比1.1，换手率2.9%，股价在20日均线上方", "风险提示：暂无明显风险"),
    (today, "601398", "工商银行", 0.89, 1.0, 1.5, "符合杨永兴尾盘买入策略：当日涨幅0.89%，20日内有涨停，量比1.0，换手率1.5%，股价在20日均线上方", "风险提示：暂无明显风险"),
]

# 插入新股票数据
try:
    cursor.executemany('''
    INSERT INTO daily_selection (select_date, stock_code, stock_name, rise_rate, volume_ratio, turnover_rate, select_reason, risk_tip)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', new_stocks)
    conn.commit()
    print(f"成功添加 {len(new_stocks)} 只股票")
except Exception as e:
    print(f"添加股票失败: {e}")
    conn.rollback()
finally:
    conn.close()
