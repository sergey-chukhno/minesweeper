"""
Minesweeper Game - Main Class
"""
import customtkinter as ctk
import os
from game.config import (
    BEGINNER, INTERMEDIATE, EXPERT,
    GAME_READY, GAME_PLAYING, GAME_WON, GAME_LOST,
    UI_COLORS
)
from game.game_logic import GameLogic
from game.ui_manager import UIManager
from game.grid_manager import GridManager
from game.sound_manager import SoundManager
from PIL import Image

class Minesweeper(ctk.CTk):
    """
    Main class for the Minesweeper game.
    """
    def __init__(self):
        super().__init__()
        
        # Initialize window properties
        self.title("Neon Minesweeper")
        self.iconbitmap("game/assets/icon.ico") if os.path.exists("game/assets/icon.ico") else None
        
        # Set window size for start page 
        self.geometry("1240x700")
        
        # Configure window properties
        self.resizable(True, True)  # Allow window resizing
        self.minsize(800, 600)  # Set minimum window size
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Initialize game components
        self.game_logic = GameLogic()
        self.ui_manager = UIManager(
            self,
            self.reset_game,
            self.reset_game,
            self.quit_game,
            self.change_difficulty
        )
        self.grid_manager = GridManager(
            self.game_logic,
            self.ui_manager,
            self.on_left_click,
            self.on_right_click
        )
        
        # Create start page first
        self.create_start_page()
        
        # Create game grid (but don't show it yet)
        self.grid_manager.create_grid()
        
        # Set up timer callback
        self.after(1000, self.update_timer)
        
        # Set up keyboard shortcuts
        self.bind("<f>", self.flag_selected_cell)
        self.bind("<F>", self.flag_selected_cell)
        self.bind("<space>", self.reveal_selected_cell)
        
        # Track currently selected cell
        self.selected_row = 0
        self.selected_col = 0
        self.bind("<Up>", lambda e: self.move_selection(-1, 0))
        self.bind("<Down>", lambda e: self.move_selection(1, 0))
        self.bind("<Left>", lambda e: self.move_selection(0, -1))
        self.bind("<Right>", lambda e: self.move_selection(0, 1))
        
        # Center the window on screen
        self.center_window()
        
        # Start background music
        self.sound_manager.play_music()
    
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def move_selection(self, row_delta, col_delta):
        """Move the selected cell using keyboard."""
        # Calculate new position
        new_row = max(0, min(self.game_logic.rows - 1, self.selected_row + row_delta))
        new_col = max(0, min(self.game_logic.cols - 1, self.selected_col + col_delta))
        
        # Unhighlight previous cell
        if self.grid_manager.grid and self.selected_row < len(self.grid_manager.grid) and self.selected_col < len(self.grid_manager.grid[0]):
            old_cell = self.grid_manager.grid[self.selected_row][self.selected_col]
            if not old_cell.is_revealed:
                old_cell.configure(border_color=UI_COLORS["cell_border"])
        
        # Update selection
        self.selected_row = new_row
        self.selected_col = new_col
        
        # Highlight new cell
        if self.grid_manager.grid and self.selected_row < len(self.grid_manager.grid) and self.selected_col < len(self.grid_manager.grid[0]):
            new_cell = self.grid_manager.grid[self.selected_row][self.selected_col]
            if not new_cell.is_revealed:
                new_cell.configure(border_color="#FFFFFF")  
        
        return "break" 
    
    def flag_selected_cell(self, event):
        """Flag the currently selected cell using keyboard."""
        if self.grid_manager.grid and self.game_logic.state == GAME_PLAYING:
            self.on_right_click(event, self.selected_row, self.selected_col)
        return "break"
    
    def reveal_selected_cell(self, event):
        """Reveal the currently selected cell using keyboard."""
        if self.grid_manager.grid:
            self.on_left_click(self.selected_row, self.selected_col)
        return "break"
    
    def on_left_click(self, row, col):
        """Handle left-click on a cell."""
        # Update selected cell
        self.selected_row = row
        self.selected_col = col
        
        # Ignore if game is over
        if self.game_logic.state in (GAME_WON, GAME_LOST):
            return
        
        # Validate cell position
        if row < 0 or row >= self.game_logic.rows or col < 0 or col >= self.game_logic.cols:
            return
        
        # Get the cell
        if not self.grid_manager.grid or row >= len(self.grid_manager.grid) or col >= len(self.grid_manager.grid[0]):
            return
        
        cell = self.grid_manager.grid[row][col]
        
        # If cell is already revealed or flagged
        if cell.is_revealed or cell.is_flagged:
            return
        
        # First click should never be a mine
        if self.game_logic.is_first_click:
            self.game_logic.is_first_click = False
            
            # Initialize mines
            self.grid_manager.initialize_mines(row, col)
            
            # Start timer
            self.game_logic.start_game()
            
            # Update UI
            self.ui_manager.update_game_status(GAME_PLAYING)
            self.ui_manager.update_mines_display(
                self.game_logic.mines_count,
                self.game_logic.flags_count
            )
        
        # Play click sound
        self.sound_manager.play_sound('click')
        
        # Reveal the cell
        hit_mine = self.grid_manager.reveal_cell(row, col)
        
        if hit_mine:
            # Game over - hit a mine
            self.sound_manager.play_sound('explosion')
            self.game_over(False, row, col)
        else:
            # Check for win
            revealed_count = self.grid_manager.get_revealed_count()
            if self.game_logic.check_win(revealed_count):
                self.sound_manager.play_sound('win')
                self.game_over(True)
    
    def on_right_click(self, event, row, col):
        """Handle right-click on a cell."""
        # Update selected cell
        self.selected_row = row
        self.selected_col = col
        
        # Ignore if game is over or hasn't started
        if self.game_logic.state in (GAME_WON, GAME_LOST):
            return
        
        # Validate cell position
        if row < 0 or row >= self.game_logic.rows or col < 0 or col >= self.game_logic.cols:
            return
        
        # Get the cell
        if not self.grid_manager.grid or row >= len(self.grid_manager.grid) or col >= len(self.grid_manager.grid[0]):
            return
        
        cell = self.grid_manager.grid[row][col]
        
        # If cell is already revealed, do nothing
        if cell.is_revealed:
            return
        
        # Play flag sound
        self.sound_manager.play_sound('flag')
        
        # Toggle flag on cell
        self.grid_manager.toggle_flag(row, col)
        
        # Check for win - some implementations allow winning by flagging all mines
        revealed_count = self.grid_manager.get_revealed_count()
        if self.game_logic.check_win(revealed_count):
            self.sound_manager.play_sound('win')
            self.game_over(True)
        
        # Prevent further event processing
        return "break"
    
    def game_over(self, win, exploded_row=None, exploded_col=None):
        """Handle game over state."""
        # Update game state
        self.game_logic.game_over(win)
        
        if win:
            # Win case
            self.grid_manager.flag_all_mines()
            
            # Check for high score
            new_high_score = self.game_logic.high_scores.get(
                self.game_logic.difficulty["name"]
            ) == self.game_logic.elapsed_time
            
            # Update UI
            self.ui_manager.update_game_status(
                GAME_WON,
                self.game_logic.elapsed_time if new_high_score else None
            )
        else:
            # Lose case
            self.grid_manager.reveal_all_mines(exploded_row, exploded_col)
            
            # Play lose sound
            self.sound_manager.play_sound('lose')
            
            # Update UI
            self.ui_manager.update_game_status(GAME_LOST)
        
        # Update display
        self.ui_manager.update_mines_display(
            self.game_logic.mines_count,
            self.game_logic.flags_count
        )
    
    def reset_game(self):
        """Reset the game to initial state."""
        # Reset game logic
        self.game_logic.reset_game()
        
        # Create new grid
        self.grid_manager.create_grid()
        
        # Update UI
        self.ui_manager.update_game_status(GAME_READY)
        self.ui_manager.update_mines_display(0, 0)
        self.ui_manager.update_timer(0)
    
    def change_difficulty(self, difficulty_name):
        """Change the game difficulty."""
        # Set the new difficulty
        if difficulty_name == "beginner":
            difficulty = BEGINNER
        elif difficulty_name == "intermediate":
            difficulty = INTERMEDIATE
        else:
            difficulty = EXPERT
            
        # Reset game with new difficulty
        self.game_logic.reset_game(difficulty)
        
        # Create new grid
        self.grid_manager.create_grid()
        
        # Update UI
        self.ui_manager.highlight_difficulty(difficulty_name)
        self.ui_manager.update_game_status(GAME_READY)
        self.ui_manager.update_mines_display(0, 0)
        self.ui_manager.update_timer(0)
    
    def update_timer(self):
        """Update the game timer."""
        # Get current elapsed time
        elapsed_time = self.game_logic.get_elapsed_time()
        
        # Update UI
        self.ui_manager.update_timer(elapsed_time)
        
        # Schedule next update - using a shorter interval for smoother updates
        self.after(100, self.update_timer)
    
    def quit_game(self):
        """Quit the game."""
        # Stop music and cleanup sound resources
        self.sound_manager.stop_music()
        self.sound_manager.cleanup()
        self.quit()

    def start_game(self):
        """Start the game and hide start page."""
        # Hide start page
        self.start_frame.pack_forget()
        
        # If the background label exists, make sure it's still visible and behind everything
        if hasattr(self.ui_manager, 'bg_label') and self.ui_manager.bg_label is not None:
            self.ui_manager.bg_label.lower()
            print("Main background ensured to be behind all elements")
        
        # Show game UI
        self.ui_manager.show_game_ui()
        
        # Reset game state
        self.reset_game()
        
        # Update display
        self.ui_manager.update_mines_display(
            self.game_logic.mines_count,
            self.game_logic.flags_count
        )
        self.ui_manager.highlight_difficulty("beginner")
        self.ui_manager.update_game_status(GAME_READY)
        self.ui_manager.update_timer(0)

    def create_start_page(self):
        """Create the start page with background and play button."""
        # Create main frame for start page
        self.start_frame = ctk.CTkFrame(self)
        self.start_frame.pack(fill="both", expand=True)
        
        # Load and display background image
        try:
            # Get the absolute path to the image file
            image_path = os.path.abspath("game/assets/background.png")
            if not os.path.exists(image_path):
                # Try the alternative filename
                image_path = os.path.abspath("game/assets/main.png")
            
            print(f"Loading start page background from: {image_path}")
            
            # Load the image with PIL
            start_bg_image = Image.open(image_path)
            print(f"Start page image loaded: {start_bg_image.size} {start_bg_image.mode}")
            
            # Create a canvas for the background image
            self.start_canvas = ctk.CTkCanvas(
                self.start_frame,
                highlightthickness=0,
                borderwidth=0,
                width=1200,
                height=700
            )
            self.start_canvas.pack(fill="both", expand=True)
            
            # Convert PIL Image to PhotoImage
            from PIL import ImageTk
            self.start_tk_image = ImageTk.PhotoImage(start_bg_image)
            
            # Add image to canvas
            self.start_canvas.create_image(0, 0, image=self.start_tk_image, anchor="nw")
            print("Start page background image added to canvas")
            
        except Exception as e:
            print(f"Error loading start page background: {e}")
            # Fallback to solid color if image loading fails
            self.start_frame.configure(fg_color="#1a1a1a")
        
        # Create play button with neon effect
        self.play_button = ctk.CTkButton(
            self.start_frame,
            text="PLAY GAME",
            font=("Helvetica", 24, "bold"),
            fg_color="#00a2ff",
            hover_color="#00c3ff",
            command=self.start_game,
            height=50,
            width=200,
            corner_radius=25,
            border_width=2,
            border_color="#00ffff"
        )
        
        # Position button at bottom center
        self.play_button.place(relx=0.55, rely=0.8, anchor="center")
        
        # Add hover effect
        self.play_button.bind("<Enter>", self.on_button_hover)
        self.play_button.bind("<Leave>", self.on_button_leave)
        
        # Ensure the button is on top of the background
        self.play_button.lift()
        
        # Ensure the start frame is visible
        self.start_frame.lift()
        self.start_frame.focus_set()
    
    def on_button_hover(self, event):
        """Handle button hover effect."""
        self.play_button.configure(
            fg_color="#00c3ff",
            border_color="#00ffff",
            border_width=3
        )
    
    def on_button_leave(self, event):
        """Handle button leave effect."""
        self.play_button.configure(
            fg_color="#00a2ff",
            border_color="#00ffff",
            border_width=2
        ) 