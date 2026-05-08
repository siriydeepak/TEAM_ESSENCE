import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
// import eslint from 'vite-plugin-eslint'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  const env = loadEnv(mode, process.cwd(), '')
  
  // Determine if we're in production
  const isProduction = mode === 'production'
  
  // Get API URL based on environment
  const getApiUrl = () => {
    if (isProduction) {
      // In production, use relative path or VERCEL_URL
      return env.VITE_API_URL || '/api'
    }
    return env.VITE_API_URL || 'http://localhost:8000/api'
  }

  return {
    plugins: [
      react(),
      // eslint({
      //   cache: false,
      //   include: ['./src/**/*.ts', './src/**/*.tsx'],
      //   exclude: ['node_modules'],
      // }),
    ],
    server: {
      host: '0.0.0.0',
      port: parseInt(env.VITE_DEV_PORT) || 5173,
      proxy: {
        '/api': {
          target: env.VITE_PROXY_TARGET || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, '/api')
        }
      },
      hmr: {
        port: parseInt(env.VITE_HMR_PORT) || 24678,
        host: env.VITE_HMR_HOST || 'localhost'
      }
    },
    build: {
      outDir: 'dist',
      sourcemap: env.VITE_BUILD_SOURCEMAP !== 'false',
      minify: env.VITE_BUILD_MINIFY !== 'false' ? 'esbuild' : false,
      target: env.VITE_BUILD_TARGET || 'es2015',
      chunkSizeWarningLimit: parseInt(env.VITE_CHUNK_SIZE_WARNING_LIMIT) || 500,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
            router: ['react-router-dom'],
            query: ['@tanstack/react-query'],
            ui: ['lucide-react', 'framer-motion'],
            utils: ['axios', 'date-fns', 'clsx', 'tailwind-merge']
          },
          // Optimize chunk naming for better caching
          chunkFileNames: (chunkInfo) => {
            const facadeModuleId = chunkInfo.facadeModuleId
            if (facadeModuleId) {
              return `chunks/[name]-[hash].js`
            }
            return `chunks/[name]-[hash].js`
          },
          entryFileNames: `assets/[name]-[hash].js`,
          assetFileNames: `assets/[name]-[hash].[ext]`
        }
      },
      // Optimize for production
      ...(isProduction && {
        cssCodeSplit: true,
        assetsInlineLimit: 4096,
        reportCompressedSize: false
      })
    },
    optimizeDeps: {
      include: [
        'react', 
        'react-dom', 
        'react-router-dom', 
        '@tanstack/react-query',
        'axios',
        'date-fns'
      ]
    },
    define: {
      __APP_VERSION__: JSON.stringify(env.VITE_APP_VERSION || '2.0.0'),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
      __API_URL__: JSON.stringify(getApiUrl()),
      __PRODUCTION__: JSON.stringify(isProduction),
      // Expose environment variables to the app
      'process.env.NODE_ENV': JSON.stringify(mode),
      'import.meta.env.VITE_API_URL': JSON.stringify(getApiUrl())
    },
    // Environment variable prefix
    envPrefix: 'VITE_',
    
    // Preview server configuration (for production builds)
    preview: {
      host: '0.0.0.0',
      port: parseInt(env.VITE_PREVIEW_PORT) || 4173,
      strictPort: true
    },
    
    // CSS configuration
    css: {
      devSourcemap: !isProduction,
      postcss: './postcss.config.js'
    }
  }
})