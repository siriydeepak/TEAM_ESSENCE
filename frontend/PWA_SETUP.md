# PWA Setup Documentation

## Overview

AetherShelf is configured as a Progressive Web Application (PWA) with offline capabilities, push notifications, and native app-like experience.

## PWA Assets Location

All PWA assets are now properly organized in the `/frontend/public` directory:

- `manifest.json` - PWA manifest with app metadata and configuration
- `sw.js` - Custom service worker with advanced caching and push notification support
- `browserconfig.xml` - Microsoft PWA configuration
- `icons/` - Directory for PWA icons (currently contains README with generation instructions)
- `robots.txt` - Search engine directives

## Service Worker Features

The custom service worker (`sw.js`) provides:

- **Offline-first caching** - App shell and static assets cached for offline use
- **Network-first API calls** - Real-time data when online, graceful offline fallback
- **Push notifications** - Background notifications with urgency-based vibration patterns
- **Automatic updates** - Service worker updates automatically when new versions are deployed
- **Cache management** - Automatic cleanup of stale caches

## PWA Icons

Currently using `logo.svg` as fallback icon. To generate proper PWA icons:

```bash
# Generate all required icon sizes from logo.svg
npm run pwa:generate-icons
```

This will create all the icon sizes referenced in the manifest.json.

## Build Integration

The PWA assets are automatically copied to the build output (`dist/`) during the build process. No additional configuration needed.

## Development

During development, the service worker is registered and functional. You can test PWA features by:

1. Opening DevTools > Application > Service Workers
2. Testing offline functionality by going offline in DevTools
3. Testing push notifications (requires HTTPS in production)

## Production Deployment

The PWA is ready for production deployment on Vercel with:

- Automatic HTTPS (required for service workers)
- Proper caching headers
- Service worker served from root domain
- All PWA assets properly served

## Browser Support

The PWA features work in all modern browsers that support:
- Service Workers
- Web App Manifest
- Push API (for notifications)

## Notes

- Removed `vite-plugin-pwa` in favor of custom service worker for more control
- Service worker paths updated for new frontend structure
- All PWA functionality preserved from original TEAM_ESSENCE implementation
- Ready for app store deployment via PWA Builder or similar tools