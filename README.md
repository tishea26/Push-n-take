# Push'n'Takes

Push'n'Takes is a terminal-based strategy game inspired by a simplified version of chess.  
It is written in Python and features a strong Minimax-based AI opponent.

The goal is simple: **outplay the AI and reach the opposite side of the board**

## Features

- **Minimax AI (Alpha-Beta Pruning)**: Play against a strong AI capable of planning several moves ahead.
- **Colorful Terminal UI**: Uses the Rich library for colored output
- **Linux Compatible**: Made for Linux terminal environments

## Game Rules

- Each player starts with 10 pawns
- Pawns can:
  - Move one tile forward
  - Capture one tile diagonally forward
- Capturing a pawn removes it from the board and moves the attacker to its position
- A player skips their turn if all pawns are blocked

### Win Conditions

You win if:
- One of your pawns reaches the opponent’s end row  
**OR**
- The enemy does not have any pawn left

A draw occurs if both players are fully blocked.

## Controls

Commands are entered directly in the terminal:

- `m <id>`: Move pawn `<id>` one tile forward

- `a <id1> <id2>`: Pawn `<id1>` attacks enemy pawn `<id2>`

Each pawn has a unique display ID (0-9) per player, shown directly on the board.

## Installation

### Requirements

- Python 3.10+
- `rich` library

### Setup

```bash
git clone https://gitlab.com/yourusername/push-n-takes.git
cd push-n-takes
pip install rich
```

## Usage

Run the game with :
```bash
python main.py
```

### Project Structure

push-n-takes/
├── main.py              # Main game loop
├── engine/
│   ├── enums.py         # Tile and color definitions
│   ├── ai.py            # Minimax AI implementation
│   ├── board.py         # Game board and rules
│   ├── pawn.py          # Pawn model
│   └── renderer.py      # Terminal UI rendering
└── README.md

## AI details

The AI uses:
- Minimax search
- Alpha-Beta pruning
- A custom heuristic evaluating:
    - Pawn advantage
    - Progress toward the goal line
    - Board control

This makes the AI challenging and suitable for training and experimentation.

## Technical Details

- **Language**: Python 3
- **UI Library**: Rich (for terminal rendering)
- **Game Logic**: Pure Python with an AI algorithm to make a worthy opponent

## Why this project?

This project was built to practice:
- Game logic and state management
- AI decision-making algorithms
- Clean Python project architecture
- Terminal UI design with Rich

