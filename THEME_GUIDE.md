# Hygen RE Dashboard - UI Theme Documentation

## Color Palette

The Hygen RE MVP uses a professional green color scheme centered around **#046307** as the primary brand color.

### Primary Colors
- **Primary Green**: `#046307` - Main brand color used for headers, primary buttons, and key UI elements
- **Primary Dark**: `#034b05` - Darker shade for hover states and emphasis
- **Primary Light**: `#0a8a0d` - Lighter shade for gradients and accents
- **Accent Green**: `#10b817` - Bright accent for highlights
- **Success Green**: `#28a745` - Success states and positive actions

### Background Colors
- **Light Background**: `#F5F9F6` - Soft green-tinted background for main app
- **White Background**: `#FFFFFF` - Cards, forms, and content areas
- **Gradient**: Linear gradient from light green to white

### Text Colors
- **Dark Text**: `#0D1B0D` - Primary text color (very dark green)
- **Muted Text**: `#5a6d5b` - Secondary text, captions, and labels
- **White Text**: `#FFFFFF` - Text on dark/colored backgrounds

### Border & Shadow Colors
- **Light Border**: `#d1e7d3` - Subtle borders for cards and inputs
- **Green Shadow**: `rgba(4, 99, 7, 0.1)` - Soft shadow with green tint

## Theme Configuration Files

### 1. `.streamlit/config.toml`
Global Streamlit theme configuration. Controls:
- Primary color for widgets and interactive elements
- Background colors for app and secondary elements
- Text color
- Font family

**Location**: `dashboard/.streamlit/config.toml`

### 2. `theme_config.py`
Centralized Python configuration file containing all color constants. Use this file when you need color values in Python code.

**Location**: `dashboard/theme_config.py`

**Usage**:
```python
from theme_config import PRIMARY_GREEN, GRADIENT_PRIMARY

# Use in string formatting
st.markdown(f"<div style='color: {PRIMARY_GREEN};'>Text</div>", unsafe_allow_html=True)
```

### 3. Custom CSS in `dashboard.py`
Comprehensive CSS injection at the top of the dashboard file. Styles all Streamlit components including:
- Buttons (primary and secondary)
- Form inputs (text, select, textarea)
- DataFrames and tables
- Cards and containers
- Status badges
- Info/success/error boxes
- Headers and typography
- Links and dividers

## Themed Components

### Buttons
- **Primary Buttons**: Green gradient background with shadow and hover effects
- **Secondary Buttons**: White background with green border, transforms to solid green on hover
- **Back Buttons**: Standard secondary styling with arrow emoji

### Form Elements
- **Text Inputs**: Light border with green focus ring
- **Select Boxes**: Rounded corners with green accent on focus
- **Labels**: Bold, dark green text

### Data Tables
- **Headers**: Green gradient background with white text
- **Rows**: Alternating light green/white rows
- **Hover**: Light green highlight on hover

### Status Badges
Custom classes for different status types:
- `.status-new`: New leads (light green)
- `.status-qualified`: Qualified leads (success green)
- `.status-contacted`: Contacted leads (blue)

### Cards & Containers
- White background with subtle green shadow
- Rounded corners (12px)
- Light green border

## Customization Guide

### Changing Colors

1. **Global Theme Colors**: Edit `dashboard/.streamlit/config.toml`
   ```toml
   [theme]
   primaryColor = "#046307"  # Change this to update main accent color
   ```

2. **All Other Colors**: Edit `dashboard/theme_config.py`
   ```python
   PRIMARY_GREEN = "#046307"  # Update this constant
   ```

3. **CSS Variables**: The custom CSS in `dashboard.py` automatically uses the values from `:root` CSS variables

### Adding New Styled Components

1. Define color constants in `theme_config.py` if needed
2. Add CSS rules in the `<style>` block in `dashboard.py`
3. Use CSS classes or inline styles with the color constants

Example:
```python
st.markdown(f"""
<div class="custom-card" style="background: {BACKGROUND_WHITE}; border: 2px solid {PRIMARY_GREEN};">
    Content here
</div>
""", unsafe_allow_html=True)
```

### Testing Theme Changes

After making changes:
1. Save the modified files
2. Restart the Streamlit server: `streamlit run dashboard/dashboard.py`
3. Hard refresh the browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

## Design Principles

1. **Consistency**: All green shades derive from the primary brand color
2. **Accessibility**: Text colors meet WCAG contrast requirements
3. **Hierarchy**: Darker greens for emphasis, lighter for backgrounds
4. **Interactivity**: Hover and focus states use color shifts for feedback
5. **Professionalism**: Subtle shadows and gradients add depth without distraction

## Browser Compatibility

The theme uses modern CSS features:
- CSS Custom Properties (CSS Variables)
- Flexbox and Grid
- Linear Gradients
- Box Shadow
- Border Radius
- Transitions

**Supported Browsers**: Chrome 49+, Firefox 31+, Safari 9.1+, Edge 15+

## Troubleshooting

### Theme not applying
- Ensure `.streamlit/config.toml` is in the correct location (`dashboard/.streamlit/`)
- Clear browser cache and hard refresh
- Restart Streamlit server
- Check browser console for CSS errors

### Colors look different
- Check if browser extensions (dark mode, color filters) are interfering
- Verify color values in theme files match expected hex codes
- Ensure no conflicting CSS from other sources

### Changes not visible
- Streamlit caches CSS - use `st.cache_data.clear()` or restart server
- Browser may cache styles - use hard refresh (Cmd+Shift+R / Ctrl+Shift+R)

## Future Enhancements

Potential theme improvements:
- [ ] Dark mode support with alternative color palette
- [ ] Custom icon set matching brand colors
- [ ] Animated transitions for page changes
- [ ] Responsive breakpoints for mobile optimization
- [ ] Print stylesheet with simplified colors
- [ ] High contrast mode for accessibility
