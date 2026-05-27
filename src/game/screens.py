from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
import math
import random
import time

# ── Procedural 3D ASCII planet ────────────────────────────────────────────────
_PLANET_W = 26
_PLANET_H = 11
# Shade ramp WITHOUT leading space — every point inside the sphere is visible
# so the silhouette stays circular even in deep shadow.
_SHADE = ".,:;+=*xoXO#@"


def _render_planet(angle: float, aspect: float = None) -> Text:
    """3D ASCII sphere rotated by `angle` rad on Y axis, Lambertian shaded.

    `aspect` is the terminal cell height/width ratio. If None, reads
    Settings.planet_aspect. Tune this per-terminal until the sphere looks round.
    """
    if aspect is None:
        from settings import Settings  # local import to avoid circular dep
        aspect = Settings.planet_aspect
    lx, ly, lz = -0.5, -0.5, 0.71  # light: upper-left, toward viewer
    out = Text()
    R = min(
        _PLANET_W / 2.0 - 0.5,
        (_PLANET_H - 0.5) * aspect / 2.0 - 0.5,
    )

    for j in range(_PLANET_H):
        y = (j - _PLANET_H / 2.0 + 0.5) * aspect
        for i in range(_PLANET_W):
            x = i - _PLANET_W / 2.0 + 0.5
            r2 = x * x + y * y
            if r2 > R * R:
                out.append(" ")
                continue
            z = math.sqrt(R * R - r2)
            nx, ny, nz = x / R, y / R, z / R
            rx = nx * math.cos(angle) + nz * math.sin(angle)
            rz = -nx * math.sin(angle) + nz * math.cos(angle)
            dot = max(0.0, nx * lx + (-ny) * ly + nz * lz)
            lat = math.asin(max(-1.0, min(1.0, ny)))
            lon = math.atan2(rx, rz)
            land = (math.sin(lat * 2.4) * math.cos(lon * 1.8)
                    + math.sin(lat * 4.7 + lon * 2.3) * 0.5) > 0.05
            intensity = (0.18 + 0.82 * dot) * (1.15 if land else 0.85)
            idx = max(0, min(int(intensity * (len(_SHADE) - 1) + 0.5), len(_SHADE) - 1))
            ch = _SHADE[idx]
            if idx >= len(_SHADE) - 3:
                style = "accent.bold" if land else "accent"
            elif idx >= 4:
                style = "primary" if land else "primary.dim"
            else:
                style = "primary.dim"
            out.append(ch, style=style)
        out.append("\n")
    return out

class AsciiArt:
    @staticmethod
    def get_game_over_screen():
        arts = [
            r"""            ╔═══════════════════════════════════════════════════════════════════════════════════════╗
            ║                                                                                       ║
            ║   ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████   ║
            ║  ██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██  ║
            ║  ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████   ║
            ║  ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██  ║
            ║   ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██  ║
            ║                                                                                       ║
            ╚═══════════════════════════════════════════════════════════════════════════════════════╝"""            
        ]
        return arts
    
    @staticmethod
    def get_game_over_animation():
        frames = [
            r"""                                          ████████████████                                          
                                    ████████████████████████████                                    
                                 ██████████████████████████████████                                 
                               ██████████████████████████████████████                               
                              ████████████████████████████████████████                              
                             ██████████████████████████████████████████                             
                            ████████████████████████████████████████████                            
                           ██████████████████████████████████████████████                           
                          ████████████████████████████████████████████████                          
                          ████████████████████████████████████████████████                          
                         ██████████████████████████████████████████████████                         
                         ██████████████████████████████████████████████████                         
                         ██████████████████████████████████████████████████                         
                         ██████████████████████████████████████████████████                         
                         ██████████████████████████████████████████████████                         
                         ██████████████████████████████████████████████████                         
                         ██████████████████████████████████████████████████                         
                           ███████████████████████████████████████████████                          
                            ███     ████████████████████████████     ███                            
                             █        ████████████████████████        █                             
                             █          ████████████████████          █                             
                            ███               ████████               ███                            
                          ███████          ██████  ██████          ███████                          
                         ██████████████████████      ██████████████████████                         
                         ██████████████████████      ██████████████████████                         
                           ███████████████████        ███████████████████                           
                             ████     ████████   ██   ████████     ████                             
                                        ████████████████████                                        
                                        ████████████████████                                        
                                        ████████████████████                                        
                                   █    ████████████████████    █                                   
                                   ██   ████████████████████   ██                                   
                                   ██   ████████████████████   ██                                   
                                   ███    ████ ██  ██ ████     ██                                   
                                   ███         ██  ██         ███                                   
                                   ████ █                  █ ████                                   
                                   ███████                ███████                                   
                                    ████████          █ ████████                                    
                                       ████████      ████████                                       
                                        ████████████████████                                        
                                          ████████████████                                          
                                           ██████████████                                           
                                             ██████████                                             """,
            r"""████████████████████████████████████████████            ████████████████████████████████████████████
████████████████████████████████████████                    ████████████████████████████████████████
████████████████████████████████████                            ████████████████████████████████████
████████████████████████████████                                    ████████████████████████████████
███████████████████████████████                                      ███████████████████████████████
█████████████████████████████                                          █████████████████████████████
█████████████████████████████                                          █████████████████████████████
████████████████████████████                                            ████████████████████████████
███████████████████████████                                              ███████████████████████████
██████████████████████████                                                ██████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
█████████████████████████                                                  █████████████████████████
██████████████████████████                                                ██████████████████████████
████████████████████████████   ███                                ███   ████████████████████████████
█████████████████████████████  ███████                         ██████   ████████████████████████████
████████████████████████████   █████████                    █████████   ████████████████████████████
███████████████████████████    ███████████████        ███████████████    ███████████████████████████
█████████████████████████        ██████████              ██████████        █████████████████████████
█████████████████████████                       ████                       █████████████████████████
█████████████████████████                      ██████                      █████████████████████████
██████████████████████████                    ████████                    ██████████████████████████
█████████████████████████████                 ██    ██                 █████████████████████████████
████████████████████████████████████████                    ████████████████████████████████████████
████████████████████████████████████████                    ████████████████████████████████████████
████████████████████████████████████████                    ████████████████████████████████████████
██████████████████████████████████  ███                      ███  ██████████████████████████████████
███████████████████████████████████  ██                      ██  ███████████████████████████████████
███████████████████████████████████  ██                      ██  ███████████████████████████████████
███████████████████████████████████   ████       ██       ████   ███████████████████████████████████
███████████████████████████████████   ██████     ██     ██████   ███████████████████████████████████
███████████████████████████████████    █  ████████████████  █    ███████████████████████████████████
██████████████████████████████████        ████████████████        ██████████████████████████████████
████████████████████████████████████        █ ████████          ████████████████████████████████████
██████████████████████████████████████                        ██████████████████████████████████████
████████████████████████████████████████                    ████████████████████████████████████████
██████████████████████████████████████████                ██████████████████████████████████████████
███████████████████████████████████████████              ███████████████████████████████████████████
█████████████████████████████████████████████          █████████████████████████████████████████████
████████████████████████████████████████████████    ████████████████████████████████████████████████"""
        ]
        return frames



    @staticmethod
    def get_victory_screen():
        arts = [
            r"""╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                  ║
║ ██    ██ ██  ██████ ████████  ██████  ██████  ██  █████      ███████ ██   ██  ██████ ███████ ██  ║
║ ██    ██ ██ ██         ██    ██    ██ ██   ██ ██ ██   ██     ██      ██   ██ ██      ██      ██  ║
║ ██    ██ ██ ██         ██    ██    ██ ██████  ██ ███████     █████    ██ ██  ██      █████   ██  ║
║  ██  ██  ██ ██         ██    ██    ██ ██   ██ ██ ██   ██     ██        ███   ██      ██          ║
║   ████   ██  ██████    ██     ██████  ██   ██ ██ ██   ██     ███████   ██     ██████ ███████ ██  ║
║                                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
            """,
        ]
        return arts
    
    @staticmethod
    def get_victory_animation():
        frames = [
            r"""                      ██████████████████████████████████████████████████████████                    
                    █████████████████████████████████████████████████████████████                   
                     ███████████████████████████████████████████████████████████                    
                      █████████████████████████████████████████████████████████                     
                      █████████████████████████████████████████████████████████                     
              █████████████████████████████████████████████████████████████████████████             
             ███████████████████████████████████████████████████████████████████████████            
             █████     ███████████████████████████████████████████████████████     █████            
             █████     ███████████████████████████████████████████████████████     █████            
             ████      ███████████████████████████████████████████████████████     █████            
             █████      █████████████████████████████████████████████████████      █████            
             █████      █████████████████████████████████████████████████████      █████            
             █████       ████████████████████████████████████████████████████      █████            
              █████      ███████████████████████████████████████████████████      ██████            
              ██████     ██████████████████████████████████████████████████      ██████             
               ██████     █████████████████████████████████████████████████     ██████              
                ██████     ███████████████████████████████████████████████     ██████               
                 ███████    █████████████████████████████████████████████    ███████                
                   ████████  ███████████████████████████████████████████  ████████                  
                     ███████████████████████████████████████████████████████████                    
                       ███████████████████████████████████████████████████████                      
                           ███████████████████████████████████████████████                          
                                █████████████████████████████████████                               
                                   ███████████████████████████████                                  
                                    ████████████████████████████                                    
                                       ███████████████████████                                      
                                          █████████████████                                         
                                            █████████████                                           
                                            █████████████                                           
                                            █████████████                                           
                                            █████████████                                           
                                            █████████████                                           
                                           ███████████████                                          
                                         ███████████████████                                        
                                      ████████████████████████                                      
                                  █████████████████████████████████                                 
                                 ███████████████████████████████████                                
                                 ███████████████████████████████████                                
                             ███████████████████████████████████████████                            
                           ███████████████████████████████████████████████                          
                          █████████████████████████████████████████████████                         
                          █████████████████████████████████████████████████                         
                          █████████████████████████████████████████████████                         
                          █████████████████████████████████████████████████                         
                          █████████████████████████████████████████████████                         
                          █████████████████████████████████████████████████                         
                                                                                                    
            """,
            r"""██████████████████████                                                         █████████████████████
███████████████████████                                                       ██████████████████████
████████████████████████                                                     ███████████████████████
████████████████████████                                                     ███████████████████████
█████████████████                                                                   ████████████████
██████████████   ███████                                                     ███████   █████████████
██████████████  ████████                                                     ████████  █████████████
██████████████  ████████                                                     ████████  █████████████
██████████████  █████████                                                   █████████  █████████████
██████████████  █████████                                                   █████████  █████████████
██████████████  ██████████                                                 ██████████  █████████████
███████████████  █████████                                                 █████████  ██████████████
███████████████  ██████████                                               ██████████  ██████████████
████████████████  █████████                                               █████████  ███████████████
█████████████████  █████████                                             █████████  ████████████████
██████████████████  █████████                                           █████████  █████████████████
███████████████████   ████████                                         ████████   ██████████████████
█████████████████████   ███████                                       ███████   ████████████████████
████████████████████████   █████                                     █████   ███████████████████████
███████████████████████████                                               ██████████████████████████
███████████████████████████████                                      ███████████████████████████████
███████████████████████████████████                               ██████████████████████████████████
█████████████████████████████████████                           ████████████████████████████████████
███████████████████████████████████████                       ██████████████████████████████████████
██████████████████████████████████████████                 █████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
█████████████████████████████████████████████           ████████████████████████████████████████████
████████████████████████████████████████████             ███████████████████████████████████████████
██████████████████████████████████████████                 █████████████████████████████████████████
██████████████████████████████████████                         █████████████████████████████████████
███████████████████████████████████                               ██████████████████████████████████
███████████████████████████████████                               ██████████████████████████████████
███████████████████████████████████                               ██████████████████████████████████
█████████████████████████████                                           ████████████████████████████
████████████████████████████                                             ███████████████████████████
███████████████████████████                                               ██████████████████████████
███████████████████████████                                               ██████████████████████████
███████████████████████████                                               ██████████████████████████
███████████████████████████                                               ██████████████████████████
████████████████████████████████████████████████████████████████████████████████████████████████████"""
        ]
        return frames

    @staticmethod
    def get_loading_animation():
        frames = [
            "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
        ]
        return frames
    
    @staticmethod
    def get_matrix_rain():
        chars = "01アカサタナハマヤラワ"
        return [random.choice(chars) for _ in range(50)]
    
    @staticmethod
    def get_error_messages():
        messages = [
            "SEGMENTATION FAULT: Core dumped",
            "NULL POINTER EXCEPTION: Memory access violation",
            "STACK OVERFLOW: Recursion limit exceeded", 
            "BUFFER OVERRUN: Heap corruption detected",
            "RACE CONDITION: Thread synchronization failed",
            "MEMORY LEAK: Garbage collection failed",
            "DEADLOCK DETECTED: System resources locked",
            "ASSERTION FAILED: Logic error in beatbugging.exe",
            "ACCESS DENIED: Permission elevation required",
            "KERNEL PANIC: System halt imminent"
        ]
        return random.choice(messages)
    
class GameOverAnimation:
    def __init__(self, console: Console):
        self.console = console

    def show_game_over_animation(self, duration: float = 3.0, speed: float = 0.1):
        frames = AsciiArt.get_game_over_animation()
        size = self.console.size
        width, height = size.width, size.height

        start_time = time.time()
        frame_index = 0

        while time.time() - start_time < duration:
            frame = frames[frame_index % len(frames)]
            frame_lines = frame.splitlines()

            # === 0) Detectar carácter de fondo ===
            # Si el frame contiene muchos █, asumimos que el fondo es █
            background_char = "█" if sum(line.count("█") for line in frame_lines) > sum(line.count(" ") for line in frame_lines) else " "

            # === 1) Centrar horizontalmente ===
            lines = [
                line.center(width, background_char)[:width]
                for line in frame_lines
            ]

            # === 2) Centrar verticalmente ===
            frame_height = len(lines)
            if frame_height < height:
                pad_top = (height - frame_height) // 2
                pad_bottom = height - frame_height - pad_top
                lines = ([background_char * width] * pad_top) + lines + ([background_char * width] * pad_bottom)
            else:
                lines = lines[:height]

            # === 3) Convertir a texto ===
            padded_frame = "\n".join(lines)
            text = Text(padded_frame, style="bold red")

            # === 4) Imprimir ===
            self.console.clear()
            self.console.print(text, end="")

            time.sleep(speed)
            frame_index += 1

def _bar(value: float, width: int = 24) -> str:
    """Render a 0-100 value as a discrete █▓▒░ progress bar."""
    pct = max(0.0, min(100.0, float(value))) / 100.0
    filled = int(pct * width)
    half = 1 if (pct * width - filled) >= 0.5 and filled < width else 0
    chars = "█" * filled + ("▓" if half else "") + "░" * (width - filled - half)
    return chars


def _row(label: str, value: str, width: int = 40) -> str:
    """LABEL...........VALUE — POST/BIOS style row."""
    dots = "." * max(3, width - len(label) - len(value))
    return f"  {label}{dots}{value}"


_PLANET_MIN_TERM_WIDTH = 100


def _text_from_entries(entries) -> Text:
    body = Text()
    for entry in entries:
        if isinstance(entry, tuple):
            body.append(entry[0] + "\n", style=entry[1])
        else:
            body.append(entry + "\n")
    return body


def _stats_with_planet(stats_body: Text, angle: float, console_width: int):
    """Compose stats panel + planet side-by-side if width permits."""
    if console_width < _PLANET_MIN_TERM_WIDTH:
        return Align.center(stats_body, vertical="middle")

    planet = _render_planet(angle)
    planet_block = Text.assemble(
        Text("ORBIT\n", style="accent.bold", justify="center"),
        Text("\n"),
        planet,
        Text("\n"),
        Text("─" * _PLANET_W + "\n", style="primary.dim"),
        Text(f"  rotation {math.degrees(angle) % 360:6.1f}°", style="primary.dim"),
    )

    grid = Table.grid(expand=False, padding=(0, 4))
    grid.add_column(justify="left")
    grid.add_column(width=_PLANET_W + 2, justify="center")
    grid.add_row(stats_body, planet_block)
    return Align.center(grid, vertical="middle")


class GameOverScreen:
    def __init__(self, console: Console):
        self.console = console

    def build(self, stats: dict, angle: float = 0.0):
        score    = stats.get("score", 0)
        combo    = stats.get("max_combo", 0)
        accuracy = stats.get("accuracy", 0.0)
        perfect  = stats.get("perfect", 0)
        health   = stats.get("health", 0)

        lines = [
            "",
            ("═" * 56, "primary.dim"),
            ("        B E A T B U G G I N G   v2.0", "primary.bold"),
            ("═" * 56, "primary.dim"),
            "",
            ("       > > >   S Y S T E M   H A L T   < < <", "danger.bold"),
            "",
            ("  " + "─" * 52, "primary.dim"),
            (_row("SCORE",        f"{score:>10,}"),       "primary"),
            (_row("MAX_COMBO",    f"{combo:>10}"),        "primary"),
            (_row("ACCURACY",     f"{accuracy:>9.1f}%"),  "primary"),
            (_row("PERFECT_HITS", f"{perfect:>10}"),      "primary"),
            (_row("HEALTH",       f"{health:>10}"),       "danger"),
            ("  " + "─" * 52, "primary.dim"),
            (f"  HEALTH_BAR  [{_bar(health, 38)}]", "danger"),
            (f"  ACCURACY    [{_bar(accuracy, 38)}]", "primary.dim"),
            ("  " + "─" * 52, "primary.dim"),
            (_row("STATUS",       "FAILED"),              "danger.bold"),
            (_row("EXIT_CODE",    "-1"),                  "danger"),
            (_row("CORE_DUMP",    "/var/log/bb/crash"),   "primary.dim"),
            ("  " + "─" * 52, "primary.dim"),
            "",
            ("  > _", "accent.bold"),
            "",
            ("  [ENTER] retry      [M] menu      [Q] quit", "primary.dim"),
        ]
        return _stats_with_planet(_text_from_entries(lines), angle, self.console.width)

    def display(self, stats: dict):
        """Static snapshot — kept for backwards compat / non-animated callers."""
        self.console.clear()
        self.console.print(self.build(stats, 0.0), end="")

class VictoryAnimation:
    def __init__(self, console: Console):
        self.console = console

    def show_victory_animation(self, duration: float = 3.0, speed: float = 0.1):
        frames = AsciiArt.get_victory_animation()
        size = self.console.size
        width, height = size.width, size.height

        start_time = time.time()
        frame_index = 0

        while time.time() - start_time < duration:
            frame = frames[frame_index % len(frames)]
            frame_lines = frame.splitlines()

            # === 0) Detectar carácter de fondo ===
            # Si el frame contiene muchos █, asumimos que el fondo es █
            background_char = "█" if sum(line.count("█") for line in frame_lines) > sum(line.count(" ") for line in frame_lines) else " "

            # === 1) Centrar horizontalmente ===
            lines = [
                line.center(width, background_char)[:width]
                for line in frame_lines
            ]

            # === 2) Centrar verticalmente ===
            frame_height = len(lines)
            if frame_height < height:
                pad_top = (height - frame_height) // 2
                pad_bottom = height - frame_height - pad_top
                lines = ([background_char * width] * pad_top) + lines + ([background_char * width] * pad_bottom)
            else:
                lines = lines[:height]

            # === 3) Convertir a texto ===
            padded_frame = "\n".join(lines)
            text = Text(padded_frame, style="bold red")

            # === 4) Imprimir ===
            self.console.clear()
            self.console.print(text, end="")

            time.sleep(speed)
            frame_index += 1

class VictoryScreen:
    def __init__(self, console: Console):
        self.console = console

    def get_performance_rank(self, stats: dict) -> str:
        accuracy = stats.get("accuracy", 0)
        score    = stats.get("score", 0)
        if accuracy >= 95 and score >= 20000: return "S+"
        if accuracy >= 90 and score >= 15000: return "S "
        if accuracy >= 85 and score >= 10000: return "A "
        if accuracy >= 75 and score >= 5000:  return "B "
        if accuracy >= 60:                    return "C "
        return "D "

    def _achievements(self, stats: dict) -> list[tuple[str, bool]]:
        return [
            ("CODE_MASTER",       stats.get("accuracy", 0) >= 90),
            ("COMBO_KING",        stats.get("max_combo", 0) >= 50),
            ("PRECISION_EXPERT",  stats.get("perfect", 0) >= stats.get("total_actions", 1) * 0.7),
            ("HIGH_SCORER",       stats.get("score", 0) >= 10000),
            ("BUG_HUNTER",        True),
            ("RHYTHM_HACKER",     True),
        ]

    def build(self, stats: dict, angle: float = 0.0):
        score    = stats.get("score", 0)
        combo    = stats.get("max_combo", 0)
        accuracy = stats.get("accuracy", 0.0)
        perfect  = stats.get("perfect", 0)
        rank     = self.get_performance_rank(stats)

        lines = [
            "",
            ("═" * 56, "primary.dim"),
            ("        B E A T B U G G I N G   v2.0", "primary.bold"),
            ("═" * 56, "primary.dim"),
            "",
            ("    > > >   D E B U G G I N G   C O M P L E T E   < < <", "accent.bold"),
            "",
            ("  " + "─" * 52, "primary.dim"),
            (_row("SCORE",        f"{score:>10,}"),       "primary"),
            (_row("MAX_COMBO",    f"{combo:>10}"),        "primary"),
            (_row("ACCURACY",     f"{accuracy:>9.1f}%"),  "primary"),
            (_row("PERFECT_HITS", f"{perfect:>10}"),      "accent"),
            ("  " + "─" * 52, "primary.dim"),
            (f"  ACCURACY    [{_bar(accuracy, 38)}]", "accent"),
            ("  " + "─" * 52, "primary.dim"),
            "",
            ("                  P E R F O R M A N C E", "primary.dim"),
            (f"                      [ R A N K   {rank} ]", "accent.bold"),
            "",
            ("  " + "─" * 52, "primary.dim"),
            ("  ACHIEVEMENTS", "primary.bold"),
        ]
        for name, unlocked in self._achievements(stats):
            mark  = "[+]" if unlocked else "[ ]"
            color = "accent" if unlocked else "primary.dim"
            state = "UNLOCKED" if unlocked else "LOCKED  "
            lines.append((f"    {mark}  {name:<22} {state}", color))
        lines += [
            ("  " + "─" * 52, "primary.dim"),
            (_row("STATUS",    "OPERATIONAL"), "accent.bold"),
            (_row("EXIT_CODE", "0"),           "primary"),
            ("  " + "─" * 52, "primary.dim"),
            "",
            ("  > _", "accent.bold"),
            "",
            ("  [ENTER] retry      [M] menu      [Q] quit", "primary.dim"),
        ]
        return _stats_with_planet(_text_from_entries(lines), angle, self.console.width)

    def display(self, stats: dict):
        """Static snapshot — kept for backwards compat / non-animated callers."""
        self.console.clear()
        self.console.print(self.build(stats, 0.0), end="")


_BIOS_BANNER = r"""
 ▄▄▄▄    ▄▄▄▄   ▄▄▄    ▓██   ██▓  ██████    ▄▄▄█████▓ ▒█████   ▒█████   ██▓
▓█████▄ ▓█████▄▒████▄   ▒██  ██▒▒██    ▒    ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
▒██▒ ▄██▒██▒ ▄██▒██  ▀█▄  ▒██ ██░░ ▓██▄      ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░
▒██░█▀  ▒██░█▀  ░██▄▄▄▄██ ░ ▐██▓░  ▒   ██▒   ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
░▓█  ▀█▓░▓█  ▀█▓ ▓█   ▓██▒░ ██▒▓░▒██████▒▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████
"""

_MODULES = [
    ("audio.subsystem      ", "freq synth + mixer"),
    ("rhythm.parser        ", "beat-map engine"),
    ("log.analyzer         ", "AST + token stream"),
    ("frequency.synth      ", "440-1760 Hz range"),
    ("beat.mapper          ", "tempo align"),
    ("debug.overlay        ", "matrix + grid"),
    ("input.controller     ", "raw stdin cbreak"),
    ("ui.compositor        ", "rich.live engine"),
]

_HEX_POOL = "0123456789ABCDEF"


def _hex_word(length: int = 8) -> str:
    return "".join(random.choice(_HEX_POOL) for _ in range(length))


def _progress_bar(pct: float, width: int) -> str:
    pct = max(0.0, min(1.0, pct))
    full = int(pct * width)
    partial_idx = int((pct * width - full) * 4)
    partials = " ░▒▓"
    bar = "█" * full
    if full < width:
        bar += partials[partial_idx]
        bar += "░" * (width - full - 1)
    return bar


class LoadingScreen:
    def __init__(self, console: Console):
        self.console = console

    def _render_frame(self, message: str, progress: float, frame: int, width: int, height: int) -> Text:
        out = Text()

        # ── Banner ──────────────────────────────────────────────────────
        banner_lines = _BIOS_BANNER.strip("\n").splitlines()
        banner_w = max(len(l) for l in banner_lines)
        pad = max(0, (width - banner_w) // 2)
        for line in banner_lines:
            out.append(" " * pad + line + "\n", style="primary.bold")

        # ── Subtitle line ────────────────────────────────────────────────
        sub = "BEATBUGGING SYSTEM   -   BIOS v2.0.42   -   (c) 2026 BB CORP"
        out.append(" " * max(0, (width - len(sub)) // 2) + sub + "\n", style="primary.dim")
        out.append(" " * max(0, (width - len(message) - 4) // 2)
                   + f">>> {message} <<<\n", style="accent.bold")
        out.append("\n")

        # ── Modules being loaded ─────────────────────────────────────────
        n_modules = len(_MODULES)
        modules_done = int(progress * n_modules)
        working_idx = min(modules_done, n_modules - 1)

        col_w = 56
        col_pad = " " * max(0, (width - col_w) // 2)

        for i, (name, desc) in enumerate(_MODULES):
            if i < modules_done:
                tag, tag_style, name_style = "[   OK   ]", "accent.bold", "primary"
            elif i == working_idx:
                spinner = "|/-\\"[frame % 4]
                tag, tag_style, name_style = f"[WORKING{spinner}]", "primary.bold", "primary.bold"
            else:
                tag, tag_style, name_style = "[        ]", "primary.dim", "primary.dim"
            out.append(col_pad)
            out.append(f"  {name}", style=name_style)
            out.append(f"{desc:<22}", style="primary.dim")
            out.append(f"{tag}\n", style=tag_style)
        out.append("\n")

        # ── Diagnostic test lines (animated hex/freq stream) ─────────────
        mem_kb = 1024 * (1 + frame % 8)
        freqs = ["440Hz", "523Hz", "659Hz", "784Hz", "880Hz"]
        chosen = " ".join(freqs[:1 + frame % 5])
        diag_lines = [
            f"  memory test ...... {mem_kb:>5}K  OK",
            f"  audio test  ...... {chosen}  OK",
            f"  hash check  ...... 0x{_hex_word()}  0x{_hex_word()}  0x{_hex_word()}",
            f"  rng seed    ...... 0x{_hex_word(16)}",
            f"  parsing     ...... node_{frame:04d} offset=0x{_hex_word(6)}",
        ]
        for line in diag_lines:
            out.append(col_pad + line + "\n", style="primary")
        out.append("\n")

        # ── Progress bar (wide) ──────────────────────────────────────────
        bar_w = max(20, width - 20)
        bar = _progress_bar(progress, bar_w)
        pct_str = f"{int(progress * 100):>3d}%"
        bar_pad = " " * max(0, (width - bar_w - 8) // 2)
        out.append(bar_pad, style="primary")
        out.append("[", style="primary.dim")
        out.append(bar, style="accent")
        out.append("] ", style="primary.dim")
        out.append(pct_str + "\n", style="accent.bold")
        out.append("\n")

        # ── Footer ───────────────────────────────────────────────────────
        footer = "press CTRL+C to abort"
        out.append(" " * max(0, (width - len(footer)) // 2) + footer + "\n",
                   style="primary.dim")

        return out

    def show_loading(self, message: str, duration: float = 3.0):
        start_time = time.time()
        frame = 0

        while True:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                break
            progress = min(0.99, elapsed / duration)

            size = self.console.size
            width, height = size.width, size.height

            content = self._render_frame(
                message.upper(), progress, frame, width, height
            )

            self.console.clear()
            self.console.print(content, end="", soft_wrap=False, overflow="crop")
            time.sleep(0.08)
            frame += 1

        # Final 100% frame so the user sees completion
        size = self.console.size
        content = self._render_frame(message.upper(), 1.0, frame, size.width, size.height)
        self.console.clear()
        self.console.print(content, end="", soft_wrap=False, overflow="crop")