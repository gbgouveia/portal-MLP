/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        mlp: {
          goldLight: "#F2D16D",
          gold: "#BF871F",
          brownDeep: "#8C4303",
          brownSoft: "#A6754B",
          whiteWarm: "#F2F1F0",
          blackCine: "#080605",
        },
      },
      fontFamily: {
        serif: ["Cinzel", "Cinzel Decorative", "Libre Baskerville", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        script: ["Playfair Display", "Great Vibes", "Brush Script MT", "cursive"],
      },
    },
  },
  plugins: [],
}
