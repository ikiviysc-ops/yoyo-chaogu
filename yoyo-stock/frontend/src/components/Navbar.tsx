import React, { useState } from 'react';
import { Home, TrendingUp, History, Shield, Settings, Menu, Bell } from 'lucide-react';
import Notification from './Notification';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const [menuOpen, setMenuOpen] = useState(false);

  const tabs = [
    { id: 'home', label: '首页', icon: <Home size={20} /> },
    { id: 'selection', label: '选股', icon: <TrendingUp size={20} /> },
    { id: 'history', label: '历史', icon: <History size={20} /> },
    { id: 'risk', label: '风控', icon: <Shield size={20} /> },
    { id: 'settings', label: '设置', icon: <Settings size={20} /> },
  ];

  return (
    <>
      {/* 顶部导航栏 */}
      <header className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md z-50 border-b border-gray-100">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <h1 className="text-xl font-bold text-primary">YOYO炒股</h1>
          <div className="flex items-center gap-4">
            <Notification />
            <button 
              className="p-2" 
              onClick={() => setMenuOpen(!menuOpen)}
            >
              <Menu size={24} />
            </button>
          </div>
        </div>
      </header>

      {/* 侧边菜单 */}
      {menuOpen && (
        <div className="fixed inset-0 bg-black/50 z-50">
          <div className="absolute right-0 top-0 h-full w-64 bg-white p-4">
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-lg font-bold">菜单</h2>
              <button onClick={() => setMenuOpen(false)}>
                <span className="text-xl">✕</span>
              </button>
            </div>
            <div className="space-y-4">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  className={`flex items-center gap-2 w-full p-3 rounded-lg ${activeTab === tab.id ? 'bg-primary/10 text-primary' : 'hover:bg-gray-100'}`}
                  onClick={() => {
                    setActiveTab(tab.id);
                    setMenuOpen(false);
                  }}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 底部导航栏（手机端） */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-md z-40 border-t border-gray-100 md:hidden">
        <div className="flex justify-around">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`flex flex-col items-center py-2 px-4 ${activeTab === tab.id ? 'text-primary' : 'text-gray-500'}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="text-xl mb-1">{tab.icon}</span>
              <span className="text-xs">{tab.label}</span>
            </button>
          ))}
        </div>
      </footer>
    </>
  );
};

export default Navbar;