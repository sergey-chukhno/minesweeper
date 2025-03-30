"""
Game logic manager for Minesweeper.
"""
import random
import time
import json
import os
from game.config import (
    BEGINNER, INTERMEDIATE, EXPERT,
    GAME_READY, GAME_PLAYING, GAME_WON, GAME_LOST,
    HIGH_SCORES_FILE, DEFAULT_HIGH_SCORES
)

class GameLogic:
    """
    Manages the game state and mechanics for Minesweeper.
    """
    def __init__(self):
        self.difficulty = BEGINNER
        self.rows = self.difficulty["rows"]
        self.cols = self.difficulty["cols"]
        self.state = GAME_READY
        self.is_first_click = True
        self.start_time = 0
        self.elapsed_time = 0
        self.mines_count = self.difficulty["mines"]
        self.flags_count = 0
        self.mines_positions = set()
        self.high_scores = self.load_high_scores()
        
    def reset_game(self, difficulty=None):
        """Reset the game to initial state."""
        if difficulty:
            self.difficulty = difficulty
            
        self.rows = self.difficulty["rows"]
        self.cols = self.difficulty["cols"]
        self.state = GAME_READY
        self.is_first_click = True
        self.start_time = 0
        self.elapsed_time = 0
        self.mines_count = self.difficulty["mines"]
        self.flags_count = 0
        self.mines_positions = set()
    
    def generate_mines(self, first_row, first_col):
        """Generate mines after the first click."""
        # Get the mines count from difficulty settings
        self.mines_count = self.difficulty["mines"]
        
        # Ensure we don't place more mines than cells
        max_mines = self.rows * self.cols - 9  # Leave safe zone around first click
        self.mines_count = min(self.mines_count, max_mines)
        
        # Create list of all possible mine positions (excluding first click and adjacents)
        possible_positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                # Exclude first click position and adjacent cells
                if abs(r - first_row) > 1 or abs(c - first_col) > 1:
                    possible_positions.append((r, c))
        
        # Place mines
        self.mines_positions = set(random.sample(possible_positions, min(self.mines_count, len(possible_positions))))
        return self.mines_positions
    
    def count_adjacent_mines(self, row, col):
        """Count mines in adjacent cells."""
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                if (r, c) != (row, col) and (r, c) in self.mines_positions:
                    count += 1
        return count
    
    def start_game(self):
        """Start the game timer."""
        self.start_time = time.time()
        self.state = GAME_PLAYING
    
    def get_elapsed_time(self):
        """Get the current elapsed time."""
        if self.state == GAME_READY:
            return 0
        elif self.state in (GAME_WON, GAME_LOST):
            return self.elapsed_time
        else:
            # Using time.time() for more accurate timing
            current_time = time.time()
            elapsed = int(current_time - self.start_time)
            return elapsed
    
    def update_flag_count(self, was_flagged, is_flagged):
        """Update the flag counter."""
        if was_flagged and not is_flagged:
            self.flags_count -= 1
        elif not was_flagged and is_flagged:
            self.flags_count += 1
    
    def check_win(self, revealed_cells):
        """Check if all non-mine cells are revealed."""
        total_cells = self.rows * self.cols
        return revealed_cells == total_cells - len(self.mines_positions)
    
    def game_over(self, win):
        """Handle game over state."""
        self.state = GAME_WON if win else GAME_LOST
        self.elapsed_time = int(time.time() - self.start_time)
        
        if win:
            self.save_high_score()
    
    def load_high_scores(self):
        """Load high scores from file."""
        if os.path.exists(HIGH_SCORES_FILE):
            try:
                with open(HIGH_SCORES_FILE, "r") as f:
                    return json.load(f)
            except:
                pass
        
        # Default high scores
        return DEFAULT_HIGH_SCORES.copy()
    
    def save_high_score(self):
        """Save high score if it's better than the current one."""
        difficulty_name = self.difficulty["name"]
        current_score = self.elapsed_time
        
        if current_score < self.high_scores.get(difficulty_name, 999):
            self.high_scores[difficulty_name] = current_score
            
            # Save to file
            with open(HIGH_SCORES_FILE, "w") as f:
                json.dump(self.high_scores, f)
            
            return True
        return False 