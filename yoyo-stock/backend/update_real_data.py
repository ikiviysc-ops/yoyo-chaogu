import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.stock_service import filter_stocks
from datetime import datetime

print("=" * 50)
print("开始获取真实股票数据...")
print("=" * 50)
print()

# 执行选股
selected_stocks = filter_stocks()

print()
print("=" * 50)
if selected_stocks:
    print(f"选股完成！共选出 {len(selected_stocks)} 只股票")
    print()
    for i, stock in enumerate(selected_stocks, 1):
        print(f"{i}. {stock['stock_name']} ({stock['stock_code']})")
        print(f"   涨幅: {stock['rise_rate']:.2f}%, 量比: {stock['volume_ratio']:.2f}, 换手率: {stock['turnover_rate']:.2f}%")
        print()
else:
    print("没有选出符合条件的股票")
print("=" * 50)
