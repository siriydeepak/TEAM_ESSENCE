# Quick Start Guide - Cyber-Kitchen Design

## Prerequisites
- Node.js (v16 or higher)
- npm or yarn

## Installation

1. **Navigate to the frontend directory**
   ```bash
   cd TEAM_ESSENCE/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Verify the background image**
   Ensure `public/assets/kitchen-bg.jpg` exists

## Development

### Start the development server
```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or the port shown in terminal)

## What to Expect

### Visual Changes
You should see:
- ✨ Full-screen kitchen background image with blur overlay
- 🎨 White floating cards with colored top stripes
- 🔵 Cyan and orange neon-bordered buttons
- 📱 Bottom navigation bar with Material icons
- ⚡ Floating action button (FAB) in bottom-right

### Typography
- **Brand**: "AetherShelf" in Great Vibes font (Aether=cyan, Shelf=orange)
- **Headlines**: Epilogue font
- **Body**: Plus Jakarta Sans font
- **Labels**: Space Grotesk font (uppercase)

### Color Scheme
- **Primary**: Deep green (#006b57)
- **Accent**: Neon cyan (#00FFD1)
- **Secondary**: Vibrant orange (#FF8A00)
- **Status Colors**:
  - Pink - Urgent
  - Yellow - Warning
  - Cyan - Stable

## Troubleshooting

### Background image not showing
1. Check if `public/assets/kitchen-bg.jpg` exists
2. Clear browser cache
3. Check browser console for 404 errors

### Fonts not loading
1. Check internet connection (fonts load from Google Fonts CDN)
2. Check browser console for font loading errors
3. Wait a few seconds for fonts to load

### Blur effect not working
- Backdrop blur requires modern browser support
- Check if your browser supports `backdrop-filter`
- Try Chrome, Firefox, or Safari (latest versions)

### Styles not applying
1. Make sure Tailwind is running: `npm run dev`
2. Clear browser cache
3. Check if `tailwind.config.js` was updated correctly
4. Restart the development server

## Building for Production

```bash
npm run build
```

The optimized build will be in the `dist/` directory.

### Preview production build
```bash
npm run preview
```

## Key Features to Test

### 1. Navigation
- Click bottom navigation items
- Active state should show dark gradient with cyan border
- Icons should change based on active page

### 2. Cards
- Inventory cards should have colored left borders
- Analytics cards should have colored top stripes
- Cards should have subtle shadows

### 3. Buttons
- Primary buttons: Dark gradient with cyan border
- Secondary buttons: Dark gradient with orange border
- Hover and active states should work

### 4. Responsive Design
- Resize browser window
- Check mobile view (< 768px)
- Bottom nav should remain accessible
- Cards should stack on mobile

## File Structure

```
frontend/
├── public/
│   └── assets/
│       └── kitchen-bg.jpg          # Background image
├── src/
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── Analytics.tsx       # ✅ Updated
│   │   │   ├── InventoryList.tsx   # ✅ Updated
│   │   │   ├── GapFinder.tsx       # ⏳ To update
│   │   │   ├── SmartCart.tsx       # ⏳ To update
│   │   │   └── WeatherImpact.tsx   # ⏳ To update
│   │   ├── layout/
│   │   │   └── DashboardLayout.tsx # ✅ Updated
│   │   └── Layout.tsx              # ✅ Updated
│   ├── pages/
│   │   ├── Dashboard.tsx           # Uses updated components
│   │   ├── Analytics.tsx           # ⏳ To update
│   │   ├── Inventory.tsx           # ⏳ To update
│   │   ├── Settings.tsx            # ⏳ To update
│   │   └── login.tsx               # ⏳ To update
│   ├── App.tsx                     # ✅ Updated
│   ├── App.css                     # ✅ Updated
│   └── index.css                   # ✅ Updated
├── tailwind.config.js              # ✅ Updated
├── CYBER_KITCHEN_INTEGRATION.md    # Documentation
└── QUICKSTART.md                   # This file
```

## Design System Reference

### CSS Classes

#### Backgrounds
```css
.cyber-bg              /* Fixed background with blur */
```

#### Buttons
```css
.btn-primary           /* Cyan neon button */
.btn-secondary         /* Orange neon button */
.dark-gradient         /* Dark gradient background */
```

#### Borders
```css
.neon-border-cyan      /* Cyan neon border */
.neon-border-orange    /* Orange neon border */
.neon-border-pink      /* Pink neon border */
```

#### Cards
```css
.dashboard-card        /* Standard card */
.glass-card            /* Glass effect card */
.hard-shadow           /* Prominent shadow */
```

#### Status Stripes
```css
.stripe-urgent         /* Pink top border */
.stripe-warning        /* Yellow top border */
.stripe-stable         /* Cyan top border */
```

### Typography Classes
```css
.font-brand-title      /* Great Vibes */
.font-headline-lg      /* Epilogue large */
.font-headline-md      /* Epilogue medium */
.font-body-lg          /* Plus Jakarta Sans large */
.font-body-md          /* Plus Jakarta Sans medium */
.font-label-caps       /* Space Grotesk uppercase */
```

### Color Classes
```css
.text-primary          /* #006b57 */
.text-primary-container /* #00FFD1 */
.text-secondary-container /* #FF8A00 */
.text-error            /* #BA1A1A */
.text-on-surface       /* #1A1C1C */
.text-on-surface-variant /* #3A4A44 */
```

## Material Symbols Icons

Common icons used:
- `kitchen` - App logo
- `inventory_2` - Inventory
- `restaurant` - Eat Me First
- `timer_off` - Expiry
- `shopping_cart` - Cart
- `analytics` - Analytics
- `settings` - Settings
- `add` - Add button
- `more_vert` - More options

Usage:
```tsx
<span className="material-symbols-outlined">kitchen</span>
```

## Next Steps

1. **Test the current implementation**
   - Run `npm run dev`
   - Navigate through the app
   - Check all visual elements

2. **Update remaining components**
   - GapFinder.tsx
   - SmartCart.tsx
   - WeatherImpact.tsx
   - Other pages (Inventory, Analytics, Settings, Login)

3. **Optimize**
   - Compress background image
   - Add loading states
   - Improve performance

4. **Enhance**
   - Add animations
   - Implement dark mode
   - Add more interactions

## Support

For issues or questions:
1. Check `CYBER_KITCHEN_INTEGRATION.md` for detailed documentation
2. Review `INTEGRATION_SUMMARY.md` for overview
3. Refer to Stitch prototypes in `stitch_aethershelf_smart_kitchen_manager/`

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Material Symbols](https://fonts.google.com/icons)
- [React Router](https://reactrouter.com)
- [Vite](https://vitejs.dev)
