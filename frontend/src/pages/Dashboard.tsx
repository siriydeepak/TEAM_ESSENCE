import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import DashboardLayout from '../components/layout/DashboardLayout'
import InventoryList from '../components/dashboard/InventoryList'
import WeatherImpact from '../components/dashboard/WeatherImpact'
import GapFinder from '../components/dashboard/GapFinder'
import SmartCart from '../components/dashboard/SmartCart'
import Analytics from '../components/dashboard/Analytics'
import LinkKitchen from '../components/dashboard/LinkKitchen'

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

  const { data: inventory, isLoading: inventoryLoading } = useQuery({
    queryKey: ['inventory'],
    queryFn: async () => {
      const res = await axios.get('/api/inventory')
      return res.data
    },
    enabled: isAuthenticated,
    refetchInterval: 5000, // Refresh every 5 seconds
  })

  const { data: analytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const res = await axios.get('/api/analytics/summary')
      return res.data
    },
    enabled: isAuthenticated,
    refetchInterval: 10000,
  })

  if (!isAuthenticated) {
    return null
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Analytics Overview */}
        {analytics && <Analytics data={analytics} />}

        {/* Link Your Kitchen — Aether-Link Protocol */}
        <LinkKitchen />

        {/* Weather Impact */}
        <WeatherImpact />

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Inventory - Takes 2 columns */}
          <div className="lg:col-span-2">
            <InventoryList 
              items={inventory?.items || []} 
              loading={inventoryLoading} 
            />
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <GapFinder />
            <SmartCart />
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}

