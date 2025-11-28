/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./pages/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}",
    "./app/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary Navy (Brand Base)
        navy: {
          DEFAULT: '#1A2B45', // Deep Navy - Sidebar background
          light: '#2C3E50',    // Lighter Navy - Hover states
          dark: '#0F172A',     // Darker Navy - Dark mode sidebar
        },
        // Accent Blue (Action/Highlight)
        accent: {
          DEFAULT: '#3B82F6',  // Standard Blue - Primary actions, progress bars
          light: '#60A5FA',    // Lighter blue for hover states
          dark: '#2563EB',     // Darker blue for active states
        },
        // Text Colors
        text: {
          heading: '#111827',   // Near Black - Headings
          body: '#374151',     // Dark Gray - Body text
          muted: '#6B7280',    // Medium Gray - Muted text
        },
        // Status Colors
        status: {
          success: '#10B981',   // Green - Success states
          warning: '#F59E0B',  // Amber - Warning/Action Required
          error: '#EF4444',    // Red - Error states (added for completeness)
          info: '#3B82F6',     // Blue - Info states
        },
        // Background Colors
        bg: {
          main: '#F3F4F6',     // Light Gray/Off-white - Main content area
          card: '#FFFFFF',     // White - Cards
          sidebar: '#1A2B45',  // Deep Navy - Sidebar background
        },
        // Dark Mode Colors
        dark: {
          bg: {
            main: '#111827',   // Very Dark Gray - Main background
            card: '#1F2937',   // Dark Gray - Cards
            sidebar: '#0F172A', // Darker Navy - Sidebar (optional, can use navy.DEFAULT)
          },
          text: {
            primary: '#F9FAFB', // White - Primary text
            secondary: '#D1D5DB', // Light Gray - Secondary text
          },
          border: '#374151',   // Border color for dark mode
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          'Roboto',
          '-apple-system',
          'BlinkMacSystemFont',
          '"Segoe UI"',
          'sans-serif',
        ],
      },
      borderRadius: {
        'card': '0.5rem',      // rounded-lg equivalent
      },
      boxShadow: {
        'card': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)', // shadow-sm
        'card-hover': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
      spacing: {
        'sidebar': '16rem',     // w-64 equivalent (256px)
      },
    },
  },
  plugins: [],
}
