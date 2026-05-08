// API Response Types
export interface ApiResponse<T = any> {
  data: T
  message?: string
  success: boolean
}

// Inventory Types
export interface InventoryItem {
  id: string
  name: string
  category: string
  quantity: number
  unit: string
  purchaseDate: string
  expiryDate: string
  daysLeft: number
  status: 'good' | 'warning' | 'critical' | 'expired'
  price?: number
  source: string
  createdAt: string
  updatedAt: string
}

export interface CreateInventoryItem {
  name: string
  category: string
  quantity: number
  unit: string
  shelfLifeDays: number
  price?: number
}

// Weather Types
export interface WeatherData {
  city: string
  temperature: number
  humidity: number
  description: string
  fluxPenalty: number
  alert: boolean
  adjustments: ShelfLifeAdjustment[]
}

export interface ShelfLifeAdjustment {
  itemId: string
  itemName: string
  originalDays: number
  adjustedDays: number
  reason: string
}

// Receipt Types
export interface ReceiptData {
  platform: string
  extractedItems: ExtractedItem[]
  collisionAlerts: string[]
  status: string
}

export interface ExtractedItem {
  name: string
  quantity: number
  unit: string
  price?: number
  category?: string
}

// Analytics Types
export interface AnalyticsData {
  wasteReduction: number
  moneySaved: number
  itemsTracked: number
  expirationTrends: ExpirationTrend[]
  categoryBreakdown: CategoryBreakdown[]
}

export interface ExpirationTrend {
  date: string
  expired: number
  expiringSoon: number
  fresh: number
}

export interface CategoryBreakdown {
  category: string
  count: number
  percentage: number
  value: number
}

// User Types
export interface User {
  id: string
  name: string
  email: string
  preferences: UserPreferences
}

export interface UserPreferences {
  notifications: {
    expirationAlerts: boolean
    weatherAlerts: boolean
  }
  theme: 'light' | 'dark' | 'system'
  language: string
}

// Form Types
export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  name: string
  email: string
  password: string
  confirmPassword: string
}

// Utility Types
export type Status = 'idle' | 'loading' | 'success' | 'error'

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}

export interface FilterOptions {
  category?: string
  status?: InventoryItem['status']
  search?: string
  sortBy?: 'name' | 'expiryDate' | 'createdAt'
  sortOrder?: 'asc' | 'desc'
}

// Error Types
export interface ApiError {
  message: string
  code?: string
  details?: Record<string, any>
}