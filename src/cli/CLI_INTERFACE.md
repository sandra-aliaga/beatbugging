# CLI Interface Module

This module provides the visual command-line interface for BeatBugging using Rich library.

## Files
- `map.py` - Game map visualization system

## Overview

The CLI module creates a real-time visual interface in the terminal featuring:
- Interactive 5×5 grid for bug debugging
- Visual timing feedback for each cell
- Health and progress bars
- Input panel for player commands

## Map Class

### Basic Usage

```python
from src.cli.map import Map

# Create and configure map
game_map = Map(size=5)
game_map.set_active_coords("AJ - SK - DL")
game_map.set_actual_line("if (user.isValid()) {")
game_map.set_progress(75)
game_map.set_health(90)

# Update cell states
game_map.set_cell_state("AJ", 3)  # Perfect timing
game_map.set_cell_state("SK", 2)  # Good timing

# Build layout
layout = game_map.build_layout()
```

### Timing States

| State | Value | Description |
|-------|-------|-------------|
| INACTIVE | 0 | No bugs |
| EARLY | 1 | Too early |
| ALMOST_EARLY | 2 | Almost perfect (early) |
| PERFECT | 3 | Perfect timing |
| ALMOST_LATE | 4 | Almost perfect (late) |
| LATE | 5 | Too late |

### Main Methods

- `update_cell(coordinate, is_active)` - Update cell state
- `set_cell_state(coordinate, state)` - Set specific timing state
- `set_progress(value)` - Update progress (0-100)
- `set_health(value)` - Update health (0-100)
- `set_input(text)` - Update user input
- `build_layout()` - Generate complete interface layout

### Real-time Implementation

```python
from rich.live import Live

def run_game():
    game_map = Map()
    
    with Live(game_map.build_layout(), refresh_per_second=30) as live:
        while game_running:
            # Update game state
            game_map.set_active_coords("Current bugs")
            game_map.set_progress(current_progress)
            
            # Refresh display
            live.update(game_map.build_layout())
```

## Grid System

- **Columns**: A, S, D, E, F (left hand)
- **Rows**: J, K, L, M, N (right hand) 
- **Coordinates**: Column+Row (e.g., AJ, SK, DL)

## Dependencies

- Rich - Terminal rendering
- typing - Type hints

---

*Simple, fast, visual debugging interface for BeatBugging.*