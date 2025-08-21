# Cyberpunk UI/UX Design System for PWA Frontend

## Overview
A comprehensive, production-grade cyberpunk design system optimized for mobile-first PWA development with specific considerations for foldable devices and accessibility compliance.

---

## 1. Design Philosophy

### Core Aesthetic
- **Neon-drenched dystopia**: High contrast dark themes with vibrant neon accents
- **Holographic interfaces**: Translucent overlays with depth and glow effects
- **Glitch aesthetics**: Intentional digital artifacts and distortion effects
- **Cybernetic precision**: Sharp geometric forms with circuit-inspired patterns

### Design Principles
1. **Mobile-first**: Every component designed for mobile before scaling up
2. **Foldable-optimized**: Seamless experience across single-screen, split-screen, and unfolded modes
3. **Accessibility-first**: WCAG 2.1 AA compliance as baseline
4. **Performance-conscious**: Optimized for PWA constraints and offline functionality
5. **Future-proof**: Scalable design tokens and component architecture

---

## 2. Color System

### Primary Palette

#### Dark Theme (Default)
```css
/* Core Colors */
--color-bg-primary: #0a0a0f        /* Deep space black */
--color-bg-secondary: #1a1a2e      /* Dark purple tint */
--color-bg-tertiary: #16213e       /* Midnight blue */

/* Neon Accents */
--color-neon-cyan: #00ffff         /* Electric cyan */
--color-neon-pink: #ff0080         /* Hot pink */
--color-neon-green: #39ff14        /* Matrix green */
--color-neon-purple: #bf00ff       /* Deep purple */
--color-neon-orange: #ff6600       /* Warning orange */

/* Semantic Colors */
--color-success: #00ff88           /* Success green */
--color-warning: #ffaa00           /* Warning amber */
--color-error: #ff0040             /* Error red */
--color-info: #0088ff              /* Info blue */

/* Text Colors */
--color-text-primary: #ffffff      /* Pure white */
--color-text-secondary: #b3b3cc    /* Soft lavender */
--color-text-tertiary: #666680     /* Muted purple */
--color-text-disabled: #404060     /* Dark purple-gray */

/* Border & Divider Colors */
--color-border-primary: #333355    /* Subtle purple border */
--color-border-secondary: #555577  /* Medium purple border */
--color-divider: #2a2a40          /* Dark divider */
```

#### Light Theme (Alternative)
```css
/* Core Colors */
--color-bg-primary: #f8f8ff        /* Soft white */
--color-bg-secondary: #e8e8ff      /* Light lavender */
--color-bg-tertiary: #d8d8ff       /* Pale purple */

/* Neon Accents (adjusted for light) */
--color-neon-cyan: #0099cc         /* Darker cyan */
--color-neon-pink: #cc0066         /* Darker pink */
--color-neon-green: #00cc44        /* Darker green */
--color-neon-purple: #9900cc       /* Darker purple */
--color-neon-orange: #cc4400       /* Darker orange */

/* Text Colors */
--color-text-primary: #0a0a0f      /* Deep black */
--color-text-secondary: #333355    /* Dark purple */
--color-text-tertiary: #555577     /* Medium purple */
--color-text-disabled: #8888aa     /* Light purple-gray */
```

### Color Usage Guidelines
- **Primary actions**: Use neon cyan (#00ffff)
- **Destructive actions**: Use neon pink (#ff0080)
- **Success states**: Use neon green (#39ff14)
- **Warning states**: Use neon orange (#ff6600)
- **Background glows**: Use 20% opacity of neon colors
- **Text on neon**: Always use dark theme background colors

---

## 3. Typography System

### Font Families

#### Primary Typeface
```css
--font-primary: 'Orbitron', 'Rajdhani', system-ui, sans-serif;
/* Weights: 400, 500, 600, 700, 900 */
```

#### Monospace Typeface
```css
--font-mono: 'Fira Code', 'JetBrains Mono', 'Cascadia Code', monospace;
/* For code, data displays, terminal-like interfaces */
```

#### Fallback Stack
```css
--font-fallback: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Type Scale
```css
/* Display */
--text-display-1: 2.5rem;   /* 40px - Hero headlines */
--text-display-2: 2rem;     /* 32px - Page titles */

/* Headings */
--text-h1: 1.75rem;         /* 28px - Main headings */
--text-h2: 1.5rem;          /* 24px - Section headings */
--text-h3: 1.25rem;         /* 20px - Subsection headings */
--text-h4: 1.125rem;        /* 18px - Card headings */
--text-h5: 1rem;            /* 16px - Small headings */
--text-h6: 0.875rem;        /* 14px - Label headings */

/* Body */
--text-body-lg: 1.125rem;   /* 18px - Large body text */
--text-body: 1rem;          /* 16px - Standard body text */
--text-body-sm: 0.875rem;   /* 14px - Small body text */
--text-body-xs: 0.75rem;    /* 12px - Tiny text */

/* Special */
--text-caption: 0.75rem;    /* 12px - Captions */
--text-button: 0.875rem;    /* 14px - Button text */
--text-overline: 0.75rem;   /* 12px - Overline text */
```

### Line Heights
```css
--leading-none: 1;
--leading-tight: 1.25;
--leading-snug: 1.375;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### Letter Spacing
```css
--tracking-tighter: -0.05em;
--tracking-tight: -0.025em;
--tracking-normal: 0;
--tracking-wide: 0.025em;
--tracking-wider: 0.05em;
--tracking-widest: 0.1em;
```

---

## 4. Component Library

### Buttons

#### Primary Button
```css
.cyberpunk-button-primary {
  background: linear-gradient(135deg, var(--color-neon-cyan), var(--color-neon-purple));
  color: var(--color-bg-primary);
  border: 1px solid var(--color-neon-cyan);
  box-shadow: 
    0 0 10px rgba(0, 255, 255, 0.5),
    inset 0 0 10px rgba(0, 255, 255, 0.2);
  font-family: var(--font-primary);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  transition: all 0.3s ease;
}

.cyberpunk-button-primary:hover {
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.8),
    inset 0 0 20px rgba(0, 255, 255, 0.4);
  transform: translateY(-1px);
}

.cyberpunk-button-primary:active {
  transform: translateY(0);
  box-shadow: 
    0 0 5px rgba(0, 255, 255, 0.5),
    inset 0 0 10px rgba(0, 255, 255, 0.3);
}
```

#### Secondary Button
```css
.cyberpunk-button-secondary {
  background: transparent;
  color: var(--color-neon-cyan);
  border: 1px solid var(--color-neon-cyan);
  position: relative;
  overflow: hidden;
}

.cyberpunk-button-secondary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.cyberpunk-button-secondary:hover::before {
  left: 100%;
}
```

#### Destructive Button
```css
.cyberpunk-button-destructive {
  background: linear-gradient(135deg, var(--color-neon-pink), var(--color-error));
  color: var(--color-bg-primary);
  border: 1px solid var(--color-neon-pink);
  box-shadow: 0 0 10px rgba(255, 0, 128, 0.5);
}
```

### Cards

#### Glassmorphism Card
```css
.cyberpunk-card {
  background: rgba(26, 26, 46, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(51, 51, 85, 0.3);
  border-radius: 12px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.cyberpunk-card:hover {
  border-color: var(--color-neon-cyan);
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.3),
    0 0 20px rgba(0, 255, 255, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}
```

#### Holographic Card
```css
.cyberpunk-card-holographic {
  background: linear-gradient(
    135deg,
    rgba(0, 255, 255, 0.1),
    rgba(255, 0, 128, 0.1),
    rgba(191, 0, 255, 0.1)
  );
  border: 1px solid rgba(0, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.cyberpunk-card-holographic::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(0, 255, 255, 0.1),
    transparent
  );
  animation: holographic-shimmer 3s infinite;
}

@keyframes holographic-shimmer {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}
```

### Form Elements

#### Input Fields
```css
.cyberpunk-input {
  background: rgba(10, 10, 15, 0.8);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  color: var(--color-text-primary);
  font-family: var(--font-mono);
  padding: 12px 16px;
  transition: all 0.3s ease;
}

.cyberpunk-input:focus {
  outline: none;
  border-color: var(--color-neon-cyan);
  box-shadow: 
    0 0 0 3px rgba(0, 255, 255, 0.2),
    inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.cyberpunk-input::placeholder {
  color: var(--color-text-tertiary);
  font-style: italic;
}
```

#### Toggle Switches
```css
.cyberpunk-toggle {
  position: relative;
  width: 48px;
  height: 24px;
  background: var(--color-bg-secondary);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cyberpunk-toggle::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: var(--color-text-tertiary);
  border-radius: 50%;
  transition: all 0.3s ease;
}

.cyberpunk-toggle.active {
  background: linear-gradient(135deg, var(--color-neon-cyan), var(--color-neon-purple));
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.cyberpunk-toggle.active::before {
  transform: translateX(24px);
  background: var(--color-bg-primary);
}
```

---

## 5. Responsive Grid System

### Breakpoints

#### Mobile-First Breakpoints
```css
/* Mobile First Approach */
--breakpoint-xs: 320px;   /* Small phones */
--breakpoint-sm: 375px;   /* Standard phones */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Small laptops */
--breakpoint-xl: 1280px;  /* Desktops */
--breakpoint-2xl: 1536px; /* Large screens */
```

#### Foldable Device Breakpoints
```css
/* Samsung Galaxy Z Fold Series */
--breakpoint-fold-closed: 320px;    /* Cover display */
--breakpoint-fold-open: 768px;      /* Main display */

/* Google Pixel Fold */
--breakpoint-pixel-fold-closed: 320px;
--breakpoint-pixel-fold-open: 768px;

/* Microsoft Surface Duo */
--breakpoint-surface-duo-single: 540px;
--breakpoint-surface-duo-dual: 720px;
```

### Grid Layouts

#### Mobile Grid
```css
.cyberpunk-grid-mobile {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  padding: 16px;
}
```

#### Foldable Single Screen
```css
@media (max-width: 767px) {
  .cyberpunk-grid-fold-closed {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
    padding: 12px;
  }
}
```

#### Foldable Unfolded
```css
@media (min-width: 768px) {
  .cyberpunk-grid-fold-open {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    padding: 24px;
  }
}
```

#### Split-Screen Layout
```css
.cyberpunk-split-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: var(--color-border-primary);
}

.cyberpunk-split-panel {
  background: var(--color-bg-primary);
  padding: 16px;
  overflow-y: auto;
}

/* Foldable hinge consideration */
@media (min-width: 768px) and (max-width: 1024px) {
  .cyberpunk-split-layout {
    gap: 24px; /* Space for hinge */
  }
}
```

---

## 6. Animation & Micro-interactions

### Animation Principles
- **Purposeful**: Every animation serves a functional purpose
- **Performant**: 60fps on mobile devices
- **Accessible**: Respect `prefers-reduced-motion`
- **Contextual**: Different animations for different states

### Key Animations

#### Glitch Effect
```css
@keyframes glitch {
  0%, 100% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
}

.cyberpunk-glitch {
  animation: glitch 0.3s ease-in-out;
}
```

#### Neon Pulse
```css
@keyframes neon-pulse {
  0%, 100% { 
    box-shadow: 0 0 5px var(--color-neon-cyan),
                0 0 10px var(--color-neon-cyan),
                0 0 15px var(--color-neon-cyan);
  }
  50% { 
    box-shadow: 0 0 10px var(--color-neon-cyan),
                0 0 20px var(--color-neon-cyan),
                0 0 30px var(--color-neon-cyan);
  }
}

.cyberpunk-neon-pulse {
  animation: neon-pulse 2s ease-in-out infinite;
}
```

#### Holographic Scan
```css
@keyframes holographic-scan {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

.cyberpunk-holographic-scan::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    var(--color-neon-cyan), 
    transparent
  );
  animation: holographic-scan 3s linear infinite;
}
```

### Micro-interactions

#### Button Hover States
```css
.cyberpunk-button-micro {
  position: relative;
  overflow: hidden;
}

.cyberpunk-button-micro::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.cyberpunk-button-micro:hover::after {
  width: 300px;
  height: 300px;
}
```

#### Loading States
```css
.cyberpunk-loading-skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-secondary) 25%,
    var(--color-bg-tertiary) 50%,
    var(--color-bg-secondary) 75%
  );
  background-size: 200% 100%;
  animation: loading-shimmer 1.5s infinite;
}

@keyframes loading-shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

---

## 7. Iconography System

### Icon Style
- **Stroke width**: 2px for most icons, 1.5px for small icons
- **Style**: Geometric, sharp corners, circuit-inspired
- **Size system**: 12px, 16px, 20px, 24px, 32px, 48px
- **Color**: Inherit from text color, neon accents for active states

### Icon Categories

#### Navigation Icons
- Home: House with circuit lines
- Back: Arrow with glitch effect
- Menu: Hamburger with neon glow
- Close: X with animated rotation

#### Action Icons
- Send: Paper plane with trail effect
- Delete: Trash with neon outline
- Edit: Pencil with glow effect
- Settings: Gear with rotation animation

#### Status Icons
- Success: Checkmark with pulse
- Warning: Triangle with glow
- Error: X with shake animation
- Loading: Spinner with neon trail

### Icon Implementation
```css
.cyberpunk-icon {
  display: inline-block;
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
  transition: all 0.3s ease;
}

.cyberpunk-icon-neon {
  filter: drop-shadow(0 0 3px currentColor);
}
```

---

## 8. Theme System

### Dark Theme (Default)
```css
[data-theme="dark"] {
  --color-bg-primary: #0a0a0f;
  --color-bg-secondary: #1a1a2e;
  --color-bg-tertiary: #16213e;
  --color-text-primary: #ffffff;
  --color-text-secondary: #b3b3cc;
  --color-text-tertiary: #666680;
}
```

### Light Theme
```css
[data-theme="light"] {
  --color-bg-primary: #f8f8ff;
  --color-bg-secondary: #e8e8ff;
  --color-bg-tertiary: #d8d8ff;
  --color-text-primary: #0a0a0f;
  --color-text-secondary: #333355;
  --color-text-tertiary: #555577;
}
```

### Theme Toggle Component
```css
.cyberpunk-theme-toggle {
  position: relative;
  width: 64px;
  height: 32px;
  background: linear-gradient(135deg, var(--color-neon-cyan), var(--color-neon-purple));
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cyberpunk-theme-toggle::before {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  width: 24px;
  height: 24px;
  background: var(--color-bg-primary);
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.cyberpunk-theme-toggle[data-theme="light"]::before {
  transform: translateX(32px);
}
```

---

## 9. Foldable Device Strategies

### Layout Adaptation

#### Single Screen Mode (Closed)
```css
@media (max-width: 767px) {
  .cyberpunk-layout {
    grid-template-areas:
      "header"
      "main"
      "footer";
    grid-template-rows: auto 1fr auto;
    height: 100vh;
  }
}
```

#### Split Screen Mode (Folded)
```css
@media (min-width: 768px) and (max-width: 1024px) {
  .cyberpunk-layout-split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px; /* Space for hinge */
    height: 100vh;
  }
  
  .cyberpunk-panel-left {
    border-right: 1px solid var(--color-border-primary);
  }
}
```

#### Unfolded Tablet Mode
```css
@media (min-width: 1025px) {
  .cyberpunk-layout-tablet {
    grid-template-areas:
      "sidebar header"
      "sidebar main"
      "sidebar footer";
    grid-template-columns: 280px 1fr;
    grid-template-rows: auto 1fr auto;
    height: 100vh;
  }
}
```

### Content Adaptation

#### Responsive Content
```css
.cyberpunk-responsive-content {
  /* Single column on phones */
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 768px) {
  .cyberpunk-responsive-content {
    /* Two columns on foldables */
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

@media (min-width: 1024px) {
  .cyberpunk-responsive-content {
    /* Three columns on tablets */
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }
}
```

---

## 10. PWA-Specific Considerations

### Offline States

#### Offline Indicator
```css
.cyberpunk-offline-indicator {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, var(--color-warning), var(--color-neon-orange));
  color: var(--color-bg-primary);
  padding: 8px 16px;
  text-align: center;
  font-weight: 600;
  transform: translateY(-100%);
  transition: transform 0.3s ease;
  z-index: 1000;
}

.cyberpunk-offline-indicator.show {
  transform: translateY(0);
}
```

#### Offline Content
```css
.cyberpunk-offline-content {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: 8px;
  padding: 24px;
  text-align: center;
}

.cyberpunk-offline-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  color: var(--color-text-tertiary);
}
```

### Install Prompt

#### Install Banner
```css
.cyberpunk-install-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--color-neon-cyan);
  padding: 16px;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  z-index: 1000;
}

.cyberpunk-install-banner.show {
  transform: translateY(0);
}
```

### Loading Skeletons

#### Skeleton Screens
```css
.cyberpunk-skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-secondary) 25%,
    var(--color-bg-tertiary) 50%,
    var(--color-bg-secondary) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 4px;
}

@keyframes skeleton-loading {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

---

## 11. Accessibility Compliance

### WCAG 2.1 Guidelines

#### Color Contrast
- **Normal text**: 4.5:1 minimum contrast ratio
- **Large text**: 3:1 minimum contrast ratio
- **Interactive elements**: 3:1 minimum contrast ratio
- **Focus indicators**: 3:1 minimum contrast ratio

#### Focus Management
```css
.cyberpunk-focus-visible {
  outline: 2px solid var(--color-neon-cyan);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px rgba(0, 255, 255, 0.2);
}

/* Remove default outline when using custom focus */
.cyberpunk-focus-visible:focus:not(:focus-visible) {
  outline: none;
  box-shadow: none;
}
```

#### Screen Reader Support
```css
/* Visually hidden but accessible to screen readers */
.cyberpunk-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

#### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .cyberpunk-animation,
  .cyberpunk-glitch,
  .cyberpunk-neon-pulse,
  .cyberpunk-holographic-scan {
    animation: none;
    transition: none;
  }
}
```

### Keyboard Navigation
```css
.cyberpunk-keyboard-nav :focus {
  outline: 2px solid var(--color-neon-cyan);
  outline-offset: 2px;
}

.cyberpunk-keyboard-nav [tabindex]:focus,
.cyberpunk-keyboard-nav button:focus,
.cyberpunk-keyboard-nav input:focus,
.cyberpunk-keyboard-nav select:focus,
.cyberpunk-keyboard-nav textarea:focus {
  box-shadow: 0 0 0 4px rgba(0, 255, 255, 0.2);
}
```

---

## 12. Implementation Guide

### CSS Architecture

#### Design Tokens
```css
/* tokens.css */
:root {
  /* Colors */
  --color-primary: var(--color-neon-cyan);
  --color-secondary: var(--color-neon-purple);
  --color-accent: var(--color-neon-pink);
  
  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  
  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.1);
  --shadow-md: 0