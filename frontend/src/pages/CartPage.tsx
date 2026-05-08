import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import DashboardLayout from '../components/layout/DashboardLayout'
import { useCart } from '../context/CartContext'

export default function CartPage() {
  const navigate = useNavigate()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const { items, removeFromCart, clearCart, getTotalCost, getItemCount } = useCart()

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

  const handleCheckout = () => {
    // Prepare order data
    const orderData = {
      items: items,
      total: getTotalCost(),
      timestamp: new Date().toISOString(),
    }
    
    console.log('Processing order:', orderData)
    
    // Here you can integrate with payment gateway or e-commerce API
    // For now, we'll show a success message
    alert(`Order placed successfully!\nTotal: ₹${getTotalCost().toFixed(2)}\nItems: ${getItemCount()}`)
    clearCart()
    navigate('/dashboard')
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="font-['Epilogue'] text-4xl font-bold text-[#1a1c1c] mb-2">
              Shopping Cart
            </h1>
            <p className="text-[#71717a] font-['Plus_Jakarta_Sans']">
              {getItemCount()} {getItemCount() === 1 ? 'item' : 'items'} ready for checkout
            </p>
          </div>
          {items.length > 0 && (
            <button
              onClick={clearCart}
              className="px-6 py-3 bg-white border-2 border-[#ba1a1a] text-[#ba1a1a] rounded-xl font-['Plus_Jakarta_Sans'] font-semibold transition-all active:scale-95 hover:bg-[#ba1a1a] hover:text-white flex items-center gap-2"
            >
              <span className="material-symbols-outlined">delete_sweep</span>
              Clear Cart
            </button>
          )}
        </div>

        {items.length === 0 ? (
          /* Empty Cart State */
          <div className="dashboard-card stripe-stable text-center py-16">
            <span className="material-symbols-outlined text-[120px] text-[#a1a1aa] mb-6">shopping_cart</span>
            <h2 className="font-['Epilogue'] text-3xl font-bold text-[#1a1c1c] mb-3">
              Your cart is empty
            </h2>
            <p className="text-[#71717a] font-['Plus_Jakarta_Sans'] mb-6 max-w-md mx-auto">
              Add items from recipe suggestions to start shopping
            </p>
            <button
              onClick={() => navigate('/dashboard')}
              className="dark-gradient neon-border-cyan text-white px-8 py-4 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold transition-all active:scale-95 hover:shadow-[0_0_30px_rgba(0,255,209,0.5)] inline-flex items-center gap-2"
            >
              <span className="material-symbols-outlined">arrow_back</span>
              Browse Recipes
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Cart Items - 2 columns */}
            <div className="lg:col-span-2 space-y-4">
              <div className="dashboard-card stripe-stable">
                <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c] mb-6 flex items-center gap-3">
                  <span className="material-symbols-outlined neon-text-cyan text-3xl">inventory_2</span>
                  Cart Items
                </h2>

                <div className="space-y-4">
                  {items.map((item) => (
                    <div
                      key={item.id}
                      className="bg-[rgba(0,255,209,0.05)] rounded-xl p-6 border-2 border-[rgba(0,255,209,0.2)] hover:border-[#00FFD1] hover:shadow-[0_0_20px_rgba(0,255,209,0.2)] transition-all"
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <h3 className="font-['Epilogue'] text-xl font-semibold text-[#1a1c1c] mb-2">
                            {item.name}
                          </h3>
                          {item.recipe_name && (
                            <div className="flex items-center gap-2 mb-2">
                              <span className="material-symbols-outlined text-sm text-[#ff8a00]">restaurant_menu</span>
                              <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans']">
                                For: <span className="font-semibold text-[#1a1c1c]">{item.recipe_name}</span>
                              </p>
                            </div>
                          )}
                          <div className="flex items-center gap-4 text-sm text-[#71717a] font-['Plus_Jakarta_Sans']">
                            <span className="flex items-center gap-1">
                              <span className="material-symbols-outlined text-sm">inventory</span>
                              {item.quantity} {item.unit}
                            </span>
                            <span className="flex items-center gap-1">
                              <span className="material-symbols-outlined text-sm">store</span>
                              {item.source}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={() => removeFromCart(item.id)}
                          className="material-symbols-outlined text-[#ba1a1a] hover:scale-110 hover:text-[#FF3366] transition-all text-3xl"
                          title="Remove item"
                        >
                          delete
                        </button>
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t-2 border-[rgba(0,255,209,0.2)]">
                        <span className="font-['Space_Grotesk'] text-sm font-bold uppercase tracking-wider text-[#71717a]">
                          Item Price
                        </span>
                        <span className="font-['Epilogue'] text-2xl font-bold neon-text-cyan">
                          ₹{(item.price * item.quantity).toFixed(2)}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Order Summary - 1 column */}
            <div className="lg:col-span-1">
              <div className="dashboard-card stripe-warning sticky top-44">
                <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c] mb-6 flex items-center gap-3">
                  <span className="material-symbols-outlined neon-text-yellow text-3xl">receipt_long</span>
                  Order Summary
                </h2>

                <div className="space-y-4 mb-6">
                  <div className="flex items-center justify-between py-3 border-b border-[#eeeeed]">
                    <span className="text-[#71717a] font-['Plus_Jakarta_Sans']">Subtotal</span>
                    <span className="font-['Epilogue'] text-lg font-semibold text-[#1a1c1c]">
                      ₹{getTotalCost().toFixed(2)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b border-[#eeeeed]">
                    <span className="text-[#71717a] font-['Plus_Jakarta_Sans']">Delivery Fee</span>
                    <span className="font-['Epilogue'] text-lg font-semibold text-[#00ffd1]">
                      FREE
                    </span>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b border-[#eeeeed]">
                    <span className="text-[#71717a] font-['Plus_Jakarta_Sans']">Tax (5%)</span>
                    <span className="font-['Epilogue'] text-lg font-semibold text-[#1a1c1c]">
                      ₹{(getTotalCost() * 0.05).toFixed(2)}
                    </span>
                  </div>
                </div>

                {/* Total */}
                <div className="bg-gradient-to-r from-[rgba(0,255,209,0.1)] to-[rgba(0,107,87,0.1)] rounded-xl p-6 border-2 border-[#00FFD1] shadow-[0_0_20px_rgba(0,255,209,0.3)] mb-6">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-['Space_Grotesk'] text-sm font-bold uppercase tracking-wider text-[#006b57]">
                      Total Amount
                    </span>
                    <span className="font-['Epilogue'] text-4xl font-bold neon-text-cyan">
                      ₹{(getTotalCost() * 1.05).toFixed(2)}
                    </span>
                  </div>
                  <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans']">
                    Including all taxes and fees
                  </p>
                </div>

                {/* Checkout Button */}
                <button
                  onClick={handleCheckout}
                  className="w-full dark-gradient neon-border-cyan text-white px-6 py-4 rounded-xl font-['Plus_Jakarta_Sans'] font-bold text-lg transition-all active:scale-95 hover:shadow-[0_0_30px_rgba(0,255,209,0.6)] flex items-center justify-center gap-3 mb-4"
                >
                  <span className="material-symbols-outlined text-2xl">shopping_bag</span>
                  Proceed to Checkout
                </button>

                <button
                  onClick={() => navigate('/dashboard')}
                  className="w-full px-6 py-3 bg-white border-2 border-[#eeeeed] text-[#71717a] rounded-xl font-['Plus_Jakarta_Sans'] font-semibold transition-all active:scale-95 hover:border-[#00FFD1] hover:text-[#006b57] flex items-center justify-center gap-2"
                >
                  <span className="material-symbols-outlined">arrow_back</span>
                  Continue Shopping
                </button>

                {/* Savings Info */}
                <div className="mt-6 p-4 bg-[rgba(255,215,0,0.05)] rounded-xl border border-[rgba(255,215,0,0.2)]">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="material-symbols-outlined neon-text-yellow text-xl">savings</span>
                    <span className="font-['Plus_Jakarta_Sans'] text-sm font-semibold text-[#1a1c1c]">
                      Smart Shopping
                    </span>
                  </div>
                  <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans']">
                    You're buying exactly what you need for your recipes, reducing waste and saving money!
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </DashboardLayout>
  )
}
