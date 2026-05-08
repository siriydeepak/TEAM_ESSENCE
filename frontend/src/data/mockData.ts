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
    description: 'A refreshing breakfast bowl perfect for using up expiring berries'
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
    description: 'Fresh Italian salad using your ripe tomatoes and avocados'
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
    description: 'Protein-packed breakfast using fresh eggs and greens'
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
    description: 'Quick stir-fry to use up chicken before it expires'
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
    description: 'Classic brunch favorite with perfectly ripe avocados'
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
    description: 'Healthy parfait using expiring dairy and berries'
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
