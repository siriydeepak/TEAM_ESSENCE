import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DashboardLayout from '../components/layout/DashboardLayout'
import Analytics from '../components/dashboard/Analytics'
import { mockAnalytics } from '../data/mockData'

export default function AnalyticsPage() {
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

  if (!isAuthenticated) {
    return null
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="mb-6">
          <h1 className="font-['Epilogue'] text-4xl font-bold text-[#1a1c1c] mb-2">
            Analytics Dashboard
          </h1>
          <p className="text-[#71717a] font-['Plus_Jakarta_Sans']">
            Track your inventory trends, waste reduction, and savings
          </p>
        </div>

        <Analytics data={mockAnalytics} />
      </div>
    </DashboardLayout>
  )
}