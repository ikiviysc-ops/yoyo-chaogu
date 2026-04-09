import React from 'react';

const History: React.FC = () => {
  return (
    <div className="container mx-auto px-4 pt-16 pb-16 bg-background min-h-screen">
      <h1 className="text-xl font-bold mb-4">历史复盘</h1>
      <div className="bg-white rounded-lg shadow-sm p-3 mb-3">
        <h2 className="text-base font-medium mb-3">历史选股记录</h2>
        <p className="text-gray-600 text-sm">这里显示历史选股记录和复盘结果</p>
      </div>
      <div className="bg-white rounded-lg shadow-sm p-3">
        <h2 className="text-base font-medium mb-3">复盘分析</h2>
        <p className="text-gray-600 text-sm">这里显示历史选股的分析结果</p>
      </div>
    </div>
  );
};

export default History;