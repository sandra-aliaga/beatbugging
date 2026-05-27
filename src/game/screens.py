from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.align import Align
import random
import time

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


class GameOverScreen:
    def __init__(self, console: Console):
        self.console = console

    def display(self, stats: dict):
        self.console.clear()

        score    = stats.get("score", 0)
        combo    = stats.get("max_combo", 0)
        accuracy = stats.get("accuracy", 0.0)
        perfect  = stats.get("perfect", 0)
        health   = stats.get("health", 0)

        lines = []
        lines.append("")
        lines.append(("═" * 56, "primary.dim"))
        lines.append(("        B E A T B U G G I N G   v2.0", "primary.bold"))
        lines.append(("═" * 56, "primary.dim"))
        lines.append("")
        lines.append(("       > > >   S Y S T E M   H A L T   < < <", "danger.bold"))
        lines.append("")
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append((_row("SCORE",        f"{score:>10,}"),       "primary"))
        lines.append((_row("MAX_COMBO",    f"{combo:>10}"),        "primary"))
        lines.append((_row("ACCURACY",     f"{accuracy:>9.1f}%"),  "primary"))
        lines.append((_row("PERFECT_HITS", f"{perfect:>10}"),      "primary"))
        lines.append((_row("HEALTH",       f"{health:>10}"),       "danger"))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append((f"  HEALTH_BAR  [{_bar(health, 38)}]", "danger"))
        lines.append((f"  ACCURACY    [{_bar(accuracy, 38)}]", "primary.dim"))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append((_row("STATUS",       "FAILED"),              "danger.bold"))
        lines.append((_row("EXIT_CODE",    "-1"),                  "danger"))
        lines.append((_row("CORE_DUMP",    "/var/log/bb/crash"),   "primary.dim"))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append("")
        lines.append(("  > _", "accent.bold"))
        lines.append("")
        lines.append(("  [ENTER] retry      [M] menu      [Q] quit", "primary.dim"))

        body = Text()
        for entry in lines:
            if isinstance(entry, tuple):
                body.append(entry[0] + "\n", style=entry[1])
            else:
                body.append(entry + "\n")

        self.console.print(Align.center(body, vertical="middle"), end="")

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

    def display(self, stats: dict):
        self.console.clear()

        score    = stats.get("score", 0)
        combo    = stats.get("max_combo", 0)
        accuracy = stats.get("accuracy", 0.0)
        perfect  = stats.get("perfect", 0)
        rank     = self.get_performance_rank(stats)

        lines = []
        lines.append("")
        lines.append(("═" * 56, "primary.dim"))
        lines.append(("        B E A T B U G G I N G   v2.0", "primary.bold"))
        lines.append(("═" * 56, "primary.dim"))
        lines.append("")
        lines.append(("    > > >   D E B U G G I N G   C O M P L E T E   < < <", "accent.bold"))
        lines.append("")
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append((_row("SCORE",        f"{score:>10,}"),       "primary"))
        lines.append((_row("MAX_COMBO",    f"{combo:>10}"),        "primary"))
        lines.append((_row("ACCURACY",     f"{accuracy:>9.1f}%"),  "primary"))
        lines.append((_row("PERFECT_HITS", f"{perfect:>10}"),      "accent"))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append((f"  ACCURACY    [{_bar(accuracy, 38)}]", "accent"))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append("")
        lines.append(("                  P E R F O R M A N C E", "primary.dim"))
        lines.append((f"                      [ R A N K   {rank} ]", "accent.bold"))
        lines.append("")
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append(("  ACHIEVEMENTS", "primary.bold"))
        for name, unlocked in self._achievements(stats):
            mark  = "[+]" if unlocked else "[ ]"
            color = "accent" if unlocked else "primary.dim"
            state = "UNLOCKED" if unlocked else "LOCKED  "
            lines.append((f"    {mark}  {name:<22} {state}", color))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append((_row("STATUS",       "OPERATIONAL"),         "accent.bold"))
        lines.append((_row("EXIT_CODE",    "0"),                   "primary"))
        lines.append(("  " + "─" * 52, "primary.dim"))
        lines.append("")
        lines.append(("  > _", "accent.bold"))
        lines.append("")
        lines.append(("  [ENTER] retry      [M] menu      [Q] quit", "primary.dim"))

        body = Text()
        for entry in lines:
            if isinstance(entry, tuple):
                body.append(entry[0] + "\n", style=entry[1])
            else:
                body.append(entry + "\n")

        self.console.print(Align.center(body, vertical="middle"), end="")


class LoadingScreen:
    def __init__(self, console: Console):
        self.console = console
        self.animation_frames = self._get_hacker_loading_frames()
        self.matrix_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.wave_chars = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        
    def _get_hacker_loading_frames(self):
        """Generate hacker-style loading animation frames"""
        return [
            "[██████████████████████████████████████████████████████████████████] 100%",
            "[████████████████████████████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 85%",
            "[████████████████████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 70%",
            "[██████████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 55%",
            "[██████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 40%",
            "[████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 25%",
            "[██████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 10%"
        ]
    
    def _generate_matrix_line(self, width=70):
        """Generate a single line of matrix-style characters"""
        line = ""
        for _ in range(width):
            if random.random() > 0.75:
                line += random.choice(self.matrix_chars)
            else:
                line += " "
        return line
    
    def _generate_wave_pattern(self, width=80, phase=0):
        """Generate audio wave visualization"""
        wave = ""
        for i in range(width):
            # Create wave pattern based on sine function
            import math
            height = int(3.5 * (1 + math.sin((i * 0.15) + (phase * 0.4))))
            if height >= len(self.wave_chars):
                height = len(self.wave_chars) - 1
            wave += self.wave_chars[height]
        return wave
    
    def _create_system_status(self, frame_index):
        """Create system status display"""
        statuses = [
            "SCANNING SYSTEM LOGS FOR RHYTHM PATTERNS",
            "PARSING ERROR FREQUENCIES AND BEAT MAPPING", 
            "ANALYZING MUSICAL PATTERNS IN DEBUG DATA",
            "CALIBRATING AUDIO SYNTHESIS ENGINE",
            "SYNCHRONIZING BEATS WITH LOG TIMESTAMPS",
            "INITIALIZING MUSICAL DEBUGGING INTERFACE",
            "LOADING RHYTHM-BASED ERROR DETECTION"
        ]
        
        current_status = statuses[frame_index % len(statuses)]
        dots = "." * ((frame_index % 4) + 1)
        return f"[SYSTEM] {current_status}{dots}"
    
    def _create_data_stream(self, width=50):
        """Create scrolling data stream effect"""
        hex_chars = "0123456789ABCDEF"
        stream = ""
        for _ in range(width):
            if random.random() > 0.6:
                stream += random.choice(hex_chars)
            else:
                stream += " "
        return f"0x{stream}"
    
    def show_loading(self, message: str, duration: float = 3.0):
        start_time = time.time()
        frame_index = 0
        
        while time.time() - start_time < duration:
            # Get current frame
            frame = self.animation_frames[frame_index % len(self.animation_frames)]
            
            # Generate dynamic content
            matrix_line_1 = self._generate_matrix_line(70)
            matrix_line_2 = self._generate_matrix_line(70)
            wave_pattern = self._generate_wave_pattern(60, frame_index)
            system_status = self._create_system_status(frame_index)
            data_stream = self._create_data_stream(50)
            
            # Create loading display with centered larger text
            loading_text = Text(
                f"{frame}",
                style="bold bright_green",
                justify="center"
            )
            
            # Create message text - larger and more prominent
            message_text = Text(
                f">>> {message.upper()} <<<",
                style="bold bright_white",
                justify="center"
            )
            
            # Create system status with better formatting
            status_text = Text(
                system_status,
                style="bright_cyan",
                justify="center"
            )
            
            # Create enhanced wave visualization
            wave_text = Text(
                f"AUDIO: {wave_pattern}",
                style="bright_yellow",
                justify="center"
            )
            
            # Create frequency display
            freq_display = Text(
                "FREQUENCIES: 440Hz | 523Hz | 659Hz | 784Hz",
                style="dim bright_yellow",
                justify="center"
            )
            
            # Create data stream
            stream_text = Text(
                f"MEMORY: {data_stream}",
                style="dim bright_green",
                justify="center"
            )
            
            # Create matrix effects - not centered for authentic matrix look
            matrix_text_1 = Text(matrix_line_1, style="dim green")
            matrix_text_2 = Text(matrix_line_2, style="dim green")
            
            # Combine all content with clean spacing
            panel_content = Text("\n").join([
                Text(""),
                matrix_text_1,
                Text(""),
                loading_text,
                Text(""),
                message_text,
                Text(""),
                status_text,
                Text(""),
                wave_text,
                freq_display,
                Text(""),
                stream_text,
                Text(""),
                matrix_text_2,
                Text("")
            ])
            
            # Create panel with clean styling
            panel = Panel(
                panel_content,
                border_style="bright_green",
                title="[bold bright_green]BEATBUGGING SYSTEM[/bold bright_green]",
                subtitle="[dim bright_red]CTRL+C to abort[/dim bright_red]",
                padding=(1, 2)
            )
            
            # Display
            self.console.clear()
            self.console.print(Align.center(panel))
            
            time.sleep(0.15)
            frame_index += 1