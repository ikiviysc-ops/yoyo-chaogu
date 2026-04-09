import akshare as ak
import pandas as pd
from datetime import datetime

print("测试 Akshare 获取实时股票数据...")
print("=" * 60)

# 测试获取沪深A股实时数据
try:
    print("1. 获取沪深A股实时数据...")
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    print(f"成功获取 {len(stock_zh_a_spot_df)} 只股票数据")
    print("前5只股票:")
    print(stock_zh_a_spot_df.head())
    print()
except Exception as e:
    print(f"获取沪深A股实时数据失败: {e}")
    print()

# 测试获取上证指数数据
try:
    print("2. 获取上证指数数据...")
    stock_zh_index_spot_df = ak.stock_zh_index_spot()
    print(f"成功获取 {len(stock_zh_index_spot_df)} 个指数数据")
    # 查找上证指数
    sh_index = stock_zh_index_spot_df[stock_zh_index_spot_df['代码'] == '000001.SH']
    if not sh_index.empty:
        print("上证指数数据:")
        print(sh_index)
    else:
        print("未找到上证指数数据")
    print()
except Exception as e:
    print(f"获取指数数据失败: {e}")
    print()

# 测试获取单个股票数据
try:
    print("3. 获取单个股票数据 (贵州茅台)...")
    # 使用新浪财经数据源获取实时数据
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    maotai = stock_zh_a_spot_df[stock_zh_a_spot_df['代码'] == '600519.SH']
    if not maotai.empty:
        print("贵州茅台数据:")
        print(maotai)
    else:
        print("未找到贵州茅台数据")
    print()
except Exception as e:
    print(f"获取单个股票数据失败: {e}")
    print()

# 测试获取历史数据
try:
    print("4. 获取历史数据 (贵州茅台)...")
    stock_zh_a_hist_df = ak.stock_zh_a_hist(
        symbol="600519",
        period="daily",
        start_date="20260101",
        end_date=datetime.now().strftime("%Y%m%d"),
        adjust="qfq"
    )
    print(f"成功获取 {len(stock_zh_a_hist_df)} 条历史数据")
    print("最近5条历史数据:")
    print(stock_zh_a_hist_df.tail())
    print()
except Exception as e:
    print(f"获取历史数据失败: {e}")
    print()

print("=" * 60)
print("测试完成！")
