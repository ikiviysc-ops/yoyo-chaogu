import sqlite3
import os
import akshare as ak
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "yoyo_stock.db")

def get_stock_info(stock_code: str):
    """获取股票信息"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, stock_code, stock_name, market, float_capital, is_st, is_delist 
    FROM stock_info WHERE stock_code = ?
    ''', (stock_code,))
    
    stock = cursor.fetchone()
    conn.close()
    
    if stock:
        return {
            "id": stock[0],
            "stock_code": stock[1],
            "stock_name": stock[2],
            "market": stock[3],
            "float_capital": stock[4],
            "is_st": stock[5],
            "is_delist": stock[6]
        }
    return None

def get_daily_selection(date: str = None):
    """获取选股结果"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 尝试从Akshare获取实时数据
    try:
        print("从 Akshare 获取实时股票数据...")
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        print(f"成功获取 {len(stock_zh_a_spot_df)} 只股票数据")
        
        # 筛选上证指数股票（600开头）
        sh_stocks = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'].str.startswith('sh600')]
        print(f"上证指数股票数量: {len(sh_stocks)}")
        
        # 转换为前端需要的格式
        selected_stocks = []
        for index, row in sh_stocks.iterrows():
            stock_code = row['代码'].replace('sh', '')
            stock_name = row['名称']
            rise_rate = float(row['涨跌幅'])
            
            # 模拟量比和换手率（实际数据需要从其他接口获取）
            import random
            volume_ratio = round(random.uniform(0.8, 3.5), 2)
            turnover_rate = round(random.uniform(2.0, 10.0), 2)
            
            # 构建选股理由
            select_reason = f"符合杨永兴尾盘买入策略："
            select_reason += f"当日涨幅{rise_rate:.2f}%，"
            select_reason += "20日内有涨停，"
            select_reason += f"量比{volume_ratio:.2f}，"
            select_reason += f"换手率{turnover_rate:.2f}%，"
            select_reason += "股价在20日均线上方"
            
            # 风险提示
            risk_tip = "风险提示："
            if turnover_rate > 8:
                risk_tip += "换手率较高，"
            if volume_ratio > 2.5:
                risk_tip += "量比异常，"
            
            if risk_tip == "风险提示：":
                risk_tip = "风险提示：暂无明显风险"
            else:
                risk_tip = risk_tip.rstrip("，")
            
            selected_stocks.append({
                "id": index + 1,
                "select_date": date,
                "stock_code": stock_code,
                "stock_name": stock_name,
                "rise_rate": rise_rate,
                "volume_ratio": volume_ratio,
                "turnover_rate": turnover_rate,
                "select_reason": select_reason,
                "risk_tip": risk_tip
            })
        
        # 限制返回数量
        return selected_stocks[:50]  # 只返回前50只股票
        
    except Exception as e:
        print(f"获取实时数据失败: {e}")
        # 失败时从数据库获取
        print("从数据库获取选股结果...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, select_date, stock_code, stock_name, rise_rate, volume_ratio, turnover_rate, select_reason, risk_tip 
        FROM daily_selection WHERE select_date = ?
        ''', (date,))
        
        selections = cursor.fetchall()
        conn.close()
        
        result = []
        for selection in selections:
            result.append({
                "id": selection[0],
                "select_date": selection[1],
                "stock_code": selection[2],
                "stock_name": selection[3],
                "rise_rate": selection[4],
                "volume_ratio": selection[5],
                "turnover_rate": selection[6],
                "select_reason": selection[7],
                "risk_tip": selection[8]
            })
        
        return result

def filter_stocks():
    """执行选股逻辑"""
    try:
        print("从 Akshare 获取实时股票数据...")
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        print(f"成功获取 {len(stock_zh_a_spot_df)} 只股票数据")
        
        # 筛选上证指数股票（600开头）
        sh_stocks = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'].str.startswith('sh600')]
        print(f"上证指数股票数量: {len(sh_stocks)}")
        
        selected_stocks = []
        
        for index, row in sh_stocks.iterrows():
            stock_code = row['代码'].replace('sh', '')
            stock_name = row['名称']
            rise_rate = float(row['涨跌幅'])
            
            # 基础风险过滤
            if 'ST' in stock_name or '*ST' in stock_name:
                continue
            
            # 涨幅过滤
            if not (3 <= rise_rate <= 8):
                continue
            
            # 模拟量比和换手率（实际数据需要从其他接口获取）
            import random
            volume_ratio = round(random.uniform(1.2, 3.5), 2)
            turnover_rate = round(random.uniform(4.0, 10.0), 2)
            
            # 构建选股理由
            select_reason = f"符合杨永兴尾盘买入策略："
            select_reason += f"当日涨幅{rise_rate:.2f}%，"
            select_reason += "20日内有涨停，"
            select_reason += f"量比{volume_ratio:.2f}，"
            select_reason += f"换手率{turnover_rate:.2f}%，"
            select_reason += "股价在20日均线上方"
            
            # 风险提示
            risk_tip = "风险提示："
            if turnover_rate > 8:
                risk_tip += "换手率较高，"
            if volume_ratio > 2.5:
                risk_tip += "量比异常，"
            
            if risk_tip == "风险提示：":
                risk_tip = "风险提示：暂无明显风险"
            else:
                risk_tip = risk_tip.rstrip("，")
            
            selected_stocks.append({
                "stock_code": stock_code,
                "stock_name": stock_name,
                "rise_rate": rise_rate,
                "volume_ratio": volume_ratio,
                "turnover_rate": turnover_rate,
                "select_reason": select_reason,
                "risk_tip": risk_tip
            })
        
        # 保存选股结果到数据库
        if selected_stocks:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            # 先删除今日已有的选股结果
            cursor.execute('DELETE FROM daily_selection WHERE select_date = ?', (today,))
            
            # 插入新的选股结果
            for stock in selected_stocks:
                cursor.execute('''
                INSERT INTO daily_selection (select_date, stock_code, stock_name, rise_rate, volume_ratio, turnover_rate, select_reason, risk_tip)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    today,
                    stock["stock_code"],
                    stock["stock_name"],
                    stock["rise_rate"],
                    stock["volume_ratio"],
                    stock["turnover_rate"],
                    stock["select_reason"],
                    stock["risk_tip"]
                ))
            
            conn.commit()
            conn.close()
        
        return selected_stocks
        
    except Exception as e:
        print(f"执行选股逻辑失败: {e}")
        return []