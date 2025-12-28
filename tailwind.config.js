/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0E0F12",
        fg: "#EDEFF3",
        muted: "#9AA1AE",
        gold: "#D4AF37",
        blue: "#4AC0FF",
        uv: "#8A5CFF",
        grayx: "#7A7F8C"
      },
      boxShadow: {
        glowGold: "0 0 12px rgba(212,175,55,0.25)",
        glowBlue: "0 0 12px rgba(74,192,255,0.25)"
      }
    }
  },
  plugins: []
};
