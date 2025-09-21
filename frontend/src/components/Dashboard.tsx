import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { orderPredictions, alerts, menuPredictions } from '../data/mockData';

const Dashboard: React.FC = () => {
  const [expandedMenu, setExpandedMenu] = useState<string | null>(null);
  const [loadingBreakdown, setLoadingBreakdown] = useState<string | null>(null);
  const [orderFeedback, setOrderFeedback] = useState<'more' | 'equal' | 'less' | null>(null);
  const [selectedReason, setSelectedReason] = useState<string>('');
  const [customReason, setCustomReason] = useState<string>('');

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

  const handleFeedbackSubmit = () => {
    if (orderFeedback && (orderFeedback === 'equal' || selectedReason)) {
      // Here you would typically send the feedback to your backend
      console.log('Feedback submitted:', {
        feedback: orderFeedback,
        reason: selectedReason,
        customReason: customReason
      });
      
      // Reset form
      setOrderFeedback(null);
      setSelectedReason('');
      setCustomReason('');
      
      // Show success message (you could add a toast notification here)
      alert('Thank you for your feedback! This helps improve our predictions.');
    }
  };

  const reasonOptions = [
    'Rainy weather',
    'Sunny weather', 
    'Festive season',
    'Holiday period',
    'Special occasion',
    'Others'
  ];

  return (
    <div className="flex flex-1 flex-col space-y-6">
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

          {/* Order Prediction Feedback */}
          <div className="bg-white rounded-lg shadow-sm p-6 mt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Order Prediction Feedback</h3>
            <p className="text-sm text-gray-600 mb-4">
              Were the actual orders for today more, equal, or less than predicted?
            </p>
            
            <div className="space-y-4">
              {/* Feedback Buttons */}
              <div className="flex space-x-3">
                <button
                  onClick={() => setOrderFeedback('more')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    orderFeedback === 'more'
                      ? 'bg-green-100 text-green-800 border-2 border-green-300'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  More than predicted
                </button>
                <button
                  onClick={() => setOrderFeedback('equal')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    orderFeedback === 'equal'
                      ? 'bg-blue-100 text-blue-800 border-2 border-blue-300'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Equal to predicted
                </button>
                <button
                  onClick={() => setOrderFeedback('less')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    orderFeedback === 'less'
                      ? 'bg-red-100 text-red-800 border-2 border-red-300'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Less than predicted
                </button>
              </div>

              {/* Reason Dropdown */}
              {(orderFeedback === 'more' || orderFeedback === 'less') && (
                <div className="space-y-3">
                  <label className="block text-sm font-medium text-gray-700">
                    What was the main reason?
                  </label>
                  <select
                    value={selectedReason}
                    onChange={(e) => setSelectedReason(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                  >
                    <option value="">Select a reason...</option>
                    {reasonOptions.map((reason) => (
                      <option key={reason} value={reason}>
                        {reason}
                      </option>
                    ))}
                  </select>

                  {/* Custom Reason Input */}
                  {selectedReason === 'Others' && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Please specify:
                      </label>
                      <input
                        type="text"
                        value={customReason}
                        onChange={(e) => setCustomReason(e.target.value)}
                        placeholder="Enter the reason..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                      />
                    </div>
                  )}

                  {/* Submit Button */}
                  <button
                    onClick={handleFeedbackSubmit}
                    disabled={!selectedReason || (selectedReason === 'Others' && !customReason)}
                    className="w-full bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    Submit Feedback
                  </button>
                </div>
              )}

              {/* Equal Feedback Submit */}
              {orderFeedback === 'equal' && (
                <button
                  onClick={handleFeedbackSubmit}
                  className="w-full bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary hover:bg-opacity-90 transition-colors"
                >
                  Submit Feedback
                </button>
              )}
            </div>
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
