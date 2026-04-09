import http.server
import socketserver
import json
import os
from datetime import datetime, timedelta
from app.services.stock_service import get_daily_selection, get_stock_info, filter_stocks

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
    
    def do_POST(self):
        # 处理API请求
        if self.path.startswith("/api/"):
            self.handle_api_request()
        else:
            # 处理静态文件请求
            super().do_POST()
    
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
                elif path_parts[3] == "filter" and self.command == "POST":
                    # 执行选股
                    self.post_filter_stocks()
                else:
                    self.send_error(404, "Not Found")
            else:
                self.send_error(404, "Not Found")
        else:
            self.send_error(404, "Not Found")
    
    def get_stock_info(self, stock_code):
        """获取股票信息"""
        stock = get_stock_info(stock_code)
        
        if stock:
            self.send_json_response(200, stock)
        else:
            self.send_json_response(404, {"detail": "股票不存在"})
    
    def get_daily_selection(self):
        """获取选股结果"""
        selections = get_daily_selection()
        self.send_json_response(200, selections)
    
    def post_filter_stocks(self):
        """执行选股"""
        # 读取请求体
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # 执行选股
        selected_stocks = filter_stocks()
        
        # 返回选股结果
        self.send_json_response(200, selected_stocks)
    
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