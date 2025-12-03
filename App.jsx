import React, { useEffect } from 'react';
import DashboardLayout from './components/DashboardLayout';
import './globals.css';

function App() {
  useEffect(() => {
    // Function to update theme based on system preference
    const updateTheme = () => {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      
      if (prefersDark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    };

    // Set initial theme
    updateTheme();

    // Listen for changes in system theme preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Modern browsers support addEventListener
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', updateTheme);
    } else {
      // Fallback for older browsers
      mediaQuery.addListener(updateTheme);
    }

    // Cleanup listener on unmount
    return () => {
      if (mediaQuery.removeEventListener) {
        mediaQuery.removeEventListener('change', updateTheme);
      } else {
        mediaQuery.removeListener(updateTheme);
      }
    };
  }, []);

  return (
    <div>
      <DashboardLayout />
    </div>
  );
}

export default App;
