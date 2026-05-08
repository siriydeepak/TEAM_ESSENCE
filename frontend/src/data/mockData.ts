// Mock data for AetherShelf application

export interface Product {
  id: string
  name: string
  category: string
  quantity: number
  unit: string
  days_left: number
  status: 'critical' | 'urgent' | 'warning' | 'good' | 'optimal'
  price: number
  source: string
  image: string
  purchase_date: string
  expiry_date: string
}

export interface Recipe {
  id: string
  name: string
  image: string
  time: number
  difficulty: 'easy' | 'medium' | 'hard'
  ingredients_available: string[]
  ingredients_needed: string[]
  gap_cost: number
  description: string
  recipe_url: string
  source: string
}

// Mock Products with realistic data
export const mockProducts: Product[] = [
  {
    id: '1',
    name: 'Organic Whole Milk',
    category: 'Dairy',
    quantity: 1,
    unit: 'liter',
    days_left: 0.5,
    status: 'critical',
    price: 85,
    source: 'BigBasket',
    image: 'https://images.unsplash.com/photo-1550583724-b2692b85b150?w=400&h=400&fit=crop',
    purchase_date: '2026-05-06',
    expiry_date: '2026-05-09'
  },
  {
    id: '2',
    name: 'Fresh Strawberries',
    category: 'Produce',
    quantity: 250,
    unit: 'grams',
    days_left: 1,
    status: 'urgent',
    price: 120,
    source: 'Amazon Fresh',
    image: 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?w=400&h=400&fit=crop',
    purchase_date: '2026-05-07',
    expiry_date: '2026-05-09'
  },
  {
    id: '3',
    name: 'Vine Tomatoes',
    category: 'Produce',
    quantity: 500,
    unit: 'grams',
    days_left: 2,
    status: 'warning',
    price: 60,
    source: 'Local Market',
    image: 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=400&h=400&fit=crop',
    purchase_date: '2026-05-06',
    expiry_date: '2026-05-10'
  },
  {
    id: '4',
    name: 'Greek Yogurt',
    category: 'Dairy',
    quantity: 400,
    unit: 'grams',
    days_left: 3,
    status: 'warning',
    price: 95,
    source: 'BigBasket',
    image: 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400&h=400&fit=crop',
    purchase_date: '2026-05-05',
    expiry_date: '2026-05-11'
  },
  {
    id: '5',
    name: 'Hass Avocados',
    category: 'Produce',
    quantity: 4,
    unit: 'pieces',
    days_left: 4,
    status: 'good',
    price: 180,
    source: 'Amazon Fresh',
    image: 'https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?w=400&h=400&fit=crop',
    purchase_date: '2026-05-04',
    expiry_date: '2026-05-12'
  },
  {
    id: '6',
    name: 'Cheddar Cheese',
    category: 'Dairy',
    quantity: 200,
    unit: 'grams',
    days_left: 5,
    status: 'good',
    price: 150,
    source: 'BigBasket',
    image: 'https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400&h=400&fit=crop',
    purchase_date: '2026-05-03',
    expiry_date: '2026-05-13'
  },
  {
    id: '7',
    name: 'Baby Spinach',
    category: 'Produce',
    quantity: 200,
    unit: 'grams',
    days_left: 6,
    status: 'optimal',
    price: 45,
    source: 'Local Market',
    image: 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=400&h=400&fit=crop',
    purchase_date: '2026-05-02',
    expiry_date: '2026-05-14'
  },
  {
    id: '8',
    name: 'Organic Eggs',
    category: 'Dairy',
    quantity: 12,
    unit: 'pieces',
    days_left: 7,
    status: 'optimal',
    price: 110,
    source: 'Amazon Fresh',
    image: 'https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&h=400&fit=crop',
    purchase_date: '2026-05-01',
    expiry_date: '2026-05-15'
  },
  {
    id: '9',
    name: 'Fresh Blueberries',
    category: 'Produce',
    quantity: 150,
    unit: 'grams',
    days_left: 8,
    status: 'optimal',
    price: 200,
    source: 'BigBasket',
    image: 'https://images.unsplash.com/photo-1498557850523-fd3d118b962e?w=400&h=400&fit=crop',
    purchase_date: '2026-04-30',
    expiry_date: '2026-05-16'
  },
  {
    id: '10',
    name: 'Sourdough Bread',
    category: 'Bakery',
    quantity: 1,
    unit: 'loaf',
    days_left: 2,
    status: 'warning',
    price: 120,
    source: 'Local Bakery',
    image: 'https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=400&h=400&fit=crop',
    purchase_date: '2026-05-06',
    expiry_date: '2026-05-10'
  },
  {
    id: '11',
    name: 'Chicken Breast',
    category: 'Meat',
    quantity: 500,
    unit: 'grams',
    days_left: 1,
    status: 'urgent',
    price: 280,
    source: 'FreshToHome',
    image: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=400&h=400&fit=crop',
    purchase_date: '2026-05-07',
    expiry_date: '2026-05-09'
  },
  {
    id: '12',
    name: 'Bell Peppers',
    category: 'Produce',
    quantity: 3,
    unit: 'pieces',
    days_left: 5,
    status: 'good',
    price: 90,
    source: 'Local Market',
    image: 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=400&h=400&fit=crop',
    purchase_date: '2026-05-03',
    expiry_date: '2026-05-13'
  }
]

// Mock Recipes for Gap Finder
export const mockRecipes: Recipe[] = [
  {
    id: 'r1',
    name: 'Creamy Strawberry Smoothie Bowl',
    image: 'https://images.unsplash.com/photo-1590301157890-4810ed352733?w=600&h=400&fit=crop',
    time: 10,
    difficulty: 'easy',
    ingredients_available: ['Strawberries', 'Greek Yogurt', 'Blueberries'],
    ingredients_needed: ['Granola', 'Honey'],
    gap_cost: 85,
    description: 'A refreshing breakfast bowl perfect for using up expiring berries',
    recipe_url: 'https://www.allrecipes.com/recipe/238491/strawberry-smoothie-bowl/',
    source: 'AllRecipes'
  },
  {
    id: 'r2',
    name: 'Caprese Salad with Avocado',
    image: 'https://images.unsplash.com/photo-1592417817098-8fd3d9eb14a5?w=600&h=400&fit=crop',
    time: 15,
    difficulty: 'easy',
    ingredients_available: ['Tomatoes', 'Avocados'],
    ingredients_needed: ['Mozzarella', 'Basil', 'Balsamic'],
    gap_cost: 120,
    description: 'Fresh Italian salad using your ripe tomatoes and avocados',
    recipe_url: 'https://www.foodnetwork.com/recipes/ree-drummond/caprese-salad-recipe-1916250',
    source: 'Food Network'
  },
  {
    id: 'r3',
    name: 'Spinach & Cheese Omelette',
    image: 'https://images.unsplash.com/photo-1525351484163-7529414344d8?w=600&h=400&fit=crop',
    time: 12,
    difficulty: 'easy',
    ingredients_available: ['Eggs', 'Spinach', 'Cheddar Cheese'],
    ingredients_needed: ['Butter', 'Salt', 'Pepper'],
    gap_cost: 45,
    description: 'Protein-packed breakfast using fresh eggs and greens',
    recipe_url: 'https://www.bbcgoodfood.com/recipes/spinach-omelette',
    source: 'BBC Good Food'
  },
  {
    id: 'r4',
    name: 'Grilled Chicken & Pepper Stir-fry',
    image: 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=600&h=400&fit=crop',
    time: 25,
    difficulty: 'medium',
    ingredients_available: ['Chicken Breast', 'Bell Peppers', 'Spinach'],
    ingredients_needed: ['Soy Sauce', 'Garlic', 'Ginger', 'Rice'],
    gap_cost: 95,
    description: 'Quick stir-fry to use up chicken before it expires',
    recipe_url: 'https://www.delish.com/cooking/recipe-ideas/a26556220/chicken-stir-fry-recipe/',
    source: 'Delish'
  },
  {
    id: 'r5',
    name: 'Avocado Toast Supreme',
    image: 'https://images.unsplash.com/photo-1541519227354-08fa5d50c44d?w=600&h=400&fit=crop',
    time: 8,
    difficulty: 'easy',
    ingredients_available: ['Sourdough Bread', 'Avocados', 'Eggs'],
    ingredients_needed: ['Chili Flakes', 'Lemon'],
    gap_cost: 35,
    description: 'Classic brunch favorite with perfectly ripe avocados',
    recipe_url: 'https://www.loveandlemons.com/avocado-toast/',
    source: 'Love and Lemons'
  },
  {
    id: 'r6',
    name: 'Berry Yogurt Parfait',
    image: 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&h=400&fit=crop',
    time: 5,
    difficulty: 'easy',
    ingredients_available: ['Greek Yogurt', 'Strawberries', 'Blueberries'],
    ingredients_needed: ['Granola', 'Honey', 'Nuts'],
    gap_cost: 75,
    description: 'Healthy parfait using expiring dairy and berries',
    recipe_url: 'https://www.eatingwell.com/recipe/249879/berry-yogurt-parfait/',
    source: 'Eating Well'
  }
]

// Analytics Mock Data
export const mockAnalytics = {
  total_items: 12,
  expiring_soon: 4,
  expired: 0,
  healthy: 8,
  freshness_score: 78,
  total_waste_inr: 245.50,
  smart_cart_savings_inr: 432.00,
  waste_by_category: [
    { category: 'Dairy', value: 95, percentage: 38.7 },
    { category: 'Produce', value: 85, percentage: 34.6 },
    { category: 'Meat', value: 45, percentage: 18.3 },
    { category: 'Bakery', value: 20.5, percentage: 8.4 }
  ],
  weekly_efficiency: [
    { day: 'Mon', efficiency: 65 },
    { day: 'Tue', efficiency: 72 },
    { day: 'Wed', efficiency: 68 },
    { day: 'Thu', efficiency: 85 },
    { day: 'Fri', efficiency: 78 },
    { day: 'Sat', efficiency: 82 },
    { day: 'Sun', efficiency: 88 }
  ],
  monthly_savings: [
    { month: 'Jan', savings: 320 },
    { month: 'Feb', savings: 385 },
    { month: 'Mar', savings: 410 },
    { month: 'Apr', savings: 395 },
    { month: 'May', savings: 432 }
  ],
  category_distribution: [
    { name: 'Dairy', value: 4, color: '#00FFD1' },
    { name: 'Produce', value: 5, color: '#FFD700' },
    { name: 'Meat', value: 1, color: '#FF8A00' },
    { name: 'Bakery', value: 1, color: '#FF00E5' },
    { name: 'Other', value: 1, color: '#A1A1AA' }
  ]
}

// Expired Product Utilization Guides
export interface UtilizationGuide {
  id: string
  product_type: string
  category: string
  title: string
  description: string
  image: string
  guide_url: string
  source: string
  difficulty: 'easy' | 'medium' | 'hard'
  time_required: string
}

export const utilizationGuides: UtilizationGuide[] = [
  {
    id: 'u1',
    product_type: 'Milk',
    category: 'Dairy',
    title: 'Turn Expired Milk into Paneer',
    description: 'Transform sour milk into fresh homemade paneer (Indian cottage cheese) in just 30 minutes',
    image: 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600&h=400&fit=crop',
    guide_url: 'https://www.indianhealthyrecipes.com/paneer-recipe-homemade-paneer/',
    source: 'Indian Healthy Recipes',
    difficulty: 'easy',
    time_required: '30 minutes'
  },
  {
    id: 'u2',
    product_type: 'Milk',
    category: 'Dairy',
    title: 'Make Homemade Yogurt from Milk',
    description: 'Convert milk into probiotic-rich yogurt with this simple fermentation method',
    image: 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&h=400&fit=crop',
    guide_url: 'https://www.thekitchn.com/how-to-make-yogurt-at-home-cooking-lessons-from-the-kitchn-125070',
    source: 'The Kitchn',
    difficulty: 'easy',
    time_required: '8-12 hours'
  },
  {
    id: 'u3',
    product_type: 'Milk',
    category: 'Dairy',
    title: 'Homemade Butter from Cream',
    description: 'Churn expired cream or milk into fresh butter and buttermilk',
    image: 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?w=600&h=400&fit=crop',
    guide_url: 'https://www.theprairiehomestead.com/2011/04/how-to-make-butter.html',
    source: 'The Prairie Homestead',
    difficulty: 'easy',
    time_required: '15 minutes'
  },
  {
    id: 'u4',
    product_type: 'Milk',
    category: 'Dairy',
    title: 'Ricotta Cheese from Sour Milk',
    description: 'Create creamy ricotta cheese from milk that has gone sour',
    image: 'https://images.unsplash.com/photo-1452195100486-9cc805987862?w=600&h=400&fit=crop',
    guide_url: 'https://www.seriouseats.com/how-to-make-fresh-ricotta-cheese',
    source: 'Serious Eats',
    difficulty: 'medium',
    time_required: '45 minutes'
  },
  {
    id: 'u5',
    product_type: 'Vegetable Peels',
    category: 'Produce',
    title: 'Compost from Kitchen Scraps',
    description: 'Turn vegetable peels and scraps into nutrient-rich compost for your garden',
    image: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=600&h=400&fit=crop',
    guide_url: 'https://www.epa.gov/recycle/composting-home',
    source: 'EPA',
    difficulty: 'easy',
    time_required: '2-3 months'
  },
  {
    id: 'u6',
    product_type: 'Vegetable Peels',
    category: 'Produce',
    title: 'Vegetable Stock from Scraps',
    description: 'Make flavorful vegetable stock from peels, stems, and leftover vegetables',
    image: 'https://images.unsplash.com/photo-1547592166-23ac45744acd?w=600&h=400&fit=crop',
    guide_url: 'https://www.thekitchn.com/how-to-make-vegetable-stock-cooking-lessons-from-the-kitchn-93916',
    source: 'The Kitchn',
    difficulty: 'easy',
    time_required: '1-2 hours'
  },
  {
    id: 'u7',
    product_type: 'Bread',
    category: 'Bakery',
    title: 'Breadcrumbs from Stale Bread',
    description: 'Transform stale bread into crispy breadcrumbs for coating and toppings',
    image: 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&h=400&fit=crop',
    guide_url: 'https://www.simplyrecipes.com/recipes/how_to_make_bread_crumbs/',
    source: 'Simply Recipes',
    difficulty: 'easy',
    time_required: '20 minutes'
  },
  {
    id: 'u8',
    product_type: 'Bread',
    category: 'Bakery',
    title: 'Bread Pudding from Old Bread',
    description: 'Create a delicious dessert from stale or expired bread',
    image: 'https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=600&h=400&fit=crop',
    guide_url: 'https://www.allrecipes.com/recipe/7177/bread-pudding/',
    source: 'AllRecipes',
    difficulty: 'easy',
    time_required: '1 hour'
  },
  {
    id: 'u9',
    product_type: 'Bananas',
    category: 'Produce',
    title: 'Banana Bread from Overripe Bananas',
    description: 'Use brown, overripe bananas to make moist and delicious banana bread',
    image: 'https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?w=600&h=400&fit=crop',
    guide_url: 'https://www.simplyrecipes.com/recipes/banana_bread/',
    source: 'Simply Recipes',
    difficulty: 'easy',
    time_required: '1 hour 15 minutes'
  },
  {
    id: 'u10',
    product_type: 'Tomatoes',
    category: 'Produce',
    title: 'Tomato Sauce from Soft Tomatoes',
    description: 'Cook down soft, overripe tomatoes into rich pasta sauce',
    image: 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?w=600&h=400&fit=crop',
    guide_url: 'https://www.bonappetit.com/recipe/simple-tomato-sauce',
    source: 'Bon Appétit',
    difficulty: 'easy',
    time_required: '45 minutes'
  },
  {
    id: 'u11',
    product_type: 'Citrus Peels',
    category: 'Produce',
    title: 'Natural Cleaner from Citrus Peels',
    description: 'Make eco-friendly all-purpose cleaner from orange and lemon peels',
    image: 'https://images.unsplash.com/photo-1600948836101-f9ffda59d250?w=600&h=400&fit=crop',
    guide_url: 'https://www.treehugger.com/how-to-make-citrus-vinegar-cleaner-4858556',
    source: 'TreeHugger',
    difficulty: 'easy',
    time_required: '2 weeks (steeping)'
  },
  {
    id: 'u12',
    product_type: 'Coffee Grounds',
    category: 'Other',
    title: 'Garden Fertilizer from Coffee Grounds',
    description: 'Use spent coffee grounds as nitrogen-rich fertilizer for plants',
    image: 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=600&h=400&fit=crop',
    guide_url: 'https://www.gardeningknowhow.com/composting/ingredients/coffee-grounds-gardening.htm',
    source: 'Gardening Know How',
    difficulty: 'easy',
    time_required: '5 minutes'
  }
]

// Get utilization guides by product name
export const getUtilizationGuides = (productName: string): UtilizationGuide[] => {
  const productLower = productName.toLowerCase()
  
  // Map product names to guide types
  if (productLower.includes('milk')) {
    return utilizationGuides.filter(g => g.product_type === 'Milk')
  } else if (productLower.includes('bread')) {
    return utilizationGuides.filter(g => g.product_type === 'Bread')
  } else if (productLower.includes('banana')) {
    return utilizationGuides.filter(g => g.product_type === 'Bananas')
  } else if (productLower.includes('tomato')) {
    return utilizationGuides.filter(g => g.product_type === 'Tomatoes')
  } else if (productLower.includes('peel') || productLower.includes('vegetable') || productLower.includes('produce')) {
    return utilizationGuides.filter(g => g.product_type === 'Vegetable Peels')
  } else if (productLower.includes('citrus') || productLower.includes('orange') || productLower.includes('lemon')) {
    return utilizationGuides.filter(g => g.product_type === 'Citrus Peels')
  } else if (productLower.includes('coffee')) {
    return utilizationGuides.filter(g => g.product_type === 'Coffee Grounds')
  }
  
  // Return general composting guide for other produce
  return utilizationGuides.filter(g => g.product_type === 'Vegetable Peels')
}

// Get products by status
export const getProductsByStatus = (status: string) => {
  return mockProducts.filter(p => p.status === status)
}

// Get expiring products (critical + urgent + warning)
export const getExpiringProducts = () => {
  return mockProducts.filter(p => ['critical', 'urgent', 'warning'].includes(p.status))
    .sort((a, b) => a.days_left - b.days_left)
}

// Get products by category
export const getProductsByCategory = (category: string) => {
  return mockProducts.filter(p => p.category === category)
}

// Get "Eat Me First" products (expiring in 3 days or less)
export const getEatMeFirstProducts = () => {
  return mockProducts.filter(p => p.days_left <= 3)
    .sort((a, b) => a.days_left - b.days_left)
}

// Get recipe suggestions based on available ingredients
export const getRecipeSuggestions = () => {
  return mockRecipes.sort((a, b) => a.gap_cost - b.gap_cost)
}
