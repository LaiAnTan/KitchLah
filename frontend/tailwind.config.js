/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2E7D32',
        secondary: '#66BB6A',
        accent: '#F9A825',
        alert: '#D32F2F',
        neutral: '#9E9E9E',
        background: '#FFFFFF',
        'off-white': '#F5F5F5',
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
