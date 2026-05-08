import { getRecipeSuggestions } from '../../data/mockData'
import { useCart } from '../../context/CartContext'

export default function SmartCart() {
  // Use mock recipe data for smart cart suggestions
  const recipes = getRecipeSuggestions().slice(0, 3)
  const { addToCart } = useCart()

  const handleAddToCart = (recipe: any) => {
    // Add each missing ingredient to cart
    recipe.ingredients_needed.forEach((ingredient: string) => {
      addToCart({
        id: `${recipe.id}-${ingredient.toLowerCase().replace(/\s+/g, '-')}`,
        name: ingredient,
        quantity: 1,
        unit: 'unit',
        price: recipe.gap_cost / recipe.ingredients_needed.length,
        source: 'Smart Cart',
        recipe_name: recipe.name
      })
    })
  }

  return (
    <div className="dashboard-card stripe-stable">
      <div className="flex items-center gap-3 mb-6">
        <span className="material-symbols-outlined neon-text-orange text-3xl">shopping_cart</span>
        <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Smart Cart</h2>
      </div>

      <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mb-4">
        AI-powered shopping suggestions based on your consumption patterns
      </p>

      {recipes.length === 0 ? (
        <div className="text-center py-8">
          <span className="material-symbols-outlined text-5xl text-[#a1a1aa] mb-3">shopping_cart</span>
          <p className="text-[#71717a] text-sm font-['Plus_Jakarta_Sans']">No items in cart</p>
        </div>
      ) : (
        <div className="space-y-3">
          {recipes.map((recipe) => (
            <div key={recipe.id} className="bg-[rgba(0,255,209,0.05)] rounded-xl p-4 border border-[rgba(0,255,209,0.2)] hover:border-[#00FFD1] hover:shadow-[0_0_15px_rgba(0,255,209,0.2)] transition-all">
              <div className="flex items-start gap-3 mb-3">
                <div className="w-12 h-12 rounded-lg overflow-hidden shrink-0">
                  <img 
                    src={recipe.image} 
                    alt={recipe.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-['Plus_Jakarta_Sans'] text-sm font-semibold text-[#1a1c1c] mb-1">
                    {recipe.name}
                  </h3>
                  <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans'] mb-2">
                    Missing: {recipe.ingredients_needed.join(', ')}
                  </p>
                  <div className="flex items-center gap-2">
                    <span className="text-xs bg-[rgba(255,138,0,0.1)] text-[#ff8a00] px-2 py-1 rounded-full font-bold">
                      ₹{recipe.gap_cost}
                    </span>
                    <span className="text-xs text-[#71717a]">⏱ {recipe.time} min</span>
                  </div>
                </div>
              </div>

              <div className="flex gap-2">
                <a
                  href={recipe.recipe_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 text-center px-3 py-2 bg-white border-2 border-[#00FFD1] text-[#006b57] rounded-lg text-xs font-semibold hover:bg-[#00FFD1] hover:text-white transition-all flex items-center justify-center gap-1"
                >
                  <span className="material-symbols-outlined text-sm">restaurant_menu</span>
                  Recipe
                </a>
                <button 
                  onClick={() => handleAddToCart(recipe)}
                  className="flex-1 text-center px-3 py-2 dark-gradient neon-border-orange text-white rounded-lg text-xs font-semibold transition-all active:scale-95 flex items-center justify-center gap-1"
                >
                  <span className="material-symbols-outlined text-sm">add_shopping_cart</span>
                  Add (₹{recipe.gap_cost})
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-4 p-3 bg-[rgba(0,255,209,0.05)] rounded-xl border border-[rgba(0,255,209,0.2)]">
        <div className="flex items-center justify-between">
          <span className="text-sm font-['Plus_Jakarta_Sans'] font-semibold text-[#1a1c1c]">
            Potential Savings
          </span>
          <span className="text-lg font-['Epilogue'] font-bold neon-text-cyan">
            ₹{recipes.reduce((sum, r) => sum + r.gap_cost, 0)}
          </span>
        </div>
        <p className="text-xs text-[#71717a] font-['Plus_Jakarta_Sans'] mt-1">
          Complete these recipes with minimal shopping
        </p>
      </div>

      {/* Material Symbols Font */}
      <link
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap"
        rel="stylesheet"
      />
    </div>
  )
}
