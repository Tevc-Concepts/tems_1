/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f3f8',
          100: '#d0dfe9ff',
          500: '#0ea5e9',
          600: '#0970a0', // TEMS Primary
          700: '#035a83ff',
        },
        success: '#10b981',
        warning: '#f59e0b',
        danger: '#ef4444',
        background: '#ebe8e8ff', // TEMS Background
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(27, 27, 27, 0.07), 0 10px 20px -2px rgba(19, 18, 18, 0.04)',
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      },
    },
  },
  plugins: [],
}