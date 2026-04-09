import sqlite3
import os
import baostock as bs
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
    # 登录baostock
    lg = bs.login()
    if lg.error_code != '0':
        print(f"登录失败: {lg.error_msg}")
        return []
    
    # 获取所有A股股票
    rs = bs.query_all_stock(day=datetime.now().strftime("%Y-%m-%d"))
    stock_list = []
    while (rs.error_code == '0') & rs.next():
        stock_list.append(rs.get_row_data())
    
    selected_stocks = []
    
    for stock in stock_list:
        stock_code = stock[0]
        stock_name = stock[2]
        
        # 基础风险过滤
        if 'ST' in stock_name or '*ST' in stock_name:
            continue
        
        # 获取股票基本信息
        rs_basic = bs.query_stock_basic(code=stock_code)
        if rs_basic.error_code != '0':
            continue
        basic_info = rs_basic.get_row_data()
        if not basic_info:
            continue
        
        # 流通市值过滤
        float_capital = float(basic_info[13]) if basic_info[13] else 0
        if float_capital >= 20000000000:  # 200亿
            continue
        
        # 获取历史行情
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        rs_daily = bs.query_history_k_data_plus(
            stock_code,
            "date,open,high,low,close,volume,amount,turn,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )
        
        if rs_daily.error_code != '0':
            continue
        
        daily_data = []
        while (rs_daily.error_code == '0') & rs_daily.next():
            daily_data.append(rs_daily.get_row_data())
        
        if len(daily_data) < 20:
            continue
        
        # 计算20日均线
        close_prices = [float(item[4]) for item in daily_data]
        ma20 = sum(close_prices[-20:]) / 20
        
        # 最新数据
        latest = daily_data[-1]
        close_price = float(latest[4])
        turnover_rate = float(latest[7]) if latest[7] else 0
        
        # 计算涨幅
        prev_close = float(daily_data[-2][4]) if len(daily_data) > 1 else close_price
        rise_rate = (close_price - prev_close) / prev_close * 100
        
        # 计算量比（简化计算，实际应该是今日成交量/过去5日平均成交量）
        if len(daily_data) >= 6:
            current_volume = float(latest[5])
            avg_volume = sum([float(item[5]) for item in daily_data[-6:-1]]) / 5
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 0
        else:
            volume_ratio = 0
        
        # 检查近期是否有涨停
        has_limit_up = False
        for item in daily_data[-20:]:
            high = float(item[2])
            low = float(item[3])
            prev_close = float(daily_data[daily_data.index(item) - 1][4]) if daily_data.index(item) > 0 else high
            limit_up = prev_close * 1.1  # 涨停价
            if high >= limit_up * 0.995:  # 允许小幅误差
                has_limit_up = True
                break
        
        # 选股条件检查
        if (
            3 <= rise_rate <= 5 and
            has_limit_up and
            volume_ratio >= 1.2 and
            5 <= turnover_rate <= 10 and
            close_price > ma20
        ):
            # 构建选股理由
            select_reason = "符合杨永兴尾盘买入策略："
            select_reason += f"当日涨幅{rise_rate:.2f}%，"
            select_reason += "20日内有涨停，"
            select_reason += f"量比{volume_ratio:.2f}，"
            select_reason += f"换手率{turnover_rate:.2f}%，"
            select_reason += "股价在20日均线上方"
            
            # 风险提示
            risk_tip = "风险提示："
            if turnover_rate > 8:
                risk_tip += "换手率较高，"
            if volume_ratio > 3:
                risk_tip += "量比异常，"
            if float_capital < 5000000000:  # 5亿
                risk_tip += "流通市值较小，"
            
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
    
    # 登出baostock
    bs.logout()
    
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