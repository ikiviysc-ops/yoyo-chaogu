import React, { useState } from 'react';

const Settings: React.FC = () => {
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);
  const [autoSelectionEnabled, setAutoSelectionEnabled] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const handleSaveSettings = async () => {
    setIsSaving(true);
    try {
      // 模拟保存过程
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 这里可以添加实际的保存逻辑
      console.log('保存系统设置:', { notificationsEnabled, autoSelectionEnabled });
      
      alert('设置保存成功');
    } catch (error) {
      console.error('保存设置失败:', error);
      alert('保存设置失败');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="container mx-auto px-4 pt-16 pb-16 bg-background min-h-screen">
      <h1 className="text-xl font-bold mb-4">设置</h1>
      <div className="bg-white rounded-lg shadow-sm p-3 mb-3">
        <h2 className="text-base font-medium mb-3">系统设置</h2>
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-700 mb-1">通知设置</label>
          <div className="flex items-center">
            <input 
              type="checkbox" 
              id="notifications" 
              className="mr-2"
              checked={notificationsEnabled}
              onChange={(e) => setNotificationsEnabled(e.target.checked)}
            />
            <label htmlFor="notifications" className="text-sm">启用通知</label>
          </div>
        </div>
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-700 mb-1">自动选股</label>
          <div className="flex items-center">
            <input 
              type="checkbox" 
              id="auto-selection" 
              className="mr-2"
              checked={autoSelectionEnabled}
              onChange={(e) => setAutoSelectionEnabled(e.target.checked)}
            />
            <label htmlFor="auto-selection" className="text-sm">启用自动选股</label>
          </div>
        </div>
        <button 
          className="w-full py-1.5 bg-primary text-white rounded-lg text-xs hover:bg-primary/90 transition-colors"
          onClick={handleSaveSettings}
          disabled={isSaving}
        >
          {isSaving ? '保存中...' : '保存设置'}
        </button>
      </div>
    </div>
  );
};

export default Settings;