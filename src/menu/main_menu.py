from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Tree, Label, Select
from textual.containers import Vertical
from textual.screen import Screen
from themes import ThemeManager
import random
import os
import pygame
import time
from threading import Thread

# Cargar tema actual
theme = ThemeManager()

def make_title_css():
    return f"""
    #menu {{
        align: center middle;
        border: round {theme.get("border")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
        padding: 0;
    }}

    #ascii {{
        text-style: bold;
        color: {theme.get("primary")};
        margin-bottom: 2;
        text-align: center;
        border-bottom: solid {theme.get("primary")};
        padding-bottom: 1;
    }}

    #subtitle {{
        color: {theme.get("secondary")};
        margin-bottom: 2;
        text-align: center;
        width: 100%;
        content-align: center middle;
        text-style: bold;
        padding: 1;
    }}

    Button {{
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
        align-horizontal: center;
        width: 20;
        margin: 1;
    }}

    #exit_button {{
        border: solid {theme.get("danger")};
        background: {theme.get("background")};
        color: {theme.get("danger")};
    }}

    #buttons_container {{
        align: center middle;
    }}
    """


def play_sound_and_wait(sound_path):
    """Play a sound file and wait for it to finish"""
    try:
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Load and play the sound
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(0.4)  # Set reduced volume for game start sound
        sound.play()
        
        # Wait for the sound to finish
        while pygame.mixer.get_busy():
            time.sleep(0.1)
            
    except Exception as e:
        # If sound fails, just continue without sound
        print(f"Could not play sound: {e}")
        pass


class SoundManager:
    """Manages menu sounds with overlap prevention"""
    
    def __init__(self):
        self.last_click_time = 0
        self.click_delay = 0.2  # Minimum delay between clicks in seconds
        self.volume = 0.3  # Volume level (0.0 to 1.0) - reduced from default
        self.menu_click_path = os.path.join(os.path.dirname(__file__), "res", "menu-click.mp3")
        
        # Initialize pygame mixer
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except:
            pass
    
    def play_menu_click(self):
        """Play menu click sound with overlap prevention"""
        current_time = time.time()
        
        # Check if enough time has passed since last click
        if current_time - self.last_click_time >= self.click_delay:
            self.last_click_time = current_time
            
            def play_click():
                try:
                    sound = pygame.mixer.Sound(self.menu_click_path)
                    sound.set_volume(self.volume)  # Set reduced volume
                    sound.play()
                except Exception as e:
                    print(f"Could not play menu click sound: {e}")
            
            # Play in separate thread to avoid blocking
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
 ░███░░░░░███ ░███░░█    ░███░░░░░███     ░███        ░███░░░░░███ ░███   ░███ ░███    █████░███    █████ ░███  ░███ ░░██████ ░███    █████
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
        # Play menu click sound for all buttons except start
        sound_manager.play_menu_click()
        
        if event.button.id == "play_button":
            self.app.push_screen(SetupScreen())
        elif event.button.id == "exit_button":
            self.app.exit()


class SetupScreen(Screen):
    CSS = f"""
    #menu {{
        align: center middle;
        border: round green;
        background: {theme.get("background")};
        color: {theme.get("primary")};
        padding: 2;
    }}

    #title {{
        text-style: bold;
        color: {theme.get("primary")};
        margin-bottom: 1;
    }}

    Tree {{
        width: 100%;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
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
            yield Static("⚡ Data Selection ⚡", id="title")

            # Use platform-appropriate root directory
            if os.name == 'nt':  # Windows
                root_dir = "C:\\"
            else:  # Linux/Unix
                root_dir = "/"
            
            tree = Tree(root_dir, id="file_tree")
            try:
                for item in os.listdir(root_dir):
                    tree.root.add_leaf(item)
            except PermissionError:
                # If we can't access root, use home directory instead
                home_dir = os.path.expanduser("~")
                tree = Tree(home_dir, id="file_tree")
                for item in os.listdir(home_dir):
                    tree.root.add_leaf(item)
            yield tree

            yield Select(
                options=[
                    ("User (normal)", "user"),
                    ("Root (hard)", "root"),
                ],
                id="difficulty_select",
                prompt="Select difficulty"
            )

            with Static(id="button_container"):
                yield Button("Start Game", id="start_button")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Play click sound when a tree node is selected"""
        sound_manager.play_menu_click()

    def on_select_changed(self, event: Select.Changed) -> None:
        # Play menu click sound when difficulty selection changes
        sound_manager.play_menu_click()
        
        start_button = self.query_one("#start_button", Button)
        if event.value == "root":
            start_button.set_class(True, "root_mode")
        else:
            start_button.set_class(False, "root_mode")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start_button":
            diff = self.query_one("#difficulty_select", Select).value
            file_tree = self.query_one("#file_tree", Tree)
            selected = file_tree.cursor_node
            if selected is None:
                self.app.bell()
                return
            file_chosen = selected.label
            
            # Play the game start sound and wait for it to finish
            sound_path = os.path.join(os.path.dirname(__file__), "res", "game-start.mp3")
            
            # Run sound in a separate thread to avoid blocking the UI
            def play_and_continue():
                play_sound_and_wait(sound_path)
                # After sound finishes, proceed with the game start
                self.app.call_from_thread(self._continue_game_start, diff, file_chosen)
            
            # Start the sound in background thread
            sound_thread = Thread(target=play_and_continue)
            sound_thread.daemon = True
            sound_thread.start()
    
    def _continue_game_start(self, diff, file_chosen):
        """Continue with game start after sound has finished"""
        self.app.pop_screen()
        self.app.push_screen(TitleScreen())
        self.app.notify(f"Starting in {diff} mode with file {file_chosen}")


class BeatBuggingApp(App):
    def on_mount(self) -> None:
        self.push_screen(TitleScreen())


if __name__ == "__main__":
    BeatBuggingApp().run()
