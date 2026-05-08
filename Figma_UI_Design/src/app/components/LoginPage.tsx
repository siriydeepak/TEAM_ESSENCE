import { useState } from 'react';

interface LoginPageProps {
  onLogin: () => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onLogin();
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{
            backgroundImage: 'url("/src/imports/WhatsApp_Image_2026-05-08_at_8.52.07_PM.jpeg")',
            filter: 'blur(0px)'
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-br from-[#006b57]/80 via-[#00ffd1]/60 to-[#006b57]/80" />
        <div className="absolute inset-0 bg-black/20" />
      </div>

      {/* Decorative Elements */}
      <div className="absolute top-20 left-10 opacity-20">
        <div className="w-32 h-32 border-4 border-[#00ffd1] rounded-full" />
      </div>
      <div className="absolute bottom-20 right-10 opacity-20">
        <div className="w-24 h-24 border-4 border-[#ff8a00] rounded-full" />
      </div>
      <div className="absolute top-1/3 right-1/4 opacity-10">
        <div className="w-16 h-16 border-4 border-[#ad009b] rounded-full" />
      </div>

      {/* Login Card */}
      <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
        <div className="w-full max-w-md">
          {/* Logo and Title */}
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <div className="bg-white/95 backdrop-blur-md p-6 rounded-3xl shadow-2xl">
                <img
                  src="/src/imports/screen.png"
                  alt="AetherShelf Logo"
                  className="h-20 w-auto"
                  onError={(e) => {
                    // Fallback to SVG if image not found
                    e.currentTarget.style.display = 'none';
                    e.currentTarget.parentElement!.innerHTML = `
                      <div class="h-20 w-20 bg-gradient-to-br from-[#006b57] to-[#00ffd1] rounded-2xl flex items-center justify-center">
                        <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                        </svg>
                      </div>
                    `;
                  }}
                />
              </div>
            </div>
            <h1 className="text-5xl md:text-6xl font-['Dancing_Script'] font-bold mb-2">
              <span className="text-[#00ffd1] drop-shadow-lg">Aether</span>
              <span className="text-[#ff8a00] drop-shadow-lg">Shelf</span>
            </h1>
            <p className="text-white/90 text-lg font-['Plus_Jakarta_Sans'] drop-shadow-md">
              Smart Pantry Management System
            </p>
          </div>

          {/* Login Form */}
          <div className="backdrop-blur-xl bg-white/95 rounded-3xl shadow-2xl p-8 border border-white/50">
            <h2 className="text-2xl font-['Epilogue'] font-semibold text-[#1a1c1c] mb-6 text-center">
              Welcome Back
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-['Plus_Jakarta_Sans'] font-semibold text-[#3a4a44] mb-2"
                >
                  Email Address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border-2 border-[#b9cbc3] focus:border-[#00ffd1] focus:ring-4 focus:ring-[#00ffd1]/20 outline-none transition-all font-['Plus_Jakarta_Sans']"
                  placeholder="you@example.com"
                  required
                />
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-['Plus_Jakarta_Sans'] font-semibold text-[#3a4a44] mb-2"
                >
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border-2 border-[#b9cbc3] focus:border-[#00ffd1] focus:ring-4 focus:ring-[#00ffd1]/20 outline-none transition-all font-['Plus_Jakarta_Sans']"
                  placeholder="••••••••"
                  required
                />
              </div>

              <div className="flex items-center justify-between text-sm">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    className="w-4 h-4 rounded border-[#b9cbc3] text-[#00ffd1] focus:ring-[#00ffd1]/20"
                  />
                  <span className="ml-2 text-[#3a4a44] font-['Plus_Jakarta_Sans']">Remember me</span>
                </label>
                <a href="#" className="text-[#006b57] hover:text-[#00ffd1] font-['Plus_Jakarta_Sans'] font-semibold transition-colors">
                  Forgot password?
                </a>
              </div>

              <button
                type="submit"
                className="w-full bg-gradient-to-r from-[#006b57] to-[#00ffd1] text-white font-['Plus_Jakarta_Sans'] font-bold py-4 rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
              >
                Sign In
              </button>

              <div className="text-center text-sm text-[#3a4a44] font-['Plus_Jakarta_Sans']">
                Don't have an account?{' '}
                <a href="#" className="text-[#006b57] hover:text-[#00ffd1] font-semibold transition-colors">
                  Sign up
                </a>
              </div>
            </form>

            {/* Quick Login Demo Button */}
            <div className="mt-6 pt-6 border-t border-[#b9cbc3]">
              <button
                onClick={onLogin}
                className="w-full bg-gradient-to-r from-[#ff8a00] to-[#fdba74] text-white font-['Plus_Jakarta_Sans'] font-bold py-3 rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
              >
                🚀 Demo Mode (Skip Login)
              </button>
            </div>
          </div>

          {/* Footer */}
          <p className="text-center text-white/70 text-sm mt-6 font-['Plus_Jakarta_Sans']">
            © 2026 AetherShelf. Smart inventory for modern living.
          </p>
        </div>
      </div>
    </div>
  );
}
