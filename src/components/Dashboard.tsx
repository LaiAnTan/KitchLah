import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { orderPredictions, alerts, menuPredictions } from '../data/mockData';

const Dashboard: React.FC = () => {
  const [expandedMenu, setExpandedMenu] = useState<string | null>(null);
  const [loadingBreakdown, setLoadingBreakdown] = useState<string | null>(null);

  // Calculate total predicted orders for the day
  const totalPredictedOrders = menuPredictions.reduce((sum, prediction) => sum + prediction.quantity, 0);

  // Get current date and time
  const now = new Date();
  const currentDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  const currentTime = now.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  });

  // Get current time slot
  const currentHour = new Date().getHours();
  const currentTimeSlot = orderPredictions.find(prediction => {
    const hour = parseInt(prediction.timeSlot.split(':')[0]);
    const isAM = prediction.timeSlot.includes('AM');
    const adjustedHour = isAM ? (hour === 12 ? 0 : hour) : (hour === 12 ? 12 : hour + 12);
    return adjustedHour === currentHour;
  });

  const handleMenuClick = async (menuName: string) => {
    if (expandedMenu === menuName) {
      setExpandedMenu(null);
      return;
    }

    setLoadingBreakdown(menuName);
    setExpandedMenu(null);

    // Simulate loading delay
    setTimeout(() => {
      setLoadingBreakdown(null);
      setExpandedMenu(menuName);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Kitchen Dashboard</h1>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <p className="text-neutral text-lg">
            Total Predicted Orders Today: <span className="font-semibold text-primary">{totalPredictedOrders}</span>
          </p>
          <div className="text-right mt-2 sm:mt-0">
            <p className="text-sm text-gray-600">{currentDate}</p>
            <p className="text-lg font-semibold text-primary">{currentTime}</p>
          </div>
        </div>
        {currentTimeSlot && (
          <p className="text-neutral text-sm mt-2">
            Current Time Slot ({currentTimeSlot.timeSlot}): {currentTimeSlot.predictedOrders} orders predicted
          </p>
        )}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel - Order Predictions */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Prediction by Menu (Daily)</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Menu
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quantity
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {menuPredictions.map((prediction, index) => (
                  <React.Fragment key={index}>
                    <tr 
                      className={`${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'} cursor-pointer hover:bg-primary hover:bg-opacity-10 transition-colors`}
                      onClick={() => handleMenuClick(prediction.menu)}
                    >
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        <div className="flex items-center">
                          <span className="mr-2">{expandedMenu === prediction.menu ? '📊' : '🍽️'}</span>
                          {prediction.menu}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {prediction.quantity}
                      </td>
                    </tr>
                    
                    {/* Loading state */}
                    {loadingBreakdown === prediction.menu && (
                      <tr className="bg-blue-50">
                        <td colSpan={2} className="px-6 py-4 text-center">
                          <div className="flex items-center justify-center">
                            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mr-3"></div>
                            <span className="text-sm text-gray-600">Generating hourly breakdown...</span>
                          </div>
                        </td>
                      </tr>
                    )}
                    
                    {/* Expanded hourly breakdown */}
                    {expandedMenu === prediction.menu && prediction.hourlyBreakdown && (
                      <tr className="bg-gray-50">
                        <td colSpan={2} className="px-6 py-4">
                          <div className="ml-6">
                            <h4 className="text-sm font-medium text-gray-900 mb-3">Hourly Breakdown</h4>
                            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                              {prediction.hourlyBreakdown.map((hour, hourIndex) => (
                                <div key={hourIndex} className="bg-white p-2 rounded border text-xs">
                                  <div className="font-medium text-gray-900">{hour.hour}</div>
                                  <div className="text-primary font-semibold">{hour.quantity}</div>
                                </div>
                              ))}
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Panel - Alerts and Insights */}
        <div className="space-y-6">
          {/* Real-Time Alerts */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Real-Time Alerts</h2>
            <div className="space-y-3">
              {alerts.map((alert) => (
                <div
                  key={alert.id}
                  className={`p-4 rounded-lg border-l-4 ${
                    alert.severity === 'high'
                      ? 'bg-red-50 border-red-400'
                      : alert.severity === 'medium'
                      ? 'bg-yellow-50 border-yellow-400'
                      : 'bg-blue-50 border-blue-400'
                  }`}
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <span className={`text-lg ${
                        alert.severity === 'high' ? 'text-red-400' : 
                        alert.severity === 'medium' ? 'text-yellow-400' : 'text-blue-400'
                      }`}>
                        {alert.type === 'delay' ? '⏰' : alert.type === 'surge' ? '📈' : '🚨'}
                      </span>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                      <p className="text-xs text-gray-500 mt-1">{alert.timestamp}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Surge Prediction */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Surge Predictions</h2>
            <div className="space-y-3">
              <div className="p-4 bg-accent bg-opacity-10 rounded-lg border border-accent">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">📊</span>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Peak Hours Expected</p>
                    <p className="text-xs text-gray-600">12:00 PM - 2:00 PM: 140 orders</p>
                  </div>
                </div>
              </div>
              <div className="p-4 bg-secondary bg-opacity-10 rounded-lg border border-secondary">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">🌅</span>
                  <div>
                    <p className="text-sm font-medium text-gray-900">Evening Rush</p>
                    <p className="text-xs text-gray-600">6:00 PM - 8:00 PM: 165 orders</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Panel - Graph View */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Predictions Chart</h2>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={orderPredictions}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="timeSlot" 
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis />
              <Tooltip 
                formatter={(value: number) => [value, 'Predicted Orders']}
                labelFormatter={(label) => `Time: ${label}`}
              />
              <Line 
                type="monotone" 
                dataKey="predictedOrders" 
                stroke="#2E7D32" 
                strokeWidth={3}
                dot={{ fill: '#2E7D32', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: '#2E7D32', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
