"""
UI Manager for Minesweeper.
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from game.settings import (
    UI_COLORS, TEXT_COLORS, EMOJIS,
    GAME_READY, GAME_PLAYING, GAME_WON, GAME_LOST
)

class UIManager:
    """
    Manages the user interface for Minesweeper.
    """
    def __init__(self, root, on_reset, on_new_game, on_exit, on_difficulty_change):
        """
        Initialize the UI manager.
        
        Parameters:
        - root: The parent CTk widget
        - on_reset: Callback for reset button
        - on_new_game: Callback for new game button
        - on_exit: Callback for exit button
        - on_difficulty_change: Callback for difficulty change
        """
        self.root = root
        self.on_reset = on_reset
        self.on_new_game = on_new_game
        self.on_exit = on_exit
        self.on_difficulty_change = on_difficulty_change
        
        # Store images as attributes to prevent garbage collection
        self.bg_image = None
        self.bg_photo = None
        
        # Create UI components - starting with a clean approach
        self._create_main_container()
        self._create_header()
        self._create_grid_frame()
        self._create_status_bar()
        self._create_help_button()
    
    def _create_main_container(self):
        """Create the main container for all UI elements with a dark neon futuristic theme."""
        # Create a main container frame with a dark blue/purple gradient-like background
        self.main_container = ctk.CTkFrame(self.root, fg_color="#0A0A1A")
        
        # Create a semi-transparent frame for UI elements with neon accents
        self.ui_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color="#121225",  # Dark blue-purple base
            corner_radius=12     # Rounded corners for modern look
        )
        self.ui_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Add a neon accent border to the UI frame
        self.ui_frame.configure(border_width=2, border_color="#00C2FF")
        
        print("Created futuristic neon UI container")
    
    def _create_header(self):
        """Create the header with game controls in neon style."""
        # Header frame with semi-transparent dark background
        self.header_frame = ctk.CTkFrame(self.ui_frame, fg_color="#0D0D1F", corner_radius=10)
        self.header_frame.configure(border_width=1, border_color="#00F0FF")  # Bright cyan neon border
        self.header_frame.pack(padx=15, pady=15, fill="x")
        
        # Game info row
        self.info_frame = ctk.CTkFrame(self.header_frame, fg_color="#0A0A1A", corner_radius=8)
        self.info_frame.pack(padx=12, pady=12, fill="x")
        
        # Mines counter with enhanced neon glow effect
        self.mines_frame = ctk.CTkFrame(self.info_frame, fg_color="#0A0A1A", corner_radius=5)
        self.mines_frame.configure(border_width=1, border_color="#00F0FF")  # Neon cyan border
        self.mines_frame.pack(side="left", padx=10)
        
        self.mines_label = ctk.CTkLabel(
            self.mines_frame, 
            text=f"{EMOJIS['mine']} 0", 
            font=("Consolas", 18, "bold"),
            text_color="#00FFFF"  # Bright cyan for neon effect
        )
        self.mines_label.pack(padx=12, pady=8)
        
        # Flags counter with enhanced neon glow effect
        self.flags_frame = ctk.CTkFrame(self.info_frame, fg_color="#0A0A1A", corner_radius=5)
        self.flags_frame.configure(border_width=1, border_color="#FF00FF")  # Pink neon border
        self.flags_frame.pack(side="left", padx=10)
        
        self.flags_label = ctk.CTkLabel(
            self.flags_frame, 
            text=f"{EMOJIS['flag']} 0", 
            font=("Consolas", 18, "bold"),
            text_color="#FF80FF"  # Light pink for neon effect
        )
        self.flags_label.pack(padx=12, pady=8)
        
        # Timer with enhanced neon glow effect
        self.timer_frame = ctk.CTkFrame(self.info_frame, fg_color="#0A0A1A", corner_radius=5)
        self.timer_frame.configure(border_width=1, border_color="#00F0FF")  # Neon cyan border
        self.timer_frame.pack(side="right", padx=10)
        
        self.timer_label = ctk.CTkLabel(
            self.timer_frame, 
            text=f"{EMOJIS['timer']} 000", 
            font=("Consolas", 18, "bold"),
            text_color="#00FFFF"  # Bright cyan for neon effect
        )
        self.timer_label.pack(padx=12, pady=8)
        
        # Reset button with neon effect
        self.reset_button = ctk.CTkButton(
            self.info_frame,
            text=EMOJIS["ready"],
            font=("Arial", 16, "bold"),
            width=50,
            height=40,
            fg_color="#0D0D1F",
            hover_color="#1A1A3A",
            corner_radius=10,
            border_width=1,
            border_color="#00F0FF",
            text_color="#00FFFF",
            command=self.on_reset
        )
        self.reset_button.pack(side="right", padx=10)
        
        # Difficulty frame
        self.difficulty_frame = ctk.CTkFrame(self.header_frame, fg_color="#0A0A1A", corner_radius=8)
        self.difficulty_frame.pack(padx=12, pady=(0, 12), fill="x")
        
        # Difficulty buttons with neon styling
        self.beginner_button = ctk.CTkButton(
            self.difficulty_frame,
            text="BEGINNER",
            font=("Arial", 14, "bold"),
            fg_color="#0D0D1F",
            hover_color="#1A1A3A",
            corner_radius=8,
            border_width=1,
            border_color="#00F0FF",
            text_color="#00FFFF",
            command=lambda: self.on_difficulty_change("beginner")
        )
        self.beginner_button.pack(side="left", padx=8, fill="x", expand=True)
        
        self.intermediate_button = ctk.CTkButton(
            self.difficulty_frame,
            text="INTERMEDIATE",
            font=("Arial", 14, "bold"),
            fg_color="#0D0D1F",
            hover_color="#1A1A3A",
            corner_radius=8,
            border_width=1,
            border_color="#00F0FF",
            text_color="#00FFFF",
            command=lambda: self.on_difficulty_change("intermediate")
        )
        self.intermediate_button.pack(side="left", padx=8, fill="x", expand=True)
        
        self.expert_button = ctk.CTkButton(
            self.difficulty_frame,
            text="EXPERT",
            font=("Arial", 14, "bold"),
            fg_color="#0D0D1F",
            hover_color="#1A1A3A",
            corner_radius=8,
            border_width=1,
            border_color="#00F0FF",
            text_color="#00FFFF",
            command=lambda: self.on_difficulty_change("expert")
        )
        self.expert_button.pack(side="left", padx=8, fill="x", expand=True)
        
        # Control buttons frame
        self.controls_frame = ctk.CTkFrame(self.header_frame, fg_color="#0A0A1A", corner_radius=8)
        self.controls_frame.pack(padx=12, pady=(0, 12), fill="x")
        
        # New Game and Exit buttons with neon styling
        self.new_game_button = ctk.CTkButton(
            self.controls_frame,
            text="NEW GAME",
            font=("Arial", 14, "bold"),
            fg_color="#0D0D1F",
            hover_color="#1A1A3A",
            corner_radius=8,
            border_width=1,
            border_color="#2FE3FE",
            text_color="#2FE3FE",
            command=self.on_new_game
        )
        self.new_game_button.pack(side="left", padx=8, fill="x", expand=True)
        
        self.exit_button = ctk.CTkButton(
            self.controls_frame,
            text="EXIT GAME",
            font=("Arial", 14, "bold"),
            fg_color="#0D0D1F",
            hover_color="#1A1A3A",
            corner_radius=8,
            border_width=1,
            border_color="#FF00FF",
            text_color="#FF80FF",
            command=self.on_exit
        )
        self.exit_button.pack(side="right", padx=8, fill="x", expand=True)
    
    def _create_grid_frame(self):
        """Create the frame for the game grid with neon styling."""
        # Create a container frame with dark background
        self.grid_container = ctk.CTkFrame(self.ui_frame, fg_color="#0A0A1A", border_width=0, corner_radius=10)
        self.grid_container.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Add a subtle neon border to the grid container for that futuristic look
        self.grid_container.configure(border_width=1, border_color="#2020FF")
        
        # Create a wrapper frame inside the container for better centering
        self.grid_wrapper = ctk.CTkFrame(self.grid_container, fg_color="transparent")
        self.grid_wrapper.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        
        # Create the actual grid frame inside the wrapper with transparent background
        self.grid_frame = ctk.CTkFrame(self.grid_wrapper, fg_color="transparent", corner_radius=0, border_width=0)
        self.grid_frame.pack(side="top", pady=10)
    
    def _create_status_bar(self):
        """Create the status bar at the bottom with neon styling."""
        self.status_frame = ctk.CTkFrame(self.ui_frame, fg_color="#0D0D1F", corner_radius=10, height=40)
        self.status_frame.configure(border_width=1, border_color="#00F0FF")  # Neon cyan border
        self.status_frame.pack(padx=15, pady=(0, 15), fill="x")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready to play! Press ? for controls",
            font=("Arial", 14, "bold"),
            text_color="#00FFFF"  # Bright cyan for neon effect
        )
        self.status_label.pack(padx=12, pady=8)
    
    def show_game_ui(self):
        """Show the game UI elements."""
        # First, make sure the background is at the bottom of the z-order
        if hasattr(self, 'bg_label') and self.bg_label is not None:
            self.bg_label.lower()
            print("Background lowered to bottom of z-order")
        
        # Show main container
        self.main_container.pack(fill="both", expand=True)
        
        # Make sure UI is above the background
        if hasattr(self, 'ui_frame'):
            self.ui_frame.lift()
            print("UI frame lifted to top of z-order")
        
        # Force update
        self.root.update_idletasks()
        print("UI elements are now visible")
    
    def _create_help_button(self):
        """Create a help button to show controls with neon styling."""
        self.help_button = ctk.CTkButton(
            self.status_frame,
            text="?",
            width=30,
            height=30,
            corner_radius=15,  # Make it circular
            fg_color="#0A0A1A",
            hover_color="#1A1A3A",
            border_width=1,
            border_color="#00F0FF",
            text_color="#00FFFF",
            font=("Arial", 16, "bold"),
            command=self.show_help
        )
        self.help_button.pack(side="right", padx=10, pady=5)
    
    def clear_grid(self):
        """Clear the grid frame."""
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
    
    def get_grid_frame(self):
        """Get the grid frame for placing cells."""
        return self.grid_frame
    
    def calculate_cell_size(self, rows, cols):
        """Calculate the optimal cell size based on grid dimensions."""
        # Base sizes - larger for beginner, smaller for expert
        if rows <= 9 and cols <= 9:  # Beginner mode
            cell_size = 42  # Larger cells for better visibility
        elif rows <= 16 and cols <= 16:  # Intermediate mode
            cell_size = 32  # Medium size cells
        else:  # Expert mode
            cell_size = 24  # Smaller cells to fit the grid
        
        # Calculate total grid size
        screen_width = self.root.winfo_screenwidth() - 100  # Leave some margin
        screen_height = self.root.winfo_screenheight() - 350  # Leave space for header and status
        
        # Check if grid would be too large and adjust if needed
        max_width = screen_width / cols
        max_height = screen_height / rows
        
        # Use the smaller of the two constraints to ensure grid fits
        max_size = min(max_width, max_height)
        
        # Adjust cell size if needed, but don't go below 20px
        return max(min(cell_size, int(max_size)), 20)
    
    def update_mines_display(self, mines, flags):
        """Update mines and flags display."""
        remaining = mines - flags
        self.mines_label.configure(text=f"{EMOJIS['mine']} {remaining}")
        self.flags_label.configure(text=f"{EMOJIS['flag']} {flags}")
    
    def update_timer(self, elapsed_time):
        """Update timer display."""
        # Format time as min:sec for better readability
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        if minutes > 0:
            formatted_time = f"{minutes}:{seconds:02d}"
        else:
            formatted_time = f"{seconds:03d}"
            
        self.timer_label.configure(text=f"{EMOJIS['timer']} {formatted_time}")
    
    def highlight_difficulty(self, difficulty):
        """Highlight the selected difficulty button."""
        # Reset all buttons
        for btn in [self.beginner_button, self.intermediate_button, self.expert_button]:
            btn.configure(fg_color="#0D0D1F")
        
        # Highlight selected button
        if difficulty == "beginner":
            self.beginner_button.configure(fg_color="#1A1A3A")
        elif difficulty == "intermediate":
            self.intermediate_button.configure(fg_color="#1A1A3A")
        else:  # Expert
            self.expert_button.configure(fg_color="#1A1A3A")
    
    def update_game_status(self, game_state, high_score=None):
        """Update the game status display."""
        if game_state == GAME_READY:
            self.reset_button.configure(text=EMOJIS["ready"])
            self.status_label.configure(text="Ready to play! Press ? for controls", text_color=TEXT_COLORS["status"])
        elif game_state == GAME_PLAYING:
            self.status_label.configure(text="Game in progress...", text_color=TEXT_COLORS["status"])
        elif game_state == GAME_WON:
            self.reset_button.configure(text=EMOJIS["win"])
            if high_score is not None:
                self.status_label.configure(
                    text=f"New high score: {high_score} seconds!",
                    text_color=TEXT_COLORS["win"]
                )
            else:
                self.status_label.configure(
                    text="You won! Congratulations!",
                    text_color=TEXT_COLORS["win"]
                )
        elif game_state == GAME_LOST:
            self.reset_button.configure(text=EMOJIS["lose"])
            self.status_label.configure(
                text="Game over! You hit a mine!",
                text_color=TEXT_COLORS["lose"]
            )
    
    def resize_window(self, rows, cols, cell_size):
        """Resize the window based on grid dimensions."""
        width = max(cols * cell_size + 40, 400)
        height = rows * cell_size + 220
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_help(self):
        """Show help dialog with control information."""
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("Minesweeper Controls")
        help_window.geometry("400x350")
        help_window.resizable(False, False)
        
        # Create frame for help content
        help_frame = ctk.CTkFrame(help_window, fg_color="#1E1E2D")
        help_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            help_frame,
            text="Game Controls",
            font=("Arial", 16, "bold"),
            text_color="#00BFFF"
        )
        title_label.pack(pady=(10, 20))
        
        # Mouse controls
        mouse_title = ctk.CTkLabel(
            help_frame, 
            text="Mouse Controls:",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        mouse_title.pack(anchor="w", padx=20, pady=(5, 0))
        
        mouse_controls = ctk.CTkLabel(
            help_frame,
            text="• Left-click: Reveal a cell\n• Right-click: Place/remove flag\n• Ctrl+Left-click: Alternative to right-click\n• Middle-click: Alternative to right-click",
            font=("Arial", 12),
            text_color="#DDDDDD",
            justify="left"
        )
        mouse_controls.pack(anchor="w", padx=40, pady=(0, 10))
        
        # Keyboard controls
        keyboard_title = ctk.CTkLabel(
            help_frame, 
            text="Keyboard Controls:",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        keyboard_title.pack(anchor="w", padx=20, pady=(5, 0))
        
        keyboard_controls = ctk.CTkLabel(
            help_frame,
            text="• Arrow keys: Move selection\n• Space: Reveal selected cell\n• F key: Flag selected cell",
            font=("Arial", 12),
            text_color="#DDDDDD",
            justify="left"
        )
        keyboard_controls.pack(anchor="w", padx=40, pady=(0, 10))
        
        # Touchpad tips
        touchpad_title = ctk.CTkLabel(
            help_frame, 
            text="Touchpad Tips:",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        touchpad_title.pack(anchor="w", padx=20, pady=(5, 0))
        
        touchpad_tips = ctk.CTkLabel(
            help_frame,
            text="• Two-finger click: Right-click\n• Hold Ctrl and click: Alternative right-click\n• Use F key with keyboard navigation",
            font=("Arial", 12),
            text_color="#DDDDDD",
            justify="left"
        )
        touchpad_tips.pack(anchor="w", padx=40, pady=(0, 10))
        
        # Close button
        close_button = ctk.CTkButton(
            help_frame,
            text="Close",
            command=help_window.destroy,
            fg_color="#0A3257",
            hover_color="#154275",
        )
        close_button.pack(pady=15)
        
        # Set focus and make modal
        help_window.transient(self.root)
        help_window.grab_set()
        help_window.focus_set()
    
    def debug_check_bg_image(self):
        """Debug method to check and fix background image issues."""
        print("DEBUG: Checking background image...")
        
        # Check if we have the background components
        if not hasattr(self, 'bg_canvas'):
            print("DEBUG: Background canvas missing, recreating...")
            # Create a background canvas for the image
            self.bg_canvas = ctk.CTkCanvas(
                self.main_container,
                highlightthickness=0,
                borderwidth=0, 
                width=1300, 
                height=700
            )
            self.bg_canvas.pack(fill="both", expand=True)
        
        # Check for image file
        image_path = "game/assets/main.png"
        if not os.path.exists(image_path):
            print(f"DEBUG: Image file not found at {image_path}")
            # List files in the assets directory
            assets_dir = "game/assets"
            if os.path.exists(assets_dir):
                print(f"Files in {assets_dir}:")
                for file in os.listdir(assets_dir):
                    print(f"  - {file}")
            return False
        
        # Try loading and displaying the image
        try:
            # Load with PIL
            self.bg_image = Image.open(image_path)
            print(f"DEBUG: Image loaded, size={self.bg_image.size}, mode={self.bg_image.mode}")
            
            # Create/update image
            self.bg_photo = ctk.CTkImage(
                light_image=self.bg_image, 
                dark_image=self.bg_image,
                size=(1300, 700)
            )
            
            # Create/update label
            if not hasattr(self, 'bg_label') or self.bg_label is None:
                print("DEBUG: Creating new background label")
                self.bg_label = ctk.CTkLabel(
                    self.bg_canvas,
                    image=self.bg_photo,
                    text=""
                )
            else:
                print("DEBUG: Updating existing background label")
                self.bg_label.configure(image=self.bg_photo)
            
            # Ensure proper placement
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
            print("DEBUG: Background check complete")
            return True
            
        except Exception as e:
            print(f"DEBUG: Error checking background: {e}")
            return False
    
    def refresh_background(self, force_reload=False):
        """Refresh the background image to ensure it's visible."""
        if hasattr(self, 'bg_label') and self.bg_label is not None:
            # Use the renamed image file
            image_path = "game/assets/main.png"
            
            # Only reload the image if forced or if the image is not already loaded
            if force_reload or self.bg_photo is None:
                try:
                    # Load with PIL
                    self.bg_image = Image.open(image_path)
                    # Keep a reference to prevent garbage collection
                    self.bg_photo = ctk.CTkImage(
                        light_image=self.bg_image,
                        dark_image=self.bg_image,
                        size=(1300, 700)  # Match window size
                    )
                    
                    # Update the label with the new image
                    self.bg_label.configure(image=self.bg_photo)
                    print("Background image refreshed")
                except Exception as e:
                    print(f"Error refreshing background image: {e}")
                    return False
            
            # Ensure the image is properly positioned and sized
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()
            print("Background repositioned to the back")
            
            # Force update
            self.root.update_idletasks()
            return True
        return False 