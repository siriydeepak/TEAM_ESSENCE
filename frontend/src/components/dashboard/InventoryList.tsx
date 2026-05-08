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
  image?: string
  expiry_date?: string
}

interface InventoryListProps {
  items: InventoryItem[]
  loading: boolean
}

export default function InventoryList({ items, loading }: InventoryListProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'expired':
      case 'urgent':
      case 'critical':
        return 'stripe-urgent'
      case 'warning':
        return 'stripe-warning'
      default:
        return 'stripe-stable'
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'expired':
      case 'urgent':
      case 'critical':
        return 'bg-[rgba(186,26,26,0.1)] text-[#ba1a1a] border border-[rgba(186,26,26,0.2)]'
      case 'warning':
        return 'bg-[rgba(255,138,0,0.1)] text-[#ff8a00] border border-[rgba(255,138,0,0.2)]'
      default:
        return 'bg-[rgba(0,255,209,0.1)] text-[#006b57] border border-[rgba(0,255,209,0.2)]'
    }
  }

  const getProgressColor = (status: string) => {
    switch (status) {
      case 'expired':
      case 'urgent':
      case 'critical':
        return 'bg-[#ba1a1a]'
      case 'warning':
        return 'bg-[#ff8a00]'
      default:
        return 'bg-[#00ffd1]'
    }
  }

  if (loading) {
    return (
      <div className="dashboard-card">
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-20 bg-surface-container rounded-lg"></div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Upcoming Expiries</h3>
        <button className="dark-gradient text-white px-4 py-2 rounded-xl flex items-center gap-2 neon-border-cyan active:scale-95 transition-transform">
          <span className="material-symbols-outlined text-sm">sort</span>
          <span className="font-['Space_Grotesk'] text-[10px] font-bold tracking-wider">TIME REMAINING</span>
        </button>
      </div>

      <div className="space-y-6">
        {items.length === 0 ? (
          <div className="dashboard-card text-center py-12">
            <span className="material-symbols-outlined text-[64px] text-zinc-300 mb-4">inventory_2</span>
            <p className="text-on-surface-variant font-['Plus_Jakarta_Sans']">No items in inventory</p>
            <p className="text-sm text-on-surface-variant/70 mt-2">
              Connect your Gmail to automatically track purchases
            </p>
          </div>
        ) : (
          items.map((item) => (
            <div 
              key={item.id} 
              className={`bg-white rounded-2xl p-6 flex items-center gap-6 shadow-[0px_20px_25px_-5px_rgba(0,0,0,0.1),0px_8px_10px_-6px_rgba(0,0,0,0.1)] ${getStatusColor(item.status)} relative overflow-hidden group transition-transform hover:scale-[1.01]`}
            >
              {/* Product Image */}
              <div className="w-16 h-16 rounded-lg bg-[#eeeeed] overflow-hidden shrink-0">
                {item.image ? (
                  <img 
                    src={item.image} 
                    alt={item.name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      // Fallback to icon if image fails to load
                      e.currentTarget.style.display = 'none'
                      e.currentTarget.nextElementSibling?.classList.remove('hidden')
                    }}
                  />
                ) : null}
                <div className={`w-full h-full flex items-center justify-center ${item.image ? 'hidden' : ''}`}>
                  <span className="material-symbols-outlined text-4xl text-[#a1a1aa]">
                    {item.category === 'Dairy' ? 'egg' : 
                     item.category === 'Produce' ? 'nutrition' : 
                     item.category === 'Meat' ? 'restaurant' :
                     item.category === 'Bakery' ? 'bakery_dining' :
                     'grocery'}
                  </span>
                </div>
              </div>

              {/* Content */}
              <div className="flex-grow">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-['Epilogue'] text-xl font-normal text-[#1a1c1c]">{item.name}</h4>
                    <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">
                      {item.quantity} {item.unit} • {item.category}
                    </p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-[10px] font-['Plus_Jakarta_Sans'] font-bold uppercase tracking-wider ${getStatusBadge(item.status)}`}>
                    {item.status}
                  </span>
                </div>

                {/* Progress Bar */}
                <div className="flex items-center gap-4 mb-2">
                  <div className="flex-grow h-2 bg-[#eeeeed] rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${getProgressColor(item.status)}`}
                      style={{ width: `${Math.max(0, Math.min(100, (item.days_left / 7) * 100))}%` }}
                    ></div>
                  </div>
                  <span className={`font-['Space_Grotesk'] text-[10px] font-normal shrink-0 ${
                    item.days_left < 0 ? 'text-[#ba1a1a]' :
                    item.days_left <= 2 ? 'text-[#ff8a00]' :
                    'text-[#006b57]'
                  }`}>
                    {item.days_left < 0 
                      ? `Expired ${Math.abs(item.days_left)}d ago`
                      : `${item.days_left} Days Left`
                    }
                  </span>
                </div>
              </div>

              {/* More Button */}
              <button className="material-symbols-outlined text-[#a1a1aa] hover:text-primary transition-colors">
                more_vert
              </button>
            </div>
          ))
        )}
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </div>
  )
}
