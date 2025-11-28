# CareerLens Design System

This document outlines the design system configuration for CareerLens, an AI Career Copilot for the Hong Kong market.

## Color Palette

### Primary Navy (Brand Base)
- **Deep Navy** (`#1A2B45`): Sidebar background
- **Lighter Navy** (`#2C3E50`): Hover states in sidebar
- **Darker Navy** (`#0F172A`): Dark mode sidebar (optional)

### Accent Blue (Action/Highlight)
- **Standard Blue** (`#3B82F6`): Primary buttons, progress bars, logos
- **Light Blue** (`#60A5FA`): Hover states
- **Dark Blue** (`#2563EB`): Active states

### Text Colors
- **Headings**: `#111827` (Near Black)
- **Body Text**: `#374151` (Dark Gray)
- **Muted Text**: `#6B7280` (Medium Gray)

### Status Colors
- **Success**: `#10B981` (Green) - Salary band arrows, positive indicators
- **Warning**: `#F59E0B` (Amber) - Action required, warnings
- **Error**: `#EF4444` (Red) - Error states
- **Info**: `#3B82F6` (Blue) - Informational messages

### Background Colors
- **Main Content Area**: `#F3F4F6` (Light Gray/Off-white)
- **Cards**: `#FFFFFF` (White) with subtle shadow
- **Sidebar**: `#1A2B45` (Deep Navy)

### Dark Mode Colors
- **Main Background**: `#111827` (Very Dark Gray)
- **Cards**: `#1F2937` (Dark Gray) with lighter borders `#374151`
- **Sidebar**: `#0F172A` (Darker Navy) or `#1A2B45` (Deep Navy)
- **Primary Text**: `#F9FAFB` (White)
- **Secondary Text**: `#D1D5DB` (Light Gray)

## Typography

- **Font Family**: Inter (primary), Roboto (fallback)
- **Font Stack**: `'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Professional, clean, and legible for data-heavy dashboards

## Component Styling

### Cards
- Rounded corners: `rounded-lg` (0.5rem)
- Border: `border-gray-200` (light) / `border-gray-700` (dark)
- Shadow: `shadow-sm` (subtle shadow)
- Hover: Slight elevation with `shadow-card-hover`

### Sidebar
- Fixed width: `w-64` (16rem / 256px)
- Full height
- Background: Deep Navy (`#1A2B45`)
- Text: White
- Hover states: Lighter Navy (`#2C3E50`)

### Buttons

#### Primary Button
- Background: Accent Blue (`#3B82F6`)
- Text: White
- Hover: Darker blue (`#2563EB`)
- Rounded: `rounded-lg`
- Shadow: Subtle shadow on hover

#### Secondary Button
- Background: White (light) / Dark Gray (dark)
- Text: Black (light) / White (dark)
- Border: `border-gray-300` (light) / `border-gray-700` (dark)
- Hover: Light gray background shift

## Dark Mode

- **Strategy**: Class-based (`class` strategy)
- Toggle dark mode by adding/removing `dark` class to the root element
- All colors automatically adapt based on dark mode state

## Usage Examples

### Using Tailwind Classes

```jsx
// Card
<div className="card card-hover">
  <h2 className="text-heading">Card Title</h2>
  <p className="text-body">Card content</p>
</div>

// Primary Button
<button className="btn-primary">Click Me</button>

// Sidebar Item
<div className="sidebar-item sidebar-item-active">Dashboard</div>

// Match Score Badge
<div className="match-score">85% Match</div>
```

### Using CSS Variables

```css
.custom-element {
  background-color: var(--color-bg-card);
  color: var(--color-text-heading);
  border-color: var(--color-border-light);
}
```

### Dark Mode Toggle

```javascript
// Toggle dark mode
document.documentElement.classList.toggle('dark');
```

## File Structure

```
/workspace
├── tailwind.config.js    # Tailwind configuration with custom colors
├── globals.css           # Global styles and CSS variables
├── postcss.config.js     # PostCSS configuration
└── package.json          # Dependencies
```

## Setup Instructions

1. Install dependencies:
   ```bash
   npm install
   ```

2. Import globals.css in your main entry file:
   ```javascript
   import './globals.css'
   ```

3. Use Tailwind classes in your components:
   ```jsx
   <div className="bg-bg-main text-text-body">
     <h1 className="text-heading">CareerLens</h1>
   </div>
   ```

4. Enable dark mode by adding `dark` class to root element:
   ```javascript
   document.documentElement.classList.add('dark');
   ```

## Component Classes

### Pre-built Component Classes

- `.card` - Card container with styling
- `.card-hover` - Card with hover effects
- `.sidebar` - Sidebar container
- `.sidebar-item` - Sidebar navigation item
- `.btn-primary` - Primary button
- `.btn-secondary` - Secondary button
- `.input` - Form input field
- `.badge` - Badge/tag component
- `.match-score` - Match score badge
- `.progress-bar` - Progress bar container
- `.progress-fill` - Progress bar fill

### Utility Classes

- `.text-heading` - Heading text color
- `.text-body` - Body text color
- `.text-muted` - Muted text color
- `.bg-main` - Main background
- `.bg-card` - Card background
- `.border-card` - Card border
- `.main-content` - Main content area (with sidebar spacing)
- `.scrollbar-thin` - Custom thin scrollbar

## Notes

- All colors are defined in both Tailwind config and CSS variables for maximum flexibility
- Dark mode is fully implemented with class-based strategy
- Typography uses Inter font for professional appearance
- All components include proper hover and focus states for accessibility
- Custom scrollbar styles included for better UX
