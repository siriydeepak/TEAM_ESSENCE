import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { format, formatDistanceToNow, isAfter, isBefore, parseISO } from 'date-fns'

// Utility function to merge Tailwind classes
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Date utilities
export const dateUtils = {
  format: (date: string | Date, formatStr: string = 'MMM dd, yyyy') => {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return format(dateObj, formatStr)
  },

  formatRelative: (date: string | Date) => {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    return formatDistanceToNow(dateObj, { addSuffix: true })
  },

  isExpired: (expiryDate: string | Date) => {
    const dateObj = typeof expiryDate === 'string' ? parseISO(expiryDate) : expiryDate
    return isBefore(dateObj, new Date())
  },

  isExpiringSoon: (expiryDate: string | Date, daysThreshold: number = 3) => {
    const dateObj = typeof expiryDate === 'string' ? parseISO(expiryDate) : expiryDate
    const thresholdDate = new Date()
    thresholdDate.setDate(thresholdDate.getDate() + daysThreshold)
    return isBefore(dateObj, thresholdDate) && isAfter(dateObj, new Date())
  },

  getDaysUntilExpiry: (expiryDate: string | Date) => {
    const dateObj = typeof expiryDate === 'string' ? parseISO(expiryDate) : expiryDate
    const today = new Date()
    const diffTime = dateObj.getTime() - today.getTime()
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  }
}

// Number utilities
export const numberUtils = {
  formatCurrency: (amount: number, currency: string = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
    }).format(amount)
  },

  formatPercentage: (value: number, decimals: number = 1) => {
    return `${value.toFixed(decimals)}%`
  },

  clamp: (value: number, min: number, max: number) => {
    return Math.min(Math.max(value, min), max)
  }
}

// String utilities
export const stringUtils = {
  capitalize: (str: string) => {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
  },

  truncate: (str: string, length: number) => {
    return str.length > length ? `${str.slice(0, length)}...` : str
  },

  slugify: (str: string) => {
    return str
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '')
  },

  generateId: () => {
    return Math.random().toString(36).substr(2, 9)
  }
}

// Local storage utilities
export const storageUtils = {
  get: <T>(key: string, defaultValue?: T): T | null => {
    try {
      const item = localStorage.getItem(key)
      return item ? JSON.parse(item) : defaultValue || null
    } catch {
      return defaultValue || null
    }
  },

  set: (key: string, value: any) => {
    try {
      localStorage.setItem(key, JSON.stringify(value))
    } catch (error) {
      console.error('Failed to save to localStorage:', error)
    }
  },

  remove: (key: string) => {
    try {
      localStorage.removeItem(key)
    } catch (error) {
      console.error('Failed to remove from localStorage:', error)
    }
  },

  clear: () => {
    try {
      localStorage.clear()
    } catch (error) {
      console.error('Failed to clear localStorage:', error)
    }
  }
}

// Validation utilities
export const validationUtils = {
  isEmail: (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  },

  isUrl: (url: string) => {
    try {
      new URL(url)
      return true
    } catch {
      return false
    }
  },

  isPhoneNumber: (phone: string) => {
    const phoneRegex = /^\+?[\d\s\-\(\)]+$/
    return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10
  }
}

// Debounce utility
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

// Throttle utility
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}

// Array utilities
export const arrayUtils = {
  unique: <T>(array: T[]): T[] => {
    return [...new Set(array)]
  },

  groupBy: <T, K extends keyof T>(array: T[], key: K): Record<string, T[]> => {
    return array.reduce((groups, item) => {
      const group = String(item[key])
      groups[group] = groups[group] || []
      groups[group].push(item)
      return groups
    }, {} as Record<string, T[]>)
  },

  sortBy: <T>(array: T[], key: keyof T, order: 'asc' | 'desc' = 'asc'): T[] => {
    return [...array].sort((a, b) => {
      const aVal = a[key]
      const bVal = b[key]
      
      if (aVal < bVal) return order === 'asc' ? -1 : 1
      if (aVal > bVal) return order === 'asc' ? 1 : -1
      return 0
    })
  }
}

// Color utilities for status indicators
export const getStatusColor = (status: string) => {
  switch (status) {
    case 'good':
      return 'text-green-600 bg-green-100'
    case 'warning':
      return 'text-yellow-600 bg-yellow-100'
    case 'critical':
      return 'text-orange-600 bg-orange-100'
    case 'expired':
      return 'text-red-600 bg-red-100'
    default:
      return 'text-gray-600 bg-gray-100'
  }
}

// Environment utilities
export const env = {
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
  apiUrl: import.meta.env.VITE_API_URL || '/api',
  appVersion: import.meta.env.VITE_APP_VERSION || '2.0.0',
}