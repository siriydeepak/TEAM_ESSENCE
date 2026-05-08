import { Package, AlertTriangle, CheckCircle, Clock } from 'lucide-react'

interface InventoryItem {
  id: string
  name: string
  category: string
  quantity: number
  unit: string
  days_left: number
  status: string
  price?: number
  source: string
}

interface InventoryListProps {
  items: InventoryItem[]
  loading: boolean
}

export default function InventoryList({ items, loading }: InventoryListProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'expired': return 'bg-red-100 text-red-800 border-red-200'
      case 'urgent': return 'bg-orange-100 text-orange-800 border-orange-200'
      case 'critical': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'warning': return 'bg-blue-100 text-blue-800 border-blue-200'
      default: return 'bg-green-100 text-green-800 border-green-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'expired':
      case 'urgent':
      case 'critical':
        return <AlertTriangle className="w-4 h-4" />
      case 'warning':
        return <Clock className="w-4 h-4" />
      default:
        return <CheckCircle className="w-4 h-4" />
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm">
      <div className="p-6 border-b">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Package className="w-6 h-6 text-primary" />
            <h2 className="text-xl font-bold text-gray-900">Inventory</h2>
          </div>
          <span className="text-sm text-gray-500">{items.length} items</span>
        </div>
      </div>

      <div className="divide-y">
        {items.length === 0 ? (
          <div className="p-12 text-center">
            <Package className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No items in inventory</p>
            <p className="text-sm text-gray-400 mt-2">
              Connect your Gmail to automatically track purchases
            </p>
          </div>
        ) : (
          items.map((item) => (
            <div key={item.id} className="p-4 hover:bg-gray-50 transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-gray-900">{item.name}</h3>
                    <span className={`
                      px-2 py-1 rounded-full text-xs font-medium border flex items-center gap-1
                      ${getStatusColor(item.status)}
                    `}>
                      {getStatusIcon(item.status)}
                      {item.status}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-gray-600">
                    <span className="font-medium">{item.quantity} {item.unit}</span>
                    <span>•</span>
                    <span>{item.category}</span>
                    <span>•</span>
                    <span className={`font-medium ${
                      item.days_left < 0 ? 'text-red-600' :
                      item.days_left <= 2 ? 'text-orange-600' :
                      'text-gray-900'
                    }`}>
                      {item.days_left < 0 
                        ? `Expired ${Math.abs(item.days_left)}d ago`
                        : `${item.days_left}d left`
                      }
                    </span>
                  </div>
                  <div className="mt-2 flex items-center gap-2 text-xs text-gray-500">
                    <span className="bg-gray-100 px-2 py-1 rounded">{item.source}</span>
                    {item.price && <span>₹{item.price}</span>}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
