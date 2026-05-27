from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
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
    # Use a centered title line whose visible width matches the planet so the
    # silhouette is not deformed by per-line re-centering inside the Table.
    title_pad = max(0, (_PLANET_W - len("ORBIT")) // 2)
    title_line = Text(" " * title_pad + "ORBIT\n", style="accent.bold")
    rotation_str = f"rotation {math.degrees(angle) % 360:6.1f}°"
    rot_pad = max(0, (_PLANET_W - len(rotation_str)) // 2)
    rotation_line = Text(" " * rot_pad + rotation_str, style="primary.dim")

    planet_block = Text.assemble(
        title_line,
        Text("\n"),
        planet,
        Text("─" * _PLANET_W + "\n", style="primary.dim"),
        rotation_line,
    )

    # Use no_wrap and a left-justified fixed-width column so Rich never
    # re-centers lines individually (which would trim trailing spaces from
    # the planet rows and break the circular shape).
    grid = Table.grid(expand=False, padding=(0, 4))
    grid.add_column(justify="left")
    grid.add_column(justify="left", no_wrap=True)
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


def _module_line(name: str, desc: str, progress: float, bar_w: int = 22) -> Text:
    """One pacman-style line: name | progress bar | percent | OK tag."""
    pct = int(progress * 100)
    bar = _progress_bar(progress, bar_w)
    done = progress >= 1.0
    tag = "[ OK ]" if done else "[....]"
    line = Text()
    line.append(f"  {name.strip():<18}", style="primary" if done else "primary.bold")
    line.append(f"{desc:<19}", style="primary.dim")
    line.append("[", style="primary.dim")
    line.append(bar, style="accent" if done else "primary.bold")
    line.append("] ", style="primary.dim")
    line.append(f"{pct:>3}% ", style="accent.bold" if done else "primary.bold")
    line.append(tag, style="accent.bold" if done else "primary.dim")
    return line


class LoadingScreen:
    def __init__(self, console: Console):
        self.console = console

    def _header(self, message: str) -> Text:
        out = Text()
        banner_lines = _BIOS_BANNER.strip("\n").splitlines()
        for line in banner_lines:
            out.append(line + "\n", style="primary.bold")
        sub = "BEATBUGGING SYSTEM   -   BIOS v2.0.42   -   (c) 2026 BB CORP"
        out.append(sub + "\n", style="primary.dim")
        out.append(f">>> {message} <<<\n\n", style="accent.bold")
        return out

    def show_loading(self, message: str, duration: float = 1.6):
        message = message.upper()
        n = len(_MODULES)
        tick = 0.04  # ~25 fps
        per_module = max(0.15, (duration * 0.85) / n)
        ticks_per_module = max(3, int(per_module / tick))

        header = self._header(message)
        completed: list[Text] = []

        with Live(console=self.console, refresh_per_second=25,
                  transient=False, screen=False) as live:
            for name, desc in _MODULES:
                for t in range(ticks_per_module + 1):
                    progress = min(1.0, t / ticks_per_module)
                    current = _module_line(name, desc, progress)
                    live.update(Group(header, *completed, current))
                    time.sleep(tick)
                completed.append(_module_line(name, desc, 1.0))

            # Final flash: all done + summary footer
            footer = Text("\n  ALL MODULES OK — entering debug session...\n",
                          style="accent.bold")
            live.update(Group(header, *completed, footer))
            time.sleep(0.25)