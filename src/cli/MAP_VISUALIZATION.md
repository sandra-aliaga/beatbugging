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
            
            # Actualizar estado de celdas basado en timing
            for coord in game_map.grid_state.keys():
                # Lógica de timing aquí
                if should_activate_cell(coord, current_time):
                    game_map.set_cell_state(coord, 3)  # Perfect
                elif should_deactivate_cell(coord, current_time):
                    game_map.transition_cell(coord, 0, 1)  # Transición a inactivo
            
            # Actualizar información del sistema
            game_map.set_progress(calculate_progress())
            game_map.set_health(calculate_health())
            
            # Refrescar pantalla
            live.update(game_map.build_layout())
            time.sleep(0.033)  # ~30 FPS
```

### 🎹 **Manejo de Entrada del Usuario**

```python
import keyboard

def handle_user_input(game_map):
    """Maneja la entrada del usuario en tiempo real"""
    
    def on_key_press(event):
        key = event.name.lower()
        
        # Teclas de columnas (mano izquierda)
        if key in ['a', 's', 'd', 'e', 'f']:
            current_input = game_map.current_input
            if len(current_input) == 0:
                game_map.set_input(key.upper())
                game_map.set_input_status("Select row key (J, K, L, M, N)...")
        
        # Teclas de filas (mano derecha)  
        elif key in ['j', 'k', 'l', 'm', 'n']:
            current_input = game_map.current_input
            if len(current_input) == 1:
                coordinate = current_input + key.upper()
                
                # Validar y procesar el hit
                if validate_hit(coordinate):
                    game_map.set_input_status("Great hit!")
                    process_successful_hit(coordinate)
                else:
                    game_map.set_input_status("Missed!")
                
                game_map.clear_input()
        
        # Teclas de control
        elif key == 'escape':
            return False  # Salir del juego
        elif key == 'space':
            toggle_pause()
    
    keyboard.on_press(on_key_press)
```

---

## Estructura del Grid CLI

### 🎯 **Sistema de Coordenadas**

El CLI utiliza un sistema de coordenadas que mapea directamente a las teclas del teclado:

```
    A    S    D    E    F     <- Columnas (mano izquierda)
J  AJ   SJ   DJ   EJ   FJ    <- Fila J
K  AK   SK   DK   EK   FK    <- Fila K  
L  AL   SL   DL   EL   FL    <- Fila L
M  AM   SM   DM   EM   FM    <- Fila M
N  AN   SN   DN   EN   FN    <- Fila N
^
Filas (mano derecha)
```

### 🎨 **Representación Visual de Estados**

Cada celda en el CLI se representa con caracteres ASCII que indican su estado:

```python
# Estado PERFECT (timing perfecto)
"╔═════╗"
"║ AJ  ║"  # Coordenada mostrada
"║█████║"  # Relleno completo
"╚═════╝"  # Bordes dobles

# Estado EARLY (muy temprano)  
"┌─────┐"
"│ AJ  │"  # Coordenada mostrada
"│░░░░░│"  # Relleno tenue
"└─────┘"  # Bordes simples
```

### 📊 **Estados Visuales del CLI**

| Estado | Bordes | Relleno | Color | Descripción |
|--------|--------|---------|-------|-------------|
| `INACTIVE` | Simples (`┌┐└┘`) | Vacío | `dim green` | Celda sin bug activo |
| `EARLY` | Simples (`┌┐└┘`) | Tenue (`░░░`) | `dim blue` | Bug muy temprano |
| `ALMOST_EARLY` | Simples (`┌┐└┘`) | Medio (`▒▒▒`) | `blue` | Bug acercándose |
| `PERFECT` | Dobles (`╔╗╚╝`) | Completo (`███`) | `bright_green blink` | Timing perfecto |
| `ALMOST_LATE` | Dobles (`╔╗╚╝`) | Degradado (`▓▓▓`) | `yellow` | Bug alejándose |
| `LATE` | Simples (`┌┐└┘`) | Tenue (`░░░`) | `dim orange` | Bug muy tardío |

---

## Personalización del CLI

### 🎨 **Personalizar Colores**

```python
# Modificar constantes de color en map.py
BORDER_COLOR = "cyan"           # Color de bordes
ACCENT_COLOR = "bright_cyan"    # Color de acentos  
PRIMARY_COLOR = "white"         # Color principal
```

### 📐 **Cambiar Tamaño del Grid**

```python
# Crear un grid más pequeño (3x3)
small_map = Map(size=3)

# El grid utilizará:
# Columnas: ['A', 'S', 'D'] 
# Filas: ['J', 'K', 'L']
```

### 🔤 **Personalizar Caracteres ASCII**

```python
# Modificar plantillas de celdas
CELL_CUSTOM = [
    "▄▄▄▄▄▄▄",
    "█ COO █", 
    "█▓▓▓▓▓█",
    "▀▀▀▀▀▀▀"
]
```

---

## Consideraciones de Rendimiento del CLI

### ⚡ **Optimizaciones Implementadas**

1. **Reutilización de Objetos**: Las plantillas de celdas se definen como constantes
2. **Actualización Selectiva**: Solo se renderizar celdas que cambiaron de estado
3. **Limitación de FPS**: Máximo 30 FPS recomendado para evitar parpadeo
4. **Truncado de Texto**: Las líneas largas se truncan automáticamente a 35 caracteres

### 💻 **Requerimientos del Terminal**

- **Tamaño mínimo**: 120x40 caracteres para visualización óptima
- **Soporte Unicode**: Necesario para caracteres de bordes y rellenos especiales
- **Soporte de colores**: Terminal compatible con ANSI colors
- **Velocidad de actualización**: Terminal que soporte actualizaciones rápidas sin parpadeo

---

## Dependencias del Módulo CLI

### 📚 **Librerías Externas Requeridas**

```python
from rich.console import Console    # Manejo de salida del terminal
from rich.layout import Layout      # Sistema de layouts flexibles
from rich.live import Live          # Renderizado en tiempo real  
from rich.panel import Panel        # Paneles con bordes decorativos
from rich.table import Table        # Tablas y grids estructurados
from rich.text import Text          # Texto formateado y con estilos
from rich.align import Align        # Alineación de contenido
from rich.box import HEAVY, DOUBLE_EDGE  # Estilos de bordes predefinidos
```

### 🔗 **Posibles Integraciones Futuras**

```python
# Integraciones típicas con otros módulos del proyecto
from src.config.timing_states import load_timing_config  # Estados de timing
from src.music.generator import LogMusicGenerator        # Generación de música
from src.game.timing_system import TimingEngine          # Motor de timing
```

---

## Limitaciones del CLI

### ⚠️ **Limitaciones Conocidas**

1. **Tamaño de grid fijo**: Optimizado para 5x5, cambios requieren modificaciones manuales en plantillas
2. **Dependencia de terminal avanzado**: Requiere terminal con soporte completo Unicode y colores ANSI
3. **Resolución mínima estricta**: Funcionalidad limitada o rota en terminales menores a 120x40
4. **Rendimiento variable por SO**: Posible menor rendimiento en cmd/PowerShell vs terminales Unix

### 🔧 **Detección y Manejo de Limitaciones**

```python
def detect_terminal_capabilities():
    """Detecta y valida las capacidades del terminal"""
    console = Console()
    
    if not console.is_terminal:
        raise RuntimeError("No se detectó terminal interactivo")
    
    if console.size.width < 120 or console.size.height < 40:
        print("⚠️ Terminal pequeño detectado. La experiencia puede ser limitada.")
        return False
    
    capabilities = {
        "unicode_support": True,  # Rich maneja esto automáticamente
        "color_support": console.color_system is not None,
        "size": console.size,
        "interactive": console.is_terminal
    }
    
    return capabilities
```

---

## Extensiones Futuras del CLI

### 🚀 **Características Planeadas**

1. **Grid dinámico**: Sistema para soportar diferentes tamaños (3x3, 7x7, etc.)
2. **Temas intercambiables**: Múltiples esquemas de colores y caracteres
3. **Efectos de transición**: Animaciones suaves entre cambios de estado
4. **Modo espectador**: Vista de solo lectura para análisis y replays
5. **Multi-panel**: Soporte para múltiples vistas simultáneas

### 💡 **Mejoras de Usabilidad Propuestas**

```python
def show_cli_help():
    """Sistema de ayuda integrado en el CLI"""
    help_panel = Panel(
        """
        🎮 CONTROLES DEL JUEGO:
        A,S,D,E,F + J,K,L,M,N = Seleccionar coordenada (ej: AJ, SK)
        SPACE = Pausar/Reanudar el juego
        ESC = Salir del juego
        
        🎯 ESTADOS VISUALES:
        ░ = Early (muy temprano)    ▒ = Almost Early (casi perfecto)
        █ = Perfect (timing perfecto)    ▓ = Almost Late (pasándose)
        ░ = Late (muy tardío)    [ ] = Inactive (sin bug)
        
        🏆 SISTEMA DE PUNTUACIÓN:
        Perfect: 300pts    Almost Early/Late: 100-150pts    
        Early/Late: 25-50pts    Miss: 0pts
        """,
        title="[bold green]AYUDA - BEATBUGGING CLI[/]",
        border_style="green"
    )
    return help_panel

def create_debug_overlay():
    """Panel de información de debug para desarrollo"""
    debug_info = Table(title="Debug Info")
    debug_info.add_column("Métrica", style="cyan")
    debug_info.add_column("Valor", style="white")
    
    debug_info.add_row("FPS", "30.0")
    debug_info.add_row("Celdas Activas", "3/25")
    debug_info.add_row("Memoria Used", "2.3MB")
    debug_info.add_row("Terminal Size", "120x40")
    
    return Panel(debug_info, title="[red]DEBUG[/]")
```
