import { ReactNode } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import toast from 'react-hot-toast'
import Cart from '../Cart'

interface DashboardLayoutProps {
  children: ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userEmail')
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const navigation = [
    { name: 'Product Info', href: '/dashboard', icon: 'inventory_2' },
    { name: 'Smart Restock', href: '/settings', icon: 'shopping_cart' },
    { name: 'Expiry Logs', href: '/inventory', icon: 'schedule' },
    { name: 'Analytics', href: '/analytics', icon: 'analytics' },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="min-h-screen relative">
      {/* Top AppBar - Lighter style */}
      <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-white/95 border-b border-[#e4e4e7] shadow-lg">
        <div className="px-6 py-4 max-w-[1280px] mx-auto">
          {/* Top Row: Logo and Actions */}
          <div className="flex items-center justify-between mb-4">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <img 
                src="/assets/logo.png" 
                alt="AetherShelf Logo" 
                className="h-12 w-12 object-contain"
              />
              <h1 className="text-3xl md:text-4xl font-['Dancing_Script'] font-bold">
                <span className="text-[#006b57]">Aether</span>
                <span className="text-[#ff8a00]">Shelf</span>
              </h1>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-3">
              {location.pathname !== '/dashboard' && (
                <button
                  onClick={() => navigate('/dashboard')}
                  className="px-4 py-2 text-sm font-['Plus_Jakarta_Sans'] font-semibold text-[#006b57] hover:text-[#00ffd1] transition-colors flex items-center gap-2"
                >
                  <span className="material-symbols-outlined text-lg">home</span>
                  <span className="hidden md:inline">Home</span>
                </button>
              )}
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-['Plus_Jakarta_Sans'] font-semibold text-[#71717a] hover:text-[#006b57] transition-colors"
              >
                Logout
              </button>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex gap-2 overflow-x-auto no-scrollbar">
            {navigation.map((item) => {
              const active = isActive(item.href)
              return (
                <button
                  key={item.name}
                  onClick={() => navigate(item.href)}
                  className={`px-6 py-3 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all flex items-center gap-2 whitespace-nowrap ${
                    active
                      ? 'bg-gradient-to-r from-[#006b57] to-[#00ffd1] text-white shadow-lg scale-105'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <span className="material-symbols-outlined text-lg">{item.icon}</span>
                  {item.name}
                </button>
              )
            })}
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="pt-40 pb-8 px-6 max-w-[1280px] mx-auto relative z-10">
        <div className="bg-white shadow-2xl rounded-2xl overflow-hidden min-h-[calc(100vh-200px)]">
          <div className="p-6">
            {children}
          </div>
        </div>
      </main>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-50 backdrop-blur-xl bg-white/95 border-t border-[#e4e4e7] shadow-2xl">
        <div className="grid grid-cols-4 max-w-[1280px] mx-auto">
          {navigation.map((item) => {
            const active = isActive(item.href)
            return (
              <button
                key={item.name}
                onClick={() => navigate(item.href)}
                className={`flex flex-col items-center justify-center py-3 px-2 transition-all ${
                  active
                    ? 'text-[#00ffd1] bg-gradient-to-b from-[#006b57]/10 to-transparent'
                    : 'text-gray-500'
                }`}
              >
                <span className={`material-symbols-outlined mb-1 ${active ? 'scale-110' : ''}`}>
                  {item.icon}
                </span>
                <span className={`text-xs font-['Plus_Jakarta_Sans'] font-semibold ${
                  active ? 'text-[#006b57]' : ''
                }`}>
                  {item.name.split(' ')[0]}
                </span>
              </button>
            )
          })}
        </div>
      </nav>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />

      {/* Shopping Cart */}
      <Cart />
    </div>
  )
}
