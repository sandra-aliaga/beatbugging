# Configuration Module Documentation# Configuration Module Documentation



This module contains specific configurations for the timing system and visual states for BeatBugging.This module contains specific configurations for the timing system and visual states for BeatBugging.



## Module Files## Module Files



- `timing_states.json` - Timing states and visual transition configuration- `timing_states.json` - Timing states and visual transition configuration



------



## Overview## Overview



The `config/` folder contains JSON format configurations that define the game's timing system behavior, including the different states a "bug" goes through from its appearance to disappearance, along with associated visual and scoring configurations.The `config/` folder contains JSON format configurations that define the game's timing system behavior, including the different states a "bug" goes through from its appearance to disappearance, along with associated visual and scoring configurations.



## timing_states.json## timing_states.json



### 🎯 **File Structure**### 🎯 **File Structure**



The `timing_states.json` file is divided into three main sections:The `timing_states.json` file is divided into three main sections:



1. **timing_states**: Defines the 6 states a bug goes through1. **timing_states**: Defines the 6 states a bug goes through

2. **global_settings**: Global timing system configurations2. **global_settings**: Global timing system configurations

3. **visual_transitions**: Visual effects configurations3. **visual_transitions**: Visual effects configurations



### ⏰ **Timing States**### ⏰ **Timing States**



Each "bug" in the game goes through different temporal states that determine its visibility, color, and potential score:Each "bug" in the game goes through different temporal states that determine its visibility, color, and potential score:



| State | Time Range (sec) | Opacity | Description | Suggested Color || State | Time Range (sec) | Opacity | Description | Suggested Color |

|--------|------------------|---------|-------------|----------------||--------|------------------|---------|-------------|----------------|

| **early** | [-4.0, -2.0] | 0.2 | Very faint, far from perfect moment | dim_blue || **early** | [-4.0, -2.0] | 0.2 | Very faint, far from perfect moment | dim_blue |

| **almost_early** | [-2.0, -1.0] | 0.5 | More visible, approaching the moment | blue || **almost_early** | [-2.0, -1.0] | 0.5 | More visible, approaching the moment | blue |

| **perfect** | [-1.0, 1.0] | 1.0 | Fully visible and solid | bright_green || **perfect** | [-1.0, 1.0] | 1.0 | Fully visible and solid | bright_green |

| **almost_late** | [1.0, 2.0] | 0.6 | Starting to fade | yellow || **almost_late** | [1.0, 2.0] | 0.6 | Starting to fade | yellow |

| **late** | [2.0, 3.0] | 0.3 | Very faint, timing lost | orange || **late** | [2.0, 3.0] | 0.3 | Very faint, timing lost | orange |

| **miss** | [3.0, 5.0] | 0.0 | Completely invisible | red || **miss** | [3.0, 5.0] | 0.0 | Completely invisible | red |



#### **Each State Details**#### **Each State Details**



```json```json

{{

  "early": {  "early": {

    "time_range": [-4.0, -2.0],           // Time window in seconds    "time_range": [-4.0, -2.0],           // Time window in seconds

    "opacity": 0.2,                       // Bug transparency (0.0-1.0)    "opacity": 0.2,                       // Bug transparency (0.0-1.0)

    "description": "Bug appears very faint...", // Behavior description    "description": "Bug appears very faint...", // Behavior description

    "color_hint": "dim_blue"               // UI color suggestion    "color_hint": "dim_blue"               // UI color suggestion

  }  }

}}

``````



### **⚙️ Complete Configuration Structure**### ⚙️ **Complete Configuration Structure**



```json```json

{{

  "timing_states": {  "timing_states": {

    "early": {    "early": {

      "time_range": [-4.0, -2.0],      "time_range": [-4.0, -2.0],

      "opacity": 0.2,      "opacity": 0.2,

      "description": "Bug appears very faint, indicating it's too early to debug",      "description": "Bug appears very faint, indicating it's too early to debug",

      "color_hint": "dim_blue",      "color_hint": "dim_blue",

      "score_weight": 0.3      "score_weight": 0.3

    },    },

    "almost_early": {    "almost_early": {

      "time_range": [-2.0, -1.0],      "time_range": [-2.0, -1.0],

      "opacity": 0.5,      "opacity": 0.5,

      "description": "Bug becomes more visible, timing is improving",      "description": "Bug becomes more visible, timing is improving",

      "color_hint": "blue",      "color_hint": "blue",

      "score_weight": 0.7      "score_weight": 0.7

    },    },

    "perfect": {    "perfect": {

      "time_range": [-1.0, 1.0],      "time_range": [-1.0, 1.0],

      "opacity": 1.0,      "opacity": 1.0,

      "description": "Perfect debugging window - bug is fully visible and solid",      "description": "Perfect debugging window - bug is fully visible and solid",

      "color_hint": "bright_green",      "color_hint": "bright_green",

      "score_weight": 1.0      "score_weight": 1.0

    },    },

    "almost_late": {    "almost_late": {

      "time_range": [1.0, 2.0],      "time_range": [1.0, 2.0],

      "opacity": 0.6,      "opacity": 0.6,

      "description": "Bug starts to fade, timing window closing",      "description": "Bug starts to fade, timing window closing",

      "color_hint": "yellow",      "color_hint": "yellow",

      "score_weight": 0.6      "score_weight": 0.6

    },    },

    "late": {    "late": {

      "time_range": [2.0, 3.0],      "time_range": [2.0, 3.0],

      "opacity": 0.3,      "opacity": 0.3,

      "description": "Bug is very faint, timing opportunity almost lost",      "description": "Bug is very faint, timing opportunity almost lost",

      "color_hint": "orange",      "color_hint": "orange",

      "score_weight": 0.2      "score_weight": 0.2

    },    },

    "miss": {    "miss": {

      "time_range": [3.0, 5.0],      "time_range": [3.0, 5.0],

      "opacity": 0.0,      "opacity": 0.0,

      "description": "Bug is invisible, timing completely missed",      "description": "Bug is invisible, timing completely missed",

      "color_hint": "red",      "color_hint": "red",

      "score_weight": 0.0      "score_weight": 0.0

    }    }

  }  }

}}

``````



### **🎮 Timing State Properties**### 🎮 **Timing State Properties**



#### **time_range** `[float, float]`#### **time_range** `[float, float]`

- **Purpose**: Defines the temporal window for each state- **Purpose**: Defines the temporal window for each state

- **Format**: `[start_seconds, end_seconds]`- **Format**: `[start_seconds, end_seconds]`

- **Usage**: Determines when a bug transitions to this state- **Usage**: Determines when a bug transitions to this state

- **Example**: `[-1.0, 1.0]` means the state is active from 1 second before to 1 second after the perfect moment- **Example**: `[-1.0, 1.0]` means the state is active from 1 second before to 1 second after the perfect moment



#### **opacity** `float (0.0-1.0)`#### **opacity** `float (0.0-1.0)`

- **Purpose**: Visual transparency of the bug in this state- **Purpose**: Visual transparency of the bug in this state

- **Range**: 0.0 (invisible) to 1.0 (fully opaque)- **Range**: 0.0 (invisible) to 1.0 (fully opaque)

- **Usage**: Controls visual feedback to player about timing accuracy- **Usage**: Controls visual feedback to player about timing accuracy

- **Example**: `0.2` makes the bug barely visible- **Example**: `0.2` makes the bug barely visible



#### **description** `string`#### **description** `string`

- **Purpose**: Human-readable explanation of the state- **Purpose**: Human-readable explanation of the state

- **Usage**: Documentation and potential UI tooltips- **Usage**: Documentation and potential UI tooltips

- **Example**: "Bug appears very faint, indicating it's too early to debug"- **Example**: "Bug appears very faint, indicating it's too early to debug"



#### **color_hint** `string`#### **color_hint** `string`

- **Purpose**: Suggested color for UI representation- **Purpose**: Suggested color for UI representation

- **Format**: Color names compatible with Rich library- **Format**: Color names compatible with Rich library

- **Usage**: Visual theming and state differentiation- **Usage**: Visual theming and state differentiation

- **Example**: `"bright_green"` for perfect state- **Example**: `"bright_green"` for perfect state



#### **score_weight** `float (0.0-1.0)`#### **score_weight** `float (0.0-1.0)`

- **Purpose**: Scoring multiplier for hits in this state- **Purpose**: Scoring multiplier for hits in this state

- **Range**: 0.0 (no points) to 1.0 (full points)- **Range**: 0.0 (no points) to 1.0 (full points)

- **Usage**: Determines point calculation for timing accuracy- **Usage**: Determines point calculation for timing accuracy

- **Example**: `1.0` gives maximum points for perfect timing- **Example**: `1.0` gives maximum points for perfect timing



### **🌟 Global Settings Section**### 🌟 **Global Settings Section**



```json```json

{{

  "global_settings": {  "global_settings": {

    "default_bug_lifetime": 5.0,    "default_bug_lifetime": 5.0,

    "perfect_window_size": 2.0,    "perfect_window_size": 2.0,

    "early_warning_time": 4.0,    "early_warning_time": 4.0,

    "fade_transition_speed": 0.5,    "fade_transition_speed": 0.5,

    "minimum_reaction_time": 0.1    "minimum_reaction_time": 0.1

  }  }

}}

``````



#### **Global Settings Properties**#### **Global Settings Properties**



- **default_bug_lifetime**: Total time a bug exists (seconds)- **default_bug_lifetime**: Total time a bug exists (seconds)

- **perfect_window_size**: Duration of the perfect timing window- **perfect_window_size**: Duration of the perfect timing window

- **early_warning_time**: How early bugs start appearing- **early_warning_time**: How early bugs start appearing

- **fade_transition_speed**: Speed of opacity transitions- **fade_transition_speed**: Speed of opacity transitions

- **minimum_reaction_time**: Minimum time required for player reaction- **minimum_reaction_time**: Minimum time required for player reaction



### **✨ Visual Transitions Section**### ✨ **Visual Transitions Section**



```json```json

{{

  "visual_transitions": {  "visual_transitions": {

    "fade_in_duration": 0.3,    "fade_in_duration": 0.3,

    "fade_out_duration": 0.5,    "fade_out_duration": 0.5,

    "blink_frequency": 3.0,    "blink_frequency": 3.0,

    "color_transition_steps": 10,    "color_transition_steps": 10,

    "opacity_curve": "ease_in_out"    "opacity_curve": "ease_in_out"

  }  }

}}

``````



#### **Visual Transition Properties**#### **Visual Transition Properties**



- **fade_in_duration**: Time for bugs to fade in (seconds)- **fade_in_duration**: Time for bugs to fade in (seconds)

- **fade_out_duration**: Time for bugs to fade out (seconds)- **fade_out_duration**: Time for bugs to fade out (seconds)

- **blink_frequency**: Blinking rate for perfect state (Hz)- **blink_frequency**: Blinking rate for perfect state (Hz)

- **color_transition_steps**: Smoothness of color transitions- **color_transition_steps**: Smoothness of color transitions

- **opacity_curve**: Animation curve type for opacity changes- **opacity_curve**: Animation curve type for opacity changes



------



## **🔧 Configuration Usage**## Uso del Sistema de Timing



### Loading Configuration### � **Carga de Configuración**



```python```python

import jsonimport json

from pathlib import Pathfrom pathlib import Path



def load_timing_config():def load_timing_config():

    """Load timing states configuration"""    config_path = Path("src/config/timing_states.json")

    config_path = Path("src/config/timing_states.json")    with open(config_path, 'r', encoding='utf-8') as file:

    with open(config_path, 'r') as f:        return json.load(file)

        return json.load(f)

timing_config = load_timing_config()

# Usage```

config = load_timing_config()

perfect_state = config['timing_states']['perfect']### 🎯 **Determinar Estado de un Bug**

print(f"Perfect opacity: {perfect_state['opacity']}")

``````python

def get_bug_state(time_offset, timing_config):

### State Calculation    """

    Determina el estado de un bug basado en su offset temporal

```python    

def get_current_state(time_offset: float, config: dict) -> dict:    Args:

    """Determine current timing state based on time offset"""        time_offset (float): Diferencia en segundos respecto al momento perfecto

    timing_states = config['timing_states']        timing_config (dict): Configuración cargada desde timing_states.json

        

    for state_name, state_config in timing_states.items():    Returns:

        start_time, end_time = state_config['time_range']        tuple: (estado, info_del_estado)

        if start_time <= time_offset <= end_time:    """

            return {    states = timing_config["timing_states"]

                'name': state_name,    

                'config': state_config    for state_name, state_info in states.items():

            }        time_range = state_info["time_range"]

            if time_range[0] <= time_offset <= time_range[1]:

    return {'name': 'miss', 'config': timing_states['miss']}            return state_name, state_info

```    

    return "miss", states["miss"]  # Estado por defecto

### Dynamic Opacity Calculation

# Ejemplo de uso

```pythontime_offset = -1.5  # 1.5 segundos antes del momento perfecto

def calculate_opacity(time_offset: float, config: dict) -> float:state, info = get_bug_state(time_offset, timing_config)

    """Calculate current opacity based on timing state"""print(f"Estado: {state}, Opacidad: {info['opacity']}")

    current_state = get_current_state(time_offset, config)```

    base_opacity = current_state['config']['opacity']

    ### � **Calcular Puntuación**

    # Add smooth transitions between states

    visual_config = config.get('visual_transitions', {})```python

    transition_speed = visual_config.get('fade_transition_speed', 0.5)def calculate_score(state, timing_config):

        """

    return base_opacity * transition_speed    Calcula la puntuación basada en el estado de timing

```    

    Args:

---        state (str): Estado del timing (early, perfect, etc.)

        timing_config (dict): Configuración cargada

## **🎨 Integration with Game Systems**    

    Returns:

### CLI Integration        int: Puntos obtenidos

    """

```python    weights = timing_config["global_settings"]["scoring_weights"]

# Example: Update CLI based on timing state    return weights.get(state, 0)

from src.cli.map import Map

# Ejemplo

def update_cli_from_config(game_map: Map, bug_coordinate: str, score = calculate_score("perfect", timing_config)  # Retorna 300 puntos

                          time_offset: float, config: dict):```

    """Update CLI visualization based on timing configuration"""

    current_state = get_current_state(time_offset, config)### � **Aplicar Efectos Visuales**

    state_name = current_state['name']

    ```python

    # Map config states to CLI statesdef get_visual_properties(state, timing_config, current_time, bug_spawn_time):

    cli_state_mapping = {    """

        'early': 1,    Calcula propiedades visuales del bug basado en su estado y configuración

        'almost_early': 2,    

        'perfect': 3,    Args:

        'almost_late': 4,        state (str): Estado actual del bug

        'late': 5,        timing_config (dict): Configuración cargada

        'miss': 0        current_time (float): Tiempo actual del juego

    }        bug_spawn_time (float): Tiempo cuando apareció el bug

        

    cli_state = cli_state_mapping.get(state_name, 0)    Returns:

    game_map.set_cell_state(bug_coordinate, cli_state)        dict: Propiedades visuales (opacity, color, effects)

```    """

    state_info = timing_config["timing_states"][state]

### Scoring System Integration    transitions = timing_config["visual_transitions"]

    

```python    base_opacity = state_info["opacity"]

def calculate_score(time_offset: float, config: dict, base_points: int) -> int:    color = state_info["color_hint"]

    """Calculate score based on timing accuracy"""    

    current_state = get_current_state(time_offset, config)    # Aplicar fade-in si es necesario

    score_weight = current_state['config']['score_weight']    time_since_spawn = current_time - bug_spawn_time

        fade_in_duration = transitions["fade_in_duration"]

    return int(base_points * score_weight)    

```    if time_since_spawn < fade_in_duration:

        fade_factor = time_since_spawn / fade_in_duration

---        actual_opacity = base_opacity * fade_factor

    else:

## **📊 Configuration Validation**        actual_opacity = base_opacity

    

### JSON Schema    # Efecto de pulso para estado perfecto

    pulse_active = (state == "perfect" and transitions["pulse_effect"])

```python    

TIMING_CONFIG_SCHEMA = {    return {

    "type": "object",        "opacity": actual_opacity,

    "required": ["timing_states"],        "color": color,

    "properties": {        "pulse": pulse_active,

        "timing_states": {        "smooth_transition": transitions["color_transition"]

            "type": "object",    }

            "required": ["early", "almost_early", "perfect", "almost_late", "late", "miss"],```

            "additionalProperties": {

                "type": "object",---

                "required": ["time_range", "opacity", "score_weight"],

                "properties": {## Personalización y Modificación

                    "time_range": {

                        "type": "array",### 🔧 **Agregar Nuevos Estados**

                        "items": {"type": "number"},

                        "minItems": 2,Para agregar un nuevo estado de timing:

                        "maxItems": 2

                    },```json

                    "opacity": {"type": "number", "minimum": 0.0, "maximum": 1.0},{

                    "score_weight": {"type": "number", "minimum": 0.0, "maximum": 1.0}  "timing_states": {

                }    "nuevo_estado": {

            }      "time_range": [-6.0, -4.0],

        }      "opacity": 0.1,

    }      "description": "Estado muy temprano con advertencia",

}      "color_hint": "purple"

```    }

  }

### Configuration Validation}

```

```python

import jsonschema### ⚙️ **Ajustar Puntuaciones**



def validate_timing_config(config: dict) -> bool:Modificar los pesos en `scoring_weights`:

    """Validate timing configuration against schema"""

    try:```json

        jsonschema.validate(config, TIMING_CONFIG_SCHEMA){

        return True  "global_settings": {

    except jsonschema.ValidationError as e:    "scoring_weights": {

        print(f"Configuration validation error: {e}")      "perfect": 500,    // Aumentar puntos por perfect

        return False      "early": 25,       // Reducir puntos por early

```      "late": 10         // Reducir más los puntos por late

    }

---  }

}

## **🔄 Configuration Updates**```



### Runtime Configuration Changes### 🎨 **Personalizar Efectos**



```pythonAjustar duración de transiciones:

class ConfigManager:

    def __init__(self, config_path: Path):```json

        self.config_path = config_path{

        self.config = self.load_config()  "visual_transitions": {

        "fade_in_duration": 0.8,     // Aparición más lenta

    def load_config(self) -> dict:    "fade_out_duration": 0.3,    // Desaparición más rápida

        """Load configuration from file"""    "pulse_effect": false        // Desactivar efecto de pulso

        with open(self.config_path, 'r') as f:  }

            return json.load(f)}

    ```

    def update_state_opacity(self, state_name: str, new_opacity: float):

        """Update opacity for a specific state"""---

        if 0.0 <= new_opacity <= 1.0:

            self.config['timing_states'][state_name]['opacity'] = new_opacity## Integración con el Sistema

            self.save_config()

    ### � **Integración con el Motor de Timing**

    def save_config(self):

        """Save current configuration to file"""El sistema de timing del juego debe:

        with open(self.config_path, 'w') as f:

            json.dump(self.config, f, indent=2)1. **Cargar la configuración** al inicio

```2. **Calcular offsets temporales** para cada bug

3. **Actualizar estados** basado en los rangos temporales

---4. **Aplicar efectos visuales** según las transiciones configuradas

5. **Calcular puntuación** usando los pesos definidos

## **📈 Performance Considerations**

### 🎵 **Sincronización con Música**

### Optimization Tips

Los estados de timing se sincronizan con:

1. **Cache Configuration**: Load once at startup, not per frame- **BPM del track**: Determina cuándo aparecen los bugs

2. **State Lookup**: Use dictionaries for O(1) state lookups- **Beats detectados**: Momentos "perfectos" para hacer click

3. **Transition Calculations**: Pre-calculate transition values when possible- **Duración de notas**: Influye en las ventanas de timing

4. **Validation**: Validate configuration at startup, not runtime

### 🎯 **Retroalimentación al Usuario**

### Memory Usage

Cada estado debe proporcionar:

- Configuration file is typically < 1KB- **Feedback visual**: Color, opacidad, efectos

- In-memory structure uses minimal RAM- **Feedback auditivo**: Sonidos diferentes por estado

- No dynamic allocation during gameplay- **Feedback numérico**: Puntos obtenidos mostrados al usuario



------



## **🎯 Future Enhancements**## Consideraciones Técnicas



### Planned Features### ⚡ **Rendimiento**



1. **Dynamic Difficulty**: Adjust timing windows based on player skill- **Carga única**: Cargar el JSON una sola vez al inicio

2. **Custom Profiles**: Player-specific timing configurations- **Búsqueda eficiente**: Optimizar la función de determinación de estados

3. **A/B Testing**: Multiple configuration variants for testing- **Actualización mínima**: Solo recalcular cuando sea necesario

4. **Hot Reloading**: Update configuration without restart

### 🔄 **Actualización en Tiempo Real**

### Configuration Extensibility

```python

```pythondef update_bug_states(bugs, current_time, beat_time, timing_config):

# Example: Extended configuration with difficulty levels    """

{    Actualiza todos los bugs activos basado en el tiempo actual

  "difficulty_profiles": {    """

    "easy": {    for bug in bugs:

      "timing_states": { /* easier timing windows */ },        time_offset = current_time - (beat_time + bug.perfect_timing)

      "perfect_window_multiplier": 1.5        new_state, state_info = get_bug_state(time_offset, timing_config)

    },        

    "normal": {        if bug.state != new_state:

      "timing_states": { /* standard timing */ },            bug.state = new_state

      "perfect_window_multiplier": 1.0            bug.visual_props = get_visual_properties(

    },                new_state, timing_config, current_time, bug.spawn_time

    "hard": {            )

      "timing_states": { /* tighter timing */ },```

      "perfect_window_multiplier": 0.7

    }### � **Validación de Datos**

  }

}```python

```def validate_timing_config(config):

    """

---    Valida que la configuración sea correcta

    """

*This documentation provides comprehensive coverage of the configuration system for BeatBugging's timing mechanics. The JSON-based approach ensures flexibility while maintaining simplicity for both developers and potential modders.*    required_sections = ["timing_states", "global_settings", "visual_transitions"]
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Sección requerida '{section}' no encontrada")
    
    # Validar que los rangos temporales no se solapen incorrectamente
    states = config["timing_states"]
    for state_name, state_info in states.items():
        time_range = state_info["time_range"]
        if time_range[0] >= time_range[1]:
            raise ValueError(f"Rango temporal inválido en estado '{state_name}'")
    
    return True
```

---

## Dependencias

- **json**: Para parseo del archivo de configuración
- **pathlib**: Para manejo de rutas de archivos

---

## Limitaciones y Consideraciones

### ⚠️ **Limitaciones Actuales**

1. **Formato fijo**: Los rangos temporales están hardcoded en el JSON
2. **Estados secuenciales**: No se contempla saltar estados intermedio
3. **Sin validación automática**: El JSON debe ser válido manualmente

### � **Mejores Prácticas**

1. **Backup**: Mantener copias de respaldo antes de modificar
2. **Validación**: Probar cambios en entorno de desarrollo primero
3. **Documentación**: Documentar cualquier modificación personalizada
4. **Consistencia**: Mantener coherencia en los rangos temporales

### 🚀 **Extensiones Futuras**

- **Estados dinámicos**: Generación de estados basada en dificultad
- **Configuración por canción**: Estados personalizados por track
- **Editor visual**: Interfaz gráfica para modificar timing states
- **Validación automática**: Sistema de validación integrado
- **Perfiles de timing**: Diferentes configuraciones para diferentes estilos de juego
