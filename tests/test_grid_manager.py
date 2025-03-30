import pytest
import customtkinter as ctk
from game.grid_manager import GridManager
from game.game_logic import GameLogic
from game.ui_manager import UIManager
from game.cell import AnimatedCell

class MockUIManager:
    """Mock UIManager for testing"""
    def __init__(self):
        self.root = ctk.CTk()
        self.grid_frame = ctk.CTkFrame(self.root)
    
    def get_grid_frame(self):
        return self.grid_frame
    
    def update_mines_display(self, mines, flags):
        pass

@pytest.fixture
def game_logic():
    """Fixture to create a GameLogic instance"""
    return GameLogic()

@pytest.fixture
def ui_manager():
    """Fixture to create a MockUIManager instance"""
    return MockUIManager()

@pytest.fixture
def grid_manager(game_logic, ui_manager):
    """Fixture to create a GridManager instance"""
    def mock_left_click(row, col):
        pass
    
    def mock_right_click(event, row, col):
        pass
    
    return GridManager(game_logic, ui_manager, mock_left_click, mock_right_click)

def create_test_grid(ui_manager, size=3):
    """Helper function to create a test grid with cells"""
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            cell = AnimatedCell(
                master=ui_manager.grid_frame,
                text="",
                width=30,
                height=30
            )
            cell.grid(row=i, column=j)
            row.append(cell)
        grid.append(row)
    return grid

def test_reveal_cell_basic(grid_manager, ui_manager):
    """Test basic cell revelation"""
    # Create a simple 3x3 grid
    grid_manager.grid = create_test_grid(ui_manager)
    
    # Test revealing a cell
    result = grid_manager.reveal_cell(1, 1)
    
    # Check if the cell was revealed
    assert grid_manager.grid[1][1].is_revealed == True
    assert result == False  # Should return False as it's not a mine

def test_reveal_cell_mine(grid_manager, ui_manager):
    """Test revealing a mine"""
    # Create a simple 3x3 grid
    grid_manager.grid = create_test_grid(ui_manager)
    
    # Place mine in center
    grid_manager.grid[1][1].is_mine = True
    
    # Test revealing the mine
    result = grid_manager.reveal_cell(1, 1)
    
    # Check if the mine was revealed
    assert grid_manager.grid[1][1].is_revealed == True
    assert grid_manager.grid[1][1].is_exploded == True
    assert result == True  # Should return True as it's a mine

def test_reveal_cell_recursive(grid_manager, ui_manager):
    """Test recursive revelation of empty cells"""
    # Create a 3x3 grid
    grid_manager.grid = create_test_grid(ui_manager)
    
    # Place mines around the edges
    for i in range(3):
        for j in range(3):
            if i == 0 or i == 2 or j == 0 or j == 2:
                grid_manager.grid[i][j].is_mine = True
    
    # Set up adjacent mine counts
    for i in range(3):
        for j in range(3):
            if not grid_manager.grid[i][j].is_mine:
                count = 0
                for r in range(max(0, i-1), min(3, i+2)):
                    for c in range(max(0, j-1), min(3, j+2)):
                        if grid_manager.grid[r][c].is_mine:
                            count += 1
                grid_manager.grid[i][j].value = count
    
    # Test revealing the center cell
    result = grid_manager.reveal_cell(1, 1)
    
    # Check if the center cell was revealed
    assert grid_manager.grid[1][1].is_revealed == True
    assert result == False
    
    # Check if the cell shows the correct number of adjacent mines
    assert grid_manager.grid[1][1].value == 8  # Should be surrounded by 8 mines

def test_reveal_cell_boundaries(grid_manager, ui_manager):
    """Test revealing cells at grid boundaries"""
    # Create a 3x3 grid
    grid_manager.grid = create_test_grid(ui_manager)
    
    # Test revealing cells at boundaries
    assert grid_manager.reveal_cell(-1, 1) == False  # Should handle negative row
    assert grid_manager.reveal_cell(1, -1) == False  # Should handle negative column
    assert grid_manager.reveal_cell(3, 1) == False   # Should handle row too large
    assert grid_manager.reveal_cell(1, 3) == False   # Should handle column too large

def test_reveal_cell_flagged(grid_manager, ui_manager):
    """Test revealing a flagged cell"""
    # Create a 3x3 grid
    grid_manager.grid = create_test_grid(ui_manager)
    
    # Flag a cell
    grid_manager.grid[1][1].is_flagged = True
    
    # Try to reveal the flagged cell
    result = grid_manager.reveal_cell(1, 1)
    
    # Check that the cell wasn't revealed
    assert grid_manager.grid[1][1].is_revealed == False
    assert result == False 