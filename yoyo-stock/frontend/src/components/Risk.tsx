import React, { useState } from 'react';

const Risk: React.FC = () => {
  const [riskPreference, setRiskPreference] = useState('保守');
  const [stopLossRatio, setStopLossRatio] = useState('5');
  const [isSaving, setIsSaving] = useState(false);

  const handleSaveSettings = async () => {
    setIsSaving(true);
    try {
      // 模拟保存过程
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // 这里可以添加实际的保存逻辑
      console.log('保存风险设置:', { riskPreference, stopLossRatio });
      
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
      <h1 className="text-xl font-bold mb-4">风控设置</h1>
      <div className="bg-white rounded-lg shadow-sm p-3 mb-3">
        <h2 className="text-base font-medium mb-3">风险控制</h2>
        <p className="text-gray-600 text-sm mb-3">设置您的风险偏好和止损策略</p>
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-700 mb-1">风险偏好</label>
          <select 
            className="w-full border border-gray-300 rounded-lg px-2 py-1.5 text-sm"
            value={riskPreference}
            onChange={(e) => setRiskPreference(e.target.value)}
          >
            <option>保守</option>
            <option>适中</option>
            <option>激进</option>
          </select>
        </div>
        <div className="mb-3">
          <label className="block text-xs font-medium text-gray-700 mb-1">止损比例</label>
          <input 
            type="number" 
            className="w-full border border-gray-300 rounded-lg px-2 py-1.5 text-sm" 
            placeholder="5"
            value={stopLossRatio}
            onChange={(e) => setStopLossRatio(e.target.value)}
          />
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

export default Risk;