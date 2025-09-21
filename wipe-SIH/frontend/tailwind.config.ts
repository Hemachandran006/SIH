import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg: {
          light: '#f6f7fb',
          dark: '#0b1220'
        },
        glass: 'rgba(255, 255, 255, 0.06)'
      },
      boxShadow: {
        soft: '0 10px 30px rgba(0,0,0,0.08)',
        glass: 'inset 0 1px 0 rgba(255,255,255,0.06), 0 10px 30px rgba(0,0,0,0.35)'
      },
      backdropBlur: {
        xs: '2px'
      }
    }
  },
  plugins: []
} satisfies Config