import json
import os

class ThemeManager:
    def __init__(self, theme_file="themes.json"):
        # Get the absolute path to the themes.json file in the same directory as this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.theme_file = os.path.join(current_dir, theme_file)
        self.themes = {}
        self.current_theme = {}

        self.load_themes()

    def load_themes(self):
        if not os.path.exists(self.theme_file):
            raise FileNotFoundError(f"No se encontró el archivo {self.theme_file}")

        with open(self.theme_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.themes = data.get("themes", {})
        default = data.get("default_theme", "default")
        self.set_theme(default)

    def set_theme(self, theme_name):
        if theme_name not in self.themes:
            raise ValueError(f"Tema '{theme_name}' no encontrado en {self.theme_file}")
        self.current_theme = self.themes[theme_name]

    def get(self, key, fallback=None):
        return self.current_theme.get(key, fallback)
