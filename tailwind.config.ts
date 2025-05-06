import type { Config } from "tailwindcss";

export default {
 darkMode: ["class"],
 content: ["./client/index.html", "./client/src/**/*.{js,jsx,ts,tsx}"],
 theme: {
 extend: {
 borderRadius: {
 lg: "var(--radius)",
 md: "calc(var(--radius) - 2px)",
 sm: "calc(var(--radius) - 4px)",
 },
 colors: {
 background: "hsl(var(--background))",
 foreground: "hsl(var(--foreground))",
 card: {
 DEFAULT: "hsl(var(--card))",
 foreground: "hsl(var(--card-foreground))",
 },
 popover: {
 DEFAULT: "hsl(var(--popover))",
 foreground: "hsl(var(--popover-foreground))",
 },
 primary: {
 DEFAULT: "hsl(var(--primary))",
 foreground: "hsl(var(--primary-foreground))",
 },
 secondary: {
 DEFAULT: "hsl(var(--secondary))",
 foreground: "hsl(var(--secondary-foreground))",
 },
 muted: {
 DEFAULT: "hsl(var(--muted))",
 foreground: "hsl(var(--muted-foreground))",
 },
 accent: {
 DEFAULT: "hsl(var(--accent))",
 foreground: "hsl(var(--accent-foreground))",
 },
 destructive: {
 DEFAULT: "hsl(var(--destructive))",
 foreground: "hsl(var(--destructive-foreground))",
 },
 border: "hsl(var(--border))",
 input: "hsl(var(--input))",
 ring: "hsl(var(--ring))",
 chart: {
 "1": "hsl(var(--chart-1))",
 "2": "hsl(var(--chart-2))",
 "3": "hsl(var(--chart-3))",
 "4": "hsl(var(--chart-4))",
 "5": "hsl(var(--chart-5))",
 },
 sidebar: {
 DEFAULT: "hsl(var(--sidebar-background))",
 foreground: "hsl(var(--sidebar-foreground))",
 primary: "hsl(var(--sidebar-primary))",
 "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
 accent: "hsl(var(--sidebar-accent))",
 "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
 border: "hsl(var(--sidebar-border))",
 ring: "hsl(var(--sidebar-ring))",
 },
 },
 keyframes: {
 "accordion-down": {
 from: {
 height: "0",
 },
 to: {
 height: "var(--radix-accordion-content-height)",
 },
 },
 "accordion-up": {
 from: {
 height: "var(--radix-accordion-content-height)",
 },
 to: {
 height: "0",
 },
 },
 "spin-slow": {
 "0%": { transform: "rotate(0deg)" },
 "100%": { transform: "rotate(360deg)" },
 },
 "spin-reverse-slow": {
 "0%": { transform: "rotate(0deg)" },
 "100%": { transform: "rotate(-360deg)" },
 },
 "float": {
 "0%, 100%": { transform: "translateY(0)" },
 "50%": { transform: "translateY(-10px)" },
 },
 "float-delay": {
 "0%, 100%": { transform: "translateY(0)" },
 "50%": { transform: "translateY(10px)" },
 },
 "float-slow": {
 "0%, 100%": { transform: "translateY(0) translateX(0)" },
 "25%": { transform: "translateY(-5px) translateX(5px)" },
 "50%": { transform: "translateY(0) translateX(10px)" },
 "75%": { transform: "translateY(5px) translateX(5px)" },
 },
 },
 animation: {
 "accordion-down": "accordion-down 0.2s ease-out",
 "accordion-up": "accordion-up 0.2s ease-out",
 "spin-slow": "spin-slow 15s linear infinite",
 "spin-reverse-slow": "spin-reverse-slow 12s linear infinite",
 "float": "float 3s ease-in-out infinite",
 "float-delay": "float-delay 4s ease-in-out infinite",
 "float-slow": "float-slow 6s ease-in-out infinite",
 },
 },
 },
 plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
} satisfies Config;
