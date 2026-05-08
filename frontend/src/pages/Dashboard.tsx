import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DashboardLayout from '../components/layout/DashboardLayout'
import InventoryList from '../components/dashboard/InventoryList'
import WeatherImpact from '../components/dashboard/WeatherImpact'
import GapFinder from '../components/dashboard/GapFinder'
import SmartCart from '../components/dashboard/SmartCart'
import Analytics from '../components/dashboard/Analytics'
import EatMeFirst from '../components/dashboard/EatMeFirst'
import { mockProducts, mockAnalytics } from '../data/mockData'

// Commented out for now - can be used when API is ready
// import { useQuery } from '@tanstack/react-query'
// import axios from 'axios'

export default function DashboardPage() {
  const navigate = useNavigate()
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const auth = localStorage.getItem('isAuthenticated')
    if (!auth) {
      navigate('/login')
    } else {
      setIsAuthenticated(true)
    }
  }, [navigate])

  // Use mock data for now - can be replaced with API calls later
  const inventory = mockProducts
  const inventoryLoading = false
  const analytics = mockAnalytics

  // Uncomment below to use real API calls
  // const { data: inventory, isLoading: inventoryLoading } = useQuery({
  //   queryKey: ['inventory'],
  //   queryFn: async () => {
  //     const res = await axios.get('/api/inventory')
  //     return res.data
  //   },
  //   enabled: isAuthenticated,
  //   refetchInterval: 5000,
  // })

  // const { data: analytics } = useQuery({
  //   queryKey: ['analytics'],
  //   queryFn: async () => {
  //     const res = await axios.get('/api/analytics/summary')
  //     return res.data
  //   },
  //   enabled: isAuthenticated,
  //   refetchInterval: 10000,
  // })

  if (!isAuthenticated) {
    return null
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Analytics Overview */}
        {analytics && <Analytics data={analytics} />}

        {/* Eat Me First - Expiring Items */}
        <EatMeFirst />

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Inventory - Takes 2 columns */}
          <div className="lg:col-span-2">
            <InventoryList 
              items={inventory || []} 
              loading={inventoryLoading} 
            />
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <GapFinder />
            <SmartCart />
          </div>
        </div>

        {/* Weather Impact */}
        <WeatherImpact />
      </div>
    </DashboardLayout>
  )
}
