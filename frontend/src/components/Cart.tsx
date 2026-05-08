import { useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'

export default function Cart() {
  const { getItemCount } = useCart()
  const navigate = useNavigate()

  if (getItemCount() === 0) return null

  const handleOpenCart = () => {
    navigate('/cart')
  }

  return (
    <>
      {/* Floating Cart Button */}
      <button
        onClick={handleOpenCart}
        className="fixed bottom-24 md:bottom-8 right-8 z-50 dark-gradient neon-border-cyan text-white p-4 rounded-full shadow-2xl hover:shadow-[0_0_30px_rgba(0,255,209,0.6)] transition-all active:scale-95 flex items-center gap-2"
      >
        <span className="material-symbols-outlined text-2xl">shopping_cart</span>
        <span className="bg-[#FF00E5] text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center absolute -top-2 -right-2">
          {getItemCount()}
        </span>
      </button>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </>
  )
}
