# Streamlit Theme Configuration - CareerLens Design System

## Overview

The Streamlit theme has been configured to match the **CareerLens Design System** with a professional navy and blue color scheme.

## Files Updated

### 1. `.streamlit/config.toml`
✅ **Updated** - Theme colors now match CareerLens design system

**Light Mode:**
- Primary Color: `#3B82F6` (Accent Blue)
- Background: `#F3F4F6` (Light Gray/Off-white)
- Secondary Background: `#FFFFFF` (White cards)
- Text Color: `#111827` (Near Black headings)

**Dark Mode:**
- Primary Color: `#3B82F6` (Accent Blue - consistent)
- Background: `#111827` (Very Dark Gray)
- Secondary Background: `#1F2937` (Dark Gray cards)
- Text Color: `#F9FAFB` (White)

### 2. `app.py` - CSS Variables
✅ **Updated** - Custom CSS variables now match CareerLens design system

**Key Changes:**
- `--primary-accent`: Changed from `#00796B` to `#3B82F6` (Accent Blue)
- `--action-accent`: Changed from `#FFC107` to `#3B82F6` (Accent Blue)
- `--bg-main`: Changed from `#FAFAFA` to `#F3F4F6` (CareerLens main background)
- `--bg-container`: Changed from `#F0F0F0` to `#FFFFFF` (White cards)
- `--text-primary`: Changed from `#333333` to `#111827` (CareerLens headings)
- `--text-secondary`: Changed from `#666666` to `#374151` (CareerLens body text)
- Added `--success-green`: `#10B981` (CareerLens success color)
- Added `--warning-amber`: `#F59E0B` (CareerLens warning color)
- Added `--error-red`: `#EF4444` (CareerLens error color)
- Added `--navy-deep`: `#1A2B45` / `#0F172A` (Navy for sidebar)
- Added `--navy-light`: `#2C3E50` / `#1A2B45` (Navy hover states)

## Color Palette Reference

### Primary Colors
| Color | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| **Accent Blue** | `#3B82F6` | `#3B82F6` | Primary buttons, links, highlights |
| **Light Blue** | `#60A5FA` | `#60A5FA` | Hover states |
| **Dark Blue** | `#2563EB` | `#2563EB` | Active states |

### Navy Colors (Sidebar)
| Color | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| **Deep Navy** | `#1A2B45` | `#0F172A` | Sidebar background |
| **Lighter Navy** | `#2C3E50` | `#1A2B45` | Hover states |

### Text Colors
| Color | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| **Headings** | `#111827` | `#F9FAFB` | Main headings |
| **Body Text** | `#374151` | `#D1D5DB` | Body text |
| **Muted Text** | `#6B7280` | `#9CA3AF` | Secondary/muted text |

### Status Colors
| Color | Value | Usage |
|-------|-------|-------|
| **Success** | `#10B981` | Success states, positive indicators |
| **Warning** | `#F59E0B` | Warnings, action required |
| **Error** | `#EF4444` | Error states |

### Background Colors
| Color | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| **Main Background** | `#F3F4F6` | `#111827` | Main content area |
| **Card Background** | `#FFFFFF` | `#1F2937` | Cards and containers |

## Configuration Details

### Theme Settings in `config.toml`

```toml
[theme]
base = "light"
primaryColor = "#3B82F6"
backgroundColor = "#F3F4F6"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#111827"
font = "sans serif"

[theme.dark]
primaryColor = "#3B82F6"
backgroundColor = "#111827"
secondaryBackgroundColor = "#1F2937"
textColor = "#F9FAFB"
font = "sans serif"
```

### Additional Configuration

- **File Watcher**: Auto (for development)
- **Usage Stats**: Disabled
- **Logger Level**: Error (reduces noise)
- **UI Elements**: Standard (hamburger menu visible)

## CSS Variables in `app.py`

All custom CSS in `app.py` now uses CareerLens design system colors via CSS variables:

```css
:root {
    --primary-accent: #3B82F6;
    --action-accent: #3B82F6;
    --bg-main: #F3F4F6;
    --bg-container: #FFFFFF;
    --text-primary: #111827;
    --text-secondary: #374151;
    --success-green: #10B981;
    --warning-amber: #F59E0B;
    --error-red: #EF4444;
    --navy-deep: #1A2B45;
    --navy-light: #2C3E50;
}
```

## Verification Checklist

- [x] Theme colors match CareerLens design system
- [x] Light mode colors configured correctly
- [x] Dark mode colors configured correctly
- [x] CSS variables updated in `app.py`
- [x] Match score colors use design system colors
- [x] Status colors (success/warning/error) match design system
- [x] Background colors match design system
- [x] Text colors match design system

## Testing the Theme

1. **Start Streamlit:**
   ```bash
   streamlit run app.py
   ```

2. **Test Light Mode:**
   - Default theme should show navy blue accents
   - Background should be light gray (`#F3F4F6`)
   - Cards should be white (`#FFFFFF`)
   - Buttons should be blue (`#3B82F6`)

3. **Test Dark Mode:**
   - Go to Settings → Theme → Dark
   - Background should be very dark gray (`#111827`)
   - Cards should be dark gray (`#1F2937`)
   - Text should be white/light gray
   - Buttons should remain blue (`#3B82F6`)

## Additional Recommendations

### 1. Sidebar Styling
If you want to style the Streamlit sidebar to match the navy theme, you can add this to the CSS in `app.py`:

```css
/* Sidebar - Navy Background */
[data-testid="stSidebar"] {
    background-color: var(--navy-deep) !important;
}

[data-testid="stSidebar"] * {
    color: white !important;
}
```

### 2. Custom Font Loading
To ensure Inter font is loaded (as per design system), add to the CSS:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

body {
    font-family: 'Inter', 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}
```

### 3. Consistent Button Styling
Buttons are already styled via CSS variables, but you can enhance them:

```css
.stButton > button[kind="primary"] {
    background-color: var(--primary-accent) !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: var(--accent-dark) !important; /* #2563EB */
    transform: translateY(-1px) !important;
}
```

## Notes

- The theme configuration is now consistent with the CareerLens design system
- All colors match the `DESIGN_SYSTEM.md` specification
- Dark mode is fully supported with appropriate color adjustments
- CSS variables ensure easy maintenance and consistency
- The theme works with Streamlit's built-in theme switcher

## Troubleshooting

**Issue:** Colors not updating
- **Solution:** Clear browser cache and restart Streamlit

**Issue:** Dark mode not working
- **Solution:** Check that `[theme.dark]` section exists in `config.toml`

**Issue:** CSS variables not applying
- **Solution:** Ensure CSS is loaded after Streamlit's default styles (it should be in the `st.markdown()` call early in `app.py`)

---

**Last Updated:** Configuration matches CareerLens Design System v1.0
**Files Modified:** `.streamlit/config.toml`, `app.py` (CSS section)
