# TEAM_ESSENCE - AetherShelf Monorepo

> Smart Inventory Management System with Weather Integration

AetherShelf is a Progressive Web Application (PWA) that helps you manage your pantry inventory intelligently, with weather-based shelf life adjustments, receipt parsing, and smart shopping recommendations.

## 🏗️ Monorepo Structure

This project is organized as a monorepo with separate frontend and backend packages:

```
/
├── frontend/                    # React/Next.js Progressive Web Application
│   ├── src/                    # React components and pages
│   ├── public/                 # Static assets and PWA manifest
│   ├── package.json           # Frontend-specific dependencies
│   └── ...                    # Frontend configuration files
├── backend/                    # FastAPI Python API Server
│   ├── routes/                # API endpoint definitions
│   ├── services/              # Business logic and data processing
│   ├── models/                # Data models and schemas
│   ├── utils/                 # Utility functions and helpers
│   ├── main.py               # FastAPI application entry point
│   └── requirements.txt      # Python dependencies
├── package.json              # Root workspace configuration
├── vercel.json              # Vercel deployment configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm 9+
- Python 3.9+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd team-essence-monorepo
   ```

2. **Install all dependencies:**
   ```bash
   npm install
   ```
   This will install dependencies for both frontend and backend workspaces.

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Start development servers:**
   ```bash
   npm run dev
   ```
   This starts both frontend (http://localhost:3000) and backend (http://localhost:8000) servers.

## 📦 Available Scripts

### Root Level Scripts

- `npm run dev` - Start both frontend and backend development servers
- `npm run build` - Build both frontend and backend for production
- `npm run test` - Run tests for both frontend and backend
- `npm run lint` - Lint both frontend and backend code
- `npm run clean` - Clean build artifacts from both workspaces

### Frontend Specific Scripts

- `npm run dev:frontend` - Start only the frontend development server
- `npm run build:frontend` - Build only the frontend
- `npm run test:frontend` - Run only frontend tests
- `npm run lint:frontend` - Lint only frontend code

### Backend Specific Scripts

- `npm run dev:backend` - Start only the backend development server
- `npm run build:backend` - Build only the backend
- `npm run test:backend` - Run only backend tests
- `npm run lint:backend` - Lint only backend code

## 🔧 Development Workflow

### Working with Workspaces

This monorepo uses npm workspaces to manage dependencies efficiently:

```bash
# Install a dependency to the frontend
npm install react-query --workspace=frontend

# Install a development dependency to the backend
npm install pytest --save-dev --workspace=backend

# Run a script in a specific workspace
npm run build --workspace=frontend
```

### Hot Reloading

Both frontend and backend support hot reloading during development:

- **Frontend**: Next.js automatically reloads on file changes
- **Backend**: FastAPI with uvicorn reloads on Python file changes

### API Development

The backend API is available at `http://localhost:8000` during development. The frontend automatically proxies API requests to the backend.

- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- API Schema: `http://localhost:8000/redoc` (ReDoc)

## 🌐 Deployment

### Vercel Deployment

This monorepo is optimized for Vercel deployment:

1. **Connect your repository to Vercel**
2. **Set environment variables in Vercel dashboard**
3. **Deploy automatically on push to main branch**

The `vercel.json` configuration handles:
- Frontend static site deployment
- Backend serverless function deployment
- API routing (`/api/*` → backend, everything else → frontend)

### Environment Variables

Required environment variables for production:

```bash
# Database
DATABASE_URL=postgresql://...

# Weather API
OWM_API_KEY=your_openweathermap_api_key

# Authentication (if using)
NEXTAUTH_SECRET=your_nextauth_secret
NEXTAUTH_URL=https://your-domain.vercel.app

# Other APIs
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 🏛️ Architecture

### Frontend (React/Next.js PWA)

- **Framework**: Next.js 14 with React 18
- **Styling**: TailwindCSS for responsive design
- **State Management**: Zustand for global state
- **API Client**: Axios with React Query for caching
- **PWA Features**: Service worker, offline support, installable

### Backend (FastAPI)

- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL (Vercel Postgres) with fallback to SQLite
- **Authentication**: JWT-based authentication
- **External APIs**: OpenWeatherMap for weather data
- **Features**: Automatic API documentation, request validation

### Key Features

- **Smart Inventory Management**: Track items with expiry dates and quantities
- **Weather Integration**: Adjust shelf life based on local weather conditions
- **Receipt Parsing**: Extract items from receipt images/text
- **Smart Shopping**: AI-powered shopping suggestions based on inventory gaps
- **Analytics**: Track waste, savings, and consumption patterns
- **PWA**: Installable app with offline capabilities

## 🧪 Testing

### Frontend Testing

```bash
# Run frontend tests
npm run test:frontend

# Run tests in watch mode
npm run test:frontend -- --watch

# Run tests with coverage
npm run test:frontend -- --coverage
```

### Backend Testing

```bash
# Run backend tests
npm run test:backend

# Run tests with coverage
npm run test:backend -- --cov

# Run specific test file
npm run test:backend -- tests/test_inventory.py
```

## 📚 API Documentation

### Core Endpoints

- `GET /api/inventory` - Get all inventory items
- `POST /api/inventory` - Add new inventory item
- `PUT /api/inventory/{id}` - Update inventory item
- `DELETE /api/inventory/{id}` - Delete inventory item
- `GET /api/weather/{city}` - Get weather data and shelf life adjustments
- `POST /api/receipts/parse` - Parse receipt text/image
- `GET /api/analytics/dashboard` - Get dashboard analytics

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes in the appropriate workspace (frontend or backend)
4. Run tests: `npm run test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Guidelines

- Follow the existing code style and conventions
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` directory for detailed guides
- **Issues**: Report bugs and request features via GitHub Issues
- **Discussions**: Join community discussions in GitHub Discussions

## 🙏 Acknowledgments

- OpenWeatherMap for weather data API
- Vercel for hosting and deployment platform
- The open-source community for the amazing tools and libraries

---

**Built with ❤️ by TEAM_ESSENCE**