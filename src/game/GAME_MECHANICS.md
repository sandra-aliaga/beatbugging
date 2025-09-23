# Game Mechanics Module Documentation# Documentación de Mecánicas de Juego - Módulo Game



This module contains the main game mechanics for BeatBugging, including timing systems, scoring, visual effects, and game screens.Este módulo contiene las mecánicas principales del juego BeatBugging, incluyendo sistemas de timing, puntuación, efectos visuales y pantallas del juego.



## Module Files## Archivos del Módulo



- `timing_system.py` - Advanced timing and scoring system- `timing_system.py` - Sistema avanzado de timing y puntuación

- `opacity_timing.py` - Opacity-based timing and visual states system- `opacity_timing.py` - Sistema de timing basado en opacidad y estados visuales

- `screens.py` - Game screens and ASCII art- `screens.py` - Pantallas del juego y arte ASCII



------



## Overview## Descripción General



The `game` module implements the core game mechanics of BeatBugging, providing:El módulo `game` implementa el núcleo de las mecánicas de juego de BeatBugging, proporcionando:



- **Advanced timing system** with precision and combos- **Sistema de timing avanzado** con precisión y combos

- **Scoring system** with multipliers and statistics- **Sistema de puntuación** con multiplicadores y estadísticas

- **Opacity effects** synchronized with timing- **Efectos de opacidad** sincronizados con timing

- **Animated game screens** with ASCII art- **Pantallas de juego** con arte ASCII animado

- **System health management**- **Gestión de salud** del sistema

- **Player performance statistics**- **Estadísticas de rendimiento** del jugador



------



## timing_system.py - Main Timing System## timing_system.py - Sistema Principal de Timing



### 🎯 **Enum: HitResult**### 🎯 **Enum: HitResult**



Defines the 4 types of precision results:Define los 4 tipos de resultado de precisión:



```python```python

class HitResult(Enum):class HitResult(Enum):

    PERFECT = "perfect"    # Exact timing    PERFECT = "perfect"    # Timing exacto

    GOOD = "good"          # Good timing      GOOD = "good"          # Timing bueno  

    OKAY = "okay"          # Acceptable timing    OKAY = "okay"          # Timing aceptable

    MISS = "miss"          # Failed timing    MISS = "miss"          # Timing fallado

``````



### 📊 **Class: ScoreSystem**### 📊 **Clase: ScoreSystem**



Complete scoring and player statistics system.Sistema completo de puntuación y estadísticas del jugador.



#### **Constructor**#### **Constructor**



```python```python

def __init__(self):def __init__(self):

    self.score = 0              # Total score    self.score = 0              # Puntuación total

    self.combo = 0              # Current combo    self.combo = 0              # Combo actual

    self.max_combo = 0          # Maximum combo reached    self.max_combo = 0          # Combo máximo alcanzado

    self.perfect_hits = 0       # Perfect hits count    self.perfect_hits = 0       # Número de hits perfectos

    self.good_hits = 0          # Good hits count    self.good_hits = 0          # Número de hits buenos

    self.okay_hits = 0          # Okay hits count    self.okay_hits = 0          # Número de hits aceptables

    self.misses = 0             # Misses count    self.misses = 0             # Número de misses

    self.accuracy = 0.0         # Hit accuracy percentage```

    self.combo_multiplier = 1   # Current combo multiplier

```#### **Configuración de Ventanas de Timing**



#### **Core Methods**| Resultado | Ventana (segundos) | Descripción |

|-----------|-------------------|-------------|

##### `add_hit(hit_result: HitResult) -> int`| `PERFECT` | ±0.1 | Timing exacto, máxima puntuación |

Processes a hit result and updates scoring statistics.| `GOOD` | ±0.2 | Timing bueno, alta puntuación |

| `OKAY` | ±0.3 | Timing aceptable, puntuación básica |

**Parameters:**| `MISS` | > 0.3 | Timing fallado, sin puntuación |

- `hit_result` (HitResult): Type of hit achieved

#### **Sistema de Puntuación Base**

**Returns:**

- `int`: Points earned for this hit```python

self.base_points = {

**Logic:**    HitResult.PERFECT: 300,    # 300 puntos base

```python    HitResult.GOOD: 200,       # 200 puntos base  

# Base scoring by hit type    HitResult.OKAY: 100,       # 100 puntos base

BASE_SCORES = {    HitResult.MISS: 0          # 0 puntos

    HitResult.PERFECT: 300,}

    HitResult.GOOD: 100,```

    HitResult.OKAY: 50,

    HitResult.MISS: 0#### **Sistema de Salud**

}

```python

# Combo multiplier increases every 10 consecutive hitsself.health_changes = {

if hit_result != HitResult.MISS:    HitResult.PERFECT: +5,     # Curación por hit perfecto

    self.combo += 1    HitResult.GOOD: +3,        # Curación por hit bueno

    self.combo_multiplier = 1 + (self.combo // 10) * 0.5    HitResult.OKAY: +2,        # Curación por hit aceptable

else:    HitResult.MISS: -2         # Daño por miss

    self.combo = 0}

    self.combo_multiplier = 1```



final_score = base_score * self.combo_multiplier#### **Métodos Principales**

```

##### `evaluate_hit(timing_offset: float) -> HitTiming`

##### `calculate_accuracy() -> float`Evalúa un hit del jugador y calcula el resultado.

Calculates current hit accuracy as a percentage.

**Parámetros:**

**Returns:**- `timing_offset` (float): Diferencia temporal entre el hit y el momento perfecto

- `float`: Accuracy percentage (0.0-100.0)

**Retorna:**

##### `get_statistics() -> dict`- `HitTiming`: Resultado con puntos, cambio de salud y tipo de hit

Returns complete performance statistics.

##### `get_accuracy() -> float`

**Returns:**Calcula la precisión del jugador usando pesos ponderados.

```python

{**Fórmula de Precisión:**

    'score': int,```python

    'combo': int, weighted_score = (

    'max_combo': int,    perfect_hits * 100 +

    'accuracy': float,    good_hits * 75 +

    'total_hits': int,    okay_hits * 50 +

    'hit_distribution': {    misses * 0

        'perfect': int,)

        'good': int, accuracy = (weighted_score / (total_hits * 100)) * 100

        'okay': int,```

        'miss': int

    }##### `get_stats() -> dict`

}Obtiene estadísticas completas del jugador.

```

**Retorna:**

### ⏱️ **Class: AdvancedTimingSystem**```python

{

Advanced timing evaluation with precision windows and combo management.    "score": 15750,

    "combo": 25,

#### **Constructor**    "max_combo": 47,

    "accuracy": 87.5,

```python    "perfect": 12,

def __init__(self):    "good": 8,

    self.score_system = ScoreSystem()    "okay": 3,

        "miss": 2

    # Timing windows (in seconds from perfect timing)}

    self.timing_windows = {```

        'perfect': 0.05,    # ±50ms for perfect

        'good': 0.15,       # ±150ms for good### ⏰ **Clase: AdvancedTimingSystem**

        'okay': 0.25        # ±250ms for okay

    }Sistema avanzado de timing con soporte para BPM y pausas.

```

#### **Constructor**

#### **Core Methods**

```python

##### `evaluate_timing(time_offset: float) -> TimingResult`def __init__(self, bpm: float = 120.0):

Evaluates timing precision and updates scoring system.    self.bpm = bpm                          # BPM de la canción

    self.beat_duration = 60.0 / bpm         # Duración de un beat

**Parameters:**    self.start_time = None                  # Tiempo de inicio

- `time_offset` (float): Time difference from perfect timing (seconds)    self.paused_time = 0                    # Tiempo acumulado en pausa

    self.is_paused = False                  # Estado de pausa

**Returns:**```

```python

@dataclass#### **Métodos de Control de Tiempo**

class TimingResult:

    result: HitResult           # Type of hit achieved##### `start()`

    points_earned: int          # Points gainedInicia el sistema de timing.

    time_difference: float      # Exact timing difference

    accuracy_rating: str        # Human-readable accuracy##### `pause()` / `resume()`

    combo_active: bool          # Whether combo is activePausa y reanuda el sistema manteniendo sincronización.

```

##### `get_current_time() -> float`

**Timing Evaluation Logic:**Obtiene el tiempo actual del juego considerando pausas.

```python

abs_offset = abs(time_offset)##### `get_current_beat() -> float`

Convierte el tiempo actual a beats musicales.

if abs_offset <= self.timing_windows['perfect']:

    return HitResult.PERFECT##### `time_to_beat(game_time: float) -> float`

elif abs_offset <= self.timing_windows['good']:Convierte tiempo de juego a beats.

    return HitResult.GOOD  

elif abs_offset <= self.timing_windows['okay']:##### `beat_to_time(beat: float) -> float`

    return HitResult.OKAYConvierte beats a tiempo de juego.

else:

    return HitResult.MISS---

```

## opacity_timing.py - Sistema de Timing Visual

##### `get_timing_feedback(time_offset: float) -> str`

Generates human-readable timing feedback.### 🎭 **Enum: TimingState**



**Parameters:**Define los 6 estados visuales de timing:

- `time_offset` (float): Time offset from perfect timing

```python

**Returns:**class TimingState(Enum):

- `str`: Feedback message like "Perfect!" or "Too early!"    EARLY = "early"              # Muy temprano

    ALMOST_EARLY = "almost_early" # Casi perfecto (temprano)

##### `adjust_difficulty(accuracy: float)`    PERFECT = "perfect"          # Timing perfecto

Dynamically adjusts timing windows based on player performance.    ALMOST_LATE = "almost_late"  # Casi perfecto (tardío)

    LATE = "late"                # Muy tardío

**Parameters:**    MISS = "miss"                # Perdido completamente

- `accuracy` (float): Current player accuracy (0.0-1.0)```



**Logic:**### 📋 **Dataclass: TimingResult**

- If accuracy > 90%: Tighten windows by 10%

- If accuracy < 50%: Widen windows by 20%Resultado completo de evaluación de timing visual:

- Maintains game challenge while preventing frustration

```python

---@dataclass

class TimingResult:

## opacity_timing.py - Visual Effects System    state: TimingState          # Estado de timing actual

    opacity: float              # Opacidad para renderizado (0.0-1.0)

### 🎨 **Class: OpacityTimingSystem**    time_offset: float          # Offset temporal en segundos

    points: int                 # Puntos potenciales

Manages visual effects based on timing states from configuration.    color_hint: str             # Sugerencia de color

    should_display: bool        # Si debe mostrarse visualmente

#### **Constructor**```



```python### 🎨 **Clase: OpacityTimingSystem**

def __init__(self, config_path: str = "src/config/timing_states.json"):

    self.config = self.load_config(config_path)Sistema de timing basado en efectos de opacidad y colores.

    self.active_effects = {}  # Track active visual effects

```#### **Constructor**



#### **Core Methods**```python

def __init__(self, config_path: Optional[str] = None):

##### `get_opacity_for_timing(time_offset: float) -> float`    self.config_path = config_path or self._get_default_config_path()

Calculates opacity based on timing state configuration.    self.config = self._load_config()

    self.states_config = self.config["timing_states"]

**Parameters:**    self.global_settings = self.config["global_settings"]

- `time_offset` (float): Time from perfect moment```



**Returns:**#### **Configuración de Estados por Defecto**

- `float`: Opacity value (0.0-1.0)

| Estado | Rango Temporal | Opacidad | Color | Descripción |

**Implementation:**|--------|----------------|----------|-------|-------------|

```python| `early` | [-4.0, -2.0] | 0.2 | dim_blue | Bug aparece muy tenue |

def get_opacity_for_timing(self, time_offset: float) -> float:| `almost_early` | [-2.0, -1.0] | 0.5 | blue | Bug se hace más visible |

    timing_states = self.config['timing_states']| `perfect` | [-1.0, 1.0] | 1.0 | bright_green | Timing perfecto, completamente visible |

    | `almost_late` | [1.0, 2.0] | 0.6 | yellow | Empieza a desvanecer |

    for state_name, state_config in timing_states.items():| `late` | [2.0, 3.0] | 0.3 | orange | Muy tenue, timing perdido |

        start_time, end_time = state_config['time_range']| `miss` | [3.0, 5.0] | 0.0 | red | Invisible, completamente perdido |

        if start_time <= time_offset <= end_time:

            return state_config['opacity']#### **Método Principal: `calculate_timing_state()`**

    

    return 0.0  # Default invisible if outside all ranges```python

```def calculate_timing_state(self, current_time: float, target_time: float) -> TimingResult:

    """

##### `get_visual_state(time_offset: float) -> VisualState`    Calcula el estado visual de timing basado en el tiempo.

Returns complete visual state information.    

    Args:

**Returns:**        current_time: Tiempo actual del juego

```python        target_time: Tiempo objetivo del bug/acción

@dataclass        

class VisualState:    Returns:

    opacity: float              # Visual opacity (0.0-1.0)        TimingResult con estado, opacidad y efectos visuales

    color_hint: str            # Suggested color    """

    should_blink: bool         # Whether element should blink```

    transition_speed: float    # Animation transition speed

    state_name: str           # Current state name**Lógica de Cálculo:**

```1. Calcula offset temporal: `time_offset = current_time - target_time`

2. Busca el estado correspondiente según rangos temporales

##### `apply_visual_effects(element, time_offset: float)`3. Extrae opacidad, color y puntos de la configuración

Applies visual effects to a game element based on timing.4. Retorna `TimingResult` completo



**Parameters:**#### **Métodos Auxiliares**

- `element`: Game element to apply effects to

- `time_offset` (float): Current timing offset##### `get_opacity_for_time(current_time: float, target_time: float) -> float`

Obtiene solo la opacidad para un momento dado.

##### `create_transition_effect(from_state: str, to_state: str) -> TransitionEffect`

Creates smooth transitions between visual states.##### `get_color_hint(current_time: float, target_time: float) -> str`

Obtiene la sugerencia de color para un momento dado.

**Returns:**

```python##### `is_in_perfect_window(current_time: float, target_time: float) -> bool`

@dataclass  Verifica si está en la ventana de timing perfecto.

class TransitionEffect:

    duration: float            # Transition duration in seconds---

    opacity_curve: Callable    # Opacity interpolation function

    color_interpolation: Callable  # Color transition function## screens.py - Pantallas del Juego

```

### 🎨 **Clase: AsciiArt**

---

Contenedor de arte ASCII para pantallas del juego.

## screens.py - Game Screens and ASCII Art

#### **Método: `get_game_over_screen()`**

### 🎮 **Class: AsciiArt**

Retorna arte ASCII para la pantalla de Game Over:

Manages animated ASCII art for game screens.

```

#### **Static Methods**╔═══════════════════════════════════════════════════════════════════════════════════════╗

║                                                                                       ║

##### `get_beat_logo() -> List[str]`║   ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████   ║

Returns the main BeatBugging logo in ASCII art.║  ██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██  ║

║  ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████   ║

**Returns:**║  ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██  ║

```python║   ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██  ║

[║                                                                                       ║

    "╔══════════════════════════════════╗",╚═══════════════════════════════════════════════════════════════════════════════════════╝

    "║  ██████╗ ███████╗ █████╗ ████████║",```

    "║  ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝",

    "║  ██████╔╝█████╗  ███████║   ██║   ║", #### **Método: `get_game_over_animation()`**

    "║  ██╔══██╗██╔══╝  ██╔══██║   ██║   ║",

    "║  ██████╔╝███████╗██║  ██║   ██║   ║",Retorna múltiples frames para animación de Game Over con efectos de:

    "║  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ║",- Expansión y contracción

    "║                                  ║",- Efectos de partículas

    "║        DEBUGGING  GAME           ║", - Transiciones suaves

    "╚══════════════════════════════════╝"- Arte ASCII detallado de explosión/implosión

]

```### 📺 **Funcionalidades de Pantalla**



##### `get_game_over_screen(score: int, accuracy: float) -> List[str]`#### **Pantalla de Game Over**

Generates game over screen with final statistics.- Arte ASCII estático con bordes decorativos

- Texto "GAME OVER" en fuente ASCII grande

**Parameters:**- Bordes con caracteres Unicode para apariencia profesional

- `score` (int): Final player score

- `accuracy` (float): Final accuracy percentage#### **Animación de Game Over**

- Múltiples frames de animación

##### `get_loading_animation(frame: int) -> List[str]`- Efectos de explosión ASCII

Returns loading animation frame.- Transición de partículas

- Sincronización con timing del juego

**Parameters:**

- `frame` (int): Animation frame number (0-7)---



**Animation Sequence:**## Integración entre Sistemas

```python

LOADING_FRAMES = [### 🔄 **Flujo de Trabajo Típico**

    "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"

]```python

```def game_loop_example():

    # Inicializar sistemas

##### `get_combo_animation(combo_count: int) -> List[str]`    timing_system = AdvancedTimingSystem(bpm=120)

Creates animated combo display for high combos.    score_system = ScoreSystem()

    opacity_system = OpacityTimingSystem()

**Parameters:**    

- `combo_count` (int): Current combo count    timing_system.start()

    

**Visual Effects:**    while game_running:

- Combos 10-49: Simple highlight        current_time = timing_system.get_current_time()

- Combos 50-99: Pulsing effect        

- Combos 100+: Multi-color rainbow effect        # Para cada bug activo

        for bug in active_bugs:

### 🏆 **Class: GameScreens**            # Calcular estado visual

            timing_result = opacity_system.calculate_timing_state(

Manages different game screen states and transitions.                current_time, bug.target_time

            )

#### **Constructor**            

            # Actualizar visualización del bug

```python            bug.opacity = timing_result.opacity

def __init__(self):            bug.color = timing_result.color_hint

    self.current_screen = "main_menu"            bug.visible = timing_result.should_display

    self.transition_time = 0.5  # Screen transition duration            

    self.ascii_art = AsciiArt()            # Si el jugador hace clic

```            if player_clicked(bug):

                hit_timing = score_system.evaluate_hit(timing_result.time_offset)

#### **Core Methods**                

                # Actualizar UI con resultados

##### `render_main_menu() -> str`                display_hit_feedback(hit_timing)

Renders the main menu screen with animated elements.                update_health(hit_timing.health_change)

                

##### `render_game_screen(game_state: GameState) -> str`                # Remover bug si fue golpeado

Renders the main gameplay screen.                if hit_timing.result != HitResult.MISS:

                    active_bugs.remove(bug)

**Parameters:**```

```python

@dataclass### 📊 **Sincronización de Sistemas**

class GameState:

    score: int#### **Timing System ↔ Opacity System**

    combo: int  ```python

    accuracy: float# El timing system proporciona tiempo actual

    health: intcurrent_time = timing_system.get_current_time()

    active_bugs: List[Bug]

    current_line: str# El opacity system calcula efectos visuales

```visual_state = opacity_system.calculate_timing_state(current_time, target_time)

```

##### `render_pause_screen() -> str`

Renders pause screen with game statistics.#### **Score System ↔ Timing Results**

```python

##### `render_settings_screen() -> str`# Evaluar hit usando offset del opacity system

Renders settings/configuration screen.hit_result = score_system.evaluate_hit(visual_state.time_offset)



##### `transition_to_screen(screen_name: str, transition_type: str = "fade")`# Combinar puntos de ambos sistemas

Handles smooth transitions between screens.total_points = hit_result.points + visual_state.points

```

**Parameters:**

- `screen_name` (str): Target screen name---

- `transition_type` (str): Type of transition ("fade", "slide", "instant")

## Ejemplos de Uso

---

### 🎮 **Implementación Básica de Juego**

## **🎮 Integration Examples**

```python

### Complete Game Loop Integrationfrom src.game.timing_system import AdvancedTimingSystem, ScoreSystem

from src.game.opacity_timing import OpacityTimingSystem

```pythonfrom src.game.screens import AsciiArt

from src.game.timing_system import AdvancedTimingSystem, HitResult

from src.game.opacity_timing import OpacityTimingSystem  def initialize_game():

from src.game.screens import GameScreens    """Inicializar todos los sistemas de juego"""

from src.cli.map import Map    timing = AdvancedTimingSystem(bpm=120)

    scoring = ScoreSystem()

class BeatBuggingGame:    opacity = OpacityTimingSystem()

    def __init__(self):    

        self.timing_system = AdvancedTimingSystem()    return timing, scoring, opacity

        self.opacity_system = OpacityTimingSystem()

        self.screens = GameScreens()def handle_player_input(bug_coordinate, target_time, systems):

        self.cli_map = Map()    """Manejar input del jugador"""

        self.game_state = "playing"    timing_sys, score_sys, opacity_sys = systems

        

    def handle_player_input(self, coordinate: str, timestamp: float):    current_time = timing_sys.get_current_time()

        """Process player input and update all systems"""    

        # Calculate timing offset    # Evaluar hit con ambos sistemas

        perfect_time = self.get_perfect_timing_for_bug(coordinate)    opacity_result = opacity_sys.calculate_timing_state(current_time, target_time)

        time_offset = timestamp - perfect_time    hit_result = score_sys.evaluate_hit(opacity_result.time_offset)

            

        # Evaluate timing    return {

        timing_result = self.timing_system.evaluate_timing(time_offset)        "hit_type": hit_result.result,

                "points": hit_result.points,

        # Update visual effects        "health_change": hit_result.health_change,

        visual_state = self.opacity_system.get_visual_state(time_offset)        "visual_feedback": {

                    "opacity": opacity_result.opacity,

        # Update CLI display            "color": opacity_result.color_hint

        if timing_result.result == HitResult.PERFECT:        }

            self.cli_map.set_cell_state(coordinate, 3)    }

            self.cli_map.set_input_status("PERFECT!")```

        elif timing_result.result == HitResult.GOOD:

            self.cli_map.set_cell_state(coordinate, 2) ### 📈 **Gestión de Estadísticas**

            self.cli_map.set_input_status("Good!")

        else:```python

            self.cli_map.set_cell_state(coordinate, 5)def display_game_stats(score_system):

            self.cli_map.set_input_status("Miss...")    """Mostrar estadísticas del juego"""

            stats = score_system.get_stats()

        return timing_result    

        print(f"Score: {stats['score']:,}")

    def update_game_state(self, delta_time: float):    print(f"Accuracy: {stats['accuracy']:.1f}%")

        """Update all game systems"""    print(f"Max Combo: {stats['max_combo']}")

        # Update timing windows based on performance    print(f"Perfect: {stats['perfect']} | Good: {stats['good']}")

        stats = self.timing_system.score_system.get_statistics()    print(f"Okay: {stats['okay']} | Miss: {stats['miss']}")

        self.timing_system.adjust_difficulty(stats['accuracy'] / 100.0)

        def check_game_over_condition(health, score_system):

        # Update visual effects for all active bugs    """Verificar condiciones de Game Over"""

        for bug in self.active_bugs:    if health <= 0:

            time_offset = self.calculate_timing_offset(bug)        show_game_over_screen()

            opacity = self.opacity_system.get_opacity_for_timing(time_offset)        return True

            bug.set_opacity(opacity)    return False

        

        # Update CLI with current statedef show_game_over_screen():

        self.cli_map.set_progress(int(self.game_progress * 100))    """Mostrar pantalla de Game Over"""

        self.cli_map.set_health(self.system_health)    game_over_art = AsciiArt.get_game_over_screen()

```    for frame in game_over_art:

        print(frame)

### Performance Monitoring```



```python---

class PerformanceTracker:

    def __init__(self):## Configuración y Personalización

        self.timing_history = []

        self.accuracy_trend = []### ⚙️ **Personalizar Ventanas de Timing**

    

    def track_performance(self, timing_result: TimingResult):```python

        """Track player performance over time"""# Modificar timing windows en ScoreSystem

        self.timing_history.append({score_system = ScoreSystem()

            'timestamp': time.time(),score_system.timing_windows[HitResult.PERFECT] = 0.05  # Más estricto

            'result': timing_result.result,score_system.timing_windows[HitResult.GOOD] = 0.15     # Más estricto

            'time_difference': timing_result.time_difference,```

            'points': timing_result.points_earned

        })### 🎨 **Personalizar Estados de Opacidad**

        

        # Calculate rolling accuracy```python

        recent_results = self.timing_history[-50:]  # Last 50 hits# Crear configuración personalizada

        hits = len([r for r in recent_results if r['result'] != HitResult.MISS])custom_config = {

        accuracy = hits / len(recent_results) if recent_results else 0.0    "timing_states": {

        self.accuracy_trend.append(accuracy)        "early": {"time_range": [-3.0, -1.5], "opacity": 0.3, "color_hint": "cyan"},

            "perfect": {"time_range": [-1.5, 1.5], "opacity": 1.0, "color_hint": "green"},

    def get_performance_analysis(self) -> dict:        "late": {"time_range": [1.5, 3.0], "opacity": 0.3, "color_hint": "magenta"}

        """Analyze player performance patterns"""    },

        if not self.timing_history:    "global_settings": {

            return {}        "scoring_weights": {"early": 75, "perfect": 500, "late": 75}

            }

        return {}

            'average_accuracy': sum(self.accuracy_trend) / len(self.accuracy_trend),

            'timing_consistency': self.calculate_consistency(),opacity_system = OpacityTimingSystem()

            'improvement_trend': self.calculate_trend(),opacity_system.config = custom_config

            'best_streak': self.find_best_streak()```

        }

```### 🏆 **Sistema de Dificultad Personalizado**



---```python

def create_difficulty_system(difficulty_level):

## **⚡ Performance Optimization**    """Crear sistema con dificultad específica"""

    

### Timing System Optimization    difficulty_configs = {

        "easy": {

1. **Cache Calculations**: Pre-calculate timing windows            "timing_windows": {"PERFECT": 0.15, "GOOD": 0.25, "OKAY": 0.35},

2. **Batch Updates**: Process multiple timing events together              "health_multiplier": 1.5,

3. **Memory Pool**: Reuse TimingResult objects            "point_multiplier": 0.8

4. **Frame Rate**: Limit updates to display refresh rate        },

        "normal": {

### Visual Effects Optimization            "timing_windows": {"PERFECT": 0.1, "GOOD": 0.2, "OKAY": 0.3},

            "health_multiplier": 1.0,

1. **Opacity Caching**: Cache opacity calculations for common offsets            "point_multiplier": 1.0

2. **Transition Smoothing**: Use interpolation for smooth animations        },

3. **Effect Culling**: Don't process off-screen effects        "hard": {

4. **State Batching**: Update visual states in batches            "timing_windows": {"PERFECT": 0.07, "GOOD": 0.15, "OKAY": 0.25},

            "health_multiplier": 0.7,

---            "point_multiplier": 1.3

        }

## **🔧 Configuration and Tuning**    }

    

### Timing Sensitivity Adjustment    config = difficulty_configs.get(difficulty_level, difficulty_configs["normal"])

    

```python    score_system = ScoreSystem()

# Easy mode - more forgiving timing    for result, window in config["timing_windows"].items():

EASY_TIMING_WINDOWS = {        score_system.timing_windows[getattr(HitResult, result)] = window

    'perfect': 0.08,    # ±80ms    

    'good': 0.20,       # ±200ms      return score_system

    'okay': 0.35        # ±350ms```

}

---

# Hard mode - precise timing required

HARD_TIMING_WINDOWS = {## Dependencias del Módulo

    'perfect': 0.03,    # ±30ms

    'good': 0.08,       # ±80ms### 📚 **Librerías Externas**

    'okay': 0.15        # ±150ms

}```python

```from rich.console import Console      # Para renderizado de pantallas

from rich.text import Text            # Para texto formateado

### Visual Effect Tuningfrom rich.panel import Panel          # Para paneles decorativos

from rich.table import Table          # Para tablas de stats

```pythonfrom rich.layout import Layout        # Para layouts de pantalla

# High-performance mode - reduced visual effectsfrom rich.align import Align          # Para alineación

PERFORMANCE_VISUAL_CONFIG = {import json                          # Para configuraciones

    "fade_in_duration": 0.1,import time                          # Para timing del sistema

    "fade_out_duration": 0.1,from enum import Enum                # Para enumeraciones

    "blink_frequency": 2.0,from dataclasses import dataclass    # Para estructuras de datos

    "color_transition_steps": 3,from typing import Optional, Dict, Any  # Para type hints

    "opacity_curve": "linear"```

}

### 🔗 **Integración con Otros Módulos**

# Enhanced mode - rich visual effects  

ENHANCED_VISUAL_CONFIG = {```python

    "fade_in_duration": 0.5,# Integración típica con otros módulos del proyecto

    "fade_out_duration": 0.7, from src.config.timing_states import load_timing_config  # Configuración de timing

    "blink_frequency": 4.0,from src.cli.map import Map                              # Visualización CLI

    "color_transition_steps": 20,```

    "opacity_curve": "ease_in_out"

}---

```

## Consideraciones de Rendimiento

---

### ⚡ **Optimizaciones Implementadas**

*This documentation covers the complete game mechanics system for BeatBugging. The modular design allows for easy customization of timing sensitivity, visual effects, and performance characteristics while maintaining consistent gameplay experience.*
1. **Cálculo eficiente de timing**: Algoritmo O(n) para determinar estado
2. **Cacheo de configuración**: Carga única del archivo JSON
3. **Dataclasses**: Estructuras optimizadas para datos de timing
4. **Enums**: Comparaciones rápidas para estados

### 💡 **Mejores Prácticas**

1. **Inicialización única**: Crear sistemas una sola vez al inicio
2. **Reutilización de objetos**: Evitar crear TimingResult en cada frame
3. **Batch processing**: Procesar múltiples bugs simultáneamente
4. **Límite de precisión**: Usar float con precisión apropiada

---

## Extensiones Futuras

### 🚀 **Características Planeadas**

1. **Sistema de power-ups**: Modificadores temporales de timing
2. **Modos de juego**: Diferentes mecánicas (survival, accuracy, speed)
3. **Replay system**: Grabación y reproducción de sesiones
4. **AI difficulty**: Ajuste automático de dificultad basado en rendimiento
5. **Multiplayer**: Soporte para múltiples jugadores

### 🎨 **Mejoras Visuales**

1. **Efectos de partículas**: Sistemas de partículas para hits especiales
2. **Transiciones suaves**: Interpolación entre estados de opacidad
3. **Temas visuales**: Múltiples esquemas de colores y efectos
4. **Pantallas dinámicas**: Generación procedural de arte ASCII
