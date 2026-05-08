import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DashboardLayout from '../components/layout/DashboardLayout'
import SmartCart from '../components/dashboard/SmartCart'

export default function SettingsPage() {
  const navigate = useNavigate()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [notifications, setNotifications] = useState({
    expiration: true,
    weather: true,
    smartCart: true,
  })

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

  const userEmail = localStorage.getItem('userEmail') || 'user@example.com'

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="mb-6">
          <h1 className="font-['Epilogue'] text-4xl font-bold text-[#1a1c1c] mb-2">
            Smart Restock
          </h1>
          <p className="text-[#71717a] font-['Plus_Jakarta_Sans']">
            AI-powered shopping recommendations based on your consumption patterns
          </p>
        </div>

        {/* Smart Cart Component */}
        <SmartCart />

        {/* Settings Sections */}
        <div className="space-y-6">
          {/* Profile Settings */}
          <div className="dashboard-card stripe-stable">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-cyan text-3xl">person</span>
              <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Profile Settings</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-[#3a4a44] mb-2 font-['Space_Grotesk'] uppercase tracking-wider">
                  Display Name
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border-2 border-[#eeeeed] rounded-xl focus:border-[#00FFD1] focus:outline-none transition-colors font-['Plus_Jakarta_Sans']"
                  placeholder="Your name"
                  defaultValue="AetherShelf User"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-[#3a4a44] mb-2 font-['Space_Grotesk'] uppercase tracking-wider">
                  Email
                </label>
                <input
                  type="email"
                  className="w-full px-4 py-3 border-2 border-[#eeeeed] rounded-xl focus:border-[#00FFD1] focus:outline-none transition-colors font-['Plus_Jakarta_Sans']"
                  placeholder="your@email.com"
                  defaultValue={userEmail}
                />
              </div>
            </div>
            <button className="mt-6 dark-gradient neon-border-cyan text-white px-6 py-3 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold active:scale-95 transition-transform">
              Save Changes
            </button>
          </div>

          {/* Notifications */}
          <div className="dashboard-card stripe-warning">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-yellow text-3xl">notifications</span>
              <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Notification Preferences</h2>
            </div>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-[rgba(0,255,209,0.05)] rounded-xl border border-[rgba(0,255,209,0.2)]">
                <div>
                  <h3 className="text-sm font-semibold text-[#1a1c1c] font-['Plus_Jakarta_Sans']">Expiration Alerts</h3>
                  <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">Get notified when items are about to expire</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={notifications.expiration}
                    onChange={(e) => setNotifications({...notifications, expiration: e.target.checked})}
                  />
                  <div className="w-14 h-7 bg-[#eeeeed] peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[rgba(0,255,209,0.3)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-[#00FFD1]"></div>
                </label>
              </div>
              <div className="flex items-center justify-between p-4 bg-[rgba(255,215,0,0.05)] rounded-xl border border-[rgba(255,215,0,0.2)]">
                <div>
                  <h3 className="text-sm font-semibold text-[#1a1c1c] font-['Plus_Jakarta_Sans']">Weather Alerts</h3>
                  <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">Notifications about weather impact on shelf life</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={notifications.weather}
                    onChange={(e) => setNotifications({...notifications, weather: e.target.checked})}
                  />
                  <div className="w-14 h-7 bg-[#eeeeed] peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[rgba(255,215,0,0.3)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-[#FFD700]"></div>
                </label>
              </div>
              <div className="flex items-center justify-between p-4 bg-[rgba(255,138,0,0.05)] rounded-xl border border-[rgba(255,138,0,0.2)]">
                <div>
                  <h3 className="text-sm font-semibold text-[#1a1c1c] font-['Plus_Jakarta_Sans']">Smart Cart Suggestions</h3>
                  <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">AI-powered shopping recommendations</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="sr-only peer" 
                    checked={notifications.smartCart}
                    onChange={(e) => setNotifications({...notifications, smartCart: e.target.checked})}
                  />
                  <div className="w-14 h-7 bg-[#eeeeed] peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[rgba(255,138,0,0.3)] rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-[#FF8A00]"></div>
                </label>
              </div>
            </div>
          </div>

          {/* Data Management */}
          <div className="dashboard-card stripe-stable">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-cyan text-3xl">database</span>
              <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Data Management</h2>
            </div>
            <div className="space-y-4">
              <button className="w-full text-left p-4 border-2 border-[#eeeeed] rounded-xl hover:border-[#00FFD1] transition-colors group">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold text-[#1a1c1c] font-['Plus_Jakarta_Sans'] group-hover:neon-text-cyan transition-colors">Export Data</h3>
                    <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">Download your inventory data as CSV</p>
                  </div>
                  <span className="material-symbols-outlined text-[#71717a] group-hover:neon-text-cyan transition-colors">download</span>
                </div>
              </button>
              <button className="w-full text-left p-4 border-2 border-[#eeeeed] rounded-xl hover:border-[#00FFD1] transition-colors group">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold text-[#1a1c1c] font-['Plus_Jakarta_Sans'] group-hover:neon-text-cyan transition-colors">Backup Data</h3>
                    <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">Create a backup of your inventory</p>
                  </div>
                  <span className="material-symbols-outlined text-[#71717a] group-hover:neon-text-cyan transition-colors">backup</span>
                </div>
              </button>
              <button className="w-full text-left p-4 border-2 border-[rgba(255,51,102,0.3)] rounded-xl hover:border-[#FF3366] transition-colors group bg-[rgba(255,51,102,0.05)]">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold text-[#ba1a1a] font-['Plus_Jakarta_Sans']">Clear All Data</h3>
                    <p className="text-sm text-[#ba1a1a]/70 font-['Plus_Jakarta_Sans'] mt-1">Permanently delete all inventory data</p>
                  </div>
                  <span className="material-symbols-outlined text-[#ba1a1a]">delete_forever</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </DashboardLayout>
  )
}