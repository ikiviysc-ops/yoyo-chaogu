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
      const response = await fetch('/api/stocks/selection');
      if (response.ok) {
        const data = await response.json();
        setSelectedStocks(data);
        setHasResults(true);
      }
    } catch (error) {
      console.error('选股失败:', error);
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
    <div className="container mx-auto px-4 pt-16 pb-16 bg-background min-h-screen">
      <h1 className="text-xl font-bold mb-4">选股页面</h1>
      <div className="bg-white rounded-lg shadow-sm p-3 mb-3">
        <h2 className="text-base font-medium mb-3">选股策略</h2>
        <p className="text-gray-600 text-sm mb-3">基于杨永兴尾盘买入策略，我们为您精选优质标的。</p>
        <button 
          className="w-full py-1.5 bg-primary text-white rounded-lg text-xs hover:bg-primary/90 transition-colors"
          onClick={handleStartSelection}
          disabled={isLoading}
        >
          {isLoading ? '选股中...' : '开始选股'}
        </button>
      </div>
      <div className="bg-white rounded-lg shadow-sm p-3">
        <h2 className="text-base font-medium mb-3">选股结果</h2>
        {isLoading ? (
          <p className="text-gray-600 text-sm">正在选股中...</p>
        ) : !hasResults ? (
          <p className="text-gray-600 text-sm">点击上方按钮开始选股</p>
        ) : (
          <div className="space-y-3">
            {selectedStocks.map((stock) => (
              <div key={stock.id} className="border-b border-gray-100 pb-3 last:border-0 last:pb-0">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center">
                      <h3 className="font-bold text-sm">{stock.stock_name}</h3>
                      <span className="ml-1 text-xs text-gray-500">{stock.stock_code}</span>
                    </div>
                    <div className="flex items-baseline mt-1">
                      <span className="text-base font-bold">{stock.rise_rate > 0 ? '+' : ''}{stock.rise_rate}%</span>
                    </div>
                  </div>
                  <button 
                    className="px-2 py-1 border border-primary text-primary rounded-lg text-xs hover:bg-primary/10 transition-colors"
                    onClick={() => handleCopyCode(stock.stock_code)}
                  >
                    复制代码
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-1 mt-2 text-xs">
                  <div>
                    <span className="text-gray-500">量比：</span>
                    <span>{stock.volume_ratio}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">换手率：</span>
                    <span>{stock.turnover_rate}%</span>
                  </div>
                </div>
                <div className="mt-2 text-xs">
                  <p className="text-gray-600 line-clamp-2">{stock.select_reason}</p>
                  <p className="mt-0.5 text-danger">{stock.risk_tip}</p>
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