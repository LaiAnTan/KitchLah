import React, { useEffect, useState } from 'react';
import { stations, aiSuggestions, Order } from '../data/mockData';
import { list } from 'postcss';


const AIDecisionMaking: React.FC = () => {
  const [activeStation, setActiveStation] = useState<string>('all');
  const [simulationInput, setSimulationInput] = useState<string>('');

  const [orders, setOrders] = useState<Array<Order>>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/schedule").then(
      (res) => res.json() 
    ).then((res) => setOrders(res))
  }, [])

  console.log(orders)

  const stationTabs = [
    { id: 'all', name: 'All Stations', icon: '🏭' },
    { id: 'prep', name: 'Prep Station', icon: '🔪' },
    { id: 'fryer', name: 'Fryer Station', icon: '🍟' },
    { id: 'grill', name: 'Grill Station', icon: '🔥' },
    { id: 'stove', name: 'Stove Station', icon: '🍳' },
    { id: 'assembly', name: 'Assembly Station', icon: '📦' },
  ];

  const getLoadColor = (load: number) => {
    if (load >= 80) return 'bg-red-100 text-red-800';
    if (load >= 60) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };

  const getLoadIcon = (load: number) => {
    if (load >= 80) return '🔴';
    if (load >= 60) return '🟡';
    return '🟢';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-gray-100 text-gray-800';
      case 'preparing':
        return 'bg-blue-100 text-blue-800';
      case 'ready':
        return 'bg-green-100 text-green-800';
      case 'completed':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredOrders = activeStation === 'all' 
    ? orders 
    : orders.filter(order => order.station === activeStation);

  const currentStation = stations.find(station => station.id === activeStation);
  const overloadedStations = stations.filter(station => station.currentLoad >= 80);
  const efficiencySuggestions = aiSuggestions.filter(suggestion => suggestion.type === 'efficiency');

  const runSimulation = () => {
    // Mock simulation logic
    return {
      bottlenecks: ['Fryer Station', 'Assembly Station'],
      recommendations: [
        'Add 2 additional staff to Fryer Station',
        'Pre-prep 15 burger patties',
        'Optimize assembly line workflow'
      ],
      estimatedWaitTime: '12 minutes'
    };
  };

  const simulationResult = simulationInput ? runSimulation() : null;

  return (
    <div className="flex flex-col space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Decision Making</h1>
        <p className="text-neutral text-lg">
          Kitchen Operations Intelligence & Optimization
        </p>
      </div>

      {/* Station Tabs */}
      <div className="bg-white rounded-lg shadow-sm">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6 overflow-x-auto">
            {stationTabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveStation(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                  activeStation === tab.id
                    ? 'border-primary text-primary'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 overflow-y-auto">
        {/* Left Panel - Order Queues */}
        <div className="bg-white rounded-lg shadow-sm p-6 overflow-y-auto">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            {activeStation === 'all' ? 'All Orders' : `${currentStation?.name} Orders`}
          </h2>
          
          {activeStation !== 'all' && currentStation && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Current Load</span>
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getLoadColor(currentStation.currentLoad)}`}>
                  <span className="mr-1">{getLoadIcon(currentStation.currentLoad)}</span>
                  {currentStation.currentLoad}%
                </span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Orders in Queue</span>
                <span className="text-sm text-gray-900">{filteredOrders.length}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Avg Processing Time</span>
                <span className="text-sm text-gray-900">{currentStation.avgProcessingTime} min</span>
              </div>
            </div>
          )}

          <div className="space-y-3">
            {filteredOrders.length > 0 ? (
              filteredOrders.map((order) => (
                <div key={order.id} className="p-4 border border-gray-200 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h4 className="text-sm font-medium text-gray-900">Order #{order.id}</h4>
                      <p className="text-xs text-gray-600">{order.customerName}</p>
                    </div>
                    <div className="flex space-x-2">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(order.priority)}`}>
                        {order.priority}
                      </span>
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(order.status)}`}>
                        {order.status}
                      </span>
                    </div>
                  </div>
                  <div className="text-sm text-gray-600 mb-2">
                    Current Task: {order.items.join(', ')}
                  </div>
                  <div className="flex justify-between items-center text-xs text-gray-500">
                    <span>Station: {order.station}</span>
                    <span>Est. Time: {order.estimatedTime} min</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-8">
                <span className="text-4xl mb-2 block">📋</span>
                <p className="text-gray-500">No orders in queue</p>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Insights & Actions */}
        <div className="space-y-6 overflow-y-auto">
          {/* Station Overload Box */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">🚨 Station Overload Status</h3>
            {overloadedStations.length > 0 ? (
              <div className="space-y-3">
                {overloadedStations.map((station) => (
                  <div key={station.id} className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{station.name}</p>
                        <p className="text-xs text-gray-600">{station.ordersInQueue} orders queued</p>
                      </div>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getLoadColor(station.currentLoad)}`}>
                        <span className="mr-1">{getLoadIcon(station.currentLoad)}</span>
                        {station.currentLoad}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-4">
                <span className="text-2xl mb-2 block">✅</span>
                <p className="text-sm text-gray-600">All stations operating normally</p>
              </div>
            )}
          </div>

          {/* AI Suggestions */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">🤖 AI Recommendations</h3>
            <div className="space-y-3">
              {efficiencySuggestions.map((suggestion) => (
                <div
                  key={suggestion.id}
                  className={`p-4 rounded-lg border ${
                    suggestion.impact === 'high'
                      ? 'bg-red-50 border-red-200'
                      : suggestion.impact === 'medium'
                      ? 'bg-yellow-50 border-yellow-200'
                      : 'bg-blue-50 border-blue-200'
                  }`}
                >
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <span className="text-lg">⚡</span>
                    </div>
                    <div className="ml-3 flex-1">
                      <h4 className="text-sm font-medium text-gray-900">{suggestion.title}</h4>
                      <p className="text-xs text-gray-600 mt-1">{suggestion.description}</p>
                      <div className="mt-2">
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          suggestion.impact === 'high'
                            ? 'bg-red-100 text-red-800'
                            : suggestion.impact === 'medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {suggestion.action}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* What-If Simulation */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">🔮 What-If Simulation</h3>
            <div className="space-y-4">
              <div>
                <label htmlFor="simulation" className="block text-sm font-medium text-gray-700 mb-2">
                  Scenario Input
                </label>
                <input
                  type="text"
                  id="simulation"
                  value={simulationInput}
                  onChange={(e) => setSimulationInput(e.target.value)}
                  placeholder="e.g., What if 20 orders arrive at 8PM?"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>
              
              {simulationResult && (
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Simulation Results</h4>
                  <div className="space-y-2">
                    <div>
                      <span className="text-xs font-medium text-gray-700">Predicted Bottlenecks:</span>
                      <p className="text-xs text-gray-600">{simulationResult.bottlenecks.join(', ')}</p>
                    </div>
                    <div>
                      <span className="text-xs font-medium text-gray-700">Recommendations:</span>
                      <ul className="text-xs text-gray-600 list-disc list-inside">
                        {simulationResult.recommendations.map((rec, index) => (
                          <li key={index}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <span className="text-xs font-medium text-gray-700">Estimated Wait Time:</span>
                      <p className="text-xs text-gray-600">{simulationResult.estimatedWaitTime}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIDecisionMaking;
