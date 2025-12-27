/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: "#0f172a",
        primary: "#3b82f6",
        accent: "#10b981",
        card: "rgba(30, 41, 59, 0.7)",
      },
    },
  },
  plugins: [],
};
