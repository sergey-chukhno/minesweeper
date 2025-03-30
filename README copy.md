# Neon Minesweeper

A modern implementation of the classic Minesweeper game using Python and Customtkinter with a futuristic neon blue theme.

## Features

- Three difficulty levels: Beginner, Intermediate, and Expert
- Dynamic mine generation with random variations
- First-click safety (never hit a mine on first click)
- Game timer and high score tracking
- Flagging system with counters
- Modern UI with dark blue neon futuristic style

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd neon-minesweeper
```

2. Install the dependencies:
```
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```
python main.py
```

2. Game Controls:
   - Left-click to reveal a cell
   - Right-click to cycle through: Empty → Flag → Question Mark → Empty
   - Click the reset button (smiley face) to start a new game
   - Select difficulty level using the buttons at the top

3. Objective:
   - Reveal all cells that don't contain mines
   - Flag all cells that contain mines
   - Avoid clicking on mines or you lose

## Game Rules

- Numbers indicate how many mines are adjacent to that cell
- If you click on a cell with no adjacent mines, all adjacent cells will be automatically revealed
- The game ends when you either reveal all safe cells (win) or click on a mine (lose)
- The timer starts on your first click
- Your best times are saved for each difficulty level

## Difficulty Levels

- **Beginner**: 9x9 grid with 8-12 mines
- **Intermediate**: 16x16 grid with 35-45 mines
- **Expert**: 24x24 grid with 90-108 mines 