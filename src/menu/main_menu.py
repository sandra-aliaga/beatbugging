from textual.app import App, ComposeResult
from textual.widgets import Static, Button, Tree, Label, Select
from textual.containers import Vertical
from textual.screen import Screen
import random
import os


# Pantalla de Título
class TitleScreen(Screen):
    CSS = """
    Screen {
        align: center middle;
        background: black;
        color: #00ff00;
    }

    #ascii {
        text-style: bold;
        color: #00ff00;
        margin-bottom: 2;
        text-align: center;
    }

    #subtitle {
        color: #39ff14;
        margin-bottom: 2;
        text-align: center;
        width: 100%;
        content-align: center middle;
        text-style: bold;
        padding: 1;
    }

    Button {
        width: 20;
        margin: 1;
        border: solid #00ff00;
        background: black;
        color: #00ff00;
    }

    Button:hover {
        background: #003300;
    }

    #exit_button {
        border: solid red;
        color: red;
    }

    #exit_button:hover {
        background: #330000;
    }
    """

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


# Setup Screen
class SetupScreen(Screen):
    CSS = """
    Screen {
        align: center middle;
        background: #0a0a0a;
        color: #00ff00;
    }

    #title {
        text-style: bold;
        color: #00ff00;
        margin-bottom: 1;
    }

    Tree {
        height: 10;
        width: 60;
        border: solid #00ff00;
        background: black;
        color: #00ff00;
    }

    Select {
        border: solid #00ff00;
        background: black;
        color: #00ff00;
        margin-top: 1;
    }

    Button {
        margin-top: 2;
        width: 25;
        border: solid #00ff00;
        background: black;
        color: #00ff00;
    }

    Button:hover {
        background: #003300;
    }

    .root_mode {
        border: solid red;
        color: red;
    }

    .root_mode:hover {
        background: #330000;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static("⚡ Selección de datos ⚡", id="title")

        # Árbol de archivos para logs - usar directorio apropiado según el sistema
        import platform
        if platform.system() == "Windows":
            root_dir = "C:\\"
        else:
            # En Linux/Unix, usar el directorio de logs del proyecto
            logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
            root_dir = logs_dir if os.path.exists(logs_dir) else "/tmp"
        
        tree = Tree(f"📁 {root_dir}", id="file_tree")
        try:
            for item in os.listdir(root_dir):
                # Solo mostrar archivos .log si es el directorio de logs
                if root_dir.endswith('logs'):
                    if item.endswith('.log'):
                        tree.root.add_leaf(f"📄 {item}")
                else:
                    tree.root.add_leaf(f"📄 {item}")
        except (PermissionError, FileNotFoundError):
            tree.root.add_leaf("📄 default.log (será creado)")
        
        yield tree

        # Selector de dificultad
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
            
            print("\n🎮 Iniciando BeatBugging (Modo Original)...")
            print(f"📁 Archivo: {file_chosen}")
            print(f"⚙️  Dificultad: {diff}")
            print("🎵 Usando mapa de texto como era antes")
            
            # Configurar el juego y cerrar el menú
            self.app.exit(file_chosen)  # Pasar el archivo seleccionado


# Aplicación Principal
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
        print(f"📁 Archivo seleccionado: {result}")
        print("🎮 El juego debería iniciar ahora...")
    else:
        print("👋 Saliendo del juego...")
