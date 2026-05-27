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