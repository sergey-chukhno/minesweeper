"""
Grid Manager for Minesweeper.
"""
import customtkinter as ctk
import random
from game.cell import AnimatedCell
from game.config import (
    EMOJIS, GAME_WON, UI_COLORS
)
from PIL import Image, ImageDraw
import os

class GridManager:
    """
    Manages the game grid.
    """
    def __init__(self, game_logic, ui_manager, on_left_click, on_right_click):
        """
        Initialize the grid manager.
        
        Parameters:
        - game_logic: The game logic instance
        - ui_manager: The UI manager instance
        - on_left_click: Callback for left-click on cell
        - on_right_click: Callback for right-click on cell
        """
        self.game_logic = game_logic
        self.ui_manager = ui_manager
        self.on_left_click = on_left_click
        self.on_right_click = on_right_click
        self.grid = []
        self.cell_size = 0
        
        # Track revealed and flagged cells
        self.revealed_cells = 0
        self.flagged_cells = []
        
        # Create number images for cells (1-8)
        self.number_colors = [
            "#2196F3",  # 1: Blue
            "#4CAF50",  # 2: Green
            "#F44336",  # 3: Red
            "#9C27B0",  # 4: Purple
            "#FF9800",  # 5: Orange
            "#00BCD4",  # 6: Cyan
            "#FFEB3B",  # 7: Yellow
            "#795548"   # 8: Brown
        ]
    
    def create_grid(self):
        """Create the grid of cells."""
        # Get dimensions from game logic
        rows = self.game_logic.rows
        cols = self.game_logic.cols
        
        # Calculate cell size
        self.cell_size = self.ui_manager.calculate_cell_size(rows, cols)
        
        # Clear previous grid if exists
        self.ui_manager.clear_grid()
        self.grid = []
        
        # Resize window to fit grid
        self.ui_manager.resize_window(rows, cols, self.cell_size)
        
        # Get the grid frame
        grid_frame = self.ui_manager.get_grid_frame()
        
        # Create button grid
        for i in range(rows):
            row = []
            for j in range(cols):
                # Create cell with neon styling
                cell = AnimatedCell(
                    master=grid_frame,
                    text="",
                    width=self.cell_size,
                    height=self.cell_size,
                    corner_radius=4,
                    fg_color="#0A0A1A",  # Dark background
                    hover_color="#1A1A3A",  # Dark blue hover
                    border_width=1,
                    border_color="#1A1A4A",  # Subtle blue border
                    text_color="#FFFFFF",  # White text
                    command=lambda r=i, c=j: self.on_left_click(r, c)
                )
                
                # Add right-click binding
                cell.bind("<Button-3>", lambda event, r=i, c=j: self.on_right_click(event, r, c))
                cell.bind("<Control-Button-1>", lambda event, r=i, c=j: self.on_right_click(event, r, c))
                
                # Position cell in grid
                cell.grid(row=i, column=j, padx=1, pady=1)
                
                # Add to row
                row.append(cell)
            
            # Add row to grid
            self.grid.append(row)
        
        # Reset counters
        self.revealed_cells = 0
        self.flagged_cells = []
        
        # Return grid size for potential use
        return rows, cols
    
    def initialize_mines(self, first_click_row, first_click_col):
        """Initialize mines in the grid, avoiding the first clicked cell."""
        rows = self.game_logic.rows
        cols = self.game_logic.cols
        mines_count = self.game_logic.mines_count
        
        
        cells = [(r, c) for r in range(rows) for c in range(cols)]
        
        # Remove first clicked cell and its surrounding cells
        safe_cells = []
        for r in range(max(0, first_click_row - 1), min(rows, first_click_row + 2)):
            for c in range(max(0, first_click_col - 1), min(cols, first_click_col + 2)):
                safe_cells.append((r, c))
        
        mine_candidates = [cell for cell in cells if cell not in safe_cells]
        
        # Make sure we don't try to place more mines than we have valid positions
        valid_mine_count = min(mines_count, len(mine_candidates))
        
        # Select random mine positions
        mine_positions = random.sample(mine_candidates, valid_mine_count)
        
        # Place mines and calculate surrounding mine counts
        for row, col in mine_positions:
            # Mark as mine
            self.grid[row][col].is_mine = True
            
            # Increment surrounding cells
            for r in range(max(0, row - 1), min(rows, row + 2)):
                for c in range(max(0, col - 1), min(cols, col + 2)):
                    if (r, c) != (row, col):  # Skip the mine itself
                        self.grid[r][c].value += 1
        
        # Update UI to show mine count
        self.ui_manager.update_mines_display(
            self.game_logic.mines_count,
            self.game_logic.flags_count
        )
    
    def reveal_cell(self, row, col):
        """Reveal a cell. Returns True if it was a mine."""
        # Validate row and column
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
            return False
        
        cell = self.grid[row][col]
        
        # Ignore if already revealed or flagged
        if cell.is_revealed or cell.is_flagged:
            return False
        
        # Stop any running animation
        cell.stop_animation()
        
        # Clear question mark state if needed
        cell.is_question = False
        
        # Mark as revealed
        cell.is_revealed = True
        self.revealed_cells += 1
        
        # Check if mine
        if cell.is_mine:
            cell.is_exploded = True
            cell.configure(
                text=EMOJIS["mine"],
                fg_color="#FF0000",  
                text_color="#FFFFFF"
            )
            
            # Start explosion animation
            cell.start_lose_animation(self.ui_manager.get_grid_frame())
            
            return True
        else:
            # Not a mine
            # Set background color and text based on number of surrounding mines
            bg_color = "#121225"  
            text = ""
            text_color = "#FFFFFF"
            
            if cell.value > 0:
                text = str(cell.value)
                text_color = self.number_colors[cell.value - 1]
                cell_font = ("Arial", 16, "bold")
                cell.configure(
                    text=text,
                    fg_color=bg_color,
                    text_color=text_color,
                    font=cell_font,
                    hover_color=bg_color  
                )
            else:
                # Empty cell
                cell.configure(
                    text=text,
                    fg_color=bg_color,
                    text_color=text_color,
                    hover_color=bg_color  
                )
            
            # If cell has no surrounding mines, reveal adjacent cells
            if cell.value == 0:
                rows = self.game_logic.rows
                cols = self.game_logic.cols
                
                for r in range(max(0, row - 1), min(rows, row + 2)):
                    for c in range(max(0, col - 1), min(cols, col + 2)):
                        if (r, c) != (row, col):  # Skip the cell itself
                            self.reveal_cell(r, c)  # Recursive reveal
            
            return False
    
    def toggle_flag(self, row, col):
        """Toggle cell marking: unrevealed -> flag -> question mark -> unrevealed."""
        # Validate row and column
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
            return
        
        cell = self.grid[row][col]
        
        # Ignore if already revealed
        if cell.is_revealed:
            return
        
        # Stop any running animation
        cell.stop_animation()
        
        # Add property to track question mark state if not exists
        if not hasattr(cell, 'is_question'):
            cell.is_question = False
        
        # Toggle between three states: none -> flag -> question -> none
        if cell.is_flagged:
            # Change from flag to question mark
            cell.is_flagged = False
            cell.is_question = True
            cell.configure(
                text="?",
                fg_color="#0A0A1A",  
                text_color="#00FFFF"  
            )
            
            # Remove from flagged cells
            if (row, col) in self.flagged_cells:
                self.flagged_cells.remove((row, col))
        
        elif cell.is_question:
            # Change from question mark to unmarked
            cell.is_question = False
            cell.configure(
                text="",
                fg_color="#0A0A1A", 
            )
        
        else:
            # Add flag
            cell.is_flagged = True
            cell.configure(
                text=EMOJIS["flag"],
                fg_color="#1A1A3A",  
                text_color="#FF80FF"  
            )
            
            
            self.flagged_cells.append((row, col))
        
        # Update flag count in UI
        self.game_logic.flags_count = len(self.flagged_cells)
        self.ui_manager.update_mines_display(
            self.game_logic.mines_count,
            self.game_logic.flags_count
        )
    
    def reveal_all_mines(self, exploded_row=None, exploded_col=None):
        """Reveal all mines at game end."""
        rows = self.game_logic.rows
        cols = self.game_logic.cols
        
        # Keep track of cells to animate
        cells_to_animate = []
        
        # Reveal all mines
        for row in range(rows):
            for col in range(cols):
                cell = self.grid[row][col]
                
                # Reveal unflagged mines (avoid removing flags)
                if cell.is_mine and not cell.is_flagged:
                    # The exploded mine has already been handled
                    if (row, col) != (exploded_row, exploded_col):
                        cell.is_revealed = True
                        cell.is_question = False  # Clear question mark state
                        cell.configure(
                            text=EMOJIS["mine"],
                            fg_color="#2A0A0A",  
                            text_color="#FFFFFF"
                        )
                        cells_to_animate.append((cell, len(cells_to_animate) * 80))
                
                # Highlight incorrectly flagged cells (not mines)
                elif cell.is_flagged and not cell.is_mine:
                    cell.configure(
                        text=EMOJIS["wrong"],
                        fg_color="#5A1A1A",  
                        text_color="#FFFFFF"
                    )
                
                # Also handle incorrectly marked question cells (not mines)
                elif cell.is_question and not cell.is_mine:
                    cell.configure(
                        text=EMOJIS["wrong"],
                        fg_color="#5A1A1A",  
                        text_color="#FFFFFF"
                    )
        
        # Start animations with appropriate delays
        for cell, delay in cells_to_animate:
            # Use a separate function to start the animation after a delay
            def start_animation(c, d):
                self.ui_manager.root.after(d, lambda: c.start_lose_animation(self.ui_manager.get_grid_frame()))
            
            try:
                start_animation(cell, delay)
            except Exception:
                # Skip if there's an error
                pass
    
    def flag_all_mines(self):
        """Flag all mines at game end."""
        rows = self.game_logic.rows
        cols = self.game_logic.cols
        
        # Track flagged mines for count and cells to animate
        flagged_count = 0
        cells_to_animate = []
        
        # Flag all mines that aren't already flagged
        for row in range(rows):
            for col in range(cols):
                cell = self.grid[row][col]
                if cell.is_mine and not cell.is_flagged and not cell.is_exploded:
                    # Add flag and clear question mark if it exists
                    cell.is_flagged = True
                    cell.is_question = False
                    cell.configure(
                        text=EMOJIS["flag"],
                        fg_color="#1A1A3A",
                        text_color="#FF80FF" 
                    )
                    flagged_count += 1
                    # Add to animation list
                    cells_to_animate.append((cell, flagged_count * 50))
        
        # Start animations with appropriate delays
        for cell, delay in cells_to_animate:
            # Use a separate function to start the animation after a delay
            def start_animation(c, d):
                self.ui_manager.root.after(d, lambda: c.start_win_animation(self.ui_manager.get_grid_frame()))
            
            try:
                start_animation(cell, delay)
            except Exception:
                # Skip if there's an error
                pass
        
        # Update flag count
        self.game_logic.flags_count = len(self.flagged_cells) + flagged_count
        self.ui_manager.update_mines_display(
            self.game_logic.mines_count,
            self.game_logic.flags_count
        )
    
    def get_revealed_count(self):
        """Get the number of revealed cells."""
        return self.revealed_cells 