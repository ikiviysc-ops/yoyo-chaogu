import React from 'react';

const Settings: React.FC = () => {
  return (
    <div className="container mx-auto px-4 pt-16 pb-16 bg-background min-h-screen">
      <h1 className="text-xl font-bold mb-4">设置</h1>
      <div className="bg-white rounded-lg shadow-sm p-3 mb-3">
        <h2 className="text-base font-medium mb-3">系统设置</h2>
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-700 mb-1">通知设置</label>
          <div className="flex items-center">
            <input type="checkbox" id="notifications" className="mr-2" />
            <label htmlFor="notifications" className="text-sm">启用通知</label>
          </div>
        </div>
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-700 mb-1">自动选股</label>
          <div className="flex items-center">
            <input type="checkbox" id="auto-selection" className="mr-2" />
            <label htmlFor="auto-selection" className="text-sm">启用自动选股</label>
          </div>
        </div>
        <button className="w-full py-1.5 bg-primary text-white rounded-lg text-xs hover:bg-primary/90 transition-colors">
          保存设置
        </button>
      </div>
    </div>
  );
};

export default Settings;