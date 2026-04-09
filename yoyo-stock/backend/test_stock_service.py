import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from services.stock_service import get_daily_selection, filter_stocks

print("测试股票服务...")
print("=" * 60)

# 测试获取选股结果
print("1. 测试获取选股结果...")
try:
    selections = get_daily_selection()
    print(f"成功获取 {len(selections)} 只股票数据")
    if selections:
        print("前5只股票:")
        for i, stock in enumerate(selections[:5], 1):
            print(f"{i}. {stock['stock_name']} ({stock['stock_code']}) - 涨幅: {stock['rise_rate']:.2f}%")
    print()
except Exception as e:
    print(f"获取选股结果失败: {e}")
    print()

# 测试执行选股逻辑
print("2. 测试执行选股逻辑...")
try:
    selected_stocks = filter_stocks()
    print(f"成功选出 {len(selected_stocks)} 只股票")
    if selected_stocks:
        print("前5只选股结果:")
        for i, stock in enumerate(selected_stocks[:5], 1):
            print(f"{i}. {stock['stock_name']} ({stock['stock_code']}) - 涨幅: {stock['rise_rate']:.2f}%")
    print()
except Exception as e:
    print(f"执行选股逻辑失败: {e}")
    print()

print("=" * 60)
print("测试完成！")
