# CLI Interface Module Documentation

This module contains the visual command-line interface implementation for BeatBugging, providing real-time game state visualization using Rich.

## Module Files

- `map.py` - Game map visualization system implementation

---

## Overview

The CLI module provides an advanced visual interface for the terminal that displays the complete BeatBugging game state in real-time. It uses the Rich library to create a rich visual experience in the terminal, including:

- Interactive 5x5 grid to represent bugs in the code
- Visual timing states for each cell
- System health and progress bars
- Input panel for player commands
- Contextual debugging information

## map.py - Map Visualization System

## Configuration Constants

### System Colors
```python
BORDER_COLOR = "green"          # Panel border color
ACCENT_COLOR = "bright_green"   # Accent and title color
PRIMARY_COLOR = "green"         # Primary text color
ACCENT_STYLE = "bold bright_green"  # Title style
```

### Timing States

The system handles 6 different timing states to represent debugging precision:

| State | Value | Description | Visual Representation |
|--------|-------|-------------|----------------------|
| `INACTIVE` | 0 | Inactive cell, no bugs | Simple borders, empty |
| `EARLY` | 1 | Very early timing | Simple borders, light fill |
| `ALMOST_EARLY` | 2 | Almost perfect timing (early) | Simple borders, medium fill |
| `PERFECT` | 3 | Perfect timing | Double borders, full fill, blinking |
| `ALMOST_LATE` | 4 | Almost perfect timing (late) | Double borders, gradient fill |
| `LATE` | 5 | Late timing | Simple borders, light fill |

### Cell Templates

Each state has its corresponding ASCII template:

```python
# Example: PERFECT State
CELL_PERFECT = [
    "╔═════╗",    # Top line with double borders
    "║ COO ║",    # Line with coordinate (replaced dynamically)
    "║█████║",    # Full fill line
    "╚═════╝"     # Bottom line with double borders
]
```

---

## Main Class: `Map`

### Constructor

```python
def __init__(self, size=5)
```

**Parameters:**
- `size` (int): Grid size (default 5x5)

**Initialized Attributes:**
- `console`: Rich Console instance
- `size`: Grid size
- `active_coords`: String with current active coordinates
- `actual_line`: Code line being debugged
- `progress_value`: Progress value (0-100)
- `health_value`: System health value (0-100)
- `row_labels`: Row labels ['J', 'K', 'L', 'M', 'N']
- `col_labels`: Column labels ['A', 'S', 'D', 'E', 'F']
- `grid_state`: Dictionary with each cell's state
- `current_input`: Current user input
- `input_status`: Status message for user

### State Management Methods

#### `update_cell(coordinate: str, is_active: bool)`
Updates a specific cell as active or inactive.

**Parameters:**
- `coordinate` (str): Cell coordinate (e.g., "AJ", "SK")
- `is_active` (bool): True for perfect state, False for inactive

#### `set_cell_state(coordinate: str, state: int)`
Sets the specific state of a cell.

**Parameters:**
- `coordinate` (str): Cell coordinate
- `state` (int): Timing state (0-5)

#### `transition_cell(coordinate: str, target_state: int, steps: int = 1)`
Performs a gradual state transition on a cell.

**Parameters:**
- `coordinate` (str): Cell coordinate
- `target_state` (int): Target state
- `steps` (int): Transition steps per update

### Information Configuration Methods

#### `set_active_coords(coords_string: str)`
Updates the active coordinates displayed in the information panel.

#### `set_actual_line(line_string: str)`
Sets the current code line being debugged (truncates to 35 characters).

#### `set_progress(value: int)`
Updates the progress value (limited between 0-100).

#### `set_health(value: int)`
Updates the system health value (limited between 0-100).

### Input Management Methods

#### `set_input(input_text: str)`
Updates the current user input text.

#### `set_input_status(status: str)`
Updates the input status message.

#### `clear_input()`
Clears the input field.

### Layout Construction Methods

#### `_create_header_layout() -> Layout`
Creates the header layout with:
- System title
- Next actions panel
- Debugging line panel

#### `_create_vertical_bar(value: int, height: int = 18) -> Text`
Generates vertical bars for progress and health.

**Parameters:**
- `value` (int): Value to represent (0-100)
- `height` (int): Bar height in characters

**Returns:**
- `Text`: Formatted vertical bar

#### `_create_stats_panel() -> Panel`
Creates the statistics panel with health and progress bars.

#### `_get_cell_display(coord: str, state: int)`
Generates the visual representation of a specific cell.

**Parameters:**
- `coord` (str): Cell coordinate
- `state` (int): Current cell state

**Returns:**
- `list[Text]`: List of formatted text lines

#### `_create_map_display() -> Panel`
Builds the main map panel with the 5x5 grid.

#### `_create_input_panel() -> Panel`
Creates the user input panel with animated cursor.

#### `build_layout() -> Layout`
**Main method** that builds the complete interface layout.

**Returns:**
- `Layout`: Complete Rich layout ready for rendering

---

## Grid Structure

### Coordinates

The system uses a 5x5 grid with:
- **Columns**: A, S, D, E, F (left-hand keys)
- **Rows**: J, K, L, M, N (right-hand keys)
- **Coordinates**: Column+row combination (e.g., AJ, SK, DL, EM, FN)

### Visual State Mapping

```python
# State -> visual style correspondence
VISUAL_STYLES = {
    0: "dim green",                    # Inactive
    1: "dim blue",                     # Early
    2: "blue",                         # Almost Early
    3: "bold blink bright_green",      # Perfect (blinking)
    4: "yellow",                       # Almost Late
    5: "dim orange"                    # Late
}
```

---

## CLI System Usage

### 📖 **Basic Integration**

```python
from src.cli.map import Map

# Create CLI map instance
game_map = Map(size=5)

# Configure game information
game_map.set_active_coords("AJ - SK - DL")
game_map.set_actual_line("if (user.isValid()) {")
game_map.set_progress(75)
game_map.set_health(90)

# Update cell states
game_map.set_cell_state("AJ", 3)  # Perfect timing
game_map.set_cell_state("SK", 2)  # Almost early
game_map.transition_cell("DL", 1, 1)  # Transition to early

# Manage user input
game_map.set_input("AJ")
game_map.set_input_status("Great timing!")

# Build layout for rendering
layout = game_map.build_layout()
```

### 🎮 **Real-time Game Implementation**

```python
from rich.live import Live
from rich.console import Console
import time

def run_game_cli():
    console = Console()
    game_map = Map()
    
    with Live(game_map.build_layout(), console=console, refresh_per_second=30) as live:
        game_running = True
        
        while game_running:
            # Update game logic
            current_time = time.time()
            
            # Process timing events
            game_map.set_active_coords("AJ - DL")
            game_map.set_actual_line(f"Processing line {int(current_time % 100)}")
            
            # Update health and progress based on game state
            progress = int((current_time * 10) % 100)
            health = max(50, 100 - int(current_time % 50))
            
            game_map.set_progress(progress)
            game_map.set_health(health)
            
            # Update live display
            live.update(game_map.build_layout())
            
            time.sleep(0.033)  # ~30 FPS
```

### 🎯 **Animation and Transitions**

```python
# Animate cell transitions
def animate_perfect_hit(game_map, coordinate):
    """Animates a perfect hit with visual effects"""
    # Transition from inactive to perfect
    game_map.transition_cell(coordinate, 3, 2)
    game_map.set_input_status(f"PERFECT! {coordinate}")
    
    # Hold perfect state briefly
    time.sleep(0.2)
    
    # Fade back to inactive
    game_map.transition_cell(coordinate, 0, 1)
    game_map.set_input_status("Ready...")
```

### ⚡ **Performance Considerations**

- **Refresh Rate**: Recommended 30 FPS for smooth animation
- **Layout Caching**: Build layouts efficiently to avoid lag
- **State Updates**: Batch state changes when possible
- **Memory Usage**: Monitor console buffer for long sessions

---

## Integration with BeatBugging Core

### Event System Integration

```python
from src.cli.map import Map
from src.game.timing_system import AdvancedTimingSystem

class GameCLIController:
    def __init__(self):
        self.map = Map()
        self.timing_system = AdvancedTimingSystem()
    
    def on_bug_spawned(self, coordinate, timing_window):
        """Called when a bug appears in the code"""
        self.map.set_cell_state(coordinate, 1)  # Early state
    
    def on_player_input(self, input_coordinate):
        """Called when player inputs a coordinate"""
        result = self.timing_system.evaluate_timing(input_coordinate)
        
        if result.is_perfect:
            self.map.set_cell_state(input_coordinate, 3)  # Perfect
            self.map.set_input_status("PERFECT HIT!")
        elif result.is_good:
            self.map.set_cell_state(input_coordinate, 2)  # Good
            self.map.set_input_status("Good timing!")
        else:
            self.map.set_cell_state(input_coordinate, 5)  # Miss
            self.map.set_input_status("Too late...")
```

### 🔧 **Configuration**

The CLI system can be configured through various constants:

```python
# Visual configuration
GRID_SIZE = 5                    # Size of the game grid
REFRESH_RATE = 30               # FPS for live updates
BAR_HEIGHT = 18                 # Height of progress/health bars
MAX_LINE_LENGTH = 35            # Maximum length for code lines

# Color themes
THEME_MATRIX = {
    'border': 'green',
    'accent': 'bright_green',
    'primary': 'green',
    'perfect': 'bold blink bright_green',
    'good': 'blue',
    'miss': 'red'
}
```

### 🚀 **Future Enhancements**

- **Multi-grid Support**: Support for different grid sizes
- **Custom Themes**: User-configurable color schemes
- **Advanced Animations**: More complex visual effects
- **Performance Metrics**: Real-time performance monitoring
- **Accessibility**: Screen reader support and high contrast modes

---

## Dependencies

- **Rich**: Terminal rendering and layout management
- **typing**: Type hints for better code documentation
- **dataclasses**: Structured data management
- **time**: Animation timing and frame rate control

## Best Practices

1. **State Management**: Keep grid state consistent with game logic
2. **Performance**: Update only changed cells when possible
3. **Visual Feedback**: Provide clear feedback for all user actions
4. **Error Handling**: Gracefully handle invalid coordinates or states
5. **Testing**: Test visual components with different terminal sizes

---

*This documentation covers the complete CLI interface system for BeatBugging. The system provides a rich, interactive terminal experience that enhances the rhythm-based debugging gameplay.*