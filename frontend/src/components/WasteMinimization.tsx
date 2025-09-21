import React, { useEffect, useState } from 'react';
import { stockItems, stockHistory, aiSuggestions, Recipe } from '../data/mockData';

const WasteMinimization: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'inventory' | 'history'>('inventory');
  const [isGeneratingRecipes, setIsGeneratingRecipes] = useState(false);
  const [recipes, setRecipes] = useState<Recipe[]>([]);

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

  useEffect(() => {

    console.log("HELLOL THEEJKWLA")

    if (isGeneratingRecipes === false) {
      return
    }

    fetch("http://127.0.0.1:5000/api/bedrock/generate-recipes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        ingredient_id: "68cfbac39cd6acf34268676a"
      })
    }).then(
      (res) => res.json() 
    ).then((res) => {
      setRecipes(res.recipes)
      setIsGeneratingRecipes(false);
    }
    )
  }, [isGeneratingRecipes])

  const calculateStockPercentage = (item: any) => {
    // Mock calculation - in real app, this would be based on actual stock levels
    const baseQuantity = 50; // Assume base quantity for percentage calculation
    return Math.round((item.quantity / baseQuantity) * 100);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Smart Waste Minimization</h1>
        <p className="text-neutral text-lg">
          Total waste cost reduced this week: <span className="font-semibold text-primary">RM135.00</span> 
          <span className="text-green-600 ml-2">(27% lower than last week)</span>
        </p>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Panel */}
        <div className="space-y-6">
          {/* Tabs */}
          <div className="bg-white rounded-lg shadow-sm">
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
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'inventory' ? (
                <div>
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
              ) : (
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
              )}
            </div>
          </div>
        </div>

        {/* Right Panel */}
        <div className="space-y-6">
          {/* Near-Expiry Items */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">⚠️ Near-Expiry Items</h3>
            <div className="space-y-3">
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
                onClick={() => setIsGeneratingRecipes(true)}
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
            {recipes.length > 0 && (
              <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 className="text-sm font-medium text-gray-900 mb-2">🍳 Generated Recipe Ideas</h4>
                <div className="space-y-4">
                  {recipes.map((recipe, index) => (
                    <div key={index} className="bg-white p-4 rounded-lg border shadow-sm">
                      <div className="flex justify-between items-start mb-3">
                        <h5 className="text-sm font-semibold text-gray-900">{recipe.name}</h5>
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                          {recipe.cuisine_type}
                        </span>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 mb-3 text-xs text-gray-600">
                        <div>⏱️ {recipe.cook_time_minutes} mins</div>
                        <div>👥 {recipe.servings} servings</div>
                        <div>💰 Cost: RM{recipe.estimated_cost.toFixed(2)}</div>
                        <div>🏷️ Sell: RM{recipe.suggested_selling_price.toFixed(2)}</div>
                      </div>

                      <div className="mb-3">
                        <h6 className="text-xs font-medium text-gray-700 mb-1">Ingredients:</h6>
                        <div className="text-xs text-gray-600 max-h-20 overflow-y-auto">
                          {recipe.ingredients.map((ingredient, idx) => (
                            <div key={idx}>
                              • {ingredient.quantity} {ingredient.unit} {ingredient.name}
                              {ingredient.notes && ` (${ingredient.notes})`}
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="mb-3">
                        <h6 className="text-xs font-medium text-gray-700 mb-1">Instructions:</h6>
                        <div className="text-xs text-gray-600 max-h-16 overflow-y-auto">
                          {recipe.instructions.map((instruction, idx) => (
                            <div key={idx} className="mb-1">
                              {instruction}
                            </div>
                          ))}
                        </div>
                      </div>

                      <div className="flex justify-between items-center text-xs">
                        <span className={`px-2 py-1 rounded-full ${
                          recipe.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                          recipe.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {recipe.difficulty}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* <div className="space-y-4">
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
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WasteMinimization;
