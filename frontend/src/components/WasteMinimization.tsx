import React, { useEffect, useState } from 'react';
import { StockItem, stockHistory, aiSuggestions, branchStocks, stockTransferRecommendations } from '../data/mockData';

const WasteMinimization: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'inventory' | 'history' | 'transfer'>('inventory');
  const [generatedRecipes, setGeneratedRecipes] = useState<string[]>([]);
  const [isGeneratingRecipes, setIsGeneratingRecipes] = useState(false);
  const [stockItems, setStockItem] = useState<Array<StockItem>>([])

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/stock")
    .then((data) => data.json())
    .then((datas) => {
      for (const data of datas) {
        console.log(data)
        const date = new Date(data["expiryDate"])
        const formatted = new Intl.DateTimeFormat("en-GB", {
          day: "2-digit",
          month: "2-digit",
          year: "numeric"
        }).format(date);
        data["expiryDate"] = formatted
      }
      setStockItem(datas)
    })
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'fresh':
        return 'bg-green-100 text-green-800';
      case 'near-expiry':
        return 'bg-yellow-100 text-yellow-800';
      case 'expired':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'fresh':
        return '✅';
      case 'near-expiry':
        return '⚠️';
      case 'expired':
        return '❌';
      default:
        return '❓';
    }
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'added':
        return 'bg-green-100 text-green-800';
      case 'used':
        return 'bg-blue-100 text-blue-800';
      case 'wasted':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'added':
        return '➕';
      case 'used':
        return '🍽️';
      case 'wasted':
        return '🗑️';
      default:
        return '❓';
    }
  };

  const nearExpiryItems = stockItems.filter(item => item.status === 'near-expiry' || item.status === 'expired');
  const totalWasteCost = stockHistory
    .filter(entry => entry.action === 'wasted')
    .reduce((sum, entry) => sum + entry.cost, 0);

  const generateRecipes = async () => {
    setIsGeneratingRecipes(true);
    
    // Simulate API call delay
    setTimeout(() => {
      const mockRecipes = [
        "🍲 Chicken & Tomato Soup - Use expiring chicken breast and tomatoes",
        "🥗 Fresh Garden Salad - Combine lettuce with fresh vegetables",
        "🍝 Pasta Primavera - Create a vegetable pasta with near-expiry items",
        "🥘 One-Pot Chicken Rice - Utilize chicken breast and vegetables",
        "🥪 Club Sandwich - Use chicken breast, lettuce, and tomatoes"
      ];
      setGeneratedRecipes(mockRecipes);
      setIsGeneratingRecipes(false);
    }, 2000);
  };

  const calculateStockPercentage = (item: any) => {
    // Mock calculation - in real app, this would be based on actual stock levels
    const baseQuantity = 50; // Assume base quantity for percentage calculation
    return Math.min(Math.round((item.quantity / baseQuantity) * 100), 100);
  };

  const getStockStatusColor = (status: string) => {
    switch (status) {
      case 'high':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStockStatusIcon = (status: string) => {
    switch (status) {
      case 'high':
        return '🟢';
      case 'medium':
        return '🟡';
      case 'low':
        return '🔴';
      default:
        return '⚪';
    }
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

  return (
    <div className="flex flex-col space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Smart Waste Minimization</h1>
        <p className="text-neutral text-lg">
          Total waste cost reduced this week: <span className="font-semibold text-primary">RM135.00</span> 
          <span className="text-green-600 ml-2">(27% lower than last week)</span>
        </p>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 overflow-auto">
        {/* Left Panel */}
        <div className="flex flex-col space-y-6 overflow-auto">
          {/* Tabs */}
          <div className="flex flex-col bg-white rounded-lg shadow-sm overflow-auto">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8 px-6">
                <button
                  onClick={() => setActiveTab('inventory')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'inventory'
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  📦 Inventory
                </button>
                <button
                  onClick={() => setActiveTab('history')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'history'
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  📊 Stock History
                </button>
                <button
                  onClick={() => setActiveTab('transfer')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'transfer'
                      ? 'border-primary text-primary'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  🚚 Stock Transfer
                </button>
              </nav>
            </div>

            <div className="flex p-6 overflow-auto">
              {activeTab === 'inventory' ? (
                <div className='flex flex-col overflow-auto'>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Stock</h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Item
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Quantity
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            % Stock Left
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Expiry
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {stockItems.map((item) => (
                          <tr key={item.id} className={parseInt(item.id) % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="text-sm font-medium text-gray-900">{item.name}</div>
                              <div className="text-sm text-gray-500">${item.cost.toFixed(2)}</div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {item.quantity} {item.unit}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              <div className="flex items-center">
                                <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                                  <div 
                                    className={`h-2 rounded-full ${
                                      calculateStockPercentage(item) >= 70 ? 'bg-green-500' :
                                      calculateStockPercentage(item) >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                                    }`}
                                    style={{ width: `${Math.min(calculateStockPercentage(item), 100)}%` }}
                                  ></div>
                                </div>
                                <span className="text-xs">{calculateStockPercentage(item)}%</span>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {item.expiryDate}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(item.status)}`}>
                                <span className="mr-1">{getStatusIcon(item.status)}</span>
                                {item.status.replace('-', ' ')}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : activeTab === 'history' ? (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Stock History</h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Date
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Item
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Action
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Quantity
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Cost
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {stockHistory.map((entry) => (
                          <tr key={entry.id} className={parseInt(entry.id) % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {entry.date}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {entry.item}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActionColor(entry.action)}`}>
                                <span className="mr-1">{getActionIcon(entry.action)}</span>
                                {entry.action}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              {entry.action === 'added' ? '+' : ''}{entry.addedQuantity}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                              ${entry.cost.toFixed(2)}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : activeTab === 'transfer' ? (
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Multi-Branch Stock Levels</h3>
                  
                  {/* Branch Stock Boxes */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    {branchStocks.map((branch) => (
                      <div key={branch.branchId} className="border border-gray-200 rounded-lg p-4">
                        <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
                          <span className="mr-2">🏪</span>
                          {branch.branchName}
                        </h4>
                        <div className="space-y-2">
                          {branch.stock.map((item) => (
                            <div key={item.itemId} className="flex justify-between items-center text-sm">
                              <span className="text-gray-700">{item.itemName}</span>
                              <div className="flex items-center space-x-2">
                                <span className="text-gray-900">{item.quantity} {item.unit}</span>
                                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStockStatusColor(item.status)}`}>
                                  <span className="mr-1">{getStockStatusIcon(item.status)}</span>
                                  {item.status}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* AI Transfer Recommendations */}
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
                      <span className="mr-2">🤖</span>
                      AI Stock Transfer Recommendations
                    </h4>
                    <div className="space-y-3">
                      {stockTransferRecommendations.map((recommendation) => (
                        <div key={recommendation.id} className="bg-white p-3 rounded border">
                          <div className="flex justify-between items-start mb-2">
                            <div>
                              <p className="text-sm font-medium text-gray-900">
                                Transfer {recommendation.quantity} {recommendation.unit} of {recommendation.item}
                              </p>
                              <p className="text-xs text-gray-600">
                                From {recommendation.fromBranch} to {recommendation.toBranch}
                              </p>
                            </div>
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(recommendation.priority)}`}>
                              {recommendation.priority} priority
                            </span>
                          </div>
                          <div className="flex justify-between items-center text-xs text-gray-500">
                            <span>⏰ {recommendation.timeFrame}</span>
                            <span>💡 {recommendation.reason}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </div>

        {/* Right Panel */}
        <div className="flex flex-col space-y-6 overflow-auto">
          {/* Near-Expiry Items */}
          <div className="flex flex-col bg-white rounded-lg shadow-sm p-6 overflow-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">⚠️ Near-Expiry Items</h3>
            <div className="space-y-3 overflow-auto">
              {nearExpiryItems.length > 0 ? (
                nearExpiryItems.map((item) => (
                  <div
                    key={item.id}
                    className={`p-4 rounded-lg border-l-4 ${
                      item.status === 'expired'
                        ? 'bg-red-50 border-red-400'
                        : 'bg-yellow-50 border-yellow-400'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{item.name}</p>
                        <p className="text-xs text-gray-600">
                          {item.quantity} {item.unit} • Expires: {item.expiryDate}
                        </p>
                      </div>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(item.status)}`}>
                        <span className="mr-1">{getStatusIcon(item.status)}</span>
                        {item.status.replace('-', ' ')}
                      </span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <span className="text-4xl mb-2 block">✅</span>
                  <p className="text-gray-500">No near-expiry items!</p>
                </div>
              )}
            </div>
          </div>

          {/* AI Suggestions */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">🤖 AI Suggestions</h3>
            
            {/* Recipe Generation Button */}
            <div className="mb-4">
              <button
                onClick={generateRecipes}
                disabled={isGeneratingRecipes}
                className="w-full bg-primary text-white px-4 py-2 rounded-lg hover:bg-primary hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isGeneratingRecipes ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Generating Recipes/Ideas...
                  </div>
                ) : (
                  'Generate Recipes/Ideas'
                )}
              </button>
            </div>

            {/* Generated Recipes */}
            {generatedRecipes.length > 0 && (
              <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 className="text-sm font-medium text-gray-900 mb-2">🍳 Generated Recipe Ideas</h4>
                <div className="space-y-2">
                  {generatedRecipes.map((recipe, index) => (
                    <div key={index} className="text-xs text-gray-700 bg-white p-2 rounded border">
                      {recipe}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-4">
              {aiSuggestions.filter(suggestion => suggestion.type === 'waste' || suggestion.type === 'inventory').map((suggestion) => (
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
                      <span className="text-lg">
                        {suggestion.type === 'waste' ? '♻️' : '📦'}
                      </span>
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
        </div>
      </div>
    </div>
  );
};

export default WasteMinimization;
