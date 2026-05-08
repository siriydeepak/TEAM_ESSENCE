# AetherShelf Frontend

A modern React Progressive Web Application (PWA) for smart inventory management with weather integration and expiration tracking.

## 🚀 Features

- **Progressive Web App (PWA)** - Installable, offline-capable, and mobile-friendly
- **Modern React Stack** - Built with React 18, TypeScript, and Vite
- **Responsive Design** - TailwindCSS for beautiful, responsive UI
- **Real-time Updates** - React Query for efficient data fetching and caching
- **Accessibility** - WCAG compliant with proper ARIA labels and keyboard navigation
- **Performance Optimized** - Code splitting, lazy loading, and optimized bundles

## 🛠️ Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS with custom design system
- **State Management**: React Query (TanStack Query)
- **Routing**: React Router v6
- **Icons**: Lucide React
- **Testing**: Vitest + React Testing Library
- **PWA**: Vite PWA Plugin with Workbox
- **Linting**: ESLint + Prettier

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Type check
npm run type-check
```

## 🏗️ Project Structure

```
frontend/
├── public/                 # Static assets
│   ├── icons/             # PWA icons
│   ├── manifest.json      # PWA manifest
│   └── robots.txt         # SEO robots file
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── types/            # TypeScript type definitions
│   ├── utils/            # Utility functions
│   ├── test/             # Test setup and utilities
│   ├── App.tsx           # Main app component
│   ├── main.tsx          # App entry point
│   └── index.css         # Global styles
├── package.json          # Dependencies and scripts
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # TailwindCSS configuration
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env.local` and configure:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api

# External Services
VITE_OPENWEATHER_API_KEY=your_api_key_here

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_PWA=true
```

### PWA Configuration

The app is configured as a PWA with:
- Service worker for offline functionality
- App manifest for installation
- Caching strategies for optimal performance
- Push notification support (future feature)

### Development Proxy

The development server proxies API calls to the backend:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/api`

## 🧪 Testing

```bash
# Run all tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui
```

### Testing Strategy

- **Unit Tests**: Component logic and utility functions
- **Integration Tests**: Component interactions and API calls
- **Accessibility Tests**: Screen reader and keyboard navigation
- **Visual Regression Tests**: UI consistency (future enhancement)

## 📱 PWA Features

### Installation
Users can install the app on their devices for a native-like experience.

### Offline Support
The app works offline with cached data and provides graceful degradation.

### Performance
- Code splitting for optimal loading
- Image optimization and lazy loading
- Service worker caching strategies

## 🎨 Design System

### Colors
- **Primary**: Blue (#2563eb)
- **Success**: Green (#22c55e)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)

### Typography
- **Font**: Inter (system fallback)
- **Scale**: Tailwind's default type scale

### Components
All components follow accessibility guidelines and include:
- Proper ARIA labels
- Keyboard navigation support
- Focus management
- Screen reader compatibility

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

### Vercel Deployment

The app is configured for Vercel deployment with:
- Automatic builds on push
- Environment variable management
- Edge caching for optimal performance

## 🔍 Performance

### Bundle Analysis

```bash
npm run analyze
```

### Optimization Features
- Tree shaking for smaller bundles
- Code splitting by route and vendor
- Image optimization
- Service worker caching
- Preloading critical resources

## 🤝 Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation as needed
4. Ensure accessibility compliance
5. Test PWA functionality

## 📄 License

MIT License - see the LICENSE file for details.