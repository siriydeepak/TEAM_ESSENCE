import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DashboardLayout from '../components/layout/DashboardLayout'
import InventoryList from '../components/dashboard/InventoryList'
import { mockProducts, getEatMeFirstProducts } from '../data/mockData'

export default function InventoryPage() {
  const navigate = useNavigate()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [filter, setFilter] = useState<'all' | 'expiring' | 'healthy'>('all')

  useEffect(() => {
    const auth = localStorage.getItem('isAuthenticated')
    if (!auth) {
      navigate('/login')
    } else {
      setIsAuthenticated(true)
    }
  }, [navigate])

  if (!isAuthenticated) {
    return null
  }

  const getFilteredProducts = () => {
    switch (filter) {
      case 'expiring':
        return getEatMeFirstProducts()
      case 'healthy':
        return mockProducts.filter(p => ['good', 'optimal'].includes(p.status))
      default:
        return mockProducts
    }
  }

  const filteredProducts = getFilteredProducts()

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="font-['Epilogue'] text-4xl font-bold text-[#1a1c1c] mb-2">
              Expiry Logs
            </h1>
            <p className="text-[#71717a] font-['Plus_Jakarta_Sans']">
              Complete inventory with expiration tracking
            </p>
          </div>
          <button className="dark-gradient neon-border-cyan text-white px-6 py-3 rounded-xl flex items-center gap-2 active:scale-95 transition-transform">
            <span className="material-symbols-outlined text-lg">add</span>
            <span className="font-['Plus_Jakarta_Sans'] font-semibold">Add Item</span>
          </button>
        </div>

        {/* Filter Tabs */}
        <div className="dashboard-card stripe-stable">
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-6 py-3 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all ${
                filter === 'all'
                  ? 'dark-gradient neon-border-cyan text-white'
                  : 'bg-[#eeeeed] text-[#71717a] hover:bg-[#d4d4d8]'
              }`}
            >
              All Items ({mockProducts.length})
            </button>
            <button
              onClick={() => setFilter('expiring')}
              className={`px-6 py-3 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all ${
                filter === 'expiring'
                  ? 'dark-gradient neon-border-orange text-white'
                  : 'bg-[#eeeeed] text-[#71717a] hover:bg-[#d4d4d8]'
              }`}
            >
              Expiring Soon ({getEatMeFirstProducts().length})
            </button>
            <button
              onClick={() => setFilter('healthy')}
              className={`px-6 py-3 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all ${
                filter === 'healthy'
                  ? 'dark-gradient neon-border-cyan text-white'
                  : 'bg-[#eeeeed] text-[#71717a] hover:bg-[#d4d4d8]'
              }`}
            >
              Healthy ({mockProducts.filter(p => ['good', 'optimal'].includes(p.status)).length})
            </button>
          </div>
        </div>

        {/* Inventory List */}
        <InventoryList items={filteredProducts} loading={false} />
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </DashboardLayout>
  )
}