# 🎵 BeatBugging

**Transform System Logs into Rhythmic Debugging Adventures**

> 🎮 **OH NO, the system crashed!** You open the logs, sit on your hacker's chair and now... IT'S TIME TO BEATBUGGING!

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?logo=pygame&logoColor=white)](https://www.pygame.org/)
[![Rich](https://img.shields.io/badge/Rich-13.9.4-purple?logo=python&logoColor=white)](https://rich.readthedocs.io/)
[![Textual](https://img.shields.io/badge/Textual-6.1.0-orange?logo=textual&logoColor=white)](https://textual.textualize.io/)
[![NumPy](https://img.shields.io/badge/NumPy-2.3.2-blue?logo=numpy&logoColor=white)](https://numpy.org/)

> **BeatBugging** revolutionizes debugging by turning system logs into playable music. Experience errors, warnings, and events as dynamic rhythmic patterns in a beautiful CLI rhythm game.

## ✨ Features

### 🎼 **Procedural Music Engine**
- **Log-to-Audio Conversion** - Transform any log file into dynamic musical sequences
- **Musical Scale Support** - Minor, major, pentatonic, and blues scales for different moods
- **Waveform Selection** - Different log severities trigger unique audio waveforms
  - `DEBUG` → Sine waves (smooth, gentle)
  - `INFO` → Triangle waves (balanced)
  - `WARNING` → Square waves (attention-grabbing)
  - `ERROR` → Sawtooth waves (aggressive, urgent)

### 🎮 **Interactive Rhythm Gameplay**
- **5×5 Grid Interface** - Visual beatmap with coordinates (AJ, SK, DL, EM, FN)
- **Real-time Hit Detection** - Perfect/Good/Okay/Miss timing system
- **Dynamic Difficulty** - Log complexity determines gameplay intensity
- **Visual Feedback** - ASCII animations with opacity-based timing cues

### 🖥️ **Beautiful CLI Experience**
- **Textual UI Framework** - Modern, responsive terminal interface
- **Sound Effects** - Menu navigation and game feedback sounds
- **Animated Screens** - Dynamic ASCII art and transitions
- **Theme System** - Customizable color schemes and visual styles

### 🔧 **Advanced Log Processing**
- **Multi-format Support** - JSON, Logcat (Android), timestamped logs, and fallback parsing
- **Smart Hash Mapping** - Stable SHA-256 conversion from log content to musical notes
- **Configurable Timing** - Adjustable speed multipliers and audio parameters
- **Real-time Generation** - Live conversion during gameplay

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Windows/Linux/macOS
- Audio output device

### Installation

```bash
# Clone the repository
git clone https://github.com/sandra-aliaga/beatbugging.git
cd beatbugging

# Create virtual environment
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Play the Game

```bash
# Run BeatBugging
python main.py
```

## 🎯 How It Works

### 1. **Log Analysis**
```python
# BeatBugging reads your log files
2025-09-11 12:16:24.503  9545-9545  pdv.test.app  E  Invalid ID 0x00000000.
2025-09-11 12:16:24.502  9545-9545  SDL           V  onCreate()
```

### 2. **Musical Conversion**
- Each log line becomes a musical note
- Error severity determines waveform and duration
- Hash algorithms ensure consistent note mapping
- Musical scales create harmonious sequences

### 3. **Rhythm Gameplay**
- Notes appear on a 5×5 grid at precise timestamps
- Players press coordinate keys (A-F, J-N) to "debug" errors
- Perfect timing rewards higher scores and combo multipliers
- Health system adds strategic depth

### 4. **Real-time Feedback**
- Visual opacity changes indicate note timing windows
- Audio feedback confirms successful hits
- Combo system rewards consistent accuracy
- Dynamic difficulty adapts to log complexity

## 🎼 Technical Innovation

### **Procedural Audio Generation**
- **Mathematical Waveforms** - Pure sine, square, triangle, and sawtooth generation
- **MIDI Note Mapping** - 128-note range with A4=440Hz reference
- **Dynamic Scaling** - Musical intervals create harmonious progressions
- **Real-time Synthesis** - Zero-latency audio generation using NumPy

### **Intelligent Log Parsing**
- **Multi-format Recognition** - Automatic detection of log formats
- **Hash-based Consistency** - Identical logs produce identical music
- **Severity Mapping** - Log levels determine gameplay mechanics
- **Content Analysis** - Message length influences volume and timing

### **Advanced Timing System**
- **Precision Windows** - Millisecond-accurate hit detection
- **Visual Feedback** - Opacity-based timing indicators
- **Adaptive Difficulty** - Dynamic adjustment based on log patterns
- **Multi-threaded Architecture** - Separate audio, input, and rendering threads

## 🤝 Contributing

We welcome contributions from developers and musicians alike!

- **🎵 Add New Scales** - Implement exotic musical scales and modes
- **🎮 Game Mechanics** - Enhance gameplay with new features
- **🖥️ UI/UX Improvements** - Polish the visual experience
- **📊 Log Formats** - Support additional log parsing formats
- **🐛 Bug Reports** - [GitHub Issues](https://github.com/sandra-aliaga/beatbugging/issues)
- **💡 Feature Requests** - Share your creative ideas!

## 📋 Dependencies

- **[NumPy](https://numpy.org/)** - High-performance audio array processing
- **[Pygame](https://pygame.org/)** - Audio playback and sound management
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal rendering and layouts
- **[Textual](https://textual.textualize.io/)** - Modern CLI application framework
- **[Keyboard](https://github.com/boppreh/keyboard)** - Cross-platform input handling

## 🆘 Support

- **Documentation**: See `src/music/DOCUMENTATION.md` for technical details
- **Issues**: [GitHub Issues](https://github.com/sandra-aliaga/beatbugging/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sandra-aliaga/beatbugging/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for the GitHub "For the Love of Code" Hackathon**

*Transforming the mundane task of log debugging into an engaging musical adventure. Because every bug deserves a beat!*

### 🏆 **Challenge Category**: Most Innovative Use of Technology
*Combining audio synthesis, rhythm gameplay, and system debugging in one unique experience.*