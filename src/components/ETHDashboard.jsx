import React, { useState, useEffect } from ‘react’;
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell } from ‘recharts’;
import { TrendingUp, Database, Github, Circle, Activity, BookOpen, Eye, Target, AlertTriangle, CheckCircle, Clock, DollarSign, Zap } from ‘lucide-react’;

const ETHForecastingDashboard = () => {
const [currentTime, setCurrentTime] = useState(new Date());
const [forecastInterval, setForecastInterval] = useState(‘1h’);
const [darkMode, setDarkMode] = useState(true);
const [isLive, setIsLive] = useState(true);
const [activeTab, setActiveTab] = useState(‘forecasting’);
const [emergencyFundThreshold, setEmergencyFundThreshold] = useState(5000);
const [checkedItems, setCheckedItems] = useState(new Set());

// Portfolio data
const portfolioValue = 1009.78;
const totalReturn = 536.10;
const returnPercentage = 113.3;

const holdings = [
{
symbol: ‘BTC’,
name: ‘Bitcoin’,
amount: 0.00499925,
value: 593.65,
price: 118638.31,
pnl: 483.04,
pnlPercent: 439.15,
knowledge: ‘strong’,
allocation: 58.8,
thesis: ‘Digital Gold / Store of Value’,
color: ‘#f7931a’
},
{
symbol: ‘ETH’,
name: ‘Ethereum’,
amount: 0.04124751,
value: 156.32,
price: 3771.18,
pnl: 18.18,
pnlPercent: 13.24,
knowledge: ‘weak’,
allocation: 15.5,
thesis: ‘Smart Contract Platform’,
color: ‘#627eea’
},
{
symbol: ‘cbETH’,
name: ‘Coinbase ETH (Staked)’,
amount: 0.03193651,
value: 133.48,
price: 4160.90,
pnl: -5.01,
pnlPercent: -3.63,
knowledge: ‘transitioning’,
allocation: 13.2,
thesis: ‘Staking Rewards’,
color: ‘#1652f0’
},
{
symbol: ‘XRP’,
name: ‘XRP’,
amount: 35.858222,
value: 126.29,
price: 3.52,
pnl: 29.88,
pnlPercent: 31.01,
knowledge: ‘weak’,
allocation: 12.5,
thesis: ‘Cross-border Payments’,
color: ‘#23292f’
}
];

// Mock data generation (same as before)
const generatePriceData = () => {
const data = [];
const basePrice = 2400;
for (let i = 0; i < 24; i++) {
const time = new Date();
time.setHours(time.getHours() - (23 - i));
data.push({
time: time.toLocaleTimeString(‘en-US’, { hour: ‘2-digit’, minute: ‘2-digit’ }),
price: basePrice + (Math.random() - 0.5) * 200 + Math.sin(i / 4) * 100,
volume: Math.random() * 1000000 + 500000
});
}
return data;
};

const generateGasData = () => {
const data = [];
for (let i = 0; i < 12; i++) {
const time = new Date();
time.setHours(time.getHours() - (11 - i) * 2);
data.push({
time: time.toLocaleTimeString(‘en-US’, { hour: ‘2-digit’, minute: ‘2-digit’ }),
gasPrice: 15 + Math.random() * 25 + Math.sin(i / 2) * 5
});
}
return data;
};

const generateMarketShareData = () => {
return [
{ name: ‘DeFi’, value: 35, color: ‘#00d4ff’ },
{ name: ‘NFTs’, value: 25, color: ‘#ff6b6b’ },
{ name: ‘Gaming’, value: 15, color: ‘#4ecdc4’ },
{ name: ‘DEX’, value: 20, color: ‘#45b7d1’ },
{ name: ‘Other’, value: 5, color: ‘#96ceb4’ }
];
};

const generateForecastData = () => {
const data = [];
const basePrice = 2400;
for (let i = 0; i < 12; i++) {
const time = new Date();
time.setHours(time.getHours() + i);
const actual = i < 6 ? basePrice + (Math.random() - 0.5) * 100 : null;
const predicted = basePrice + (Math.random() - 0.5) * 120 + Math.sin(i / 3) * 80;
data.push({
time: time.toLocaleTimeString(‘en-US’, { hour: ‘2-digit’, minute: ‘2-digit’ }),
actual: actual,
predicted: predicted
});
}
return data;
};

const [priceData] = useState(generatePriceData());
const [gasData] = useState(generateGasData());
const [marketShareData] = useState(generateMarketShareData());
const [forecastData] = useState(generateForecastData());

const latestForecast = forecastData[forecastData.length - 1]?.predicted || 2456.78;

useEffect(() => {
const timer = setInterval(() => {
setCurrentTime(new Date());
}, 1000);
return () => clearInterval(timer);
}, []);

const handleUpdateForecast = () => {
console.log(`Updating forecast for ${forecastInterval} interval`);
};

const toggleCheck = (id) => {
const newChecked = new Set(checkedItems);
if (newChecked.has(id)) {
newChecked.delete(id);
} else {
newChecked.add(id);
}
setCheckedItems(newChecked);
};

const theme = {
background: ‘linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%)’,
cardBg: ‘rgba(255, 255, 255, 0.05)’,
text: ‘#ffffff’,
textSecondary: ‘#b0b0b0’,
border: ‘rgba(255, 255, 255, 0.1)’,
accent: ‘#4facfe’,
positive: ‘#00ff88’,
negative: ‘#ff4444’,
warning: ‘#ffaa00’
};

const getKnowledgeColor = (knowledge) => {
switch (knowledge) {
case ‘strong’: return theme.positive;
case ‘weak’: return theme.negative;
case ‘transitioning’: return theme.warning;
default: return theme.textSecondary;
}
};

const CustomTooltip = ({ active, payload, label }) => {
if (active && payload && payload.length) {
return (
<div style={{ background: ‘rgba(0, 0, 0, 0.9)’, backdropFilter: ‘blur(10px)’ }}
className=“p-3 rounded-lg shadow-lg border border-gray-600”>
<p className="text-gray-300 text-sm">{`Time: ${label}`}</p>
{payload.map((entry, index) => (
<p key={index} style={{ color: entry.color }} className=“text-sm”>
{`${entry.dataKey}: ${typeof entry.value === 'number' ? entry.value.toFixed(2) : entry.value}`}
</p>
))}
</div>
);
}
return null;
};

const TabButton = ({ id, children, icon: Icon }) => (
<button
onClick={() => setActiveTab(id)}
className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${ activeTab === id  ? 'bg-blue-500 bg-opacity-30 border border-blue-400 text-blue-300'  : 'bg-white bg-opacity-10 border border-white border-opacity-20 hover:bg-opacity-20' }`}
>
<Icon size={18} />
{children}
</button>
);

const HoldingCard = ({ holding }) => (
<div style={{ background: theme.cardBg, backdropFilter: ‘blur(10px)’, borderColor: theme.border }}
className=“rounded-2xl border p-6 transition-all duration-300 hover:transform hover:-translate-y-2 hover:shadow-2xl”>
<div className="flex items-center justify-between mb-4">
<div className="flex items-center gap-3">
<div style={{ backgroundColor: holding.color }}
className=“w-10 h-10 rounded-full flex items-center justify-center font-bold text-white text-lg”>
{holding.symbol[0]}
</div>
<div>
<h3 className="font-semibold text-lg">{holding.name}</h3>
<p className="text-sm opacity-70">{holding.symbol}</p>
</div>
</div>
<div style={{
backgroundColor: getKnowledgeColor(holding.knowledge) + ‘33’,
color: getKnowledgeColor(holding.knowledge),
border: `1px solid ${getKnowledgeColor(holding.knowledge)}`
}} className=“px-3 py-1 rounded-full text-xs font-bold uppercase”>
{holding.knowledge}
</div>
</div>

```
  <div className="grid grid-cols-2 gap-4 mb-4">
    <div>
      <p className="text-sm opacity-70 mb-1">Holdings</p>
      <p className="font-bold">{holding.amount.toFixed(6)} {holding.symbol}</p>
    </div>
    <div>
      <p className="text-sm opacity-70 mb-1">Value</p>
      <p className="font-bold">${holding.value.toFixed(2)}</p>
    </div>
    <div>
      <p className="text-sm opacity-70 mb-1">Current Price</p>
      <p style={{ color: theme.positive }} className="font-bold">${holding.price.toLocaleString()}</p>
    </div>
    <div>
      <p className="text-sm opacity-70 mb-1">Unrealized P&L</p>
      <p style={{ color: holding.pnl > 0 ? theme.positive : theme.negative }} className="font-bold">
        {holding.pnl > 0 ? '+' : ''}${holding.pnl.toFixed(2)} ({holding.pnlPercent.toFixed(2)}%)
      </p>
    </div>
  </div>
  
  <div className="w-full h-2 bg-white bg-opacity-10 rounded-full mb-4 overflow-hidden">
    <div style={{ 
      width: `${holding.allocation}%`,
      background: 'linear-gradient(90deg, #00ff88 0%, #4facfe 100%)'
    }} className="h-full rounded-full transition-all duration-300"></div>
  </div>
  
  <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.05)' }} className="rounded-lg p-4">
    <h4 style={{ color: theme.accent }} className="font-bold mb-2">
      {holding.knowledge === 'strong' ? 'Your Thesis:' : '⚠️ Knowledge Gap:'} {holding.thesis}
    </h4>
    <div className="space-y-2 text-sm">
      {holding.knowledge === 'strong' ? (
        <>
          <div className="flex items-center gap-2">
            <CheckCircle size={14} style={{ color: theme.positive }} />
            <span>Strong conviction maintained</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle size={14} style={{ color: theme.positive }} />
            <span>Regular monitoring in place</span>
          </div>
        </>
      ) : (
        <>
          <div className="flex items-center gap-2">
            <AlertTriangle size={14} style={{ color: theme.warning }} />
            <span>Need to research fundamentals</span>
          </div>
          <div className="flex items-center gap-2">
            <AlertTriangle size={14} style={{ color: theme.warning }} />
            <span>Understand value proposition</span>
          </div>
        </>
      )}
    </div>
  </div>
</div>
```

);

const ChecklistItem = ({ id, children, completed = false }) => (
<div
onClick={() => toggleCheck(id)}
className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer transition-all duration-200 hover:bg-white hover:bg-opacity-10 ${ checkedItems.has(id) ? 'line-through opacity-60' : '' }`}
>
<div className={`w-5 h-5 border-2 rounded flex items-center justify-center transition-all duration-200 ${ checkedItems.has(id)  ? 'bg-green-500 border-green-500'  : 'border-gray-400 hover:border-blue-400' }`}>
{checkedItems.has(id) && <span className="text-white text-xs">✓</span>}
</div>
<span className={checkedItems.has(id) ? ‘text-green-400’ : ‘’}>{children}</span>
</div>
);

return (
<div style={{ background: theme.background, color: theme.text, minHeight: ‘100vh’ }}>
<div className="container mx-auto p-6 max-w-7xl">
{/* Enhanced Header */}
<div className="text-center mb-8">
<div className="flex items-center justify-center gap-3 mb-4">
<TrendingUp size={40} style={{ color: theme.accent }} />
<h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
{portfolioValue.toLocaleString(undefined, { style: ‘currency’, currency: ‘USD’ })}
</h1>
</div>

```
      <div className="flex items-center justify-center gap-2 mb-4">
        <div style={{ 
          background: 'rgba(0, 255, 136, 0.2)',
          border: '1px solid #00ff88',
          color: theme.positive
        }} className="px-4 py-2 rounded-full text-sm font-medium flex items-center gap-2">
          <BookOpen size={16} />
          🎓 Learning Portfolio Mode
        </div>
      </div>
      
      <div style={{ color: theme.positive }} className="text-xl font-semibold mb-4">
        +${totalReturn.toFixed(2)} Total Return ({returnPercentage.toFixed(1)}%)
      </div>
      
      <div style={{ 
        background: 'rgba(255, 170, 0, 0.2)',
        border: '1px solid #ffaa00'
      }} className="rounded-lg p-4 mb-6 max-w-md mx-auto">
        <div className="flex items-center gap-2 mb-2">
          <strong>Emergency Fund Threshold:</strong>
          <input 
            type="number" 
            value={emergencyFundThreshold}
            onChange={(e) => setEmergencyFundThreshold(Number(e.target.value))}
            style={{ 
              background: 'rgba(255, 255, 255, 0.1)',
              border: '1px solid rgba(255, 255, 255, 0.2)',
              color: 'white'
            }}
            className="w-24 px-2 py-1 rounded text-center"
          />
        </div>
        <p className="text-sm">
          Current: {((portfolioValue / emergencyFundThreshold) * 100).toFixed(0)}% of threshold | Status: Play Money
        </p>
      </div>
      
      <div className="flex items-center justify-center gap-2 mb-4">
        <Circle 
          size={12} 
          className={`${isLive ? 'text-green-400' : 'text-red-400'} fill-current`} 
        />
        <p style={{ color: theme.textSecondary }} className="text-lg">
          Last updated at {currentTime.toLocaleTimeString()}
        </p>
      </div>
    </div>

    {/* Navigation Tabs */}
    <div className="flex justify-center gap-4 mb-8 flex-wrap">
      <TabButton id="forecasting" icon={Activity}>AI Forecasting</TabButton>
      <TabButton id="holdings" icon={DollarSign}>Holdings</TabButton>
      <TabButton id="learning" icon={BookOpen}>Learning Plan</TabButton>
      <TabButton id="monitoring" icon={Eye}>Monitoring</TabButton>
      <TabButton id="decisions" icon={Target}>Decision Framework</TabButton>
    </div>

    {/* AI Forecasting Tab */}
    {activeTab === 'forecasting' && (
      <div className="space-y-8">
        {/* Real-Time ETH Price Section */}
        <div style={{ backgroundColor: theme.cardBg, borderColor: theme.border, backdropFilter: 'blur(10px)' }} 
             className="rounded-2xl shadow-2xl border p-6">
          <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
            <Database size={24} style={{ color: theme.accent }} />
            Real-Time ETH Price (USD)
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={priceData}>
              <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
              <XAxis dataKey="time" stroke={theme.textSecondary} />
              <YAxis stroke={theme.textSecondary} />
              <Tooltip content={<CustomTooltip />} />
              <Line 
                type="monotone" 
                dataKey="price" 
                stroke={theme.accent} 
                strokeWidth={3}
                dot={{ fill: theme.accent, strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Market Signals Section */}
        <div className="grid md:grid-cols-2 gap-8">
          <div style={{ backgroundColor: theme.cardBg, borderColor: theme.border, backdropFilter: 'blur(10px)' }} 
               className="rounded-2xl shadow-2xl border p-6">
            <h3 className="text-xl font-semibold mb-4">ETH Gas Fees (Gwei)</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={gasData}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
                <XAxis dataKey="time" stroke={theme.textSecondary} />
                <YAxis stroke={theme.textSecondary} />
                <Tooltip content={<CustomTooltip />} />
                <Line 
                  type="monotone" 
                  dataKey="gasPrice" 
                  stroke="#ff6b6b" 
                  strokeWidth={2}
                  dot={{ fill: '#ff6b6b', strokeWidth: 2, r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div style={{ backgroundColor: theme.cardBg, borderColor: theme.border, backdropFilter: 'blur(10px)' }} 
               className="rounded-2xl shadow-2xl border p-6">
            <h3 className="text-xl font-semibold mb-4">ETH Market Share by Sector</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={marketShareData}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
                <XAxis dataKey="name" stroke={theme.textSecondary} />
                <YAxis stroke={theme.textSecondary} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="value" fill={theme.accent} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Forecasting Section */}
        <div className="grid md:grid-cols-2 gap-8">
          <div style={{ backgroundColor: theme.cardBg, borderColor: theme.border, backdropFilter: 'blur(10px)' }} 
               className="rounded-2xl shadow-2xl border p-6">
            <h3 className="text-xl font-semibold mb-4">Predicted vs Actual ETH Prices</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={forecastData}>
                <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
                <XAxis dataKey="time" stroke={theme.textSecondary} />
                <YAxis stroke={theme.textSecondary} />
                <Tooltip content={<CustomTooltip />} />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  stroke="#4ecdc4" 
                  strokeWidth={2}
                  name="Actual"
                  connectNulls={false}
                  dot={{ fill: '#4ecdc4', strokeWidth: 2, r: 3 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#ff6b6b" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Predicted"
                  dot={{ fill: '#ff6b6b', strokeWidth: 2, r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div style={{ backgroundColor: theme.cardBg, borderColor: theme.border, backdropFilter: 'blur(10px)' }} 
               className="rounded-2xl shadow-2xl border p-6 flex flex-col justify-center items-center">
            <h3 className="text-xl font-semibold mb-6">Latest Forecast</h3>
            <div className="text-center">
              <div style={{ color: theme.accent }} className="text-5xl font-bold mb-2">
                ${latestForecast.toFixed(2)}
              </div>
              <p style={{ color: theme.textSecondary }} className="text-lg">
                Next {forecastInterval} prediction
              </p>
              <div className="mt-4 flex items-center justify-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm" style={{ color: theme.textSecondary }}>
                  Model confidence: 87.3%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Controls Section */}
        <div style={{ backgroundColor: theme.cardBg, borderColor: theme.border, backdropFilter: 'blur(10px)' }} 
             className="rounded-2xl shadow-2xl border p-6">
          <div className="flex flex-wrap justify-center items-center gap-4">
            <div className="flex items-center gap-2">
              <label className="text-sm font-medium">Forecast Interval:</label>
              <select 
                value={forecastInterval}
                onChange={(e) => setForecastInterval(e.target.value)}
                style={{ backgroundColor: theme.cardBg, color: theme.text, borderColor: theme.border }}
                className="border rounded px-3 py-2 text-sm"
              >
                <option value="1h">1 Hour</option>
                <option value="6h">6 Hours</option>
                <option value="1d">1 Day</option>
              </select>
            </div>
            
            <button 
              onClick={handleUpdateForecast}
              style={{ backgroundColor: theme.accent }}
              className="px-6 py-2 rounded-lg font-medium text-black hover:opacity-80 transition-opacity"
            >
              Update Forecast
            </button>
          </div>
        </div>
      </div>
    )}

    {/* Holdings Tab */}
    {activeTab === 'holdings' && (
      <div className="grid lg:grid-cols-2 gap-8">
        {holdings.map((holding, index) => (
          <HoldingCard key={index} holding={holding} />
        ))}
      </div>
    )}

    {/* Learning Plan Tab */}
    {activeTab === 'learning' && (
      <div className="grid md:grid-cols-2 gap-8">
        <div style={{ background: theme.cardBg, backdropFilter: 'blur(10px)', borderColor: theme.border }}
             className="rounded-2xl border p-6">
          <div style={{ background: 'rgba(255, 68, 68, 0.2)', color: theme.negative }}
               className="inline-block px-3 py-1 rounded-full text-xs font-bold mb-4">
            IMMEDIATE (2 weeks)
          </div>
          <h3 style={{ color: theme.accent }} className="text-xl font-bold mb-4">
            <Zap className="inline mr-2" size={20} />
            Operational Actions
          </h3>
          <div className="space-y-2">
            <ChecklistItem id="cbeth-convert">Execute cbETH → ETH conversion when optimal</ChecklistItem>
            <ChecklistItem id="price-alerts">Set up price alerts for major moves (±15%)</ChecklistItem>
            <ChecklistItem id="threshold">Determine your "meaningful money" threshold</ChecklistItem>
            <ChecklistItem id="news-sources">Bookmark key news sources for crypto</ChecklistItem>
          </div>
        </div>

        <div style={{ background: theme.cardBg, backdropFilter: 'blur(10px)', borderColor: theme.border }}
             className="rounded-2xl border p-6">
          <div style={{ background: 'rgba(255, 170, 0, 0.2)', color: theme.warning }}
               className="inline-block px-3 py-1 rounded-full text-xs font-bold mb-4">
            MEDIUM-TERM (2 months)
          </div>
          <h3 style={{ color: theme.accent }} className="text-xl font-bold mb-4">
            <BookOpen className="inline mr-2" size={20} />
            Knowledge Building
          </h3>
          <div className="space-y-2">
            <ChecklistItem id="eth-basics">Learn Ethereum basics: What problem does it solve?</ChecklistItem>
            <ChecklistItem id="xrp-partnerships">Understand XRP's banking partnerships model</ChecklistItem>
            <ChecklistItem id="protocol-upgrades">Research major protocol upgrade impacts</ChecklistItem>
            <ChecklistItem id="market-cycles">Study crypto market cycles and patterns</ChecklistItem>
            <ChecklistItem id="staking-tradeoffs">Learn about staking vs holding trade-offs</ChecklistItem>
          </div>
        </div>

        <div style={{ background: theme.cardBg, backdropFilter: 'blur(10px)', borderColor: theme.border }}
             className="rounded-2xl border p-6">
          <div style={{ background: 'rgba(79, 172, 254, 0.2)', color: theme.accent }}
               className="inline-block px-3 py-1 rounded-full text-xs font-bold mb-4">
            ONGOING
          </div>
          <h3 style={{ color: theme.accent }} className="text-xl font-bold mb-4">
            <Activity className="inline mr-2" size={20} />
            Monitoring System
          </h3>
          <div className="space-y-2">
            <ChecklistItem id="weekly-review">Weekly 10-minute portfolio review</ChecklistItem>
            <ChecklistItem id="monthly-thesis">Monthly reassessment of thesis for each holding</ChecklistItem>
            <ChecklistItem id="news-tracking">Track major news that could affect investments</ChecklistItem>
            <ChecklistItem id="regulatory">Review regulatory developments</ChecklistItem>
            <ChecklistItem id="macro-factors">Monitor macro factors (interest rates, inflation)</ChecklistItem>
          </div>
        </div>

        <div style={{ background: theme.cardBg, backdropFilter: 'blur(10px)', borderColor: theme.border }}
             className="rounded-2xl border p-6">
          <h3 style={{ color: theme.accent }} className="text-xl font-bold mb-4">
            <Target className="inline mr-2" size={20} />
            Knowledge Validation
          </h3>
          <p className="mb-4 opacity-70">Can you answer these about each holding?</p>
          <div className="space-y-2">
            <ChecklistItem id="eth-explain">ETH: Explain in 2 sentences why you own it</ChecklistItem>
            <ChecklistItem id="xrp-partnerships-know">XRP: Name 3 major partnerships or use cases</ChecklistItem>
            <ChecklistItem id="sell-triggers">All holdings: What news would make you sell immediately?</ChecklistItem>
            <ChecklistItem id="technical-levels">All holdings: What technical levels matter?</ChecklistItem>
          </div>
        </div>
      </div>
    )}

    {/* Monitoring Tab */}
    {activeTab === 'monitoring' && (
      <div className="space-y-8">
        <div style={{ background: theme.cardBg, backdropFilter: 'blur(10px)', borderColor: theme.border }}
             className="rounded-2xl border p-6">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Eye size={24} style={{ color: theme.accent }} />
            Key Events to Monitor
          </h2>
          <div className
```