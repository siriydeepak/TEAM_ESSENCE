import React from 'react'
import { BarChart3, TrendingUp, PieChart } from 'lucide-react'

const Analytics: React.FC = () => {
  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        <p className="text-gray-600 mt-2">Track your inventory trends and waste reduction</p>
      </div>

      {/* Analytics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Waste Reduction</h3>
            <TrendingUp className="w-6 h-6 text-green-600" />
          </div>
          <div className="text-3xl font-bold text-green-600 mb-2">0%</div>
          <p className="text-sm text-gray-600">Compared to last month</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Money Saved</h3>
            <PieChart className="w-6 h-6 text-blue-600" />
          </div>
          <div className="text-3xl font-bold text-blue-600 mb-2">$0</div>
          <p className="text-sm text-gray-600">This month</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Items Tracked</h3>
            <BarChart3 className="w-6 h-6 text-purple-600" />
          </div>
          <div className="text-3xl font-bold text-purple-600 mb-2">0</div>
          <p className="text-sm text-gray-600">Total items managed</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Expiration Trends</h2>
          </div>
          <div className="p-6">
            <div className="text-center py-12">
              <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No data available</p>
              <p className="text-sm text-gray-400 mt-1">Start tracking items to see trends</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Category Breakdown</h2>
          </div>
          <div className="p-6">
            <div className="text-center py-12">
              <PieChart className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No categories yet</p>
              <p className="text-sm text-gray-400 mt-1">Add items to see category distribution</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Analytics