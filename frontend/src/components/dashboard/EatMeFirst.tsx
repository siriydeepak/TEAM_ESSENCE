import { getEatMeFirstProducts } from '../../data/mockData'

export default function EatMeFirst() {
  const expiringItems = getEatMeFirstProducts()

  if (expiringItems.length === 0) {
    return null
  }

  const getStatusColor = (daysLeft: number) => {
    if (daysLeft <= 0.5) return 'stripe-danger'
    if (daysLeft <= 1) return 'stripe-urgent'
    if (daysLeft <= 2) return 'stripe-warning'
    return 'stripe-stable'
  }

  const getUrgencyText = (daysLeft: number) => {
    if (daysLeft <= 0.5) return 'Expires Today!'
    if (daysLeft <= 1) return 'Expires Tomorrow'
    if (daysLeft <= 2) return 'Expires in 2 Days'
    return `${daysLeft} Days Left`
  }

  return (
    <div className="dashboard-card stripe-danger">
      <div className="flex items-center gap-3 mb-6">
        <span className="material-symbols-outlined text-[#FF3366] text-3xl">restaurant</span>
        <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">
          🔥 Eat Me First
        </h2>
        <span className="ml-auto bg-[rgba(255,51,102,0.1)] text-[#FF3366] px-3 py-1 rounded-full text-sm font-bold">
          {expiringItems.length} items
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {expiringItems.map((item) => (
          <div 
            key={item.id}
            className={`bg-white rounded-xl p-4 shadow-md ${getStatusColor(item.days_left)} border border-white/20 hover:scale-105 transition-transform`}
          >
            {/* Product Image */}
            <div className="w-full h-32 rounded-lg bg-[#eeeeed] overflow-hidden mb-3">
              {item.image ? (
                <img 
                  src={item.image} 
                  alt={item.name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <span className="material-symbols-outlined text-5xl text-[#a1a1aa]">
                    {item.category === 'Dairy' ? 'egg' : 
                     item.category === 'Produce' ? 'nutrition' : 
                     item.category === 'Meat' ? 'restaurant' :
                     item.category === 'Bakery' ? 'bakery_dining' :
                     'grocery'}
                  </span>
                </div>
              )}
            </div>

            {/* Product Info */}
            <h4 className="font-['Epilogue'] text-lg font-semibold text-[#1a1c1c] mb-1">
              {item.name}
            </h4>
            <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans'] mb-2">
              {item.quantity} {item.unit}
            </p>

            {/* Urgency Badge */}
            <div className="flex items-center justify-between">
              <span className={`text-xs font-bold font-['Space_Grotesk'] uppercase tracking-wider ${
                item.days_left <= 0.5 ? 'neon-text-pink' :
                item.days_left <= 1 ? 'neon-text-orange' :
                item.days_left <= 2 ? 'neon-text-yellow' :
                'neon-text-cyan'
              }`}>
                {getUrgencyText(item.days_left)}
              </span>
              <span className="material-symbols-outlined text-[#FF3366] text-xl">
                {item.days_left <= 1 ? 'priority_high' : 'schedule'}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </div>
  )
}
