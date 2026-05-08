import { useState } from 'react';
import { Package, ShoppingCart, Clock, TrendingUp } from 'lucide-react';
import ProductInfoTrackerDarkerGreenBg from '../imports/ProductInfoTrackerDarkerGreenBg/ProductInfoTrackerDarkerGreenBg';
import SmartCartRestockDarkerGreenBg from '../imports/SmartCartRestockDarkerGreenBg/SmartCartRestockDarkerGreenBg';
import ExpiryLogsDarkerGreenBg from '../imports/ExpiryLogsDarkerGreenBg/ExpiryLogsDarkerGreenBg';
import GapFinderAnalyticsDarkerGreenBg from '../imports/GapFinderAnalyticsDarkerGreenBg/GapFinderAnalyticsDarkerGreenBg';
import LoginPage from './components/LoginPage';

type ScreenType = 'product' | 'restock' | 'expiry' | 'analytics';

const screens = [
  { id: 'product' as ScreenType, label: 'Product Info', icon: Package },
  { id: 'restock' as ScreenType, label: 'Smart Restock', icon: ShoppingCart },
  { id: 'expiry' as ScreenType, label: 'Expiry Logs', icon: Clock },
  { id: 'analytics' as ScreenType, label: 'Analytics', icon: TrendingUp },
];

export default function App() {
  const [activeScreen, setActiveScreen] = useState<ScreenType>('product');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  if (!isLoggedIn) {
    return <LoginPage onLogin={() => setIsLoggedIn(true)} />;
  }

  const renderScreen = () => {
    switch (activeScreen) {
      case 'product':
        return <ProductInfoTrackerDarkerGreenBg />;
      case 'restock':
        return <SmartCartRestockDarkerGreenBg />;
      case 'expiry':
        return <ExpiryLogsDarkerGreenBg />;
      case 'analytics':
        return <GapFinderAnalyticsDarkerGreenBg />;
      default:
        return <ProductInfoTrackerDarkerGreenBg />;
    }
  };

  const navigateScreen = (direction: 'prev' | 'next') => {
    const currentIndex = screens.findIndex(s => s.id === activeScreen);
    if (direction === 'prev') {
      const prevIndex = currentIndex === 0 ? screens.length - 1 : currentIndex - 1;
      setActiveScreen(screens[prevIndex].id);
    } else {
      const nextIndex = currentIndex === screens.length - 1 ? 0 : currentIndex + 1;
      setActiveScreen(screens[nextIndex].id);
    }
  };

  return (
    <div className="relative w-full min-h-screen overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="fixed inset-0 z-0">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: 'url("/src/imports/WhatsApp_Image_2026-05-08_at_8.52.07_PM.jpeg")',
          }}
        />
        {/* Soft Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#e8f5f1]/95 via-[#e2ede7]/90 to-[#d4e9e0]/95" />
        {/* Pattern Overlay */}
        <div className="absolute inset-0 opacity-5" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, #006b57 1px, transparent 0)`,
          backgroundSize: '32px 32px'
        }} />
      </div>

      {/* Mobile/Tablet Container */}
      <div className="relative z-10 mx-auto max-w-[780px] w-full min-h-screen">
        {/* Header with Logo */}
        <div className="absolute top-0 left-0 right-0 z-50 backdrop-blur-xl bg-white/95 border-b border-[#e4e4e7] shadow-lg">
          <div className="flex items-center justify-between px-6 py-4">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-[#006b57] to-[#00ffd1] p-2 rounded-xl shadow-md">
                <img
                  src="/src/imports/screen.png"
                  alt="Logo"
                  className="h-8 w-8"
                  onError={(e) => {
                    // Fallback icon
                    e.currentTarget.outerHTML = `
                      <svg class="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                      </svg>
                    `;
                  }}
                />
              </div>
              <h1 className="text-3xl md:text-4xl font-['Dancing_Script'] font-bold">
                <span className="text-[#006b57]">Aether</span>
                <span className="text-[#ff8a00]">Shelf</span>
              </h1>
            </div>

            {/* Logout Button */}
            <button
              onClick={() => setIsLoggedIn(false)}
              className="px-4 py-2 text-sm font-['Plus_Jakarta_Sans'] font-semibold text-[#71717a] hover:text-[#006b57] transition-colors"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Screen Content with elevated white background */}
        <div className="relative w-full min-h-screen pt-20">
          <div className="w-full min-h-[calc(100vh-80px)] bg-white shadow-2xl overflow-auto">
            {renderScreen()}
          </div>
        </div>

        {/* Desktop Navigation Tabs */}
        <div className="hidden md:block absolute top-24 left-1/2 -translate-x-1/2 z-50">
          <div className="backdrop-blur-xl bg-white/95 rounded-2xl shadow-2xl border border-white/50 p-2">
            <div className="flex gap-2">
              {screens.map((screen) => {
                const Icon = screen.icon;
                return (
                  <button
                    key={screen.id}
                    onClick={() => setActiveScreen(screen.id)}
                    className={`px-6 py-3 rounded-xl font-['Plus_Jakarta_Sans'] font-semibold text-sm transition-all flex items-center gap-2 ${
                      activeScreen === screen.id
                        ? 'bg-gradient-to-r from-[#006b57] to-[#00ffd1] text-white shadow-lg scale-105'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    {screen.label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Mobile Bottom Navigation */}
        <div className="md:hidden fixed bottom-0 left-0 right-0 z-50">
          <div className="backdrop-blur-xl bg-white/95 border-t border-[#e4e4e7] shadow-2xl">
            <div className="grid grid-cols-4 max-w-[780px] mx-auto">
              {screens.map((screen) => {
                const Icon = screen.icon;
                return (
                  <button
                    key={screen.id}
                    onClick={() => setActiveScreen(screen.id)}
                    className={`flex flex-col items-center justify-center py-3 px-2 transition-all ${
                      activeScreen === screen.id
                        ? 'text-[#00ffd1] bg-gradient-to-b from-[#006b57]/10 to-transparent'
                        : 'text-gray-500'
                    }`}
                  >
                    <Icon className={`w-6 h-6 mb-1 ${
                      activeScreen === screen.id ? 'scale-110' : ''
                    }`} />
                    <span className={`text-xs font-['Plus_Jakarta_Sans'] font-semibold ${
                      activeScreen === screen.id ? 'text-[#006b57]' : ''
                    }`}>
                      {screen.label.split(' ')[0]}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Swipe Navigation Buttons (Mobile) */}
        <div className="md:hidden fixed top-1/2 -translate-y-1/2 left-4 z-40">
          <button
            onClick={() => navigateScreen('prev')}
            className="backdrop-blur-md bg-white/90 p-3 rounded-full shadow-xl hover:bg-white hover:scale-110 transition-all border border-[#00ffd1]/20"
          >
            <svg className="w-6 h-6 text-[#006b57]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        </div>
        <div className="md:hidden fixed top-1/2 -translate-y-1/2 right-4 z-40">
          <button
            onClick={() => navigateScreen('next')}
            className="backdrop-blur-md bg-white/90 p-3 rounded-full shadow-xl hover:bg-white hover:scale-110 transition-all border border-[#00ffd1]/20"
          >
            <svg className="w-6 h-6 text-[#006b57]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        {/* Page Indicators (Mobile) */}
        <div className="md:hidden fixed bottom-20 left-1/2 -translate-x-1/2 z-40">
          <div className="backdrop-blur-sm bg-black/60 px-4 py-2 rounded-full shadow-lg">
            <div className="flex gap-2">
              {screens.map((screen) => (
                <div
                  key={screen.id}
                  onClick={() => setActiveScreen(screen.id)}
                  className={`rounded-full transition-all cursor-pointer ${
                    activeScreen === screen.id
                      ? 'bg-[#00ffd1] w-8 h-2'
                      : 'bg-white/40 w-2 h-2 hover:bg-white/60'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Decorative Background Elements */}
      <div className="hidden lg:block fixed top-20 left-10 opacity-10 z-0">
        <svg width="200" height="200" viewBox="0 0 200 200">
          <circle cx="100" cy="100" r="90" stroke="#006b57" strokeWidth="3" fill="none" />
          <circle cx="100" cy="100" r="60" stroke="#00ffd1" strokeWidth="3" fill="none" />
          <circle cx="100" cy="100" r="30" stroke="#ff8a00" strokeWidth="3" fill="none" />
        </svg>
      </div>
      <div className="hidden lg:block fixed bottom-20 right-10 opacity-10 z-0">
        <svg width="200" height="200" viewBox="0 0 200 200">
          <circle cx="100" cy="100" r="90" stroke="#ad009b" strokeWidth="3" fill="none" />
          <circle cx="100" cy="100" r="60" stroke="#00ffd1" strokeWidth="3" fill="none" />
          <circle cx="100" cy="100" r="30" stroke="#ff8a00" strokeWidth="3" fill="none" />
        </svg>
      </div>
    </div>
  );
}
