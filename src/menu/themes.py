import json
import os

DEFAULT_THEME = {
    "border": "green",
    "background": "black",
    "primary": "green",
    "secondary": "cyan",
    "danger": "red",
    "success": "green",
}

class ThemeManager:
    def __init__(self, theme_file="themes.json"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.theme_file = os.path.join(current_dir, theme_file)
        self.themes = {}
        self.current_theme = {}
        self.load_themes()

    def load_themes(self):
        if not os.path.exists(self.theme_file):
            self.themes = {"default": DEFAULT_THEME}
            self.current_theme = DEFAULT_THEME
            return

        with open(self.theme_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.themes = data.get("themes", {})
        default = data.get("default_theme", "default")
        self.set_theme(default)

    def set_theme(self, theme_name):
        if theme_name not in self.themes:
            self.current_theme = DEFAULT_THEME
            return
        self.current_theme = self.themes[theme_name]

    def get(self, key, fallback=None):
        return self.current_theme.get(key, fallback)
