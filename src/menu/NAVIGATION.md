# Navigation System Module Documentation# Documentación del Sistema de Navegación - Módulo Menu



This module contains the complete navigation and menu system for BeatBugging, including the main interface, theme management, log file search, and sound effects.Este módulo contiene el sistema completo de navegación y menús para BeatBugging, incluyendo la interfaz principal, gestión de temas, búsqueda de archivos log y efectos de sonido.



## Module Files## Archivos del Módulo



- `main_menu.py` - Main menu interface with navigation and search- `main_menu.py` - Interfaz principal del menú con navegación y búsqueda

- `themes.py` - Visual theme management system- `themes.py` - Sistema de gestión de temas visuales

- `themes.json` - Color theme configuration- `themes.json` - Configuración de temas de colores

- `res/` - Audio resources for sound effects- `res/` - Recursos de audio para efectos de sonido



------



## Overview## Descripción General



The `menu` module implements a complete user interface based on Textual that provides:El módulo `menu` implementa una interfaz de usuario completa basada en Textual que proporciona:



- **Navigable main menu** with TUI (Terminal User Interface)- **Menú principal navegable** con interfaz TUI (Terminal User Interface)

- **Fuzzy search system** for log files- **Sistema de búsqueda fuzzy** para archivos de log

- **Interchangeable theme management** with colors- **Gestión de temas** intercambiables de colores

- **Sound effects** for interactions- **Efectos de sonido** para interacciones

- **Intuitive navigation** between screens- **Navegación intuitiva** entre pantallas

- **File validation** and visual feedback- **Validación de archivos** y feedback visual



------



## main_menu.py - Main Navigation System## main_menu.py - Sistema Principal de Navegación



### 🎯 **Main Components**### 🎯 **Componentes Principales**



#### **Dataclass: LogFile**#### **Dataclass: LogFile**



Structure to represent found log files:Estructura para representar archivos de log encontrados:



```python```python

@dataclass@dataclass

class LogFile:class LogFile:

    path: Path          # Full path to file    path: Path          # Ruta completa al archivo

    score: float        # Similarity score (0.0-1.0)    score: float        # Puntuación de similaridad (0.0-1.0)

    name: str          # File name    name: str          # Nombre del archivo

    parent_dir: str    # Parent directory    parent_dir: str    # Directorio padre

    size: int          # File size in bytes    size: int          # Tamaño del archivo en bytes

``````



#### **Class: SimpleFuzzyMatcher**#### **Clase: SimpleFuzzyMatcher**



Optimized fuzzy search system for `.log` files:Sistema de búsqueda fuzzy optimizado para archivos `.log`:



```python```python

class SimpleFuzzyMatcher:class SimpleFuzzyMatcher:

    def __init__(self, base_paths: List[Path]):    @staticmethod

        self.base_paths = base_paths    def calculate_ratio(query: str, filename: str) -> float:

        self.log_files = []        """Calcula similaridad entre query y nombre de archivo"""

        self.scan_for_logs()        

        @staticmethod 

    def scan_for_logs(self):    def find_matches(query: str, files: List[LogFile], limit: int = 100) -> List[LogFile]:

        """Scan all base paths for .log files"""        """Encuentra archivos que coinciden con la búsqueda"""

        for base_path in self.base_paths:```

            if base_path.exists():

                log_files = list(base_path.rglob("*.log"))**Algoritmo de Puntuación:**

                self.log_files.extend(log_files)- **Similaridad base**: Usa `difflib.SequenceMatcher` para ratio básico

```- **Bonus de contención**: +0.4 si el query está contenido en el filename

- **Bonus de prefijo**: +0.3 si el filename empieza con el query

#### **Fuzzy Search Algorithm**- **Puntuación máxima**: 1.0 (coincidencia perfecta)

- **Umbral mínimo**: 0.1 (para filtrar resultados irrelevantes)

Advanced search with multiple scoring criteria:

### 🎨 **Sistema de Estilos CSS**

```python

def calculate_score(self, query: str, file_path: Path) -> float:#### **Función: `make_title_css()`**

    """Calculate fuzzy match score for a file"""

    query_lower = query.lower()Genera CSS dinámico para la interfaz basado en el tema actual:

    name_lower = file_path.name.lower()

    ```python

    # Exact match bonusdef make_title_css():

    if query_lower == name_lower:    # Obtiene colores del tema con fallbacks seguros

        return 1.0    border_color = theme.get("border") or "green"

        bg_color = theme.get("background") or "black" 

    # Substring match    primary_color = theme.get("primary") or "green"

    if query_lower in name_lower:    # ... más colores

        substring_score = len(query_lower) / len(name_lower)    

        return 0.7 + (substring_score * 0.3)    return f"""CSS_STRING_WITH_DYNAMIC_COLORS"""

    ```

    # Character similarity

    char_score = self.calculate_char_similarity(query_lower, name_lower)**Elementos Estilizados:**

    return char_score * 0.5- `#menu`: Container principal con bordes redondeados

```- `#title`: Título principal con estilo bold

- `#subtitle`: Subtítulo con colores secundarios

**Scoring System:**- `Button`: Botones con borders dinámicos

- **1.0**: Exact file name match- `#exit_button`: Botón de salida con colores de peligro

- **0.7-1.0**: Substring match (weighted by length ratio)- `#search_input`: Campo de búsqueda estilizado

- **0.0-0.5**: Character similarity match- `#file_list`: Lista de archivos con scrolling

- **0.1 minimum**: Ensures all files appear with some relevance- `#start_button`: Botón de inicio con colores de éxito



### 🎮 **Class: BeatBuggingApp**### 🔊 **Sistema de Audio**



Main Textual application managing the complete interface:#### **Función: `play_sound_and_wait(sound_path)`**



```pythonReproduce un archivo de sonido y espera a que termine:

class BeatBuggingApp(App):

    CSS_PATH = "menu_styles.css"```python

    BINDINGS = [def play_sound_and_wait(sound_path):

        Binding("q", "quit", "Quit"),    """Reproduce sonido y espera a que termine"""

        Binding("ctrl+c", "quit", "Quit"),    try:

        Binding("escape", "back", "Back"),        if not pygame.mixer.get_init():

        Binding("enter", "select", "Select"),            pygame.mixer.init()

        Binding("ctrl+t", "toggle_theme", "Theme")        

    ]        sound = pygame.mixer.Sound(sound_path)

```        sound.set_volume(0.4)  # Volumen al 40%

        sound.play()

#### **Core Attributes**        

        # Esperar a que termine

```python        while pygame.mixer.get_busy():

def __init__(self):            time.sleep(0.1)

    super().__init__()            

    self.theme_manager = ThemeManager()    except Exception as e:

    self.sound_manager = SoundManager()        print(f"No se pudo reproducir sonido: {e}")

    self.fuzzy_matcher = SimpleFuzzyMatcher([```

        Path("logs/"),

        Path("../logs/"),#### **Clase: SoundManager**

        Path("./")

    ])Gestor avanzado de sonidos con prevención de solapamiento:

    self.current_screen = "main"

    self.selected_log_file = None```python

```class SoundManager:

    def __init__(self):

#### **Main Interface Methods**        self.last_click_time = 0        # Tiempo del último click

        self.click_delay = 0.2          # Delay mínimo entre clicks

##### `compose() -> ComposeResult`        self.volume = 0.3               # Volumen por defecto

Builds the main interface layout:        self.menu_click_path = "..."    # Ruta al sonido de click

```

```python

def compose(self) -> ComposeResult:**Características:**

    """Build main interface"""- **Prevención de spam**: Delay de 0.2s entre sonidos

    with Container(id="main-container"):- **Gestión de volumen**: Control centralizado del volumen

        yield Header()- **Manejo de errores**: Graceful degradation si falla el audio

        - **Inicialización lazy**: pygame.mixer se inicializa solo cuando es necesario

        # Main menu section

        with Vertical(id="menu-section"):### 🎮 **Navegación y Screens**

            yield Static(AsciiArt.get_logo(), id="logo")

            yield Button("🎮 Start Game", id="start-game", variant="primary")El sistema utiliza **Textual** para crear una interfaz de usuario rica en terminal:

            yield Button("📁 Select Log File", id="select-log", variant="success") 

            yield Button("⚙️ Settings", id="settings", variant="secondary")#### **Estructura de la Aplicación**

            yield Button("❌ Exit", id="exit", variant="error")

        ```python

        # Search section (initially hidden)from textual.app import App, ComposeResult

        with Vertical(id="search-section", classes="hidden"):from textual.widgets import Static, Button, Label, Input, ListView, ListItem

            yield Input(placeholder="Search log files...", id="search-input")from textual.containers import Vertical

            yield ListView(id="file-list")from textual.screen import Screen

        from textual.binding import Binding

        yield Footer()```

```

**Widgets Principales:**

##### `on_button_pressed(event: Button.Pressed)`- **Static**: Para elementos de texto estático (títulos, labels)

Handles button interactions with sound feedback:- **Button**: Para botones interactivos con acciones

- **Label**: Para información dinámica (status, feedback)

```python- **Input**: Para campos de entrada de texto (búsqueda)

async def on_button_pressed(self, event: Button.Pressed) -> None:- **ListView/ListItem**: Para listas scrolleables de archivos

    """Handle button press events"""- **Vertical**: Container para layout vertical

    self.sound_manager.play_click()

    #### **Bindings y Controles**

    if event.button.id == "start-game":

        if self.selected_log_file:El sistema soporta navegación por teclado y mouse:

            self.sound_manager.play_game_start()- **Enter**: Confirmar selección

            await self.start_game()- **Escape**: Volver/cancelar

        else:- **Tab**: Navegar entre elementos

            self.notify("Please select a log file first", severity="warning")- **Arrow keys**: Navegar en listas

    - **Mouse clicks**: Interacción directa

    elif event.button.id == "select-log":

        await self.show_log_selection()---

    

    elif event.button.id == "settings":## themes.py - Sistema de Gestión de Temas

        await self.show_settings()

    ### 🎨 **Clase: ThemeManager**

    elif event.button.id == "exit":

        self.exit()Gestor centralizado de temas visuales para la interfaz:

```

#### **Constructor**

##### `on_input_changed(event: Input.Changed)`

Handles real-time search with fuzzy matching:```python

def __init__(self, theme_file="themes.json"):

```python    current_dir = os.path.dirname(os.path.abspath(__file__))

async def on_input_changed(self, event: Input.Changed) -> None:    self.theme_file = os.path.join(current_dir, theme_file)

    """Handle search input changes"""    self.themes = {}                    # Diccionario de todos los temas

    query = event.value    self.current_theme = {}             # Tema actualmente activo

        

    if len(query) < 2:    self.load_themes()                  # Carga automática de temas

        # Show all files for short queries```

        matches = self.fuzzy_matcher.get_all_files()

    else:#### **Métodos Principales**

        # Perform fuzzy search

        matches = self.fuzzy_matcher.search(query, limit=20)##### `load_themes()`

    Carga los temas desde el archivo JSON:

    # Update file list

    file_list = self.query_one("#file-list", ListView)```python

    file_list.clear()def load_themes(self):

        if not os.path.exists(self.theme_file):

    for log_file in matches:        raise FileNotFoundError(f"No se encontró {self.theme_file}")

        score_indicator = "⭐" * int(log_file.score * 5)    

        size_mb = log_file.size / (1024 * 1024)    with open(self.theme_file, "r", encoding="utf-8") as f:

                data = json.load(f)

        file_item = ListItem(    

            Label(f"{log_file.name} {score_indicator}"),    self.themes = data.get("themes", {})

            Label(f"{log_file.parent_dir} ({size_mb:.1f}MB)", classes="file-details")    default = data.get("default_theme", "default")

        )    self.set_theme(default)

        file_list.append(file_item)```

```

##### `set_theme(theme_name)`

### 🔊 **Class: SoundManager**Cambia al tema especificado:



Audio system with spam prevention and volume control:```python

def set_theme(self, theme_name):

```python    if theme_name not in self.themes:

class SoundManager:        raise ValueError(f"Tema '{theme_name}' no encontrado")

    def __init__(self):    self.current_theme = self.themes[theme_name]

        pygame.mixer.init()```

        self.sounds = {}

        self.last_played = {}##### `get(key, fallback=None)`

        self.min_interval = 0.1  # Minimum time between same soundsObtiene un color del tema actual con fallback seguro:

        self.load_sounds()

    ```python

    def load_sounds(self):def get(self, key, fallback=None):

        """Load all sound effects"""    return self.current_theme.get(key, fallback)

        sound_files = {```

            'click': 'res/menu-click.mp3',

            'game_start': 'res/game-start.mp3'**Uso Típico:**

        }```python

        theme = ThemeManager()

        for name, file_path in sound_files.items():primary_color = theme.get("primary", "green")  # Fallback a verde

            full_path = Path(__file__).parent / file_pathborder_color = theme.get("border", "white")    # Fallback a blanco

            if full_path.exists():```

                self.sounds[name] = pygame.mixer.Sound(str(full_path))

```---



#### **Spam Prevention System**## themes.json - Configuración de Temas



```python### 🌈 **Estructura del Archivo**

def play_sound(self, sound_name: str, volume: float = 0.7) -> bool:

    """Play sound with spam prevention"""```json

    current_time = time.time(){

      "themes": {

    # Check spam prevention    "theme_name": {

    if sound_name in self.last_played:      "color_key": "color_value",

        time_diff = current_time - self.last_played[sound_name]      ...

        if time_diff < self.min_interval:    }

            return False  # Too soon, ignore  },

      "default_theme": "theme_name"

    # Play sound}

    if sound_name in self.sounds:```

        sound = self.sounds[sound_name]

        sound.set_volume(volume)### 🎨 **Temas Disponibles**

        sound.play()

        self.last_played[sound_name] = current_time#### **Tema "default" (Verde Matrix)**

        return True

    ```json

    return False"default": {

```  "background": "black",        // Fondo negro

  "primary": "#00ff00",         // Verde brillante principal  

---  "secondary": "#39ff14",       // Verde neón secundario

  "hover": "#003300",           // Verde oscuro para hover

## themes.py - Theme Management System  "danger": "red",              // Rojo para acciones peligrosas

  "danger_hover": "#330000",    // Rojo oscuro para hover peligroso

### 🎨 **Class: ThemeManager**  "border": "green"             // Verde para bordes

}

Complete theme management with hot-swapping capabilities:```



```python#### **Tema "blue" (Cibernético Azul)**

class ThemeManager:

    def __init__(self, config_path: str = "src/menu/themes.json"):```json

        self.config_path = Path(config_path)"blue": {

        self.themes = self.load_themes()  "background": "#001122",      // Fondo azul muy oscuro

        self.current_theme = "default"  "primary": "#33ccff",         // Azul cian principal

```  "secondary": "#66ffff",       // Azul cian claro secundario

  "hover": "#003344",           // Azul oscuro para hover

#### **Theme Loading System**  "danger": "#ff3333",          // Rojo brillante para peligro

  "danger_hover": "#660000"     // Rojo oscuro para hover

```python}

def load_themes(self) -> Dict[str, Dict]:```

    """Load themes from JSON configuration"""

    try:#### **Tema "fixed" (Colores por Defecto)**

        with open(self.config_path, 'r') as f:

            themes_data = json.load(f)```json

        "fixed": {

        # Validate theme structure  "background": "default",      // Usa colores por defecto del terminal

        validated_themes = {}  "primary": "default",         // Para máxima compatibilidad

        for theme_name, theme_data in themes_data.items():  "secondary": "default",

            if self.validate_theme_structure(theme_data):  "hover": "default",

                validated_themes[theme_name] = theme_data  "danger": "default", 

            else:  "danger_hover": "default"

                print(f"Warning: Invalid theme structure for '{theme_name}'")}

        ```

        return validated_themes

        ### ⚙️ **Configuración Global**

    except FileNotFoundError:

        return self.get_default_themes()```json

    except json.JSONDecodeError as e:"default_theme": "default"      // Tema que se carga automáticamente

        print(f"Error loading themes: {e}")```

        return self.get_default_themes()

```---



#### **Theme Application**## res/ - Recursos de Audio



```python### 🔊 **Archivos de Sonido**

def apply_theme(self, theme_name: str, app_instance) -> bool:

    """Apply theme to Textual app instance"""#### **menu-click.mp3**

    if theme_name not in self.themes:- **Propósito**: Feedback auditivo para clicks en menú

        return False- **Duración**: Sonido corto (~0.1-0.2 segundos)

    - **Volumen**: Configurado al 30% por defecto

    theme = self.themes[theme_name]- **Uso**: Reproducido por `SoundManager.play_menu_click()`

    

    # Apply colors to CSS variables#### **game-start.mp3**  

    css_variables = self.convert_theme_to_css(theme)- **Propósito**: Sonido de inicio de juego

    app_instance.stylesheet.update(css_variables)- **Duración**: Sonido más largo para transición

    - **Volumen**: Configurado al 40% por defecto

    # Update current theme- **Uso**: Reproducido al iniciar una sesión de juego

    self.current_theme = theme_name

    ### 🎵 **Especificaciones de Audio**

    # Refresh display

    app_instance.refresh()```python

    return True# Configuración típica en SoundManager

self.volume = 0.3                    # 30% del volumen máximo

def convert_theme_to_css(self, theme: Dict) -> str:self.click_delay = 0.2               # 200ms entre clicks

    """Convert theme colors to CSS variables"""sound.set_volume(0.4)                # 40% para sonidos especiales

    css_vars = []```

    

    for category, colors in theme['colors'].items():---

        for color_name, color_value in colors.items():

            css_var = f"--{category}-{color_name.replace('_', '-')}: {color_value};"## Flujo de Navegación

            css_vars.append(css_var)

    ### 🚀 **Inicialización del Sistema**

    return "\n".join(css_vars)

``````python

def initialize_menu_system():

### 🎭 **Theme Structure**    """Inicializa el sistema completo de menú"""

    

#### **Theme JSON Format**    # 1. Cargar gestión de temas

    theme_manager = ThemeManager()

```json    

{    # 2. Inicializar sistema de sonido

  "default": {    sound_manager = SoundManager()

    "name": "Default Green",    

    "description": "Classic green terminal theme",    # 3. Configurar CSS dinámico

    "colors": {    css_styles = make_title_css()

      "primary": {    

        "bg": "#001100",    # 4. Crear aplicación Textual

        "fg": "#00ff00",    app = MenuApp(css=css_styles)

        "accent": "#55ff55"    

      },    return app, theme_manager, sound_manager

      "secondary": {```

        "bg": "#002200", 

        "fg": "#88ff88",### 📝 **Flujo de Búsqueda de Archivos**

        "muted": "#556655"

      },```python

      "interactive": {def search_workflow_example():

        "button_bg": "#003300",    """Ejemplo del flujo de búsqueda"""

        "button_hover": "#004400",    

        "button_pressed": "#002200",    # 1. Usuario ingresa query en Input widget

        "input_bg": "#001a00",    user_query = "error"

        "input_border": "#00aa00"    

      },    # 2. Buscar archivos .log en el sistema

      "status": {    log_files = scan_for_log_files()  # Función hipotética

        "success": "#00ff00",    

        "warning": "#ffaa00",     # 3. Aplicar fuzzy matching

        "error": "#ff0000",    matches = SimpleFuzzyMatcher.find_matches(

        "info": "#00aaff"        user_query, log_files, limit=100

      }    )

    }    

  }    # 4. Actualizar ListView con resultados

}    update_file_list(matches)

```    

    # 5. Usuario selecciona archivo

#### **Dynamic Theme Creation**    selected_file = get_user_selection()

    

```python    # 6. Validar y iniciar juego

def create_custom_theme(self, base_theme: str, modifications: Dict) -> str:    if validate_log_file(selected_file):

    """Create custom theme based on existing theme"""        play_sound_and_wait("res/game-start.mp3")

    if base_theme not in self.themes:        start_game_with_file(selected_file)

        return None```

    

    # Deep copy base theme### 🎮 **Estados de Navegación**

    custom_theme = copy.deepcopy(self.themes[base_theme])

    #### **Estado Principal (Main Menu)**

    # Apply modifications- **Elementos visibles**: Título, botones principales, tema

    for category, colors in modifications.items():- **Acciones disponibles**: 

        if category in custom_theme['colors']:  - "Buscar Archivos Log" → Estado de Búsqueda

            custom_theme['colors'][category].update(colors)  - "Configuración" → Estado de Configuración  

      - "Salir" → Cerrar aplicación

    # Generate unique theme name

    theme_name = f"custom_{int(time.time())}"#### **Estado de Búsqueda (File Search)**

    self.themes[theme_name] = custom_theme- **Elementos visibles**: Campo de búsqueda, lista de archivos, botones

    - **Acciones disponibles**:

    return theme_name  - Escribir en campo de búsqueda → Filtrar resultados

```  - Seleccionar archivo → Habilitar botón "Iniciar"

  - "Iniciar" → Comenzar juego con archivo seleccionado

---  - "Volver" → Regresar al menú principal



## **🎹 Navigation Key Bindings**#### **Estado de Configuración (Settings)**

- **Elementos visibles**: Opciones de tema, volumen, controles

### Global Bindings- **Acciones disponibles**:

  - Cambiar tema → Actualizar colores en tiempo real

```python  - Ajustar volumen → Test de audio

GLOBAL_BINDINGS = [  - "Aplicar" → Guardar cambios

    Binding("q", "quit", "Quit Application"),  - "Cancelar" → Descartar cambios

    Binding("ctrl+c", "quit", "Force Quit"),

    Binding("escape", "back", "Go Back"),---

    Binding("ctrl+t", "toggle_theme", "Switch Theme"),

    Binding("f1", "help", "Show Help"),## Integración con Otros Módulos

    Binding("ctrl+r", "refresh", "Refresh")

]### 🔗 **Integración con Sistema de Configuración**

```

```python

### Context-Specific Bindings# Cargar configuración global del juego

from src.config import Config

```python

MENU_BINDINGS = [def apply_game_config_to_menu():

    Binding("enter", "select", "Select Option"),    """Aplica configuración del juego al menú"""

    Binding("space", "select", "Select Option"),    

    Binding("tab", "next_option", "Next Option"),    # Colores de la configuración global

    Binding("shift+tab", "prev_option", "Previous Option")    if hasattr(Config, 'PRIMARY_COLOR'):

]        theme.current_theme["primary"] = Config.PRIMARY_COLOR

    

SEARCH_BINDINGS = [    # Controles del juego

    Binding("ctrl+f", "focus_search", "Focus Search"),    menu_bindings = create_bindings_from_config(Config.COLUMN_KEYS, Config.ROW_KEYS)

    Binding("ctrl+l", "clear_search", "Clear Search"),```

    Binding("up", "prev_result", "Previous Result"),

    Binding("down", "next_result", "Next Result")### 🎵 **Integración con Sistema de Música**

]

``````python

# Preparar generador de música con archivo seleccionado

---from src.music.generator import LogMusicGenerator



## **🔧 Integration Examples**def start_game_with_selected_file(log_file: LogFile):

    """Inicia el juego con el archivo de log seleccionado"""

### Complete Menu System Setup    

    # Reproducir sonido de inicio

```python    sound_manager.play_sound_and_wait("res/game-start.mp3")

def run_menu_system():    

    """Initialize and run the complete menu system"""    # Crear generador de música

        music_generator = LogMusicGenerator(str(log_file.path))

    # Initialize theme system    

    theme_manager = ThemeManager()    # Validar que el archivo sea procesable

        if not music_generator.fileState:

    # Set up application with themes        show_error_message("Archivo de log no válido")

    app = BeatBuggingApp()        return

    app.theme_manager = theme_manager    

        # Iniciar juego principal

    # Apply initial theme    transition_to_game_screen()

    theme_manager.apply_theme("default", app)```

    

    # Run application### 🎯 **Integración con Sistema de Juego**

    app.run()

```python

# Usage# Transición del menú al juego

if __name__ == "__main__":from src.game.timing_system import AdvancedTimingSystem

    run_menu_system()from src.cli.map import Map

```

def transition_to_game_screen():

### Custom Theme Integration    """Transición suave del menú al juego"""

    

```python    # Fade out del menú

def setup_custom_themes():    fade_out_menu_screen()

    """Setup custom themes for different game modes"""    

    theme_manager = ThemeManager()    # Inicializar sistemas de juego

        timing_system = AdvancedTimingSystem()

    # Create high-contrast theme for accessibility    game_map = Map()

    high_contrast = theme_manager.create_custom_theme("default", {    

        "primary": {    # Fade in de la pantalla de juego

            "bg": "#000000",    fade_in_game_screen(game_map)

            "fg": "#ffffff",```

            "accent": "#ffff00"

        },---

        "interactive": {

            "button_bg": "#333333",## Personalización y Extensión

            "button_hover": "#666666"

        }### 🎨 **Crear Nuevos Temas**

    })

    ```python

    # Create cyberpunk theme# Agregar nuevo tema al themes.json

    cyberpunk = theme_manager.create_custom_theme("default", {new_theme = {

        "primary": {    "cyberpunk": {

            "bg": "#0a0a23",        "background": "#0a0a0a",

            "fg": "#ff00ff",         "primary": "#ff00ff",        # Magenta

            "accent": "#00ffff"        "secondary": "#00ffff",       # Cian

        },        "hover": "#330033",

        "status": {        "danger": "#ff6600",          # Naranja

            "success": "#00ff41",        "danger_hover": "#663300",

            "error": "#ff073a"        "border": "#ff00ff"

        }    }

    })}

    

    return theme_manager# Cargar tema dinámicamente

```theme_manager.themes["cyberpunk"] = new_theme["cyberpunk"]

theme_manager.set_theme("cyberpunk")

### Sound System Integration```



```python### 🔊 **Agregar Nuevos Sonidos**

class EnhancedSoundManager(SoundManager):

    def __init__(self):```python

        super().__init__()class ExtendedSoundManager(SoundManager):

        self.music_volume = 0.3    def __init__(self):

        self.sfx_volume = 0.7        super().__init__()

                self.sounds = {

    def play_background_music(self, music_file: str):            "menu_click": "res/menu-click.mp3",

        """Play background music with looping"""            "game_start": "res/game-start.mp3",

        music_path = Path(__file__).parent / "res" / music_file            "error": "res/error.mp3",           # Nuevo

        if music_path.exists():            "success": "res/success.mp3",       # Nuevo

            pygame.mixer.music.load(str(music_path))            "hover": "res/hover.mp3"            # Nuevo

            pygame.mixer.music.set_volume(self.music_volume)        }

            pygame.mixer.music.play(-1)  # Loop indefinitely    

        def play_error_sound(self):

    def set_master_volume(self, volume: float):        self.play_sound("error")

        """Set master volume for all audio"""    

        self.sfx_volume = volume    def play_success_sound(self):

        self.music_volume = volume * 0.5  # Music quieter than SFX        self.play_sound("success")

        pygame.mixer.music.set_volume(self.music_volume)```

```

### 📝 **Personalizar Búsqueda Fuzzy**

---

```python

## **⚡ Performance Optimization**class AdvancedFuzzyMatcher(SimpleFuzzyMatcher):

    @staticmethod

### Fuzzy Search Optimization    def calculate_ratio(query: str, filename: str) -> float:

        base_score = SimpleFuzzyMatcher.calculate_ratio(query, filename)

```python        

class OptimizedFuzzyMatcher(SimpleFuzzyMatcher):        # Bonus adicionales personalizados

    def __init__(self, base_paths: List[Path]):        

        super().__init__(base_paths)        # Bonus por extensión específica

        self.search_cache = {}  # Cache search results        if filename.endswith('.log'):

        self.max_cache_size = 100            base_score += 0.1

            

    def search(self, query: str, limit: int = 10) -> List[LogFile]:        # Bonus por palabras clave

        """Optimized search with caching"""        keywords = ['error', 'debug', 'info', 'warn']

        # Check cache first        for keyword in keywords:

        cache_key = f"{query}:{limit}"            if keyword in filename.lower():

        if cache_key in self.search_cache:                base_score += 0.05

            return self.search_cache[cache_key]                

                # Penalty por archivos muy grandes o pequeños

        # Perform search        file_size = get_file_size(filename)

        results = super().search(query, limit)        if file_size < 1024 or file_size > 10*1024*1024:  # < 1KB o > 10MB

                    base_score *= 0.9

        # Cache results        

        if len(self.search_cache) < self.max_cache_size:        return min(base_score, 1.0)

            self.search_cache[cache_key] = results```

        

        return results---

```

## Consideraciones de Rendimiento

### Memory Management

### ⚡ **Optimizaciones del Sistema**

```python

def cleanup_resources(self):#### **Búsqueda Eficiente**

    """Clean up resources when menu closes"""```python

    # Stop all sounds# Cacheo de resultados de búsqueda

    pygame.mixer.stop()class CachedFuzzyMatcher:

        def __init__(self):

    # Clear caches        self.cache = {}

    if hasattr(self, 'fuzzy_matcher'):        self.cache_limit = 1000

        self.fuzzy_matcher.search_cache.clear()    

        def find_matches_cached(self, query: str, files: List[LogFile]) -> List[LogFile]:

    # Clear theme data        cache_key = f"{query}:{len(files)}"

    if hasattr(self, 'theme_manager'):        

        self.theme_manager.themes.clear()        if cache_key in self.cache:

```            return self.cache[cache_key]

        

---        results = SimpleFuzzyMatcher.find_matches(query, files)

        

## **🎯 Future Enhancements**        if len(self.cache) >= self.cache_limit:

            # Limpiar cache más antiguo

### Planned Features            oldest_key = next(iter(self.cache))

            del self.cache[oldest_key]

1. **Custom Key Bindings**: User-configurable keyboard shortcuts        

2. **Theme Editor**: In-app theme creation and editing        self.cache[cache_key] = results

3. **Advanced Search**: Regex and content-based search        return results

4. **Recent Files**: Quick access to recently used log files```

5. **Bookmarks**: Save favorite log file locations

#### **Renderizado Optimizado**

### Advanced Navigation```python

# Actualización incremental de la UI

```pythondef update_file_list_optimized(new_results: List[LogFile]):

# Planned breadcrumb navigation    """Actualiza solo los elementos que cambiaron"""

class BreadcrumbNavigation:    

    def __init__(self):    current_items = get_current_list_items()

        self.navigation_stack = []    

        self.current_path = []    # Calcular diff entre listas

        to_remove = set(current_items) - set(new_results)

    def navigate_to(self, screen: str, context: Dict = None):    to_add = set(new_results) - set(current_items)

        """Navigate with history tracking"""    

        self.navigation_stack.append({    # Aplicar solo cambios necesarios

            'screen': self.current_screen,    for item in to_remove:

            'context': self.current_context        remove_list_item(item)

        })    

        self.current_screen = screen    for item in to_add:

        self.current_context = context or {}        add_list_item(item)

    ```

    def go_back(self):

        """Navigate back through history"""### 🔧 **Gestión de Memoria**

        if self.navigation_stack:

            previous = self.navigation_stack.pop()```python

            self.current_screen = previous['screen']# Limpieza automática de recursos

            self.current_context = previous['context']class ResourceManager:

```    def __init__(self):

        self.loaded_sounds = {}

---        self.max_cached_sounds = 10

    

*This documentation provides complete coverage of the navigation and menu system for BeatBugging. The modular design ensures easy customization of themes, sounds, and navigation behavior while maintaining a consistent user experience across all interfaces.*    def cleanup_unused_resources(self):
        """Limpia recursos no utilizados"""
        
        # Limpiar sonidos no utilizados recientemente
        current_time = time.time()
        to_remove = []
        
        for sound_key, (sound, last_used) in self.loaded_sounds.items():
            if current_time - last_used > 300:  # 5 minutos
                to_remove.append(sound_key)
        
        for key in to_remove:
            del self.loaded_sounds[key]
    
    def get_sound(self, sound_path: str):
        """Obtiene sonido con cache inteligente"""
        if sound_path in self.loaded_sounds:
            sound, _ = self.loaded_sounds[sound_path]
            self.loaded_sounds[sound_path] = (sound, time.time())
            return sound
        
        # Cargar nuevo sonido
        if len(self.loaded_sounds) >= self.max_cached_sounds:
            self.cleanup_unused_resources()
        
        sound = pygame.mixer.Sound(sound_path)
        self.loaded_sounds[sound_path] = (sound, time.time())
        return sound
```

---

## Dependencias del Módulo

### 📚 **Librerías Externas**

```python
from textual.app import App, ComposeResult     # Framework TUI principal
from textual.widgets import Static, Button, Label, Input, ListView, ListItem
from textual.containers import Vertical        # Contenedores de layout
from textual.screen import Screen             # Sistema de pantallas
from textual.binding import Binding           # Bindings de teclado

import pygame                                # Para sistema de audio
import json                                  # Para configuración de temas
import os                                    # Para manejo de archivos
import time                                  # Para timing de sonidos
import difflib                               # Para algoritmo fuzzy
from threading import Thread                 # Para audio asíncrono
from pathlib import Path                     # Para manejo de rutas
from dataclasses import dataclass            # Para estructuras de datos
from typing import List                      # Para type hints
```

### 🔗 **Integración con Otros Módulos**

```python
# Integraciones típicas con otros módulos del proyecto
from src.config import Config                           # Configuración global
from src.music.generator import LogMusicGenerator       # Generador de música  
from src.game.timing_system import AdvancedTimingSystem # Sistema de timing
from src.cli.map import Map                             # Visualización CLI
```

---

## Limitaciones y Consideraciones

### ⚠️ **Limitaciones Actuales**

1. **Dependencia de terminal**: Requiere terminal compatible con Textual
2. **Audio opcional**: El juego funciona sin audio, pero pierde inmersión
3. **Búsqueda simple**: El algoritmo fuzzy es básico, se puede mejorar
4. **Temas estáticos**: Los temas no se pueden cambiar en tiempo real sin reinicio

### 💡 **Mejores Prácticas**

1. **Manejo de errores graceful**: Todos los sistemas tienen fallbacks
2. **Recursos cleanup**: Limpieza automática de memoria y recursos
3. **UI responsive**: La interfaz responde rápido incluso con muchos archivos
4. **Accesibilidad**: Navegación completa por teclado

---

## Extensiones Futuras

### 🚀 **Características Planeadas**

1. **Editor de temas in-app**: Crear/modificar temas desde el menú
2. **Historial de archivos**: Recordar archivos utilizados recientemente
3. **Favoritos**: Sistema de bookmarks para archivos frecuentes
4. **Previsualización**: Vista previa del contenido de logs antes de iniciar
5. **Configuración avanzada**: Más opciones de personalización
6. **Plugins de sonido**: Sistema extensible de efectos de audio
7. **Animaciones**: Transiciones suaves entre pantallas
8. **Multi-idioma**: Soporte para diferentes idiomas en la interfaz
