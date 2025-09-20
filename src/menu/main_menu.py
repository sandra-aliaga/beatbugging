from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Tree, Label, Select
from textual.containers import Vertical
from textual.screen import Screen
from themes import ThemeManager
import random
import os

# Cargar tema actual
theme = ThemeManager()

def make_title_css():
    return f"""
    Screen {{
        align: center middle;
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    #ascii {{
        text-style: bold;
        color: {theme.get("primary")};
        margin-bottom: 2;
        text-align: center;
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
        width: 20;
        margin: 1;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    Button:hover {{
        background: {theme.get("hover")};
    }}

    #exit_button {{
        border: solid {theme.get("danger")};
        color: {theme.get("danger")};
    }}

    #exit_button:hover {{
        background: {theme.get("danger_hover")};
    }}
    """


class TitleScreen(Screen):
    CSS = make_title_css()

    def compose(self) -> ComposeResult:
        ascii_logo = r"""
██████  ███████  █████  ████████     ██████  ██    ██  ██████   ██████   ██ ███    ██  ██████  
██   ██ ██      ██   ██    ██        ██   ██ ██    ██ ██       ██        ██ ████   ██ ██       
██████  █████   ███████    ██        ██████  ██    ██ ██   ███ ██   ███  ██ ██ ██  ██ ██   ███ 
██   ██ ██      ██   ██    ██        ██   ██ ██    ██ ██    ██ ██    ██  ██ ██  ██ ██ ██    ██ 
███████ ███████ ██   ██    ██        ███████  ██████   ██████   ██████   ██ ██   ████  ██████  
"""
        yield Static(ascii_logo, id="ascii")

        errors = random.randint(5000, 99999)
        yield Label(f"{errors} errores encontrados", id="subtitle")

        yield Vertical(
            Button("🚀 Jugar", id="play_button"),
            Button("❌ Salir", id="exit_button"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play_button":
            self.app.push_screen(SetupScreen())
        elif event.button.id == "exit_button":
            self.app.exit()


class SetupScreen(Screen):
    CSS = f"""
    Screen {{
        align: center middle;
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    #title {{
        text-style: bold;
        color: {theme.get("primary")};
        margin-bottom: 1;
    }}

    Tree {{
        height: 10;
        width: 60;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    Select {{
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
        margin-top: 1;
    }}

    Button {{
        margin-top: 2;
        width: 25;
        border: solid {theme.get("primary")};
        background: {theme.get("background")};
        color: {theme.get("primary")};
    }}

    Button:hover {{
        background: {theme.get("hover")};
    }}

    .root_mode {{
        border: solid {theme.get("danger")};
        color: {theme.get("danger")};
    }}

    .root_mode:hover {{
        background: {theme.get("danger_hover")};
    }}
    """

    def compose(self) -> ComposeResult:
        yield Static("⚡ Selección de datos ⚡", id="title")

        tree = Tree("C:\\", id="file_tree")
        for item in os.listdir("C:\\"):
            tree.root.add_leaf(item)
        yield tree

        yield Select(
            options=[
                ("User (normal)", "user"),
                ("Root (difícil)", "root"),
            ],
            id="difficulty_select",
            prompt="Seleccione dificultad"
        )

        yield Button("✅ Iniciar Juego", id="start_button")

    def on_select_changed(self, event: Select.Changed) -> None:
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
            self.app.pop_screen()
            self.app.push_screen(TitleScreen())
            self.app.notify(f"Iniciando en modo {diff} con archivo {file_chosen}")


class BeatBuggingApp(App):
    def on_mount(self) -> None:
        self.push_screen(TitleScreen())


if __name__ == "__main__":
    BeatBuggingApp().run()
