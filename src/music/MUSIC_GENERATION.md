# Music Module Documentation

This module contains the main functionalities for converting log files into music and generating gameplay data for the BeatBugging game.

## Module Files

- `generator.py` - Main music generator from logs
- `log_utils.py` - Utilities for parsing and processing log files

---

## generator.py

### Main Class: `LogMusicGenerator`

Class responsible for converting log files into procedural music and generating corresponding gameplay data.

#### Constructor

```python
def __init__(self, log_path="none")
```

**Parameters:**
- `log_path` (str): Path to log file. If "none", default log will be used.

**Initialized Attributes:**
- `log_path`: Path to log file
- `fileState`: Boolean file state (True if exists)
- `musicState`: Music state (reserved for future functionalities)
- `default_path`: Default path to `test-app.log` file
- `scale`: Selected musical scale
- `freq`: Base frequency
- `rate`: Audio sampling rate
- `coords`: Coordinates dictionary (reserved)
- `waves`: Dictionary of available wave functions
- `grid_columns`: List of game grid columns ['A', 'S', 'D', 'E', 'F']
- `grid_rows`: List of game grid rows ['J', 'K', 'L', 'M', 'N']

#### Public Methods

##### `useDefaultLog()`
Configures the generator to use the default log file (`logs/test-app.log`).

##### `generate_music(scale="minor", freq=440, rate=44100, speed=2.0)`
Main method that generates music and gameplay data from log file.

**Parameters:**
- `scale` (str): Musical scale ("minor", "major", "pentatonic", "blues")
- `freq` (float): Base frequency in Hz (default 440Hz = A4)
- `rate` (int): Sampling rate in Hz (default 44100Hz)
- `speed` (float): Speed multiplier (higher value = faster)

**Returns:**
```python
{
    "audio_data": np.array,          # Audio data in int16 format
    "sample_rate": int,              # Sampling rate used
    "scale_used": str,               # Musical scale used
    "speed_multiplier": float,       # Speed multiplier applied
    "gameplay_actions": list         # List of gameplay actions
}
```

**Structure of `gameplay_actions`:**
```python
{
    "line": str,           # Original log line
    "tiempo": float,       # Time in seconds from start
    "coordenada": str,     # Grid coordinate (e.g. "A1", "S2")
    "tipo": str,           # Action type ("tap" or "hold")
    "duracion": float      # Action duration (0 for tap)
}
```

#### Private Methods

##### `__generate_scale_notes()`
Generates musical notes for the selected scale.

**Available scales:**
- `minor`: Natural minor scale - melancholic sound [0, 2, 3, 5, 7, 8, 10]
- `major`: Major scale - bright/happy sound [0, 2, 4, 5, 7, 9, 11]
- `pentatonic`: Pentatonic scale - oriental/folk sound [0, 2, 4, 7, 9]
- `blues`: Blues scale - jazzy sound [0, 3, 5, 6, 7, 10]

**Returns:** List of dictionaries with `{"midi": int, "freq": float}`

##### Wave Functions

All wave functions receive the same parameters:
- `freq` (float): Frequency in Hz
- `duration` (float): Duration in seconds
- `volume` (float): Volume (0.0 to 1.0)

###### `__sin_wave(freq, duration, volume=0.5)`
Generates a smooth sine wave using formula: `volume * sin(2π * freq * t)`

###### `__square_wave(freq, duration, volume=0.5)`
Generates a square wave using: `volume * sign(sin(2π * freq * t))`

###### `__saw_wave(freq, duration, volume=0.5)`
Generates a sawtooth wave using: `volume * 0.5 * (t * freq - floor(t * freq + 0.5))`

###### `__triangle_wave(freq, duration, volume=0.5)`
Generates a triangle wave using: `volume * 0.5 * |2 * (t * freq - floor(t * freq + 0.5))| - volume`

##### `_select_wave_severity(log_line)`
Selects wave type based on log severity.

**Severity mapping:**
- `DEBUG` → `sin` (smooth wave)
- `INFO` → `triangle` (moderate wave)
- `WARNING` → `square` (aggressive wave)
- `ERROR` → `saw` (very aggressive wave)
- Other → `triangle` (default)

##### `_generate_wave_sample(wave_type, freq, duration, volume)`
Generates an audio sample using the specified wave type.

##### `_generate_coordinate(note_info, original_line)`
Generates game grid coordinates based on the note's MIDI hash.

**Algorithm:**
- `col_index = midi_hash % len(grid_columns)`
- `row_index = (midi_hash // len(grid_columns)) % len(grid_rows)`

##### `_determine_action_type(original_line, duration)`
Determines if the game action should be "tap" or "hold".

**Logic:**
- `ERROR` → always "hold"
- `WARNING` with duration > 0.5s → "hold"
- Other cases → "tap"

#### Main Function

##### `main()`
Test function that:
1. Creates a generator with default log
2. Generates music in pentatonic scale at 2.0x speed
3. Shows generated gameplay actions
4. Plays audio using pygame (optional)

---

## log_utils.py

### Main Class: `LogMusic`

Utility class for reading, parsing and converting log files into structured musical data.

#### Class Attributes

- `path`: Default path to `test-app.log` file
- `size`: MIDI range (0-127) for mapping hashes to notes
- `log_path`: Current log file path

#### Constructor

```python
def __init__(self, log_path: str | Path | None = None)
```

**Parameters:**
- `log_path`: Path to log file. If None, uses default path.

**Exceptions:**
- `FileNotFoundError`: If specified file doesn't exist.

#### Public Methods

##### `generate_music()`
Test method that reads the log file and displays the number of extracted notes.

##### `read_log_file(log_path=None, default_path=None, encoding='utf-8')`
Reads a log file and returns lines as a list of strings.

**Parameters:**
- `log_path`: Primary file path
- `default_path`: Fallback path
- `encoding`: File encoding (default UTF-8)

**Returns:** List of strings (log lines without whitespace)

**Behavior:**
1. Tries to read `log_path` if it exists
2. If fails, tries `default_path`
3. If both fail, returns empty list
4. Automatically filters empty lines

##### `parse_log_line(line: str) -> dict`
Parses an individual log line and returns a structured dictionary.

**Supported formats:**

1. **Valid JSON**: Returns the dict directly
2. **Logcat (Android)**: Parses format like:
   ```
   2024-01-01 12:00:00.123 1234-5678 TAG PACKAGE LEVEL message
   ```
   Extracted fields: `fecha`, `pid_tid`, `tag`, `paquete`, `nivel`, `mensaje`

3. **Logs with timestamp in brackets**:
   ```
   [2024-01-01 12:00:00] LEVEL message
   ```
   Extracted fields: `fecha`, `nivel`, `mensaje`

4. **Fallback**: `{"mensaje": line}` for any other format

**Parameters:**
- `line` (str): Log line to parse

**Returns:** Dictionary with extracted fields

##### `log_lines_to_dicts(log_lines)`
Converts list of log lines into list of structured "musical notes".

**Conversion algorithm:**
1. Parse each line with `parse_log_line()`
2. Generate stable SHA-256 hash of all fields
3. Convert hash to integer number
4. Map number to MIDI note (0-127)
5. Convert MIDI note to Hz frequency using A4=440Hz
6. Determine duration based on log level
7. Calculate volume based on message length

**Duration mapping by level:**
- `INFO` / `I`: 0.4 seconds
- `DEBUG` / `D`: 0.3 seconds  
- `WARNING` / `W`: 0.6 seconds
- `ERROR` / `E`: 0.8 seconds
- Other: 0.5 seconds

**Volume calculation:**
```python
volume = min(1.0, 0.5 + (len(mensaje) % 50) / 100)
```

**Returns:** List of dictionaries with structure:
```python
{
    "midi": int,        # MIDI note (0-127)
    "freq": float,      # Frequency in Hz
    "duration": float,  # Duration in seconds
    "volume": float,    # Volume (0.0-1.0)
    "raw": dict         # Original parsed data
}
```

#### Regular Expression Patterns

##### `LOGCAT_PATTERN`
```regex
^(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)?\s*
(?P<pid_tid>\d+-\d+)?\s*
(?P<tag>[A-Za-z0-9._]+)?\s*
(?P<paquete>[A-Za-z0-9._]+)?\s*
(?P<nivel>[VDIWEF])?\s*
(?P<mensaje>.*)
```

##### `BRACKET_PATTERN`
```regex
^\[(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+
(?P<nivel>[A-Z]+)\s+
(?P<mensaje>.*)
```

### Global Instance

```python
log_music = LogMusic()
log_music.generate_music()
```

A global instance is created that runs a basic test of the system.

---

## Complete Workflow

1. **Log reading**: `LogMusic.read_log_file()` reads the file
2. **Parsing**: `LogMusic.parse_log_line()` structures each line
3. **Musical conversion**: `LogMusic.log_lines_to_dicts()` converts to notes
4. **Scale generation**: `LogMusicGenerator.__generate_scale_notes()` creates the scale
5. **Wave selection**: `LogMusicGenerator._select_wave_severity()` chooses wave type
6. **Audio generation**: Wave functions create audio samples
7. **Gameplay data**: Coordinates and action types are generated
8. **Final compilation**: All samples are combined into complete audio

## Dependencies

- `numpy`: For wave generation and array manipulation
- `pygame`: For audio playback
- `pathlib`: For file path handling
- `hashlib`: For generating stable hashes
- `json`: For parsing JSON format logs
- `re`: For regular expressions in log parsing
- `time`: For timing functions
- `os`: For file system operations

## Technical Notes

- **Audio format**: Int16, configurable sampling rate (default 44.1kHz)
- **MIDI range**: 0-127 (MIDI standard)
- **Musical scales**: Intervals based on semitones from base note
- **Stable hash**: SHA-256 for consistent log→note mapping
- **Game grid**: 5x5 (25 total positions)
- **Action types**: "tap" (instant) and "hold" (extended duration)
