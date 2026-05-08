import { createContext, useContext, useState, ReactNode } from 'react'
import toast from 'react-hot-toast'

interface CartItem {
  id: string
  name: string
  quantity: number
  unit: string
  price: number
  source: string
  recipe_name?: string
}

interface CartContextType {
  items: CartItem[]
  addToCart: (item: CartItem) => void
  removeFromCart: (id: string) => void
  clearCart: () => void
  getTotalCost: () => number
  getItemCount: () => number
}

const CartContext = createContext<CartContextType | undefined>(undefined)

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([])

  const addToCart = (item: CartItem) => {
    setItems((prevItems) => {
      // Check if item already exists
      const existingItem = prevItems.find((i) => i.id === item.id)
      
      if (existingItem) {
        // Update quantity if item exists
        toast.success(`Updated ${item.name} quantity in cart`)
        return prevItems.map((i) =>
          i.id === item.id
            ? { ...i, quantity: i.quantity + item.quantity }
            : i
        )
      } else {
        // Add new item
        toast.success(`Added ${item.name} to cart`)
        return [...prevItems, item]
      }
    })
  }

  const removeFromCart = (id: string) => {
    setItems((prevItems) => {
      const item = prevItems.find((i) => i.id === id)
      if (item) {
        toast.success(`Removed ${item.name} from cart`)
      }
      return prevItems.filter((i) => i.id !== id)
    })
  }

  const clearCart = () => {
    setItems([])
    toast.success('Cart cleared')
  }

  const getTotalCost = () => {
    return items.reduce((total, item) => total + item.price * item.quantity, 0)
  }

  const getItemCount = () => {
    return items.reduce((count, item) => count + item.quantity, 0)
  }

  return (
    <CartContext.Provider
      value={{
        items,
        addToCart,
        removeFromCart,
        clearCart,
        getTotalCost,
        getItemCount,
      }}
    >
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}
