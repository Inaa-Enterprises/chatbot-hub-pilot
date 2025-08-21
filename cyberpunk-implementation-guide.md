# Cyberpunk Design System - Implementation Guide

## Quick Start

### 1. Setup Project Structure
```bash
mkdir cyberpunk-pwa-frontend
cd cyberpunk-pwa-frontend
npm init -y
npm install -D vite @vitejs/plugin-react tailwindcss postcss autoprefixer
npm install react react-dom
```

### 2. Install Required Fonts
```html
<!-- Add to index.html -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500;600&display=swap" rel="stylesheet">
```

### 3. Configure Tailwind CSS
```javascript
// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'cyber-black': '#0a0a0f',
        'cyber-purple': '#1a1a2e',
        'cyber-blue': '#16213e',
        'neon-cyan': '#00ffff',
        'neon-pink': '#ff0080',
        'neon-green': '#39ff14',
        'neon-purple': '#bf00ff',
        'neon-orange': '#ff6600',
      },
      fontFamily: {
        'orbitron': ['Orbitron', 'sans-serif'],
        'rajdhani': ['Rajdhani', 'sans-serif'],
        'fira-code': ['Fira Code', 'monospace'],
      },
      animation: {
        'glitch': 'glitch 0.3s ease-in-out',
        'neon-pulse': 'neon-pulse 2s ease-in-out infinite',
        'holographic-scan': 'holographic-scan 3s linear infinite',
        'skeleton-loading': 'skeleton-loading 1.5s infinite',
      },
      keyframes: {
        glitch: {
          '0%, 100%': { transform: 'translate(0)' },
          '20%': { transform: 'translate(-2px, 2px)' },
          '40%': { transform: 'translate(-2px, -2px)' },
          '60%': { transform: 'translate(2px, 2px)' },
          '80%': { transform: 'translate(2px, -2px)' },
        },
        'neon-pulse': {
          '0%, 100%': { 
            boxShadow: '0 0 5px var(--neon-cyan), 0 0 10px var(--neon-cyan), 0 0 15px var(--neon-cyan)' 
          },
          '50%': { 
            boxShadow: '0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan), 0 0 30px var(--neon-cyan)' 
          },
        },
        'holographic-scan': {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        },
        'skeleton-loading': {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [],
}
```

## Component Library Structure

### 1. Base Components
```
src/
├── components/
│   ├── atoms/
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Toggle/
│   │   └── Icon/
│   ├── molecules/
│   │   ├── Card/
│   │   ├── FormField/
│   │   └── LoadingSpinner/
│   ├── organisms/
│   │   ├── Navigation/
│   │   ├── ChatInterface/
│   │   └── SettingsPanel/
│   └── templates/
│       ├── MainLayout/
│       └── SplitLayout/
```

### 2. Theme Provider
```typescript
// src/contexts/ThemeContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'dark' | 'light' | 'system';

interface ThemeContextType {
  theme: Theme;
  setTheme: (theme: Theme) => void;
  systemTheme: 'dark' | 'light';
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system');
  const [systemTheme, setSystemTheme] = useState<'dark' | 'light'>('dark');

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    setSystemTheme(mediaQuery.matches ? 'dark' : 'light');
    
    const handler = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'dark' : 'light');
    };
    
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, []);

  useEffect(() => {
    const root = document.documentElement;
    const actualTheme = theme === 'system' ? systemTheme : theme;
    root.classList.toggle('dark', actualTheme === 'dark');
    localStorage.setItem('theme', theme);
  }, [theme, systemTheme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, systemTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};
```

### 3. Foldable Device Hook
```typescript
// src/hooks/useFoldableDevice.ts
import { useEffect, useState } from 'react';

interface FoldableState {
  isFoldable: boolean;
  isFolded: boolean;
  screenSpanning: 'none' | 'single-fold-vertical' | 'single-fold-horizontal';
}

export function useFoldableDevice() {
  const [state, setState] = useState<FoldableState>({
    isFoldable: false,
    isFolded: true,
    screenSpanning: 'none',
  });

  useEffect(() => {
    const updateFoldableState = () => {
      const isFoldable = 'screen' in window && 'spanning' in window.screen;
      const screenSpanning = (window.screen as any).spanning || 'none';
      
      setState({
        isFoldable,
        isFolded: window.innerWidth < 768,
        screenSpanning,
      });
    };

    updateFoldableState();
    window.addEventListener('resize', updateFoldableState);
    
    return () => window.removeEventListener('resize', updateFoldableState);
  }, []);

  return state;
}
```

### 4. PWA Configuration
```json
// public/manifest.json
{
  "name": "Cyberpunk Chatbot Hub",
  "short_name": "CyberChat",
  "description": "AI-powered chatbot interface with cyberpunk aesthetics",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0a0a0f",
  "theme_color": "#00ffff",
  "orientation": "any",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "categories": ["productivity", "utilities"],
  "lang": "en",
  "dir": "ltr"
}
```

### 5. Service Worker
```javascript
// public/sw.js
const CACHE_NAME = 'cyberpunk-pwa-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/src/main.tsx',
  '/src/index.css',
  '/icons/icon-192.png',
  '/icons/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
```

## Performance Optimization

### 1. Code Splitting
```typescript
// Lazy load components
const ChatInterface = lazy(() => import('./components/organisms/ChatInterface'));
const SettingsPanel = lazy(() => import('./components/organisms/SettingsPanel'));
```

### 2. Image Optimization
```typescript
// Use responsive images
const ResponsiveImage = ({ src, alt }: { src: string; alt: string }) => (
  <img
    src={src}
    alt={alt}
    loading="lazy"
    srcSet={`${src}?w=320 320w, ${src}?w=640 640w, ${src}?w=1024 1024w`}
    sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  />
);
```

### 3. Font Loading
```css
/* Preload critical fonts */
@font-face {
  font-family: 'Orbitron';
  src: url('/fonts/Orbitron-Regular.woff2') format('woff2');
  font-display: swap;
  font-weight: 400;
}
```

## Testing Strategy

### 1. Accessibility Testing
```bash
npm install -D @axe-core/react
```

### 2. Performance Testing
```bash
npm install -D lighthouse
```

### 3. Foldable Device Testing
- Use Chrome DevTools device emulation
- Test with Surface Duo emulator
- Test with Samsung Galaxy Fold emulator

## Deployment

### 1. Build for Production
```bash
npm run build
```

### 2. Deploy to Netlify
```bash
netlify deploy --prod --dir=dist
```

### 3. Deploy to Vercel
```bash
vercel --prod
```

## Browser Support

| Browser | Minimum Version | Notes |
|---------|----------------|--------|
| Chrome | 88+ | Full support |
| Firefox | 85+ | Full support |
| Safari | 14+ | Full support |
| Edge | 88+ | Full support |
| Samsung Internet | 15+ | Foldable support |

## Next Steps

1. **Set up development environment** using the Quick Start guide
2. **Create base components** following the component structure
3. **Implement theme system** with dark/light mode toggle
4. **Add foldable device support** using the provided hook
5. **Test on actual devices** including foldable phones
6. **Optimize for PWA** with offline functionality
7. **Run accessibility audit** using axe-core
8. **Performance audit** using Lighthouse
9. **Deploy to production** with CDN optimization
10. **Monitor real-world usage** with analytics

## Support

For questions or issues:
- Check the [design system documentation](./cyberpunk-design-system.md)
- Review component examples in `/examples`
- Submit issues to the project repository