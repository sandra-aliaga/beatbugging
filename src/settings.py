import json
from pathlib import Path
from rich.theme import Theme
from rich.console import Console

# Base color per role for each theme.
_BASE: dict[str, dict[str, str]] = {
    "matrix": {
        "primary": "green",
        "accent":  "bright_green",
        "info":    "cyan",
        "warning": "yellow",
        "danger":  "red",
    },
    "blood": {
        "primary": "red",
        "accent":  "bright_red",
        "info":    "white",
        "warning": "yellow",
        "danger":  "bright_red",
    },
    "ocean": {
        "primary": "blue",
        "accent":  "bright_blue",
        "info":    "cyan",
        "warning": "yellow",
        "danger":  "red",
    },
    "phosphor": {
        "primary": "yellow",
        "accent":  "bright_yellow",
        "info":    "white",
        "warning": "bright_white",
        "danger":  "red",
    },
}

# Modifiers that need precomposed theme entries.
# Rich does NOT resolve theme names inside style strings like "bold primary"
# (it tries to parse "primary" as a raw color and fails). We must register
# each composed variant explicitly so the whole token resolves via the theme.
_MODIFIERS = ["bold", "dim", "bold reverse"]


def _build_theme(roles: dict[str, str]) -> Theme:
    styles: dict[str, str] = {}
    for role, color in roles.items():
        styles[role] = color
        for mod in _MODIFIERS:
            key = f"{role}.{mod.replace(' ', '_')}"
            styles[key] = f"{mod} {color}"
    # "muted" is a semantic alias for the dim variant of primary.
    styles["muted"] = f"dim {roles['primary']}"
    return Theme(styles)


THEMES: dict[str, Theme] = {name: _build_theme(roles) for name, roles in _BASE.items()}

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
_DEFAULTS: dict = {"theme": "matrix", "scale": "minor", "planet_aspect": 2.4}

PLANET_ASPECT_MIN = 1.5
PLANET_ASPECT_MAX = 3.5
PLANET_ASPECT_STEP = 0.1


class Settings:
    theme: str = "matrix"
    scale: str = "minor"
    planet_aspect: float = 2.4  # terminal cell height/width ratio for planet render

    @classmethod
    def load(cls) -> None:
        try:
            data = json.loads(SETTINGS_PATH.read_text())
            cls.theme = data.get("theme", _DEFAULTS["theme"])
            cls.scale = data.get("scale", _DEFAULTS["scale"])
            if cls.theme not in THEMES:
                cls.theme = _DEFAULTS["theme"]
            try:
                aspect = float(data.get("planet_aspect", _DEFAULTS["planet_aspect"]))
                cls.planet_aspect = max(PLANET_ASPECT_MIN,
                                        min(PLANET_ASPECT_MAX, aspect))
            except (TypeError, ValueError):
                cls.planet_aspect = _DEFAULTS["planet_aspect"]
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

    @classmethod
    def save(cls) -> None:
        try:
            SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
            SETTINGS_PATH.write_text(
                json.dumps({
                    "theme": cls.theme,
                    "scale": cls.scale,
                    "planet_aspect": round(cls.planet_aspect, 2),
                }, indent=2)
            )
        except OSError:
            pass

    @classmethod
    def make_console(cls, **kwargs) -> Console:
        return Console(theme=THEMES.get(cls.theme, THEMES["matrix"]), **kwargs)
