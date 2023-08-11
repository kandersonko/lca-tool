/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': [
          'Inter',
          'system-ui',
          'sans-serif',
        ],
        'roboto': ['Roboto', 'sans-serif'],
      },
      colors: {
        'brand': '#F6B700'
      },
    },
  },
  plugins: [],
}
