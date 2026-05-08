import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import { ShoppingCart, Check, X, TrendingDown } from 'lucide-react'
import toast from 'react-hot-toast'

export default function SmartCart() {
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['smart-cart'],
    queryFn: async () => {
      const res = await axios.get('/api/smart-cart')
      return res.data
    },
    refetchInterval: 30000,
  })

  const approveMutation = useMutation({
    mutationFn: async ({ item_id, approved }: { item_id: string; approved: boolean }) => {
      const res = await axios.post('/api/smart-cart/approve', { item_id, approved })
      return res.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['smart-cart'] })
      toast.success('Cart updated')
    },
  })

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow-sm p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-2/3"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
        </div>
      </div>
    )
  }

  const items = data?.items || []
  const totalSavings = data?.total_savings || 0

  return (
    <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl shadow-sm p-6 border border-green-100">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <ShoppingCart className="w-6 h-6 text-green-600" />
          <h2 className="text-xl font-bold text-gray-900">Smart Cart</h2>
        </div>
        {totalSavings > 0 && (
          <div className="flex items-center gap-1 text-green-600">
            <TrendingDown className="w-4 h-4" />
            <span className="text-sm font-bold">₹{totalSavings.toFixed(2)}</span>
          </div>
        )}
      </div>

      {items.length === 0 ? (
        <div className="text-center py-8">
          <ShoppingCart className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500 text-sm">No items in cart</p>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map((item: any) => (
            <div key={item.id} className="bg-white rounded-lg p-4">
              <div className="flex items-start justify-between mb-2">
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 text-sm mb-1">
                    {item.name}
                  </h3>
                  <p className="text-xs text-gray-600 mb-2">{item.reason}</p>
                  <div className="flex items-center gap-2">
                    <span className={`
                      text-xs px-2 py-1 rounded-full font-medium
                      ${item.urgency === 'high' ? 'bg-red-100 text-red-700' :
                        item.urgency === 'medium' ? 'bg-orange-100 text-orange-700' :
                        'bg-blue-100 text-blue-700'}
                    `}>
                      {item.urgency}
                    </span>
                    <span className="text-xs text-gray-500">{item.source}</span>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between pt-3 border-t">
                <div>
                  <p className="text-xs text-gray-500 line-through">₹{item.original_price}</p>
                  <p className="text-lg font-bold text-green-600">₹{item.best_price}</p>
                  <p className="text-xs text-green-600">Save {item.savings_pct}%</p>
                </div>

                {!item.approved && (
                  <div className="flex gap-2">
                    <button
                      onClick={() => approveMutation.mutate({ item_id: item.id, approved: true })}
                      className="p-2 bg-green-100 hover:bg-green-200 text-green-700 rounded-lg transition"
                      title="Approve"
                    >
                      <Check className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => approveMutation.mutate({ item_id: item.id, approved: false })}
                      className="p-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition"
                      title="Reject"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                )}
                {item.approved && (
                  <span className="text-xs bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
                    ✓ Approved
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
