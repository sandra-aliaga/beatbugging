# Navigation System - Menu Module

Menu system for BeatBugging with TUI interface, theme management, fuzzy search, and sound effects.

## Files

- `main_menu.py` - Main interface with navigation and fuzzy search
- `themes.py` - Theme management system  
- `themes.json` - Color theme configuration
- `res/` - Audio resources (menu-click.mp3, game-start.mp3)

## Features

- **TUI Interface** - Terminal-based UI with Textual
- **Fuzzy Search** - Smart log file discovery and filtering
- **Theme System** - Swappable color themes
- **Sound Effects** - Audio feedback for interactions
- **Smart Navigation** - Screen management with history

## main_menu.py

### Key Components

**LogFile dataclass** - Represents found log files with path, score, size info

**SimpleFuzzyMatcher** - Fuzzy search for .log files using difflib

- Base similarity + bonuses for substring/prefix matches
- Scores 0.0-1.0, filters results above 0.1 threshold

**TitleScreen** - Main menu with animated ASCII logos and sound effects

**SetupScreen** - File selection with fuzzy search, difficulty modes, and preview

**SoundManager** - Audio system with spam prevention and volume control

## themes.py

**ThemeManager** - Loads themes from JSON, applies CSS colors dynamically

- Default themes: "default" (green), "blue" (cyberpunk), "fixed" (terminal colors)

## themes.json

Theme configuration with color schemes:

```json
{
  "themes": {
    "default": {
      "background": "black",
      "primary": "#00ff00", 
      "secondary": "#39ff14",
      "danger": "red",
      "border": "green"
    }
  },
  "default_theme": "default"
}
```

## res/

**Audio files**:

- `menu-click.mp3` - Button click feedback (30% volume)
- `game-start.mp3` - Game start transition (40% volume)

## Navigation Flow

1. **TitleScreen** → Main menu with animated ASCII
2. **SetupScreen** → File search and selection
3. **Game Launch** → Transitions to gameplay with selected log file

**Key bindings**: Enter (select), Escape (back), Tab (navigate), Arrow keys (lists)