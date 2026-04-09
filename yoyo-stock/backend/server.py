import http.server
import socketserver
import json
import os
import sqlite3
from datetime import datetime, timedelta

PORT = 8001

DB_PATH = os.path.join(os.path.dirname(__file__), "yoyo_stock.db")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 处理API请求
        if self.path.startswith("/api/"):
            self.handle_api_request()
        else:
            # 处理静态文件请求
            super().do_GET()
    
    def handle_api_request(self):
        # 解析API路径
        path_parts = self.path.split("/")
        if len(path_parts) < 3:
            self.send_error(404, "Not Found")
            return
        
        api_endpoint = path_parts[2]
        
        # 处理不同的API端点
        if api_endpoint == "stocks":
            if len(path_parts) > 3:
                if path_parts[3] == "info" and len(path_parts) > 4:
                    # 获取单个股票信息
                    stock_code = path_parts[4]
                    self.get_stock_info(stock_code)
                elif path_parts[3] == "selection":
                    # 获取选股结果
                    self.get_daily_selection()
                else:
                    self.send_error(404, "Not Found")
            else:
                self.send_error(404, "Not Found")
        else:
            self.send_error(404, "Not Found")
    
    def get_stock_info(self, stock_code):
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
            response = {
                "id": stock[0],
                "stock_code": stock[1],
                "stock_name": stock[2],
                "market": stock[3],
                "float_capital": stock[4],
                "is_st": stock[5],
                "is_delist": stock[6]
            }
            self.send_json_response(200, response)
        else:
            self.send_json_response(404, {"detail": "股票不存在"})
    
    def get_daily_selection(self):
        """获取选股结果"""
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
        
        self.send_json_response(200, result)
    
    def send_json_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

if __name__ == "__main__":
    # 更改当前工作目录到backend目录
    os.chdir(os.path.dirname(__file__))
    
    # 创建服务器
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        print(f"服务器运行在 http://0.0.0.0:{PORT}")
        httpd.serve_forever()