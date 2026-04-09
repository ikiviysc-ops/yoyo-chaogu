import React from 'react';

const Dashboard: React.FC = () => {
  // 模拟数据
  const marketData = {
    index: '3,258.63',
    change: '+0.25%',
    up: 1856,
    down: 2143,
  };

  const positionAdvice = {
    level: '保守',
    risk: '中等',
    suggestion: '控制仓位，关注业绩优良的蓝筹股',
  };

  const selectedStocks = [
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
  ];

  return (
    <div className="container mx-auto px-4 pt-20 pb-20 bg-background min-h-screen">
      {/* 市场概览 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-4">
          <h3 className="text-sm text-gray-500 mb-2">大盘指数</h3>
          <div className="flex items-baseline">
            <span className="text-2xl font-bold">{marketData.index}</span>
            <span className="ml-2 text-success">{marketData.change}</span>
          </div>
          <div className="flex justify-between mt-2 text-sm">
            <span className="text-success">上涨 {marketData.up}</span>
            <span className="text-danger">下跌 {marketData.down}</span>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-4">
          <h3 className="text-sm text-gray-500 mb-2">仓位建议</h3>
          <div className="flex items-center">
            <span className="text-xl font-bold">{positionAdvice.level}</span>
            <span className="ml-2 px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs">
              {positionAdvice.risk}风险
            </span>
          </div>
          <p className="mt-2 text-sm text-gray-600">{positionAdvice.suggestion}</p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-4">
          <h3 className="text-sm text-gray-500 mb-2">今日选股</h3>
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold">{selectedStocks.length}</span>
            <span className="text-sm text-gray-500">只优质标的</span>
          </div>
          <button className="mt-3 w-full py-2 bg-primary text-white rounded-lg text-sm">
            查看详情
          </button>
        </div>
      </div>

      {/* 选股结果 */}
      <div className="mb-8">
        <h2 className="text-lg font-bold mb-4">今日选股结果</h2>
        <div className="space-y-4">
          {selectedStocks.map((stock) => (
            <div key={stock.id} className="bg-white rounded-lg shadow-sm p-4">
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center">
                    <h3 className="font-bold">{stock.name}</h3>
                    <span className="ml-2 text-sm text-gray-500">{stock.code}</span>
                  </div>
                  <div className="flex items-baseline mt-1">
                    <span className="text-lg font-bold">{stock.price}</span>
                    <span className="ml-2 text-success">{stock.change}</span>
                  </div>
                </div>
                <button className="px-3 py-1 border border-primary text-primary rounded-lg text-sm">
                  复制代码
                </button>
              </div>
              <div className="grid grid-cols-2 gap-2 mt-3 text-sm">
                <div>
                  <span className="text-gray-500">量比：</span>
                  <span>{stock.volumeRatio}</span>
                </div>
                <div>
                  <span className="text-gray-500">换手率：</span>
                  <span>{stock.turnover}%</span>
                </div>
              </div>
              <div className="mt-3 text-sm">
                <p className="text-gray-600">{stock.reason}</p>
                <p className="mt-1 text-danger">{stock.risk}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 快捷功能 */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-sm p-4 text-center">
          <div className="text-2xl mb-2">📊</div>
          <h3 className="text-sm font-medium">盘前分析</h3>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 text-center">
          <div className="text-2xl mb-2">📈</div>
          <h3 className="text-sm font-medium">尾盘选股</h3>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 text-center">
          <div className="text-2xl mb-2">📋</div>
          <h3 className="text-sm font-medium">历史复盘</h3>
        </div>
        <div className="bg-white rounded-lg shadow-sm p-4 text-center">
          <div className="text-2xl mb-2">🛡️</div>
          <h3 className="text-sm font-medium">风控设置</h3>
        </div>
      </div>

      {/* 风险提示 */}
      <div className="mt-8 p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-center">
        <p className="text-sm text-yellow-800">
          投资有风险，入市需谨慎，本系统仅为选股参考，不构成投资建议
        </p>
      </div>
    </div>
  );
};

export default Dashboard;