import React, { useState } from 'react';

const Selection: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [selectedStocks, setSelectedStocks] = useState<any[]>([]);
  const [hasResults, setHasResults] = useState(false);

  const handleStartSelection = async () => {
    setIsLoading(true);
    try {
      // 模拟选股过程
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // 获取选股结果
      const response = await fetch('/api/stocks/filter', {
        method: 'POST'
      });
      if (response.ok) {
        const data = await response.json();
        setSelectedStocks(data);
        setHasResults(true);
      }
    } catch (error) {
      console.error('选股失败:', error);
      // 模拟数据
      const mockStocks = [
        {
          id: 1,
          stock_code: '600519',
          stock_name: '贵州茅台',
          rise_rate: 3.25,
          volume_ratio: 1.5,
          turnover_rate: 6.8,
          select_reason: '符合杨永兴尾盘买入策略：当日涨幅3.25%，20日内有涨停，量比1.5，换手率6.8%，股价在20日均线上方',
          risk_tip: '风险提示：暂无明显风险'
        },
        {
          id: 2,
          stock_code: '000858',
          stock_name: '五粮液',
          rise_rate: 4.12,
          volume_ratio: 1.8,
          turnover_rate: 5.2,
          select_reason: '符合杨永兴尾盘买入策略：当日涨幅4.12%，20日内有涨停，量比1.8，换手率5.2%，股价在20日均线上方',
          risk_tip: '风险提示：量比异常'
        },
        {
          id: 3,
          stock_code: '601318',
          stock_name: '中国平安',
          rise_rate: -1.85,
          volume_ratio: 1.2,
          turnover_rate: 4.5,
          select_reason: '符合杨永兴尾盘买入策略：当日涨幅-1.85%，20日内有涨停，量比1.2，换手率4.5%，股价在20日均线上方',
          risk_tip: '风险提示：股价下跌'
        }
      ];
      setSelectedStocks(mockStocks);
      setHasResults(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code)
      .then(() => {
        alert('代码已复制到剪贴板');
      })
      .catch(err => {
        console.error('复制失败:', err);
      });
  };

  return (
    <div className="bg-[#17171a] min-h-screen pt-8 pb-24 px-4">
      <h1 className="text-xl font-bold mb-4 text-white">选股页面</h1>
      <div className="bg-[#2a2a2d] rounded-3xl p-4 mb-4">
        <h2 className="text-base font-medium mb-3 text-white">选股策略</h2>
        <p className="text-gray-400 text-sm mb-4">基于杨永兴尾盘买入策略，我们为您精选优质标的。</p>
        <button 
          className="w-full py-3 bg-[#3d3d40] text-white rounded-2xl text-sm font-semibold hover:bg-[#4d4d50] transition-colors"
          onClick={handleStartSelection}
          disabled={isLoading}
        >
          {isLoading ? '选股中...' : '开始选股'}
        </button>
      </div>
      <div className="bg-[#2a2a2d] rounded-3xl p-4">
        <h2 className="text-base font-medium mb-3 text-white">选股结果</h2>
        {isLoading ? (
          <p className="text-gray-400 text-sm">正在选股中...</p>
        ) : !hasResults ? (
          <p className="text-gray-400 text-sm">点击上方按钮开始选股</p>
        ) : (
          <div className="space-y-4">
            {selectedStocks.map((stock) => (
              <div key={stock.id} className="border-b border-gray-700 pb-4 last:border-0 last:pb-0">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center">
                      <h3 className="font-bold text-sm text-white">{stock.stock_name}</h3>
                      <span className="ml-1 text-xs text-gray-400">{stock.stock_code}</span>
                    </div>
                    <div className="flex items-baseline mt-1">
                      <span className={`text-base font-bold ${stock.rise_rate >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                        {stock.rise_rate > 0 ? '+' : ''}{stock.rise_rate}%
                      </span>
                    </div>
                  </div>
                  <button 
                    className="px-3 py-1.5 bg-[#3d3d40] text-white rounded-lg text-xs hover:bg-[#4d4d50] transition-colors"
                    onClick={() => handleCopyCode(stock.stock_code)}
                  >
                    复制代码
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
                  <div>
                    <span className="text-gray-400">量比：</span>
                    <span className="text-white">{stock.volume_ratio}</span>
                  </div>
                  <div>
                    <span className="text-gray-400">换手率：</span>
                    <span className="text-white">{stock.turnover_rate}%</span>
                  </div>
                </div>
                <div className="mt-3 text-xs">
                  <p className="text-gray-400 line-clamp-2">{stock.select_reason}</p>
                  <p className="mt-1 text-red-500">{stock.risk_tip}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Selection;