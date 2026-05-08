import React from 'react'
import { Link, useLocation } from 'react-router-dom'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()

  const navigation = [
    { name: 'Collision', href: '/dashboard', icon: 'auto_awesome_motion' },
    { name: 'Eat Me First', href: '/inventory', icon: 'restaurant' },
    { name: 'Expiry', href: '/analytics', icon: 'timer_off' },
    { name: 'Cart', href: '/settings', icon: 'shopping_cart' },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="min-h-screen">
      {/* Top AppBar */}
      <header className="fixed top-0 left-0 w-full z-50 bg-white/95 backdrop-blur-xl border-b border-zinc-200/50 shadow-sm">
        <div className="flex justify-between items-center w-full px-6 py-4">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-full overflow-hidden border border-zinc-100 shadow-sm">
              <div className="w-full h-full bg-gradient-to-br from-primary to-primary-container flex items-center justify-center">
                <span className="material-symbols-outlined text-white text-2xl">kitchen</span>
              </div>
            </div>
            <h1 className="font-brand-title text-brand-title flex items-baseline">
              <span className="text-primary">Aether</span>
              <span className="text-secondary-container">Shelf</span>
            </h1>
          </div>
          <div className="flex items-center gap-6">
            <button className="material-symbols-outlined text-zinc-500 hover:bg-zinc-100 transition-colors p-2 rounded-xl active:scale-95 duration-200">
              settings
            </button>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="pt-24 pb-32 px-margin-page max-w-container-max mx-auto relative z-10">
        {children}
      </main>

      {/* Bottom Navigation Bar */}
      <nav className="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-4 pb-6 pt-3 bg-white/98 backdrop-blur-xl border-t border-zinc-100 shadow-[0_-8px_30px_rgba(0,0,0,0.08)]">
        {navigation.map((item) => {
          const active = isActive(item.href)
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`flex flex-col items-center justify-center px-4 py-2 transition-all active:scale-90 duration-150 ${
                active
                  ? 'bg-gradient-to-b from-[#121414] to-[#1E2222] text-neon-cyan rounded-xl ring-1 ring-neon-cyan shadow-neon-cyan'
                  : 'text-zinc-400 hover:text-primary'
              }`}
            >
              <span className={`material-symbols-outlined ${active ? 'font-variation-settings-fill' : ''}`}>
                {item.icon}
              </span>
              <span className="font-['Epilogue'] text-[10px] font-bold uppercase tracking-widest mt-1">
                {item.name}
              </span>
            </Link>
          )
        })}
      </nav>

      {/* Floating Action Button */}
      <button className="fixed bottom-28 right-8 w-14 h-14 rounded-full dark-gradient text-neon-cyan flex items-center justify-center neon-border-cyan shadow-xl active:scale-90 transition-transform z-40">
        <span className="material-symbols-outlined text-3xl">add</span>
      </button>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </div>
  )
}

export default Layout