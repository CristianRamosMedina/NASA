module.exports = {
  content: ["./views/**/*.ejs", "./public/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        orbitron: ["Orbitron", "sans-serif"],
      },
      colors: {
        "space-dark": "#0b0d17",
        "space-star": "#f8fafc",
        "nasa": "#ff4c4c",
        "rocket": "#3b82f6",
        "planet": "#10b981",
      },
    },
  },
  plugins: [],
};
