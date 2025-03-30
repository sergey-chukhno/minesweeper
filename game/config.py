"""
Configuration values for Minesweeper.
"""

# Difficulty levels
BEGINNER = {
    "name": "beginner",
    "rows": 9,
    "cols": 9,
    "mines": 10
}

INTERMEDIATE = {
    "name": "intermediate",
    "rows": 16,
    "cols": 16,
    "mines": 40
}

EXPERT = {
    "name": "expert",
    "rows": 16,
    "cols": 30,
    "mines": 99
}

# Game states
GAME_READY = 0   # Game is ready to start
GAME_PLAYING = 1 # Game is in progress
GAME_WON = 2     # Game is won
GAME_LOST = 3    # Game is lost

# UI Colors - Neon Futuristic Theme
UI_COLORS = {
    # Background colors
    "bg_main": "#0A0A1A",         # Very dark blue/black for main background
    "bg_header": "#0D0D1F",       # Dark blue for header
    "bg_grid": "#0A0A1A",         # Dark blue for grid background
    
    # Cell colors
    "cell_bg": "#0A0A1A",         # Dark background for unrevealed cells
    "cell_revealed": "#121225",   # Slightly lighter for revealed cells
    "cell_hover": "#1A1A3A",      # Blue hover effect
    "cell_mine": "#FF2020",       # Bright red for mines
    "cell_wrong": "#5A1A1A",      # Dark red for incorrect flags
    "cell_border": "#1A1A4A",     # Subtle blue border
    
    # Neon accent colors
    "neon_cyan": "#00F0FF",       # Bright cyan for neon effects
    "neon_blue": "#2F80ED",       # Bright blue
    "neon_pink": "#FF80FF",       # Neon pink
    "neon_green": "#00FF99",      # Neon green
    "neon_yellow": "#FFFC00",     # Neon yellow
    
    # Button colors
    "btn_bg": "#0D0D1F",          # Dark blue background
    "btn_hover": "#1A1A3A",       # Lighter blue on hover
    "btn_border": "#00F0FF",      # Neon cyan border
}

# Text colors
TEXT_COLORS = {
    "status": "#00FFFF",  # Cyan for status messages
    "win": "#00FF99",     # Neon green for win messages
    "lose": "#FF5555",    # Bright red for lose messages
    "timer": "#00FFFF",   # Cyan for timer
}

# Emojis
EMOJIS = {
    "mine": "💣",
    "flag": "🚩",
    "wrong": "❌",
    "ready": "😎",
    "win": "🏆",
    "lose": "💀",
    "timer": "⏱️"
}

# Colors for the UI
UI_COLORS = {
    "background": "#051224",  # Main background
    "frame_bg": "#081830",    # Frame background
    "dark_bg": "#070E1A",     # Dark background (for counters)
    "hover": "#152238",       # Hover color
    "cell_bg": "#0A1428",     # Cell background
    "cell_border": "#101B2D", # Cell border
    "cell_revealed": "#101B2D", # Revealed cell
    "mine_bg": "#330000",     # Mine background
    "new_game_bg": "#0A3257", # New game button background
    "new_game_hover": "#154275", # New game button hover
    "new_game_border": "#00BFFF", # New game button border
    "exit_bg": "#321030",     # Exit button background
    "exit_hover": "#4A1846",  # Exit button hover
    "exit_border": "#FF69B4", # Exit button border
}

# Text colors for numbers and UI elements
TEXT_COLORS = {
    "mines": "#00BFFF",       # Mines counter
    "flags": "#FF3333",       # Flags counter
    "timer": "#00FF7F",       # Timer
    "status": "#00BFFF",      # Status message
    "win": "#00FF7F",         # Win message
    "lose": "#FF3333",        # Lose message
    "flag": "#FF3333",        # Flag color
    "question": "#3399FF",    # Question mark color
    "mine": "#FF0000",        # Mine color
}

# Number colors for adjacent mines (1-8)
NUMBER_COLORS = {
    0: "#001833",  # Empty cell - dark blue
    1: "#00BFFF",  # 1 adjacent mine - light blue
    2: "#00FF7F",  # 2 adjacent mines - green
    3: "#FF6347",  # 3 adjacent mines - red
    4: "#800080",  # 4 adjacent mines - purple
    5: "#FF00FF",  # 5 adjacent mines - magenta
    6: "#FFD700",  # 6 adjacent mines - gold
    7: "#FF69B4",  # 7 adjacent mines - pink
    8: "#FF4500",  # 8 adjacent mines - orange
}

# Cell states
CELL_COVERED = 0
CELL_FLAGGED = 1
CELL_QUESTION = 2
CELL_REVEALED = 3

# File paths
HIGH_SCORES_FILE = "high_scores.json"
SOUNDS_DIR = "game/assets/sounds"

# Sound settings
SOUND_SETTINGS = {
    "sound_volume": 0.5,
    "music_volume": 0.3,
    "enabled": True
}

DEFAULT_HIGH_SCORES = {
    "Beginner": 999,
    "Intermediate": 999,
    "Expert": 999
} 