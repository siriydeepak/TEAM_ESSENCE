# Environment Configuration Guide

This document provides comprehensive guidance for configuring environment variables for the TEAM_ESSENCE monorepo in both development and production environments.

## Overview

The monorepo uses environment variables to configure:
- Database connections (PostgreSQL for production, SQLite for development)
- External API keys (OpenWeatherMap, authentication services)
- CORS settings and security configurations
- Feature flags and application behavior
- Build and deployment settings

## Environment Files Structure

```
/
├── .env.example                 # Root-level environment template
├── .env                        # Root-level environment (gitignored)
├── frontend/.env.example       # Frontend-specific environment template
├── frontend/.env.local         # Frontend-specific environment (gitignored)
├── backend/.env.example        # Backend-specific environment template
└── backend/.env               # Backend-specific environment (gitignored)
```

## Development Setup

### 1. Copy Environment Templates

```bash
# Copy root environment template
cp .env.example .env

# Copy frontend environment template
cp frontend/.env.example frontend/.env.local

# Copy backend environment template
cp backend/.env.example backend/.env
```

### 2. Configure Required Variables

#### Essential Variables for Development:

```bash
# Database (SQLite fallback for development)
DATABASE_URL=sqlite:///./database.sqlite

# Weather API (get free key from OpenWeatherMap)
OWM_API_KEY=your_actual_openweathermap_api_key

# Application URLs
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000

# Environment
ENVIRONMENT=development
NODE_ENV=development
```

#### Frontend Development Variables:

```bash
# API endpoint
VITE_API_URL=http://localhost:8000/api

# Feature flags
VITE_ENABLE_PWA=true
VITE_ENABLE_ANALYTICS=false
VITE_DEV_TOOLS=true
```

### 3. Start Development Servers

```bash
# Install dependencies
npm install

# Start both frontend and backend
npm run dev

# Or start individually
npm run dev:frontend  # Starts on http://localhost:5173
npm run dev:backend   # Starts on http://localhost:8000
```

## Production Deployment (Vercel)

### 1. Vercel Environment Variables

Configure these variables in your Vercel dashboard:

#### Database Configuration:
```
DATABASE_URL=postgresql://username:password@host:port/database
```

#### API Keys:
```
OWM_API_KEY=your_openweathermap_api_key
```

#### Security:
```
JWT_SECRET=your_secure_jwt_secret_here
SESSION_SECRET=your_secure_session_secret_here
NEXTAUTH_SECRET=your_nextauth_secret_here
```

#### CORS Configuration:
```
CORS_ORIGINS=https://your-domain.vercel.app,https://your-custom-domain.com
FRONTEND_URL=https://your-domain.vercel.app
```

#### Feature Flags:
```
ENABLE_WEATHER_INTEGRATION=true
ENABLE_RECEIPT_PARSING=true
ENABLE_SMART_SHOPPING=true
ENABLE_ANALYTICS=true
ENABLE_PUSH_NOTIFICATIONS=true
```

#### Frontend Build Variables:
```
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_PWA=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_GA_TRACKING_ID=your_google_analytics_id
VITE_SENTRY_DSN=your_sentry_dsn
```

### 2. Vercel Configuration Mapping

The `vercel.json` file automatically maps environment variables:

- `@database_url` → `DATABASE_URL`
- `@owm_api_key` → `OWM_API_KEY`
- `@jwt_secret` → `JWT_SECRET`
- `@cors_origins` → `CORS_ORIGINS`
- And more...

### 3. Build Environment Variables

During build, Vercel automatically sets:

```bash
VITE_API_URL=https://$VERCEL_URL/api
ENVIRONMENT=production
NODE_ENV=production
FASTAPI_ENV=production
```

## Environment Variable Reference

### Backend Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `OWM_API_KEY` | OpenWeatherMap API key | Yes | - |
| `ENVIRONMENT` | Application environment | No | development |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |
| `JWT_SECRET` | JWT signing secret | Yes | - |
| `CORS_ORIGINS` | Allowed CORS origins | No | * (dev) |
| `LOG_LEVEL` | Logging level | No | info |
| `ENABLE_WEATHER_INTEGRATION` | Enable weather features | No | true |
| `ENABLE_RECEIPT_PARSING` | Enable receipt parsing | No | true |
| `ENABLE_SMART_SHOPPING` | Enable smart shopping | No | true |
| `ENABLE_ANALYTICS` | Enable analytics | No | true |
| `SENTRY_DSN` | Sentry error tracking | No | - |

### Frontend Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | Yes | - |
| `VITE_APP_VERSION` | Application version | No | 2.0.0 |
| `VITE_PWA_NAME` | PWA display name | No | AetherShelf |
| `VITE_PWA_THEME_COLOR` | PWA theme color | No | #2563eb |
| `VITE_ENABLE_PWA` | Enable PWA features | No | true |
| `VITE_ENABLE_ANALYTICS` | Enable analytics | No | true |
| `VITE_GA_TRACKING_ID` | Google Analytics ID | No | - |
| `VITE_SENTRY_DSN` | Frontend error tracking | No | - |
| `VITE_DEV_TOOLS` | Enable dev tools | No | true (dev) |

## CORS Configuration

### Development CORS

In development, CORS is configured to allow all origins (`*`) for ease of development.

### Production CORS

In production, CORS is strictly configured based on:

1. `CORS_ORIGINS` environment variable (comma-separated list)
2. `VERCEL_URL` (automatically added)
3. `FRONTEND_URL` (if specified)

Example production CORS setup:
```bash
CORS_ORIGINS=https://aethershelf.vercel.app,https://aethershelf.com
FRONTEND_URL=https://aethershelf.com
```

## Security Best Practices

### 1. Environment Variable Security

- Never commit `.env` files to version control
- Use strong, unique secrets for JWT and session keys
- Rotate API keys regularly
- Use Vercel's encrypted environment variables for sensitive data

### 2. CORS Security

- Always specify exact origins in production
- Never use `*` for CORS origins in production
- Include credentials only when necessary
- Set appropriate cache headers

### 3. API Security

- Use HTTPS in production (automatically handled by Vercel)
- Implement rate limiting
- Validate all inputs
- Use proper authentication and authorization

## Troubleshooting

### Common Issues

#### 1. CORS Errors
```
Access to fetch at 'https://api.domain.com' from origin 'https://app.domain.com' has been blocked by CORS policy
```

**Solution:** Add the frontend domain to `CORS_ORIGINS`:
```bash
CORS_ORIGINS=https://app.domain.com,https://api.domain.com
```

#### 2. Environment Variables Not Loading
```
Error: Environment variable 'DATABASE_URL' is not defined
```

**Solutions:**
- Verify the variable is set in Vercel dashboard
- Check variable name spelling and case
- Ensure the variable is mapped in `vercel.json`
- Redeploy after adding variables

#### 3. Build Failures
```
Error: VITE_API_URL is not defined during build
```

**Solution:** Set build-time environment variables in Vercel:
```bash
VITE_API_URL=https://$VERCEL_URL/api
```

#### 4. Database Connection Issues
```
Error: Connection to database failed
```

**Solutions:**
- Verify `DATABASE_URL` format: `postgresql://user:pass@host:port/db`
- Check database server accessibility
- Verify credentials and permissions
- Ensure database exists

### Development vs Production Differences

| Aspect | Development | Production |
|--------|-------------|------------|
| Database | SQLite (local file) | PostgreSQL (Vercel) |
| CORS | Permissive (`*`) | Strict (specific origins) |
| API URL | `http://localhost:8000` | `https://domain.vercel.app` |
| Logging | Debug level | Info/Warning level |
| Source Maps | Always enabled | Configurable |
| Hot Reload | Enabled | Disabled |

## Environment Validation

The application includes environment validation to ensure required variables are present:

### Backend Validation
```python
# Validates required environment variables on startup
required_vars = ['DATABASE_URL', 'OWM_API_KEY', 'JWT_SECRET']
```

### Frontend Validation
```typescript
// Validates required Vite variables during build
const requiredVars = ['VITE_API_URL']
```

## Monitoring and Logging

### Environment-Based Logging

- **Development:** Debug level, console output
- **Production:** Info level, structured logging
- **Error Tracking:** Sentry integration (if configured)

### Health Checks

The application provides health check endpoints that report environment status:

- Backend: `GET /api/health`
- Frontend: Available in browser console (development)

## Migration from Legacy Setup

If migrating from the old structure:

1. **Copy existing environment variables** from root `.env` to appropriate locations
2. **Update API URLs** to use the new monorepo structure
3. **Reconfigure CORS** for the new frontend/backend separation
4. **Update build scripts** to use the new workspace structure
5. **Test thoroughly** in both development and production environments

## Support

For environment configuration issues:

1. Check this documentation first
2. Verify Vercel dashboard settings
3. Review application logs in Vercel dashboard
4. Test locally with production-like environment variables
5. Check the health endpoints for configuration status