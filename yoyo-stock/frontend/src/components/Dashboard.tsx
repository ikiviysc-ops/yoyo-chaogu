import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, History, Shield } from 'lucide-react';

const Dashboard: React.FC = () => {
  // 按钮点击处理函数
  const handleButtonClick = (action: string) => {
    console.log(`${action} 按钮被点击`);
    // 这里可以添加具体的功能逻辑
  };

  const handleCopyCode = (code: string) => {
    console.log(`复制代码: ${code}`);
    // 这里可以添加复制到剪贴板的逻辑
  };
  
  // 状态管理
  const [marketData, setMarketData] = useState({
    index: '3,258.63',
    change: '+0.25%',
    up: 1856,
    down: 2143,
  });

  const [positionAdvice, setPositionAdvice] = useState({
    level: '保守',
    risk: '中等',
    suggestion: '控制仓位，关注业绩优良的蓝筹股',
  });

  const [selectedStocks, setSelectedStocks] = useState([
    {
      id: 1,
      code: '600519',
      name: '贵州茅台',
      price: '1,789.00',
      change: '+3.25%',
      volumeRatio: 1.5,
      turnover: 6.8,
      reason: '符合杨永兴尾盘买入策略：当日涨幅3.25%，20日内有涨停，量比1.5，换手率6.8%，股价在20日均线上方',
      risk: '风险提示：暂无明显风险',
    },
    {
      id: 2,
      code: '000858',
      name: '五粮液',
      price: '168.50',
      change: '+4.12%',
      volumeRatio: 1.8,
      turnover: 5.2,
      reason: '符合杨永兴尾盘买入策略：当日涨幅4.12%，20日内有涨停，量比1.8，换手率5.2%，股价在20日均线上方',
      risk: '风险提示：量比异常',
    },
  ]);

  // 从后端API获取数据
  useEffect(() => {
    const fetchData = async () => {
      try {
        // 获取选股结果
        const selectionResponse = await fetch('/api/stocks/selection');
        if (selectionResponse.ok) {
          const selectionData = await selectionResponse.json();
          if (selectionData.length > 0) {
            // 转换数据格式以匹配前端需要的结构
            const formattedStocks = selectionData.map((stock: any) => ({
              id: stock.id,
              code: stock.stock_code,
              name: stock.stock_name,
              price: '1,000.00', // 模拟价格
              change: `+${stock.rise_rate}%`,
              volumeRatio: stock.volume_ratio,
              turnover: stock.turnover_rate,
              reason: stock.select_reason,
              risk: stock.risk_tip,
            }));
            setSelectedStocks(formattedStocks);
          }
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        console.error('Error type:', typeof error);
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container mx-auto px-4 pt-16 pb-16 bg-background min-h-screen">
      {/* 市场概览 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        <div className="bg-white rounded-lg shadow-sm p-3">
          <h3 className="text-xs text-gray-500 mb-1">大盘指数</h3>
          <div className="flex items-baseline">
            <span className="text-xl font-bold">{marketData.index}</span>
            <span className="ml-1 text-success">{marketData.change}</span>
          </div>
          <div className="flex justify-between mt-1 text-xs">
            <span className="text-success">上涨 {marketData.up}</span>
            <span className="text-danger">下跌 {marketData.down}</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-3">
          <h3 className="text-xs text-gray-500 mb-1">仓位建议</h3>
          <div className="flex items-center">
            <span className="text-lg font-bold">{positionAdvice.level}</span>
            <span className="ml-1 px-1.5 py-0.5 bg-yellow-100 text-yellow-800 rounded-full text-xs">
              {positionAdvice.risk}风险
            </span>
          </div>
          <p className="mt-1 text-xs text-gray-600">{positionAdvice.suggestion}</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-3">
          <h3 className="text-xs text-gray-500 mb-1">今日选股</h3>
          <div className="flex items-center justify-between">
            <span className="text-xl font-bold">{selectedStocks.length}</span>
            <span className="text-xs text-gray-500">只优质标的</span>
          </div>
          <button 
            className="mt-2 w-full py-1.5 bg-primary text-white rounded-lg text-xs hover:bg-primary/90 transition-colors"
            onClick={() => handleButtonClick('查看详情')}
          >
            查看详情
          </button>
        </div>
      </div>

      {/* 选股结果 */}
      <div className="mb-6">
        <h2 className="text-base font-bold mb-3">今日选股结果</h2>
        <div className="space-y-3">
          {selectedStocks.map((stock) => (
            <div key={stock.id} className="bg-white rounded-lg shadow-sm p-3">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center">
                    <h3 className="font-bold text-sm">{stock.name}</h3>
                    <span className="ml-1 text-xs text-gray-500">{stock.code}</span>
                  </div>
                  <div className="flex items-baseline mt-1">
                    <span className="text-base font-bold">{stock.price}</span>
                    <span className="ml-1 text-success">{stock.change}</span>
                  </div>
                </div>
                <button 
                  className="px-2 py-1 border border-primary text-primary rounded-lg text-xs hover:bg-primary/10 transition-colors"
                  onClick={() => handleCopyCode(stock.code)}
                >
                  复制代码
                </button>
              </div>
              <div className="grid grid-cols-2 gap-1 mt-2 text-xs">
                <div>
                  <span className="text-gray-500">量比：</span>
                  <span>{stock.volumeRatio}</span>
                </div>
                <div>
                  <span className="text-gray-500">换手率：</span>
                  <span>{stock.turnover}%</span>
                </div>
              </div>
              <div className="mt-2 text-xs">
                <p className="text-gray-600 line-clamp-2">{stock.reason}</p>
                <p className="mt-0.5 text-danger">{stock.risk}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 快捷功能 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button 
          className="bg-white rounded-lg shadow-sm p-3 text-center hover:shadow-md transition-shadow"
          onClick={() => handleButtonClick('盘前分析')}
        >
          <div className="flex justify-center mb-1">
            <BarChart3 size={20} className="text-primary" />
          </div>
          <h3 className="text-xs font-medium">盘前分析</h3>
        </button>
        <button 
          className="bg-white rounded-lg shadow-sm p-3 text-center hover:shadow-md transition-shadow"
          onClick={() => handleButtonClick('尾盘选股')}
        >
          <div className="flex justify-center mb-1">
            <TrendingUp size={20} className="text-primary" />
          </div>
          <h3 className="text-xs font-medium">尾盘选股</h3>
        </button>
        <button 
          className="bg-white rounded-lg shadow-sm p-3 text-center hover:shadow-md transition-shadow"
          onClick={() => handleButtonClick('历史复盘')}
        >
          <div className="flex justify-center mb-1">
            <History size={20} className="text-primary" />
          </div>
          <h3 className="text-xs font-medium">历史复盘</h3>
        </button>
        <button 
          className="bg-white rounded-lg shadow-sm p-3 text-center hover:shadow-md transition-shadow"
          onClick={() => handleButtonClick('风控设置')}
        >
          <div className="flex justify-center mb-1">
            <Shield size={20} className="text-primary" />
          </div>
          <h3 className="text-xs font-medium">风控设置</h3>
        </button>
      </div>

      {/* 风险提示 */}
      <div className="mt-6 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-center">
        <p className="text-xs text-yellow-800">
          投资有风险，入市需谨慎，本系统仅为选股参考，不构成投资建议
        </p>
      </div>
    </div>
  );
};

export default Dashboard;