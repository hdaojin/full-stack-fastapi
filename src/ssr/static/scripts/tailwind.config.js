const plugin = require('@tailwindcss/typography');
const { postcss } = require('tailwindcss');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/scripts/**/*.js",
   ],
  theme: {
    extend: {},
  },
  daisyui: {
    theme: ["cupcake", "dark"],
  },
  plugins: [
      require('@tailwindcss/typography'),
      require('daisyui'),
    ],
}