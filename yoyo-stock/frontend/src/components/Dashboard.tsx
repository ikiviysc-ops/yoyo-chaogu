import React, { useState, useEffect } from 'react';
import { Search, Star, TrendingUp, TrendingDown, ChevronDown, ChevronRight, X } from 'lucide-react';

interface Stock {
  id: number;
  code: string;
  name: string;
  price: number;
  change: number;
  mcap: string;
  volume: string;
}

const Dashboard: React.FC = () => {
  const [showDetails, setShowDetails] = useState(false);
  const [selectedStock, setSelectedStock] = useState<Stock | null>(null);
  const [activeTab, setActiveTab] = useState('hot');
  const [sortBy, setSortBy] = useState('mcap');
  const [sortOrder, setSortOrder] = useState('desc');

  const [stocks, setStocks] = useState<Stock[]>([]);
  const [hotStocks, setHotStocks] = useState<Stock[]>([]);

  // 从后端API获取数据
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/stocks/selection');
        if (response.ok) {
          const data = await response.json();
          if (data.length > 0) {
            const formattedStocks: Stock[] = data.map((stock: any, index: number) => ({
              id: stock.id,
              code: stock.stock_code,
              name: stock.stock_name,
              price: 100 + Math.random() * 900,
              change: stock.rise_rate,
              mcap: `${(Math.random() * 500 + 10).toFixed(2)}B`,
              volume: `${(Math.random() * 1000 + 100).toFixed(2)}M`,
            }));
            setStocks(formattedStocks);
            setHotStocks(formattedStocks.slice(0, 6));
          }
        }
      } catch (error) {
        console.error('获取数据失败:', error);
        // 模拟数据
        const mockStocks: Stock[] = [
          { id: 1, code: '600519', name: '贵州茅台', price: 1789.00, change: 3.25, mcap: '2.35T', volume: '45.23M' },
          { id: 2, code: '601318', name: '中国平安', price: 58.50, change: -1.85, mcap: '1.08T', volume: '89.56M' },
          { id: 3, code: '600036', name: '招商银行', price: 35.80, change: 2.15, mcap: '890.5B', volume: '123.45M' },
          { id: 4, code: '000858', name: '五粮液', price: 168.50, change: 4.12, mcap: '652.3B', volume: '67.89M' },
          { id: 5, code: '601899', name: '紫金矿业', price: 15.60, change: -0.75, mcap: '405.2B', volume: '156.78M' },
          { id: 6, code: '000001', name: '平安银行', price: 12.30, change: 1.25, mcap: '350.1B', volume: '98.76M' },
          { id: 7, code: '600276', name: '恒瑞医药', price: 48.90, change: -2.35, mcap: '312.8B', volume: '54.32M' },
          { id: 8, code: '600585', name: '海螺水泥', price: 38.50, change: 0.85, mcap: '205.6B', volume: '43.21M' },
        ];
        setStocks(mockStocks);
        setHotStocks(mockStocks.slice(0, 6));
      }
    };

    fetchData();
  }, []);

  const generateMiniChart = (isUp: boolean) => {
    const points = [];
    let y = 50;
    for (let i = 0; i < 20; i++) {
      y += (Math.random() - (isUp ? 0.4 : 0.6)) * 10;
      y = Math.max(10, Math.min(90, y));
      points.push(`${i * 5},${y}`);
    }
    return points.join(' ');
  };

  const formatPrice = (price: number) => {
    return `$${price.toFixed(2)}`;
  };

  const formatChange = (change: number) => {
    const sign = change >= 0 ? '+' : '';
    return `${sign}${change.toFixed(2)}%`;
  };

  const getStockColor = (change: number) => {
    return change >= 0 ? '#10b981' : '#ef4444';
  };

  const handleStockClick = (stock: Stock) => {
    setSelectedStock(stock);
    setShowDetails(true);
  };

  const sortedStocks = [...stocks].sort((a, b) => {
    let comparison = 0;
    switch (sortBy) {
      case 'mcap':
        comparison = parseFloat(a.mcap) - parseFloat(b.mcap);
        break;
      case 'change':
        comparison = a.change - b.change;
        break;
      case 'price':
        comparison = a.price - b.price;
        break;
      default:
        comparison = 0;
    }
    return sortOrder === 'desc' ? -comparison : comparison;
  });

  return (
    <div className="bg-[#17171a] min-h-screen pt-8 pb-24">
      {/* Header */}
      <div className="px-4 mb-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-white">热门</h1>
          <button className="p-2 hover:bg-white/10 rounded-full transition-colors">
            <Search size={24} className="text-white" />
          </button>
        </div>

        {/* Hot Stocks Horizontal Scroll */}
        <div className="mb-6">
          <h2 className="text-white text-xl font-bold mb-4">交易量最高（24小时）</h2>
          <div className="flex gap-4 overflow-x-auto pb-2 -mx-4 px-4">
            {hotStocks.map((stock) => (
              <div
                key={stock.id}
                className="flex-shrink-0 w-44 bg-[#2a2a2d] rounded-3xl p-5 cursor-pointer hover:bg-[#353538] transition-colors"
                onClick={() => handleStockClick(stock)}
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-gray-400 font-semibold text-sm">{stock.name}</span>
                  <div className="w-9 h-9 bg-[#3d3d40] rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-xs">{stock.name.charAt(0)}</span>
                  </div>
                </div>
                <div className="text-2xl font-bold text-white mb-2">
                  {formatPrice(stock.price)}
                </div>
                <div className="text-lg font-semibold mb-3" style={{ color: getStockColor(stock.change) }}>
                  {formatChange(stock.change)}
                </div>
                <div className="h-16">
                  <svg viewBox="0 0 95 60" className="w-full h-full">
                    <defs>
                      <linearGradient id={`gradient-${stock.id}`} x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor={getStockColor(stock.change)} stopOpacity="0.3" />
                        <stop offset="100%" stopColor={getStockColor(stock.change)} stopOpacity="0" />
                      </linearGradient>
                    </defs>
                    <path
                      d={`M 0 60 L ${generateMiniChart(stock.change >= 0)} L 95 60 Z`}
                      fill={`url(#gradient-${stock.id})`}
                    />
                    <polyline
                      points={generateMiniChart(stock.change >= 0)}
                      fill="none"
                      stroke={getStockColor(stock.change)}
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-3 mb-6 overflow-x-auto pb-2">
          <button
            className={`px-8 py-3 rounded-full font-semibold text-lg transition-all ${activeTab === 'hot' ? 'bg-[#3d3d40] text-white' : 'bg-[#2a2a2d] text-gray-400'}`}
            onClick={() => setActiveTab('hot')}
          >
            Hot tokens
          </button>
          <button
            className={`px-8 py-3 rounded-full font-semibold text-lg transition-all ${activeTab === 'gainers' ? 'bg-[#3d3d40] text-white' : 'bg-[#2a2a2d] text-gray-400'}`}
            onClick={() => setActiveTab('gainers')}
          >
            Top Gainers
          </button>
          <button
            className={`px-8 py-3 rounded-full font-semibold text-lg transition-all ${activeTab === 'rwa' ? 'bg-[#3d3d40] text-white' : 'bg-[#2a2a2d] text-gray-400'}`}
            onClick={() => setActiveTab('rwa')}
          >
            RWA
          </button>
          <button
            className={`px-8 py-3 rounded-full font-semibold text-lg transition-all ${activeTab === 'meme' ? 'bg-[#3d3d40] text-white' : 'bg-[#2a2a2d] text-gray-400'}`}
            onClick={() => setActiveTab('meme')}
          >
            Meme
          </button>
        </div>

        {/* Sort Controls */}
        <div className="flex justify-between items-center mb-4">
          <button className="flex items-center gap-2 px-5 py-2 bg-[#2a2a2d] rounded-full">
            <span className="text-gray-400 font-medium text-lg">网络</span>
            <ChevronDown size={20} className="text-gray-400" />
          </button>
          <div className="flex gap-3">
            <button
              className="flex items-center gap-2 px-5 py-2 bg-[#2a2a2d] rounded-full"
              onClick={() => {
                setSortBy('mcap');
                setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc');
              }}
            >
              <span className="text-gray-400 font-medium text-lg">市值</span>
              {sortBy === 'mcap' && (
                sortOrder === 'desc' ? <ChevronDown size={20} className="text-gray-400" /> : <ChevronRight size={20} className="text-gray-400" />
              )}
            </button>
            <button
              className="flex items-center gap-2 px-5 py-2 bg-[#2a2a2d] rounded-full"
              onClick={() => {
                setSortBy('change');
                setSortOrder(sortOrder === 'desc' ? 'asc' : 'desc');
              }}
            >
              <span className="text-gray-400 font-medium text-lg">24h</span>
              {sortBy === 'change' && (
                sortOrder === 'desc' ? <ChevronDown size={20} className="text-gray-400" /> : <ChevronRight size={20} className="text-gray-400" />
              )}
            </button>
          </div>
        </div>

        {/* Stock List */}
        <div className="space-y-5">
          {sortedStocks.map((stock) => (
            <div
              key={stock.id}
              className="flex items-center justify-between py-2 cursor-pointer hover:bg-white/5 rounded-xl transition-colors"
              onClick={() => handleStockClick(stock)}
            >
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white font-bold text-xl">{stock.name.charAt(0)}</span>
                </div>
                <div>
                  <h3 className="text-white font-bold text-2xl">{stock.name}</h3>
                  <p className="text-gray-400 text-lg">
                    ${stock.mcap} MCap · ${stock.volume} Vol
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <div className="text-white font-bold text-2xl">
                    {formatPrice(stock.price)}
                  </div>
                  <div className="flex items-center justify-end gap-1">
                    <div className="h-10 w-24">
                      <svg viewBox="0 0 95 40" className="w-full h-full">
                        <defs>
                          <linearGradient id={`list-gradient-${stock.id}`} x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stopColor={getStockColor(stock.change)} stopOpacity="0.3" />
                            <stop offset="100%" stopColor={getStockColor(stock.change)} stopOpacity="0" />
                          </linearGradient>
                        </defs>
                        <path
                          d={`M 0 40 L ${generateMiniChart(stock.change >= 0)} L 95 40 Z`}
                          fill={`url(#list-gradient-${stock.id})`}
                        />
                        <polyline
                          points={generateMiniChart(stock.change >= 0)}
                          fill="none"
                          stroke={getStockColor(stock.change)}
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <span className="font-semibold text-xl" style={{ color: getStockColor(stock.change) }}>
                      {formatChange(stock.change)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Detail Modal */}
      {showDetails && selectedStock && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
          <div className="bg-[#17171a] rounded-3xl max-w-md w-full max-h-[80vh] overflow-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-700 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-lg">{selectedStock.name.charAt(0)}</span>
                  </div>
                  <div>
                    <h2 className="text-white font-bold text-xl">{selectedStock.name}</h2>
                    <p className="text-gray-400">{selectedStock.code}</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowDetails(false)}
                  className="p-2 hover:bg-white/10 rounded-full transition-colors"
                >
                  <X size={24} className="text-white" />
                </button>
              </div>

              <div className="mb-6">
                <div className="text-4xl font-bold text-white mb-2">
                  {formatPrice(selectedStock.price)}
                </div>
                <div className="text-2xl font-semibold" style={{ color: getStockColor(selectedStock.change) }}>
                  {formatChange(selectedStock.change)}
                </div>
              </div>

              <div className="h-40 mb-6">
                <svg viewBox="0 0 300 150" className="w-full h-full">
                  <defs>
                    <linearGradient id="detail-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                      <stop offset="0%" stopColor={getStockColor(selectedStock.change)} stopOpacity="0.3" />
                      <stop offset="100%" stopColor={getStockColor(selectedStock.change)} stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  <path
                    d={`M 0 150 L ${generateMiniChart(selectedStock.change >= 0)} L 300 150 Z`}
                    fill="url(#detail-gradient)"
                  />
                  <polyline
                    points={generateMiniChart(selectedStock.change >= 0)}
                    fill="none"
                    stroke={getStockColor(selectedStock.change)}
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-[#2a2a2d] rounded-2xl p-4">
                  <p className="text-gray-400 text-sm mb-1">市值</p>
                  <p className="text-white font-bold text-lg">${selectedStock.mcap}</p>
                </div>
                <div className="bg-[#2a2a2d] rounded-2xl p-4">
                  <p className="text-gray-400 text-sm mb-1">成交量</p>
                  <p className="text-white font-bold text-lg">${selectedStock.volume}</p>
                </div>
              </div>

              <button className="w-full py-4 bg-[#3d3d40] text-white font-bold text-lg rounded-2xl hover:bg-[#4d4d50] transition-colors">
                查看更多详情
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;