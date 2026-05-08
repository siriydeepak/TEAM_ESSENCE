import { getRecipeSuggestions } from '../../data/mockData'
import { useCart } from '../../context/CartContext'

export default function GapFinder() {
  const recipes = getRecipeSuggestions()
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
        source: 'Smart Suggestion',
        recipe_name: recipe.name
      })
    })
  }

  return (
    <div className="dashboard-card stripe-stable">
      <div className="flex items-center gap-3 mb-6">
        <span className="material-symbols-outlined neon-text-yellow text-3xl">lightbulb</span>
        <h2 className="font-['Epilogue'] text-2xl font-semibold text-[#1a1c1c]">Recipe Suggestions</h2>
      </div>

      <div className="space-y-4 max-h-[600px] overflow-y-auto no-scrollbar">
        {recipes.length === 0 ? (
          <div className="text-center py-8">
            <span className="material-symbols-outlined text-5xl text-[#a1a1aa] mb-3">restaurant</span>
            <p className="text-[#71717a] text-sm font-['Plus_Jakarta_Sans']">No recipe suggestions available</p>
          </div>
        ) : (
          recipes.map((recipe) => (
            <div 
              key={recipe.id}
              className="bg-white rounded-xl overflow-hidden shadow-md border-l-4 border-[#FFD700] hover:shadow-xl transition-all hover:scale-[1.02]"
            >
              {/* Recipe Image */}
              <div className="w-full h-40 bg-[#eeeeed] overflow-hidden">
                <img 
                  src={recipe.image} 
                  alt={recipe.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.currentTarget.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&h=400&fit=crop'
                  }}
                />
              </div>

              {/* Recipe Info */}
              <div className="p-4">
                <h3 className="font-['Epilogue'] text-lg font-semibold text-[#1a1c1c] mb-2">
                  {recipe.name}
                </h3>
                <p className="text-sm text-[#71717a] font-['Plus_Jakarta_Sans'] mb-3">
                  {recipe.description}
                </p>

                {/* Recipe Meta */}
                <div className="flex items-center gap-3 mb-3 flex-wrap">
                  <span className="flex items-center gap-1 text-xs text-[#3a4a44] font-['Plus_Jakarta_Sans']">
                    <span className="material-symbols-outlined text-sm">schedule</span>
                    {recipe.time} min
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                    recipe.difficulty === 'easy' ? 'bg-[rgba(0,255,209,0.1)] text-[#006b57]' :
                    recipe.difficulty === 'medium' ? 'bg-[rgba(255,215,0,0.1)] text-[#ff8a00]' :
                    'bg-[rgba(255,51,102,0.1)] text-[#ba1a1a]'
                  }`}>
                    {recipe.difficulty}
                  </span>
                  <span className="flex items-center gap-1 text-xs font-bold neon-text-orange">
                    <span className="material-symbols-outlined text-sm">shopping_cart</span>
                    ₹{recipe.gap_cost}
                  </span>
                </div>

                {/* Available Ingredients */}
                <div className="mb-3">
                  <p className="text-xs font-semibold text-[#006b57] mb-2 font-['Space_Grotesk'] uppercase tracking-wider">
                    ✓ You Have:
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {recipe.ingredients_available.map((ingredient, idx) => (
                      <span 
                        key={idx}
                        className="text-xs bg-[rgba(0,255,209,0.1)] text-[#006b57] px-2 py-1 rounded-full border border-[rgba(0,255,209,0.3)]"
                      >
                        {ingredient}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Missing Ingredients */}
                <div>
                  <p className="text-xs font-semibold text-[#ff8a00] mb-2 font-['Space_Grotesk'] uppercase tracking-wider">
                    Missing:
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {recipe.ingredients_needed.map((ingredient, idx) => (
                      <span 
                        key={idx}
                        className="text-xs bg-[rgba(255,138,0,0.1)] text-[#ff8a00] px-2 py-1 rounded-full border border-[rgba(255,138,0,0.3)]"
                      >
                        {ingredient}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-2">
                  <a
                    href={recipe.recipe_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 dark-gradient neon-border-cyan text-white px-4 py-2 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all active:scale-95 flex items-center justify-center gap-2 hover:shadow-[0_0_25px_rgba(0,255,209,0.5)]"
                  >
                    <span className="material-symbols-outlined text-lg">restaurant_menu</span>
                    View Recipe
                  </a>
                  <button 
                    onClick={() => handleAddToCart(recipe)}
                    className="flex-1 dark-gradient neon-border-orange text-white px-4 py-2 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all active:scale-95 flex items-center justify-center gap-2 hover:shadow-[0_0_25px_rgba(255,138,0,0.5)]"
                  >
                    <span className="material-symbols-outlined text-lg">add_shopping_cart</span>
                    Add Items (₹{recipe.gap_cost})
                  </button>
                </div>
                
                {/* Recipe Source */}
                <p className="text-xs text-[#71717a] text-center font-['Plus_Jakarta_Sans'] mt-2">
                  Recipe from <span className="font-semibold">{recipe.source}</span>
                </p>
              </div>
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
