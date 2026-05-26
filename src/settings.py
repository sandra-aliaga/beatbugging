import json
from pathlib import Path
from rich.theme import Theme
from rich.console import Console

THEMES: dict[str, Theme] = {
    "matrix": Theme({
        "primary": "green",
        "accent":  "bright_green",
        "muted":   "dim green",
        "info":    "cyan",
        "warning": "yellow",
        "danger":  "red",
    }),
    "blood": Theme({
        "primary": "red",
        "accent":  "bright_red",
        "muted":   "dim red",
        "info":    "white",
        "warning": "yellow",
        "danger":  "bright_red",
    }),
    "ocean": Theme({
        "primary": "blue",
        "accent":  "bright_blue",
        "muted":   "dim blue",
        "info":    "cyan",
        "warning": "yellow",
        "danger":  "red",
    }),
    "phosphor": Theme({
        "primary": "yellow",
        "accent":  "bright_yellow",
        "muted":   "dim yellow",
        "info":    "white",
        "warning": "bright_white",
        "danger":  "red",
    }),
}

THEME_LABELS: dict[str, str] = {
    "matrix":   "Matrix   (Green)",
    "blood":    "Blood    (Red)",
    "ocean":    "Ocean    (Blue)",
    "phosphor": "Phosphor (Amber)",
}

# Hardcoded preview colors for swatches — always correct regardless of active theme
THEME_PREVIEW_COLORS: dict[str, str] = {
    "matrix":   "green",
    "blood":    "red",
    "ocean":    "blue",
    "phosphor": "yellow",
}

THEME_ORDER: list[str] = list(THEMES.keys())

SETTINGS_PATH = Path.home() / ".config" / "beatbugging" / "settings.json"
_DEFAULTS: dict = {"theme": "matrix", "scale": "minor"}


class Settings:
    theme: str = "matrix"
    scale: str = "minor"

    @classmethod
    def load(cls) -> None:
        try:
            data = json.loads(SETTINGS_PATH.read_text())
            cls.theme = data.get("theme", _DEFAULTS["theme"])
            cls.scale = data.get("scale", _DEFAULTS["scale"])
            if cls.theme not in THEMES:
                cls.theme = _DEFAULTS["theme"]
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

    @classmethod
    def save(cls) -> None:
        try:
            SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
            SETTINGS_PATH.write_text(
                json.dumps({"theme": cls.theme, "scale": cls.scale}, indent=2)
            )
        except OSError:
            pass

    @classmethod
    def make_console(cls, **kwargs) -> Console:
        return Console(theme=THEMES.get(cls.theme, THEMES["matrix"]), **kwargs)
