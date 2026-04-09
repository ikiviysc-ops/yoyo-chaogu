import React from 'react';

const Selection: React.FC = () => {
  return (
    <div className="container mx-auto px-4 pt-16 pb-16 bg-background min-h-screen">
      <h1 className="text-xl font-bold mb-4">选股页面</h1>
      <div className="bg-white rounded-lg shadow-sm p-3 mb-3">
        <h2 className="text-base font-medium mb-3">选股策略</h2>
        <p className="text-gray-600 text-sm mb-3">基于杨永兴尾盘买入策略，我们为您精选优质标的。</p>
        <button className="w-full py-1.5 bg-primary text-white rounded-lg text-xs hover:bg-primary/90 transition-colors">
          开始选股
        </button>
      </div>
      <div className="bg-white rounded-lg shadow-sm p-3">
        <h2 className="text-base font-medium mb-3">选股结果</h2>
        <p className="text-gray-600 text-sm">点击上方按钮开始选股</p>
      </div>
    </div>
  );
};

export default Selection;