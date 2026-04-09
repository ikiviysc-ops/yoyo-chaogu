import React, { useState } from 'react';
import { Bell, Check, X, AlertCircle, Info } from 'lucide-react';

interface Notification {
  id: number;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  time: string;
  read: boolean;
}

const Notification: React.FC = () => {
  const [notifications] = useState<Notification[]>([
    {
      id: 1,
      title: '选股完成',
      message: '今日尾盘选股已完成，共选出2只优质标的',
      type: 'success',
      time: '14:30',
      read: false,
    },
    {
      id: 2,
      title: '盘前分析',
      message: '今日市场情绪中性，建议保守仓位',
      type: 'info',
      time: '09:00',
      read: true,
    },
  ]);

  const [showNotifications, setShowNotifications] = useState(false);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'success':
        return 'bg-success';
      case 'error':
        return 'bg-danger';
      case 'warning':
        return 'bg-yellow-500';
      default:
        return 'bg-primary';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <Check size={12} />;
      case 'error':
        return <X size={12} />;
      case 'warning':
        return <AlertCircle size={12} />;
      default:
        return <Info size={12} />;
    }
  };

  return (
    <div className="relative">
      <button
        className="relative p-2"
        onClick={() => setShowNotifications(!showNotifications)}
      >
        <Bell size={24} />
        {notifications.some(n => !n.read) && (
          <span className="absolute top-0 right-0 w-2 h-2 bg-danger rounded-full"></span>
        )}
      </button>

      {showNotifications && (
        <div className="absolute right-0 top-full mt-2 w-80 bg-white rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
          <div className="p-4 border-b border-gray-100">
            <h3 className="font-bold">通知中心</h3>
          </div>
          <div className="divide-y divide-gray-100">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`p-4 ${notification.read ? 'bg-white' : 'bg-gray-50'}`}
              >
                <div className="flex items-start">
                  <div
                    className={`${getTypeColor(notification.type)} text-white w-6 h-6 rounded-full flex items-center justify-center text-xs mr-3 flex-shrink-0`}
                  >
                    {getTypeIcon(notification.type)}
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between">
                      <h4 className="font-medium">{notification.title}</h4>
                      <span className="text-xs text-gray-500">{notification.time}</span>
                    </div>
                    <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="p-3 border-t border-gray-100">
            <button className="w-full text-center text-sm text-primary">
              查看全部
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Notification;