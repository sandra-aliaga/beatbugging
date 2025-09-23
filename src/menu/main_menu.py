from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Label, Input, ListView, ListItem, Select
from textual.containers import Vertical
from textual.screen import Screen
from textual.binding import Binding
from .themes import ThemeManager
import random
import os
import pygame
import time
import difflib
from threading import Thread
from pathlib import Path
from dataclasses import dataclass
from typing import List

# Cargar tema actual
theme = ThemeManager()

@dataclass
class LogFile:
    """Archivo de log encontrado"""
    path: Path
    score: float
    name: str
    parent_dir: str
    size: int
    line_count: int = 0
    content_preview: str = ""

class SimpleFuzzyMatcher:
    """Matcher fuzzy simple solo para nombres de archivos .log"""
    
    @staticmethod
    def calculate_ratio(query: str, filename: str) -> float:
        if not query:
            return 1.0
        
        query_lower = query.lower()
        filename_lower = filename.lower()
        
        # Usar difflib para similitud básica
        ratio = difflib.SequenceMatcher(None, query_lower, filename_lower).ratio()
        
        # Bonus si contiene el query
        if query_lower in filename_lower:
            ratio += 0.4
        
        # Bonus si comienza con el query
        if filename_lower.startswith(query_lower):
            ratio += 0.3
        
        return min(ratio, 1.0)
    
    @staticmethod
    def find_matches(query: str, files: List[LogFile], limit: int = 100) -> List[LogFile]:
        if not query.strip():
            return files[:limit]
        
        scored_files = []
        for file in files:
            score = SimpleFuzzyMatcher.calculate_ratio(query, file.name)
            if score > 0.1:
                file.score = score
                scored_files.append(file)
        
        scored_files.sort(key=lambda x: x.score, reverse=True)
        return scored_files[:limit]

def make_title_css():
    # Obtener colores del tema con fallbacks seguros
    border_color = theme.get("border") or "green"
    bg_color = theme.get("background") or "black"
    primary_color = theme.get("primary") or "green"
    secondary_color = theme.get("secondary") or "cyan"
    danger_color = theme.get("danger") or "red"
    success_color = theme.get("success") or "green"
    
    return f"""
    #menu {{
        align: center middle;
        border: round {border_color};
        background: {bg_color};
        color: {primary_color};
<<<<<<< HEAD
        padding: 1;
=======
        padding: 2;
>>>>>>> 398ea52 (WIP: Menu improvements with file selection and difficulty modes)
        height: 100%;
        width: 100%;
        content-align: center middle;
    }}

    #ascii {{
        text-align: center;
        align: center middle;
        color: {theme.get("primary")};
        margin-bottom: 1;
    }}

    #title {{
        text-style: bold;
        color: {primary_color};
        margin-bottom: 1;
        text-align: center;
<<<<<<< HEAD
        border-bottom: solid {theme.get("primary")};
=======
        border-bottom: solid {primary_color};
>>>>>>> 398ea52 (WIP: Menu improvements with file selection and difficulty modes)
        align: center middle;
        padding-bottom: 0;
        height: auto;
        
    }}

    #subtitle {{
        color: {secondary_color};
        margin-bottom: 1;
        text-align: center;
        text-style: bold;
        height: auto;
    }}

    Button {{
        border: solid {primary_color};
        background: {bg_color};
        color: {primary_color};
        align-horizontal: center;
        width: 20;
        margin: 1;
    }}

    #exit_button {{
        border: solid {danger_color};
        background: {bg_color};
        color: {danger_color};
    }}

    #buttons_container {{
        align: center middle;
    }}

    #search_input {{
        height: 3;
        margin: 1;
        border: solid {primary_color};
        background: {bg_color};
        color: {primary_color};
    }}

    #file_list {{
        height: 25;
        border: solid {primary_color};
        background: {bg_color};
        color: {primary_color};
        margin: 1;
    }}

    #file_list.collapsed {{
        height: 8;
        border: solid {success_color};
    }}

    #status_label {{
        height: 1;
        color: {secondary_color};
        text-align: center;
        margin: 1;
    }}

    #difficulty_label {{
        color: {secondary_color};
        text-align: center;
        margin: 1;
        text-style: bold;
    }}

    #difficulty_container {{
        align: center middle;
        margin: 1;
    }}

    .difficulty_button {{
        width: 20;
        margin: 1;
        border: solid {primary_color};
        background: {bg_color};
        color: {primary_color};
    }}

    .difficulty_button:hover {{
        background: {primary_color};
        color: {bg_color};
    }}

    .root_mode {{
        border: solid {danger_color};
        color: {danger_color};
    }}

    .root_mode:hover {{
        background: {danger_color};
        color: {bg_color};
    }}

    .selected {{
        background: {primary_color};
        color: {bg_color};
        text-style: bold;
    }}

    .root_selected {{
        background: {danger_color};
        color: {bg_color};
        text-style: bold;
    }}

    #start_button {{
        border: solid {success_color};
        background: {bg_color};
        color: {success_color};
        width: 25;
        margin-top: 2;
    }}

    #back_button {{
        border: solid {primary_color};
        background: {bg_color};
        color: {primary_color};
        width: 15;
    }}
    """

def play_sound_and_wait(sound_path):
    """Play a sound file and wait for it to finish"""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(0.4)
        sound.play()
        
        while pygame.mixer.get_busy():
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Could not play sound: {e}")
        pass

class SoundManager:
    """Manages menu sounds with overlap prevention"""
    
    def __init__(self):
        self.last_click_time = 0
        self.click_delay = 0.2
        self.volume = 0.3
        self.menu_click_path = os.path.join(os.path.dirname(__file__), "res", "menu-click.mp3")
        
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except:
            pass
    
    def play_menu_click(self):
        current_time = time.time()
        
        if current_time - self.last_click_time >= self.click_delay:
            self.last_click_time = current_time
            
            def play_click():
                try:
                    sound = pygame.mixer.Sound(self.menu_click_path)
                    sound.set_volume(self.volume)
                    sound.play()
                except Exception as e:
                    print(f"Could not play menu click sound: {e}")
            
            click_thread = Thread(target=play_click)
            click_thread.daemon = True
            click_thread.start()

# Global sound manager instance
sound_manager = SoundManager()

class TitleScreen(Screen):
    CSS = make_title_css()

    def compose(self) -> ComposeResult:
        with Static(id="menu"):  
            self.logos = [
                r"""
 ███████████  ██████████   █████████   ███████████    ███████████  █████  █████   █████████    █████████  █████ ██████   █████   █████████ 
░░███░░░░░███░░███░░░░░█  ███░░░░░███ ░█░░░███░░░█   ░░███░░░░░███░░███  ░░███   ███░░░░░███  ███░░░░░███░░███ ░░██████ ░░███   ███░░░░░███
 ░███    ░███ ░███  █ ░  ░███    ░███ ░   ░███  ░     ░███    ░███ ░███   ░███  ███     ░░░  ███     ░░░  ░███  ░███░███ ░███  ███     ░░░ 
 ░██████████  ░██████    ░███████████     ░███        ░██████████  ░███   ░███ ░███         ░███          ░███  ░███░░███░███ ░███         
 ░███░░░░░███ ░███░░█    ░███░░░░░███     ░███        ░███░░░░░███ ░███   ░███ ░███    █████░███    █████ ░███  ░███  ░░██████ ░███    █████
 ░███    ░███ ░███ ░   █ ░███    ░███     ░███        ░███    ░███ ░███   ░███ ░░███  ░░███ ░░███  ░░███  ░███  ░███  ░░█████ ░░███  ░░███ 
 ███████████  ██████████ █████   █████    █████       ███████████  ░░████████   ░░█████████  ░░█████████  █████ █████  ░░█████ ░░█████████ 
░░░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░    ░░░░░       ░░░░░░░░░░░    ░░░░░░░░     ░░░░░░░░░    ░░░░░░░░░  ░░░░░ ░░░░░    ░░░░░   ░░░░░░░░░
""",
                r"""
 ███████████  ██████████   █████████   ███████████    ███████████  █████  █████   █████████    █████████  █████ ██████   █████   █████████ 
▒▒███▒▒▒▒▒███▒▒███▒▒▒▒▒█  ███▒▒▒▒▒███ ▒█▒▒▒███▒▒▒█   ▒▒███▒▒▒▒▒███▒▒███  ▒▒███   ███▒▒▒▒▒███  ███▒▒▒▒▒███▒▒███ ▒▒██████ ▒▒███   ███▒▒▒▒▒███
 ▒███    ▒███ ▒███  █ ▒  ▒███    ▒███ ▒   ▒███  ▒     ▒███    ▒███ ▒███   ▒███  ███     ▒▒▒  ███     ▒▒▒  ▒███  ▒███▒███ ▒███  ███     ▒▒▒ 
 ▒██████████  ▒██████    ▒███████████     ▒███        ▒██████████  ▒███   ▒███ ▒███         ▒███          ▒███  ▒███▒▒███▒███ ▒███         
 ▒███▒▒▒▒▒███ ▒███▒▒█    ▒███▒▒▒▒▒███     ▒███        ▒███▒▒▒▒▒███ ▒███   ▒███ ▒███    █████▒███    █████ ▒███  ▒███ ▒▒██████ ▒███    █████
 ▒███    ▒███ ▒███ ▒   █ ▒███    ▒███     ▒███        ▒███    ▒███ ▒███   ▒███ ▒▒███  ▒▒███ ▒▒███  ▒▒███  ▒███  ▒███  ▒▒█████ ▒▒███  ▒▒███ 
 ███████████  ██████████ █████   █████    █████       ███████████  ▒▒████████   ▒▒█████████  ▒▒█████████  █████ █████  ▒▒█████ ▒▒█████████ 
▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒   ▒▒▒▒▒    ▒▒▒▒▒       ▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒     ▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒   ▒▒▒▒▒▒▒▒▒
"""
            ]
            self.ascii_widget = Static(self.logos[0], id="ascii")
            yield self.ascii_widget

            errors = random.randint(5000, 99999)
            yield Label(f"{errors} errors found", id="subtitle")

            yield Vertical(
                Button("Play", id="play_button"),
                Button("Exit", id="exit_button"),
                id="buttons_container"
            )

    def on_mount(self) -> None:
        self.logo_index = 0
        self.pattern = [0.8, 0.8, 0.2, 0.2]
        self.pattern_index = 0
        self.schedule_next()

    def schedule_next(self) -> None:
        delay = self.pattern[self.pattern_index]
        self.set_timer(delay, self.swap_ascii)

    def swap_ascii(self) -> None:
        self.logo_index = (self.logo_index + 1) % len(self.logos)
        self.ascii_widget.update(self.logos[self.logo_index])
        self.pattern_index = (self.pattern_index + 1) % len(self.pattern)
        self.schedule_next()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        sound_manager.play_menu_click()
        
        if event.button.id == "play_button":
            self.app.push_screen(SetupScreen())
        elif event.button.id == "exit_button":
            self.app.exit(None)

class SetupScreen(Screen):
    CSS = make_title_css()
    
    BINDINGS = [
        Binding("ctrl+c", "cancel", "Cancel"),
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "select", "Select"),
    ]

    def __init__(self):
        super().__init__()
        self.all_log_files: List[LogFile] = []
        self.filtered_files: List[LogFile] = []
        self.selected_file: LogFile = None
        self.selected_difficulty: str = "user"  # Por defecto user mode
        self.fuzzy_matcher = SimpleFuzzyMatcher()

    def compose(self) -> ComposeResult:
        with Static(id="menu"):  
<<<<<<< HEAD
            yield Static("Log File Search", id="title")
            yield Label("Search by filename only...", id="subtitle")
    CSS = f"""
    #menu {{
        align: center middle;
        border: round green;
        background: {theme.get("background")};
        color: {theme.get("primary")};
        padding: 2;
        height: 100%;
        width: 100%;
        content-align: center middle;
    }}

    #title {{
        text-style: bold;
        color: {theme.get("primary")};
        margin-bottom: 1;
        text-align: center;
        align: center middle;
    }}

    Tree {{
        width: 100%;
        height: 35%;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
        margin-bottom: 1;
        align: center middle;
    }}

    Tree:focus {{
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
        outline: none;
    }}

    Tree > .tree--guides {{
        color: {theme.get("secondary")};
    }}

    Tree > .tree--cursor {{
        background: {theme.get("primary")};
        color: {theme.get("background")};
    }}

    Select {{
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
        margin-top: 1;
        width: 100%;
        align: center middle;
    }}

    Select > SelectCurrent {{
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    Select > SelectOverlay {{
        background: {theme.get("background")};
        color: {theme.get("primary")};
        border: solid {theme.get("primary")};
    }}

    OptionList {{
        background: {theme.get("background")};
        color: {theme.get("primary")};
        border: solid {theme.get("primary")};
    }}

    OptionList > .option-list--option {{
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    OptionList > .option-list--option-highlighted {{
        background: {theme.get("primary")} !important;
        color: {theme.get("background")} !important;
        text-style: bold;
    }}

    OptionList > .option-list--option-selected {{
        background: {theme.get("primary")} !important;
        color: {theme.get("background")} !important;
        text-style: bold;
    }}

    OptionList:focus > .option-list--option-highlighted {{
        background: {theme.get("primary")} !important;
        color: {theme.get("background")} !important;
    }}

    Button {{
        margin-top: 2;
        width: 25;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    #start_button {{
        margin-top: 2;
        width: 25;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    #button_container {{
        align: center middle;
        width: 100%;
    }}

    .root_mode {{
        border: solid {theme.get("primary")};
        background: {theme.get("primary")};
        color: {theme.get("background")};
    }}
    """

    def compose(self) -> ComposeResult:
        with Static(id="menu"):  
=======
>>>>>>> 398ea52 (WIP: Menu improvements with file selection and difficulty modes)
            yield Static(
                """╺┳┓┏━┓╺┳╸┏━┓   ┏━┓┏━╸╻  ┏━╸┏━╸╺┳╸╻┏━┓┏┓╻
 ┃┃┣━┫ ┃ ┣━┫   ┗━┓┣╸ ┃  ┣╸ ┃   ┃ ┃┃ ┃┃┗┫
╺┻┛╹ ╹ ╹ ╹ ╹   ┗━┛┗━╸┗━╸┗━╸┗━╸ ╹ ╹┗━┛╹ ╹""", id="title")

            yield Input(
                placeholder="Type filename to search (e.g. 'system', 'error', 'app')...",
                id="search_input"
            )

            yield ListView(id="file_list")
            yield Label("Scanning...", id="status_label")

            # Selector de dificultad con botones como antes
            yield Label("Select difficulty:", id="difficulty_label")
            from textual.containers import Horizontal
            difficulty_container = Horizontal(
                Button("User (Normal)", id="user_mode", classes="difficulty_button selected"),
                Button("Root (Hard)", id="root_mode", classes="difficulty_button root_mode"),
                id="difficulty_container"
            )
            yield difficulty_container

            yield Vertical(
                Button("Start Game", id="start_button"),
                Button("Back", id="back_button"),
                id="buttons_container"
            )

    async def on_mount(self) -> None:
        search_input = self.query_one("#search_input", Input)
        search_input.focus()
        
        def scan_logs():
            self._scan_log_files()
            self.call_from_thread(self._update_results)
        
        scan_thread = Thread(target=scan_logs)
        scan_thread.daemon = True
        scan_thread.start()

    def _scan_log_files(self) -> None:
        """Escanea archivos .log optimizado con información de contenido"""
        self.all_log_files = []
        
        search_paths = [
            os.path.expanduser("~"),
            "/var/log",
            "/tmp", 
            "."
        ]
        
        if os.name == 'nt':
            search_paths.extend([
                "C:\\Windows\\Logs",
                "C:\\ProgramData"
            ])

        for search_path in search_paths:
            try:
                if not os.path.exists(search_path):
                    continue
                    
                path_obj = Path(search_path)
                
                for log_file in path_obj.rglob("*.log"):
                    try:
                        if log_file.is_file():
                            stat = log_file.stat()
                            
                            # Leer contenido para obtener información adicional
                            line_count = 0
                            content_preview = ""
                            try:
                                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    lines = f.readlines()
                                    line_count = len([line for line in lines if line.strip()])
                                    # Tomar las primeras líneas no vacías como preview
                                    non_empty_lines = [line.strip() for line in lines if line.strip()]
                                    if non_empty_lines:
                                        content_preview = non_empty_lines[0][:50] + "..." if len(non_empty_lines[0]) > 50 else non_empty_lines[0]
                                    else:
                                        content_preview = "(empty file)"
                            except:
                                content_preview = "(cannot read)"
                            
                            # Filtrar archivos vacíos
                            if line_count == 0:
                                continue
                            
                            log_obj = LogFile(
                                path=log_file,
                                score=1.0,
                                name=log_file.name,
                                parent_dir=str(log_file.parent),
                                size=stat.st_size,
                                line_count=line_count,
                                content_preview=content_preview
                            )
                            
                            self.all_log_files.append(log_obj)
                            
                    except (OSError, PermissionError):
                        continue
                        
            except (OSError, PermissionError):
                continue

        # Ordenar por número de líneas (más contenido primero)
        self.all_log_files.sort(key=lambda f: f.line_count, reverse=True)

    def _update_results(self) -> None:
        """Actualiza la lista de resultados limpia y con información útil"""
        file_list = self.query_one("#file_list", ListView)
        search_input = self.query_one("#search_input", Input)
        
        # Quitar clase collapsed cuando estamos buscando
        file_list.set_class(False, "collapsed")
        
        file_list.clear()
        
        query = search_input.value
        self.filtered_files = self.fuzzy_matcher.find_matches(query, self.all_log_files, 50)
        
        for log_file in self.filtered_files:
            size_mb = log_file.size / (1024 * 1024)
            
            # Formato limpio: filename | lines | size | path
            text = f"{log_file.name} | {log_file.line_count} lines | {size_mb:.1f}MB"
            
            if query:
                score_percent = int(log_file.score * 100)
                text += f" [{score_percent}%]"
            
            # Mostrar ruta del archivo en segunda línea
            text += f"\n   Path: {log_file.parent_dir}"
            
            # Preview del contenido en tercera línea
            text += f"\n   Content: {log_file.content_preview}"
            
            list_item = ListItem(Label(text))
            list_item.log_file = log_file
            file_list.append(list_item)
        
        status_label = self.query_one("#status_label", Label)
        total_found = len(self.all_log_files)
        filtered_count = len(self.filtered_files)
        
        # Mostrar archivo seleccionado si hay uno
        if self.selected_file:
            status_label.update(f"Selected: {self.selected_file.name} | {filtered_count}/{total_found} log files")
        else:
            status_label.update(f"{filtered_count}/{total_found} log files | navigate | Enter select")
        
        if file_list.children:
            file_list.index = 0

    async def on_mount(self) -> None:
        search_input = self.query_one("#search_input", Input)
        search_input.focus()
        
        def scan_logs():
            self._scan_log_files()
            self.call_from_thread(self._update_results)
        
        scan_thread = Thread(target=scan_logs)
        scan_thread.daemon = True
        scan_thread.start()

    async def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search_input":
            self._update_results()

    async def on_select_changed(self, event: Select.Changed) -> None:
        """Remover - ya no usamos Select"""
        pass

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        sound_manager.play_menu_click()
        
        if event.button.id == "user_mode":
            self.selected_difficulty = "user"
            self._update_difficulty_buttons()
        elif event.button.id == "root_mode":
            self.selected_difficulty = "root"
            self._update_difficulty_buttons()
        elif event.button.id == "start_button":
            await self._start_game()
        elif event.button.id == "back_button":
            self.app.pop_screen()

    def _update_difficulty_buttons(self):
        """Actualizar visual de botones de dificultad"""
        user_button = self.query_one("#user_mode", Button)
        root_button = self.query_one("#root_mode", Button)
        
        if self.selected_difficulty == "user":
            user_button.set_class(True, "selected")
            root_button.set_class(False, "root_selected")
        else:
            user_button.set_class(False, "selected")
            root_button.set_class(True, "root_selected")

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        sound_manager.play_menu_click()
        if event.item and hasattr(event.item, 'log_file'):
            self.selected_file = event.item.log_file
            
            # Colapsar la lista después de seleccionar
            self._collapse_file_list()

    async def action_select(self) -> None:
        file_list = self.query_one("#file_list", ListView)
        if file_list.children and file_list.index is not None:
            selected_item = file_list.children[file_list.index]
            if hasattr(selected_item, 'log_file'):
                self.selected_file = selected_item.log_file
                
                # Colapsar la lista después de seleccionar
                self._collapse_file_list()

    def _collapse_file_list(self):
        """Colapsa la lista de archivos después de seleccionar uno"""
        file_list = self.query_one("#file_list", ListView)
        search_input = self.query_one("#search_input", Input)
        
        # Agregar clase CSS para achicarlo
        file_list.set_class(True, "collapsed")
        
        # Limpiar la lista para que ocupe menos espacio
        file_list.clear()
        
        # Mostrar solo el archivo seleccionado
        if self.selected_file:
            size_mb = self.selected_file.size / (1024 * 1024)
            text = f"✓ SELECTED: {self.selected_file.name} | {self.selected_file.line_count} lines | {size_mb:.1f}MB"
            text += f"\n   Path: {self.selected_file.parent_dir}"
            text += f"\n   Content: {self.selected_file.content_preview}"
            
            list_item = ListItem(Label(text))
            list_item.log_file = self.selected_file
            file_list.append(list_item)
        
        # Actualizar status
        status_label = self.query_one("#status_label", Label)
        if self.selected_file:
            status_label.update(f"✓ Selected: {self.selected_file.name} | Type to search again")
        
        # Foco en el input para poder buscar de nuevo si quiere
        search_input.focus()

    async def _start_game(self):
        if not self.selected_file:
            self.app.notify("Please select a log file first", severity="warning")
            return

        # Verificar si el archivo tiene contenido suficiente
        if self.selected_file.line_count < 5:
            self.app.notify(f"Warning: File has only {self.selected_file.line_count} lines. May generate very short music.", severity="warning")

        # Debug: Mostrar información detallada del archivo seleccionado
        print(f"\n=== DEBUG: Archivo seleccionado ===")
        print(f"Nombre: {self.selected_file.name}")
        print(f"Ruta completa: {self.selected_file.path}")
        print(f"Tamaño: {self.selected_file.size} bytes")
        print(f"Líneas: {self.selected_file.line_count}")
        print(f"Preview: {self.selected_file.content_preview}")
        print(f"Dificultad: {self.selected_difficulty}")
        print("=== FIN DEBUG ===\n")

        game_start_sound_path = os.path.join(os.path.dirname(__file__), "res", "game-start.mp3")
        play_sound_and_wait(game_start_sound_path)

        game_config = {
            "file": str(self.selected_file.path),
            "difficulty": self.selected_difficulty
        }
        
        print(f"Configuración del juego: {game_config}")
        
        self.app.exit(game_config)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        sound_manager.play_menu_click()
        
        if event.button.id == "start_button":
            await self._start_game()
        elif event.button.id == "back_button":
            self.app.pop_screen()

    async def action_cancel(self) -> None:
        self.app.pop_screen()

class BeatBuggingApp(App):
    def on_mount(self) -> None:
        self.push_screen(TitleScreen())

def run_menu():
    """Ejecuta el menú y retorna la información del juego seleccionado"""
    app = BeatBuggingApp()
    result = app.run()
    return result

if __name__ == "__main__":
    result = run_menu()
    
    if result:
        print(f"Archivo seleccionado: {result}")
        print("El juego debería iniciar ahora...")
    else:
        print("Saliendo del juego...")
        print("El juego debería iniciar ahora...")
