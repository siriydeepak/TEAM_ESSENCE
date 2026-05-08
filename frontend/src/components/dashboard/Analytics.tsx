import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'

interface AnalyticsProps {
  data: {
    total_items: number
    expiring_soon: number
    expired: number
    healthy: number
    freshness_score: number
    total_waste_inr: number
    smart_cart_savings_inr: number
    waste_by_category?: Array<{ category: string; value: number; percentage: number }>
    weekly_efficiency?: Array<{ day: string; efficiency: number }>
    monthly_savings?: Array<{ month: string; savings: number }>
    category_distribution?: Array<{ name: string; value: number; color: string }>
  }
}

export default function Analytics({ data }: AnalyticsProps) {
  const stats = [
    {
      label: 'Total Items',
      value: data.total_items,
      icon: 'inventory_2',
      stripe: 'stripe-stable',
    },
    {
      label: 'Expiring Soon',
      value: data.expiring_soon,
      icon: 'warning',
      stripe: 'stripe-warning',
    },
    {
      label: 'Expired',
      value: data.expired,
      icon: 'dangerous',
      stripe: 'stripe-urgent',
    },
    {
      label: 'Healthy',
      value: data.healthy,
      icon: 'check_circle',
      stripe: 'stripe-stable',
    },
  ]

  // Custom label for pie chart
  const renderCustomLabel = (entry: any) => {
    return `${entry.name}: ${entry.value}`
  }

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.label} className={`dashboard-card ${stat.stripe}`}>
            <div className="flex items-center gap-3 mb-4">
              <span className="material-symbols-outlined text-[#006b57] text-3xl">
                {stat.icon}
              </span>
            </div>
            <p className="text-4xl font-['Epilogue'] font-bold text-[#1a1c1c] mb-1">{stat.value}</p>
            <p className="font-['Space_Grotesk'] text-[12px] font-normal text-[#3a4a44] uppercase tracking-wider">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Category Distribution Pie Chart */}
        {data.category_distribution && (
          <div className="dashboard-card stripe-stable">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-cyan text-3xl">pie_chart</span>
              <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Category Distribution</h3>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={data.category_distribution}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={renderCustomLabel}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {data.category_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Waste by Category */}
        {data.waste_by_category && (
          <div className="dashboard-card stripe-warning">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-yellow text-3xl">bar_chart</span>
              <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Waste by Category</h3>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.waste_by_category}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eeeeed" />
                <XAxis dataKey="category" stroke="#3a4a44" style={{ fontSize: '12px' }} />
                <YAxis stroke="#3a4a44" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.98)', 
                    border: '2px solid #FFD700',
                    borderRadius: '12px',
                    boxShadow: '0 0 20px rgba(255, 215, 0, 0.3)'
                  }}
                />
                <Bar dataKey="value" fill="#FFD700" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Weekly Efficiency & Monthly Savings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Weekly Efficiency Line Chart */}
        {data.weekly_efficiency && (
          <div className="dashboard-card stripe-stable">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-cyan text-3xl">trending_up</span>
              <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Weekly Efficiency</h3>
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={data.weekly_efficiency}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eeeeed" />
                <XAxis dataKey="day" stroke="#3a4a44" style={{ fontSize: '12px' }} />
                <YAxis stroke="#3a4a44" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.98)', 
                    border: '2px solid #00FFD1',
                    borderRadius: '12px',
                    boxShadow: '0 0 20px rgba(0, 255, 209, 0.3)'
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey="efficiency" 
                  stroke="#00FFD1" 
                  strokeWidth={3}
                  dot={{ fill: '#00FFD1', r: 5 }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Monthly Savings Bar Chart */}
        {data.monthly_savings && (
          <div className="dashboard-card stripe-stable">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined neon-text-orange text-3xl">savings</span>
              <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Monthly Savings (₹)</h3>
            </div>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={data.monthly_savings}>
                <CartesianGrid strokeDasharray="3 3" stroke="#eeeeed" />
                <XAxis dataKey="month" stroke="#3a4a44" style={{ fontSize: '12px' }} />
                <YAxis stroke="#3a4a44" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.98)', 
                    border: '2px solid #FF8A00',
                    borderRadius: '12px',
                    boxShadow: '0 0 20px rgba(255, 138, 0, 0.3)'
                  }}
                />
                <Bar dataKey="savings" fill="#FF8A00" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Freshness Score & Savings */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Freshness Score */}
        <div className="dashboard-card stripe-stable">
          <div className="flex items-center gap-3 mb-6">
            <span className="material-symbols-outlined text-[#006b57] text-3xl">analytics</span>
            <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Freshness Score</h3>
          </div>
          <div className="flex items-end gap-2 mb-4">
            <span className="text-5xl font-['Epilogue'] font-bold neon-text-cyan">{data.freshness_score}</span>
            <span className="text-2xl text-[#3a4a44] mb-2">/100</span>
          </div>
          <div className="bg-[#eeeeed] rounded-full h-4 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-[#00FFD1] to-[#006b57] h-full rounded-full transition-all duration-500 shadow-[0_0_20px_rgba(0,255,209,0.5)]"
              style={{ width: `${data.freshness_score}%` }}
            />
          </div>
          <p className="mt-4 text-sm text-[#3a4a44] font-['Plus_Jakarta_Sans']">
            Your kitchen efficiency is <span className="font-bold neon-text-cyan">
              {data.freshness_score >= 80 ? 'excellent' : data.freshness_score >= 60 ? 'good' : 'needs improvement'}
            </span>
          </p>
        </div>

        {/* Savings & Waste */}
        <div className="dashboard-card stripe-warning">
          <div className="flex items-center gap-3 mb-6">
            <span className="material-symbols-outlined text-[#ff8a00] text-3xl">payments</span>
            <h3 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Savings & Waste</h3>
          </div>
          <div className="space-y-4">
            <div className="p-4 bg-[rgba(0,255,209,0.1)] rounded-xl border-2 border-[#00FFD1] shadow-[0_0_15px_rgba(0,255,209,0.3)]">
              <p className="font-['Space_Grotesk'] text-[12px] font-normal text-[#006b57] uppercase tracking-wider mb-2">Smart Cart Savings</p>
              <p className="text-3xl font-['Epilogue'] font-bold neon-text-cyan">
                ₹{data.smart_cart_savings_inr.toFixed(2)}
              </p>
            </div>
            <div className="p-4 bg-[rgba(255,51,102,0.1)] rounded-xl border-2 border-[#FF3366] shadow-[0_0_15px_rgba(255,51,102,0.3)]">
              <p className="font-['Space_Grotesk'] text-[12px] font-normal text-[#ba1a1a] uppercase tracking-wider mb-2">Total Waste Value</p>
              <p className="text-3xl font-['Epilogue'] font-bold neon-text-pink">
                ₹{data.total_waste_inr.toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </div>
  )
}
