/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#165DFF',
        success: '#36CFC9',
        danger: '#FF4D4F',
        background: '#F9FAFB',
        card: '#FFFFFF',
        text: {
          primary: '#1D2129',
          secondary: '#6E7681',
        },
        border: '#E5E6EB',
      },
      fontSize: {
        'xs': '12px',
        'sm': '14px',
        'base': '16px',
        'lg': '18px',
        'xl': '20px',
      },
    },
  },
  plugins: [],
}