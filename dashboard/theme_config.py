"""
Centralized Color Theme Configuration for Hygen RE MVP
All brand colors are defined here for easy maintenance and consistency.
"""

# Primary Brand Colors
PRIMARY_GREEN = "#046307"
PRIMARY_DARK = "#034b05"
PRIMARY_LIGHT = "#0a8a0d"
ACCENT_GREEN = "#10b817"
SUCCESS_GREEN = "#28a745"

# Background Colors
BACKGROUND_LIGHT = "#F5F9F6"
BACKGROUND_WHITE = "#FFFFFF"
BACKGROUND_CARD = "#FFFFFF"

# Text Colors
TEXT_DARK = "#0D1B0D"
TEXT_MUTED = "#5a6d5b"
TEXT_LIGHT = "#FFFFFF"

# Border & UI Colors
BORDER_LIGHT = "#d1e7d3"
BORDER_MEDIUM = "#b8d9bb"
SHADOW_GREEN = "rgba(4, 99, 7, 0.1)"
SHADOW_GREEN_MEDIUM = "rgba(4, 99, 7, 0.25)"
SHADOW_GREEN_STRONG = "rgba(4, 99, 7, 0.3)"

# Status Colors
STATUS_NEW_BG = "#e8f5e9"
STATUS_NEW_TEXT = PRIMARY_GREEN
STATUS_QUALIFIED_BG = "#d4edda"
STATUS_QUALIFIED_TEXT = SUCCESS_GREEN
STATUS_CONTACTED_BG = "#cce5ff"
STATUS_CONTACTED_TEXT = "#004085"

# Alert Colors
ERROR_BG = "#f8d7da"
ERROR_BORDER = "#dc3545"
WARNING_BG = "#fff3cd"
WARNING_BORDER = "#ffc107"
INFO_BG = "#e8f5e9"
INFO_BORDER = PRIMARY_GREEN
SUCCESS_BG = "#d4edda"
SUCCESS_BORDER = SUCCESS_GREEN

# Gradient Definitions
GRADIENT_PRIMARY = f"linear-gradient(135deg, {PRIMARY_GREEN} 0%, {PRIMARY_LIGHT} 100%)"
GRADIENT_DARK = f"linear-gradient(135deg, {PRIMARY_DARK} 0%, {PRIMARY_GREEN} 100%)"
GRADIENT_BACKGROUND = f"linear-gradient(135deg, {BACKGROUND_LIGHT} 0%, {BACKGROUND_WHITE} 100%)"
GRADIENT_SIDEBAR = f"linear-gradient(180deg, {PRIMARY_GREEN} 0%, {PRIMARY_DARK} 100%)"

# Helper function to get CSS variables
def get_css_variables():
    """Returns CSS custom properties string for injection"""
    return f"""
    :root {{
        --primary-green: {PRIMARY_GREEN};
        --primary-dark: {PRIMARY_DARK};
        --primary-light: {PRIMARY_LIGHT};
        --accent-green: {ACCENT_GREEN};
        --success-green: {SUCCESS_GREEN};
        --background-light: {BACKGROUND_LIGHT};
        --background-white: {BACKGROUND_WHITE};
        --text-dark: {TEXT_DARK};
        --text-muted: {TEXT_MUTED};
        --border-light: {BORDER_LIGHT};
        --shadow-green: {SHADOW_GREEN};
    }}
    """
