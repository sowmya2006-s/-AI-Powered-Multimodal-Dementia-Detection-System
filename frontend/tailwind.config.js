/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4A90E2',
          600: '#2C6DB4',
        },
        soft: '#E8F2FF',
        card: '#FFFFFF',
        muted: '#7D9BCB',
        sub: '#566979',
        bg: '#F4F8FF',
      },
      borderRadius: {
        'radius': '14px',
      },
      boxShadow: {
        'shadow': '0 8px 26px rgba(36,78,140,0.06)',
      }
    },
  },
  plugins: [],
}


