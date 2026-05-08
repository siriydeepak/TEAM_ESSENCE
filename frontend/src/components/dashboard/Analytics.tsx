import { TrendingUp, Package, AlertTriangle, CheckCircle, DollarSign } from 'lucide-react'

interface AnalyticsProps {
  data: {
    total_items: number
    expiring_soon: number
    expired: number
    healthy: number
    freshness_score: number
    total_waste_inr: number
    smart_cart_savings_inr: number
  }
}

export default function Analytics({ data }: AnalyticsProps) {
  const stats = [
    {
      label: 'Total Items',
      value: data.total_items,
      icon: Package,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Expiring Soon',
      value: data.expiring_soon,
      icon: AlertTriangle,
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
    {
      label: 'Expired',
      value: data.expired,
      icon: AlertTriangle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
    },
    {
      label: 'Healthy',
      value: data.healthy,
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
  ]

  return (
    <div className="space-y-4">
      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="bg-white rounded-xl shadow-sm p-4">
              <div className={`inline-flex p-2 rounded-lg ${stat.bgColor} mb-3`}>
                <Icon className={`w-5 h-5 ${stat.color}`} />
              </div>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-sm text-gray-600">{stat.label}</p>
            </div>
          )
        })}
      </div>

      {/* Freshness Score & Savings */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-primary/10 to-primary-light/10 rounded-xl shadow-sm p-6 border border-primary/20">
          <div className="flex items-center gap-3 mb-4">
            <TrendingUp className="w-6 h-6 text-primary" />
            <h3 className="text-lg font-bold text-gray-900">Freshness Score</h3>
          </div>
          <div className="flex items-end gap-2">
            <span className="text-4xl font-bold text-primary">{data.freshness_score}</span>
            <span className="text-xl text-gray-600 mb-1">/100</span>
          </div>
          <div className="mt-4 bg-gray-200 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-primary h-full rounded-full transition-all duration-500"
              style={{ width: `${data.freshness_score}%` }}
            />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl shadow-sm p-6 border border-green-100">
          <div className="flex items-center gap-3 mb-4">
            <DollarSign className="w-6 h-6 text-green-600" />
            <h3 className="text-lg font-bold text-gray-900">Savings & Waste</h3>
          </div>
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-600 mb-1">Smart Cart Savings</p>
              <p className="text-2xl font-bold text-green-600">
                ₹{data.smart_cart_savings_inr.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Waste Value</p>
              <p className="text-2xl font-bold text-red-600">
                ₹{data.total_waste_inr.toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
