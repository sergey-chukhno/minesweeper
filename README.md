# Neon Minesweeper

A modern, neon-styled implementation of the classic Minesweeper game using Python and CustomTkinter.

## Features

- 🎮 Three difficulty levels (Beginner, Intermediate, Expert)
- 🎨 Modern neon UI with animations
- 🔊 Sound effects and background music
- ⌨️ Keyboard controls support
- 🏆 High score tracking
- 🎯 First-click protection (never hit a mine on first click)
- 🚩 Flag and question mark cell marking
- ⚡ Smooth animations and visual feedback

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sergey-chukhno/minesweeper.git
cd minesweeper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## Controls

### Mouse Controls
- Left-click: Reveal a cell
- Right-click: Place/remove flag
- Ctrl+Left-click: Alternative to right-click
- Middle-click: Alternative to right-click

### Keyboard Controls
- Arrow keys: Move selection
- Space: Reveal selected cell
- F key: Flag selected cell

### Touchpad Tips
- Two-finger click: Right-click
- Hold Ctrl and click: Alternative right-click
- Use F key with keyboard navigation

## Game Rules

1. The game starts with a grid of hidden cells
2. Some cells contain mines
3. Numbers indicate how many mines are adjacent to a cell
4. Left-click to reveal a cell
5. Right-click to place/remove a flag
6. Win by revealing all non-mine cells
7. Lose by revealing a mine

## Difficulty Levels

- **Beginner**: 9x9 grid, 10 mines
- **Intermediate**: 16x16 grid, 40 mines
- **Expert**: 16x30 grid, 99 mines

## Project Structure

```
neon-minesweeper/
├── game/
│   ├── assets/
│   │   ├── sounds/     # Sound effects and music
│   │   └── images/     # Game images and icons
│   ├── cell.py         # Custom cell widget
│   ├── config.py       # Game configuration
│   ├── game_logic.py   # Game rules and state
│   ├── grid_manager.py # Grid management
│   ├── minesweeper.py  # Main game class
│   ├── sound_manager.py # Sound handling
│   └── ui_manager.py   # UI management
├── tests/              # Test files
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Adding Sound Files
Place your sound files in `game/assets/sounds/`:
- `click.wav`: Cell click sound
- `flag.wav`: Flag placement sound
- `explosion.wav`: Mine explosion sound
- `win.wav`: Victory sound
- `lose.wav`: Defeat sound
- `hover.wav`: Cell hover sound
- `background.mp3`: Background music

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
