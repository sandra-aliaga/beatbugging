# BeatBugging

### OH NO, the system crashed, you open the logs, sits on your hacker's chair and now... IT'S TIME TO BEATBUGGING!!!

## Features

- **Interactive Console Game**: Debug logs through rhythm-based gameplay
- **Dynamic Music Generation**: Real-time beats that respond to log patterns
- **Musical Debugging**: Find errors and patterns through audio-visual cues
- **Various Waveforms**: Sine, square, sawtooth, and triangle waves for different log types
- **Adaptive Audio**: Music changes based on log severity and error patterns
- **Collaborative Design**: Music engine + CLI interface working in harmony
- **Interactive Menu System**: Beautiful terminal-based UI with animated ASCII art
- **Dynamic Audio Feedback**: Menu sounds and game start audio with volume control
- **Cross-Platform Support**: Works seamlessly on Windows, Linux, and macOS
- **Theme System**: Customizable color themes for personalized experience
- **Smart File Navigation**: Interactive file tree with difficulty selection modes
- **Audio System**: Non-blocking sound effects with intelligent overlap prevention
- **Responsive Design**: Full-screen layouts with proper focus management

## Game Concept

**BeatBugging** combines the analytical process of log debugging with the engaging experience of rhythm games. Players navigate through system logs while the music engine generates beats and melodies that correspond to different types of errors, warnings, and system events.

**OUR GOAL**: The developer should feel like a hacker - you open the console, see your logs, now it's time to *beatbugging*.

- **Music Engine**: Converts log patterns into dynamic audio
- **CLI Interface**: Interactive console game mechanics
- **Together**: A unique debugging experience where finding bugs feels like playing music

## Project Structure

Current structure with latest updates:

```text
beatbugging/
├── src/
│   ├── menu/                    # Terminal UI and menu system
│   │   ├── main_menu.py        # Main menu screens and navigation
│   │   ├── themes.py           # Theme management system
│   │   ├── themes.json         # Color theme configurations
│   │   └── res/                # Audio resources
│   │       ├── game-start.mp3  # Game start sound effect
│   │       └── menu-click.mp3  # Menu interaction sounds
│   └── music/                  # Music generation core
│       └── generator.py        # Dynamic music generation engine
├── logs/                       # Log files for gameplay
│   └── default.log            # Default log file for testing
├── requirements.txt           # Python dependencies (cross-platform)
├── LICENSE                    # Project license
└── README.md                 # This documentation
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- System audio support (usually pre-installed)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/sandra-aliaga/beatbugging.git
   cd beatbugging
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   cd src/menu
   python main_menu.py
   ```

### Platform Notes
- **Windows**: All dependencies install automatically
- **Linux/macOS**: The `windows-curses` dependency is automatically skipped
- **Audio**: Uses pygame mixer for cross-platform audio support

## How to Play

1. **Launch**: Run `python main_menu.py` from the `src/menu` directory
2. **Navigate**: Use Tab to move between menu elements, Enter to select
3. **Experience**: Enjoy animated ASCII art and responsive audio feedback
4. **Setup Game**: 
   - Browse files using the interactive tree navigation
   - Choose difficulty: **User (normal)** or **Root (hard)** mode
   - Click **Start Game** to begin your musical debugging adventure

## Audio Features

### Sound Effects
- **Menu Clicks**: Subtle audio feedback for all menu interactions
- **Game Start**: Special audio sequence when launching a new game
- **Volume Control**: Optimized levels (30% for UI, 40% for game sounds)
- **Overlap Prevention**: Smart timing system prevents audio interference

### Technical Details
- **Format**: High-quality MP3 audio files
- **Engine**: Pygame mixer for reliable cross-platform playback
- **Threading**: Non-blocking audio to maintain UI responsiveness
- **Fallback**: Graceful degradation if audio system unavailable

## Theme System

The game features a flexible theming system supporting multiple visual styles:

### Available Themes
- **Default**: Classic green terminal hacker aesthetic
- **Blue**: Ocean-inspired blue color scheme
- **Fixed**: System default colors for compatibility

### Customization
Edit `src/menu/themes.json` to modify:
- Background and text colors
- Border and accent colors
- Primary and secondary color schemes
- Danger/warning color indicators

## Planned Features

### Advanced Music Features
- Dynamic tempo adjustments based on log severity levels
- Multi-layered audio composition for complex error patterns
- Real-time audio visualization during gameplay
- Custom audio themes and sound packs
- Adaptive rhythm that responds to debugging progress

### Game Mechanics
- Score system based on debugging accuracy and speed
- Time-based challenges with increasing difficulty
- Multiple game modes with different log complexity levels
- Achievement system for debugging milestones and streaks
- Leaderboards for competitive debugging sessions

### Technical Implementation
- Real-time log streaming and pattern analysis
- Advanced error pattern recognition algorithms
- Multiplayer collaborative debugging sessions
- Cloud log integration for remote debugging
- Plugin system for custom log parsers and audio generators

## Technical Architecture

### Core Components
1. **Menu System** (`main_menu.py`) - Textual-based terminal UI with screen management
2. **Theme Manager** (`themes.py`) - Dynamic color theme system with JSON configuration
3. **Sound Manager** - Pygame-based audio with overlap prevention and volume control
4. **Music Engine** (`generator.py`) - Log pattern analysis and dynamic music generation

### Dependencies
- **textual**: Modern terminal UI framework for responsive interfaces
- **pygame**: Audio playback and game functionality
- **rich**: Enhanced terminal text formatting and styling
- **numpy**: Numerical computations for music generation algorithms

### Cross-Platform Compatibility
- **Windows**: Full compatibility with native terminal and audio systems
- **Linux**: Complete support with system curses and ALSA/PulseAudio
- **macOS**: Native terminal integration with Core Audio support
- **Auto-detection**: Platform-specific paths, audio drivers, and configurations

## Contributing

This is a collaborative project for the GitHub "For the Love of Code" hackathon.

- **Music Engine**: Transforming logs into beats and melodies
- **CLI Game Interface**: Interactive console debugging experience
- **Together**: Creating a unique rhythm-based debugging game

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Navigate to the menu directory for development
cd src/menu

# Run the main application
python main_menu.py
```

### Areas for Contribution
- **Music Engine**: Enhance audio generation algorithms and rhythm patterns
- **UI/UX**: Improve menu design, animations, and user experience
- **Game Mechanics**: Add new gameplay features and debugging challenges
- **Performance**: Optimize audio rendering and UI responsiveness
- **Cross-Platform**: Test and improve compatibility across different systems

## License

See [LICENSE](LICENSE) file for details.

## Topics

`terminal-game` `rhythm-game` `debugging` `music-generation` `python` `textual` `pygame` `hackathon` `audio` `cross-platform` `interactive-menu` `sound-effects` `theme-system`
---

*Made with love for the GitHub For the Love of Code Hackathon*

**Ready to debug with rhythm? Let's start BeatBugging!**
