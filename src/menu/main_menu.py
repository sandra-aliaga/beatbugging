from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Label, Input, ListView, ListItem, Select, RichLog
from textual.containers import Vertical
from textual.screen import Screen
from textual.binding import Binding
from textual.message import Message
from rich.text import Text
import random
import os
import pygame
import time
import difflib
import itertools
import numpy as np
from threading import Thread
from pathlib import Path
from dataclasses import dataclass
from typing import List
from textual.containers import Horizontal, Vertical
from music.generator import LogMusicGenerator

@dataclass
class LogFile:
    path: Path
    score: float
    name: str
    parent_dir: str
    size: int
    line_count: int = 0
    content_preview: str = ""

class SimpleFuzzyMatcher:
    
    @staticmethod
    def calculate_ratio(query: str, filename: str) -> float:
        if not query:
            return 1.0
        
        query_lower = query.lower()
        filename_lower = filename.lower()
        
        ratio = difflib.SequenceMatcher(None, query_lower, filename_lower).ratio()
        
        if query_lower in filename_lower:
            ratio += 0.4
        
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

TITLE_CSS = """
    Screen {
        background: ansi_black;
    }

    #menu {
        align: center middle;
        border: round ansi_green;
        background: ansi_black;
        color: ansi_green;
        padding: 2;
        height: 100%;
        width: 100%;
        content-align: center middle;
    }

    #ascii {
        text-align: center;
        align: center middle;
        color: ansi_green;
        margin-bottom: 1;
    }

    #title {
        text-style: bold;
        color: ansi_green;
        margin-bottom: 1;
        text-align: center;
        border-bottom: solid ansi_green;
        align: center middle;
        padding-bottom: 0;
        height: auto;
    }

    #subtitle_container {
        align: center middle;
        width: 100%;
        height: auto;
        content-align: center middle;
    }

    #subtitle {
        color: ansi_cyan;
        margin-bottom: 1;
        text-align: center;
        text-style: bold;
        height: auto;
        align: center middle;
        width: 100%;
        content-align: center middle;
    }

    Button {
        border: solid ansi_green;
        background: ansi_black;
        color: ansi_green;
        align-horizontal: center;
        width: 30%;
        margin: 1;
    }

    #exit_button {
        border: solid ansi_red;
        background: ansi_black;
        color: ansi_red;
    }

    #buttons_container {
        align: center middle;
    }

    #search_input {
        height: 3;
        margin-top: 0;
        margin-bottom: 0;
        border: solid ansi_green;
        background: ansi_black;
        color: ansi_green;
    }

    #file_list {
        height: 20%;
        border: solid ansi_green;
        background: ansi_black;
        color: ansi_green;
    }

    #file_list.collapsed {
        height: 3;
        border: solid ansi_bright_green;
    }

    #status_label {
        height: 1;
        color: ansi_cyan;
        text-align: center;
        margin-bottom: 0;
        margin-top: 0;
    }

    #difficulty_label {
        color: ansi_cyan;
        text-align: center;
        margin-top: 1;
        margin-bottom: 0;
        text-style: bold;
    }

    #difficulty_container {
        align: center middle;
        margin-top: 0;
        margin-bottom: 0;
    }

    #game_modes_container {
        align: center middle;
        margin-top: 0;
        margin-bottom: 1;
    }

    #control_buttons_container {
        align: center middle;
        margin-top: 0;
        margin-bottom: 0;
    }

    #buttons_section {
        align: center middle;
        margin-top: 1;
        margin-bottom: 0;
    }

    .difficulty_button {
        margin: 0 1;
        border: solid ansi_green;
        background: ansi_black;
        color: ansi_green;
    }

    .difficulty_button:hover {
        background: ansi_green;
        color: ansi_black;
    }

    .difficulty_button.selected {
        background: ansi_green;
        color: ansi_black;
        text-style: bold;
    }

    .difficulty_button.selected:hover {
        background: ansi_green;
        color: ansi_black;
    }

    .root_mode {
        border: solid ansi_red;
        background: ansi_black;
        color: ansi_red;
    }

    .root_mode:hover {
        background: ansi_red;
        color: ansi_black;
    }

    .root_mode.root_selected {
        background: ansi_red;
        color: ansi_black;
        text-style: bold;
    }

    .root_mode.root_selected:hover {
        background: ansi_red;
        color: ansi_black;
    }

    #start_button {
        border: solid ansi_bright_green;
        background: ansi_black;
        color: ansi_bright_green;
        width: auto;
        margin: 0 1;
    }

    #listen_button {
        border: solid ansi_green;
        background: ansi_black;
        color: ansi_green;
        width: auto;
        margin: 0 1;
    }

    #back_button {
        border: solid ansi_green;
        background: ansi_black;
        color: ansi_green;
        width: auto;
        margin: 0 1;
    }

    ListItem {
        background: ansi_black;
        color: ansi_green;
    }

    ListItem:hover {
        background: ansi_green;
        color: ansi_black;
    }

    ListItem.--highlight {
        background: ansi_green;
        color: ansi_black;
    }

    Input {
        background: ansi_black;
        color: ansi_green;
        border: solid ansi_green;
    }

    Input:focus {
        background: ansi_black;
        border: solid ansi_cyan;
    }
"""

def play_sound_and_wait(sound_path):
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

sound_manager = SoundManager()

class TitleScreen(Screen):
    CSS = TITLE_CSS

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
            with Vertical(id="subtitle_container"):
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
    CSS = TITLE_CSS

    BINDINGS = [
        Binding("ctrl+c", "cancel", "Cancel"),
        Binding("escape", "cancel", "Cancel"),
        Binding("enter", "select", "Select"),
    ]

    class UpdateFilesMessage(Message):
        """Message to trigger file list update from background thread"""
        pass

    def __init__(self):
        super().__init__()
        self.all_log_files: List[LogFile] = []
        self.filtered_files: List[LogFile] = []
        self.selected_file: LogFile = None
        self.selected_difficulty: str = "user"
        self.fuzzy_matcher = SimpleFuzzyMatcher()
        self.search_timer = None

    def compose(self) -> ComposeResult:
        with Static(id="menu"):  
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

            yield Label("Select difficulty:", id="difficulty_label")

            game_modes_container = Horizontal(
                Button("User (Normal)", id="user_mode", classes="difficulty_button"),
                Button("Root (Hard)", id="root_mode", classes="difficulty_button root_mode"),
                id="game_modes_container"
            )

            control_buttons_container = Horizontal(
                Button("Back", id="back_button"),
                Button("Listen", id="listen_button"),
                Button("Start Game", id="start_button"),
                id="control_buttons_container"
            )

            buttons_section = Vertical(
                game_modes_container,
                control_buttons_container,
                id="buttons_section"
            )
            yield buttons_section

    async def on_mount(self) -> None:
        search_input = self.query_one("#search_input", Input)
        search_input.focus()
        
        def scan_logs():
            self._scan_log_files()
            # Post message to main thread to update UI
            self.post_message(self.UpdateFilesMessage())

        scan_thread = Thread(target=scan_logs)
        scan_thread.daemon = True
        scan_thread.start()

    def _scan_log_files(self) -> None:
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
                            
                            line_count = 0
                            content_preview = ""
                            MAX_PREVIEW_LINES = 200
                            try:
                                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                                    sampled = list(itertools.islice(f, MAX_PREVIEW_LINES))
                                non_empty = [l.strip() for l in sampled if l.strip()]
                                line_count = len(non_empty)
                                if non_empty:
                                    first = non_empty[0]
                                    content_preview = first[:50] + "..." if len(first) > 50 else first
                                else:
                                    content_preview = "(empty file)"
                            except Exception:
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

        self.all_log_files.sort(key=lambda f: f.line_count, reverse=True)

    def _debounced_update_results(self) -> None:
        """Update results with debounce - called by timer"""
        try:
            self._update_results()
        except Exception as e:
            # Silently handle errors to prevent crashes
            pass

    def _update_results(self) -> None:
        try:
            file_list = self.query_one("#file_list", ListView)
            search_input = self.query_one("#search_input", Input)

            file_list.set_class(False, "collapsed")
            file_list.clear()

            # Don't proceed if files aren't loaded yet
            if not self.all_log_files:
                status_label = self.query_one("#status_label", Label)
                status_label.update("Still scanning for log files...")
                return

            query = search_input.value
            self.filtered_files = self.fuzzy_matcher.find_matches(query, self.all_log_files, 50)

            for log_file in self.filtered_files:
                size_mb = log_file.size / (1024 * 1024)

                # Formato limpio: filename | lines | size | path
                text_content = f"{log_file.name} | {log_file.line_count} lines | {size_mb:.1f}MB"

                if query:
                    score_percent = int(log_file.score * 100)
                    text_content += f" [{score_percent}%]"

                # Mostrar ruta del archivo en segunda línea
                text_content += f"\n   Path: {log_file.parent_dir}"

                # Preview del contenido en tercera línea
                text_content += f"\n   Content: {log_file.content_preview}"

                # Create Text object without markup to prevent Rich interpretation
                safe_text = Text(text_content)
                list_item = ListItem(Label(safe_text))
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

        except Exception as e:
            # Silently handle any errors during search to prevent UI blocking
            pass

    async def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "search_input":
            # Cancel previous timer if exists
            if self.search_timer:
                self.search_timer.stop()

            # Set new timer with debounce delay
            self.search_timer = self.set_timer(0.3, self._debounced_update_results)

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
        elif event.button.id == "listen_button":
            await self._start_listen()
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
            
            self._collapse_file_list()

    async def action_select(self) -> None:
        file_list = self.query_one("#file_list", ListView)
        if file_list.children and file_list.index is not None:
            selected_item = file_list.children[file_list.index]
            if hasattr(selected_item, 'log_file'):
                self.selected_file = selected_item.log_file
                
                self._collapse_file_list()

    def _collapse_file_list(self):
        file_list = self.query_one("#file_list", ListView)
        search_input = self.query_one("#search_input", Input)
        
        file_list.set_class(True, "collapsed")
        
        file_list.clear()
        
        if self.selected_file:
            size_mb = self.selected_file.size / (1024 * 1024)
            text_content = f"✓ SELECTED: {self.selected_file.name} | {self.selected_file.line_count} lines | {size_mb:.1f}MB"
            text_content += f"\n   Path: {self.selected_file.parent_dir}"
            text_content += f"\n   Content: {self.selected_file.content_preview}"

            # Create Text object without markup to prevent Rich interpretation
            safe_text = Text(text_content)
            list_item = ListItem(Label(safe_text))
            list_item.log_file = self.selected_file
            file_list.append(list_item)
        
        status_label = self.query_one("#status_label", Label)
        if self.selected_file:
            status_label.update(f"✓ Selected: {self.selected_file.name} | Type to search again")
        
        search_input.focus()

    async def _start_game(self):
        if not self.selected_file:
            self.app.notify("Please select a log file first", severity="warning")
            return

        if self.selected_file.line_count < 5:
            self.app.notify(f"Warning: File has only {self.selected_file.line_count} lines. May generate very short music.", severity="warning")

        game_start_sound_path = os.path.join(os.path.dirname(__file__), "res", "game-start.mp3")
        play_sound_and_wait(game_start_sound_path)

        game_config = {
            "file": str(self.selected_file.path),
            "difficulty": self.selected_difficulty
        }
        
        
        self.app.exit(game_config)

    async def _start_listen(self) -> None:
        if not self.selected_file:
            self.app.notify("Please select a log file first", severity="warning")
            return
        self.app.push_screen(ListenScreen(self.selected_file))

    async def action_cancel(self) -> None:
        self.app.pop_screen()

    def on_setup_screen_update_files_message(self, message: UpdateFilesMessage) -> None:
        """Handle file update message from background thread"""
        self._update_results()

LISTEN_CSS = TITLE_CSS + """
    #listen_info {
        text-align: center;
        color: ansi_green;
        text-style: bold;
        margin-bottom: 1;
        height: auto;
    }
    #listen_progress_label {
        text-align: center;
        color: ansi_cyan;
        height: auto;
        margin-bottom: 1;
    }
    #listen_log {
        border: solid ansi_green;
        background: ansi_black;
        height: 1fr;
        margin: 1;
    }
    #listen_hint {
        text-align: center;
        color: ansi_cyan;
        height: auto;
        margin-top: 1;
    }
"""

class ListenScreen(Screen):
    CSS = LISTEN_CSS

    BINDINGS = [
        Binding("escape", "stop", "Stop"),
    ]

    class MusicReadyMessage(Message):
        def __init__(self, audio_data, actions, total_duration: float) -> None:
            super().__init__()
            self.audio_data = audio_data
            self.actions = actions
            self.total_duration = total_duration

    def __init__(self, log_file: LogFile) -> None:
        super().__init__()
        self.log_file = log_file
        self.start_time: float | None = None
        self.total_duration: float = 0.0
        self.actions: list = []
        self.lines_shown: int = 0
        self._tick_timer = None

    def compose(self) -> ComposeResult:
        size_mb = self.log_file.size / (1024 * 1024)
        with Static(id="menu"):
            yield Static(
                f"♪ LISTEN MODE — {self.log_file.name} | {self.log_file.line_count} lines | {size_mb:.1f}MB",
                id="listen_info"
            )
            yield Label("░" * 40 + "  0%  0:00 / 0:00", id="listen_progress_label")
            yield RichLog(id="listen_log", auto_scroll=True, highlight=True, markup=False)
            yield Label("ESC → volver al menú", id="listen_hint")

    async def on_mount(self) -> None:
        richlog = self.query_one("#listen_log", RichLog)
        richlog.write("Generating music from log file...")

        def generate() -> None:
            try:
                gen = LogMusicGenerator(log_path=str(self.log_file.path))
                result = gen.generate_music()
                actions = result["gameplay_actions"]
                total = max((a["tiempo"] for a in actions), default=0.0)
                self.post_message(self.MusicReadyMessage(
                    audio_data=result["audio_data"],
                    actions=actions,
                    total_duration=total,
                ))
            except Exception:
                self.post_message(self.MusicReadyMessage(
                    audio_data=None,
                    actions=[],
                    total_duration=0.0,
                ))

        t = Thread(target=generate)
        t.daemon = True
        t.start()

    def on_listen_screen_music_ready_message(self, msg: "ListenScreen.MusicReadyMessage") -> None:
        self.actions = msg.actions
        self.total_duration = msg.total_duration

        richlog = self.query_one("#listen_log", RichLog)
        richlog.clear()

        if msg.audio_data is None or len(msg.audio_data) == 0:
            richlog.write("Error: could not generate music from this file.")
            return

        def play() -> None:
            try:
                audio = msg.audio_data
                if not pygame.mixer.get_init():
                    pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
                    pygame.mixer.init()
                mixer_config = pygame.mixer.get_init()
                if mixer_config and mixer_config[2] == 2 and audio.ndim == 1:
                    audio = np.column_stack((audio, audio))
                audio = audio.astype(np.int16)
                sound = pygame.sndarray.make_sound(audio)
                sound.play()
            except Exception:
                pass

        t = Thread(target=play)
        t.daemon = True
        t.start()

        self.start_time = time.time()
        self._tick_timer = self.set_interval(0.1, self._tick)

    def _tick(self) -> None:
        if self.start_time is None:
            return

        elapsed = time.time() - self.start_time

        if self.total_duration > 0:
            pct = min(100, int(elapsed / self.total_duration * 100))
            bar_width = 36
            filled = int(pct / 100 * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)

            def fmt(s: float) -> str:
                return f"{int(s) // 60}:{int(s) % 60:02d}"

            label = self.query_one("#listen_progress_label", Label)
            label.update(f"{bar}  {pct}%  {fmt(elapsed)} / {fmt(self.total_duration)}")

        richlog = self.query_one("#listen_log", RichLog)
        while self.lines_shown < len(self.actions):
            action = self.actions[self.lines_shown]
            if action["tiempo"] <= elapsed:
                richlog.write(action["line"])
                self.lines_shown += 1
            else:
                break

        if self.total_duration > 0 and elapsed >= self.total_duration:
            self.call_after_refresh(self.action_stop)

    def action_stop(self) -> None:
        try:
            pygame.mixer.stop()
        except Exception:
            pass
        if self._tick_timer is not None:
            self._tick_timer.stop()
        self.app.pop_screen()


class BeatBuggingApp(App):
    THEME = "textual-dark"

    def on_mount(self) -> None:
        self.push_screen(TitleScreen())

def run_menu():
    app = BeatBuggingApp()
    result = app.run()
    return result

if __name__ == "__main__":
    result = run_menu()
