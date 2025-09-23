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

class GameOverScreen:
    def __init__(self, console: Console):
        self.console = console
        
    def create_error_log_panel(self, stats: dict) -> Panel:
        error_log = Table(show_header=False, box=None, padding=0)
        error_log.add_column(style="red", width=60)
        
        error_msgs = [
            f"[FATAL] {AsciiArt.get_error_messages()}",
            f"[ERROR] Music synchronization lost at frame {stats.get('score', 0)}",
            f"[ERROR] Input buffer overflow after {stats.get('combo', 0)} operations",
            f"[WARN]  System integrity compromised - {stats.get('accuracy', 0):.1f}% data loss",
            f"[FATAL] Process terminated with exit code: -1",
            f"[DEBUG] Last successful operation: {stats.get('perfect', 0)} PERFECT hits",
            f"[ERROR] Memory dump written to /var/log/beatbugging/crash.log"
        ]
        
        for msg in error_msgs:
            error_log.add_row(f"[{time.strftime('%H:%M:%S')}] {msg}")
        
        return Panel(
            error_log,
            title="[bold red]SYSTEM ERROR LOG[/bold red]",
            border_style="red",
            padding=(1, 1)
        )
    
    def create_stats_panel(self, stats: dict) -> Panel:
        stats_table = Table(show_header=False, box=None)
        stats_table.add_column("Metric", style="yellow", width=20)
        stats_table.add_column("Value", style="white", width=15)
        stats_table.add_column("Status", style="red", width=15)
        
        stats_table.add_row("Final Score", f"{stats.get('score', 0):,}", "CORRUPTED")
        stats_table.add_row("Max Combo", f"{stats.get('max_combo', 0)}", "LOST")
        stats_table.add_row("Accuracy", f"{stats.get('accuracy', 0):.1f}%", "INSUFFICIENT")
        stats_table.add_row("Perfect Hits", f"{stats.get('perfect', 0)}", "PARTIAL")
        stats_table.add_row("System Health", f"{stats.get('health', 0)}%", "CRITICAL")
        
        return Panel(
            stats_table,
            title="[bold yellow]DIAGNOSTIC REPORT[/bold yellow]",
            border_style="yellow",
            padding=(1, 1)
        )

    def display(self, stats: dict):
        self.console.clear()
        
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=11),
            Layout(name="content"),
            Layout(name="footer", size=3)
        )
        
        layout["content"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )

        ascii_art = AsciiArt.get_game_over_screen()[0]
        header_panel = Panel(
            Align.center(Text(ascii_art, style="bold red")),
            border_style="red",
            title="[bold red]CRITICAL SYSTEM FAILURE[/bold red]",
        )
        
        layout["header"].update(header_panel)
        layout["left"].update(self.create_error_log_panel(stats))
        layout["right"].update(self.create_stats_panel(stats))

        footer_text = Text("ESC to shutdown | Press q to return to the menu | ENTER to restart level", style="green")
        footer_panel = Panel(Align.center(footer_text), border_style="green")
        layout["footer"].update(footer_panel)

        self.console.print(layout, end="")

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
    
    def create_success_log_panel(self, stats: dict) -> Panel:
        success_log = Table(show_header=False, box=None, padding=0)
        success_log.add_column(style="green", width=60)
        
        success_msgs = [
            f"[INFO]  System debugging completed successfully",
            f"[SUCCESS] All {stats.get('perfect', 0)} critical errors resolved",
            f"[INFO]  Code optimization achieved {stats.get('accuracy', 0):.1f}% efficiency",
            f"[SUCCESS] Maximum processing chain: {stats.get('max_combo', 0)} operations",
            f"[INFO]  Performance score: {stats.get('score', 0):,} points",
            f"[SUCCESS] Memory optimization complete - 0 leaks detected",
            f"[INFO]  System status: OPERATIONAL"
        ]
        
        for msg in success_msgs:
            success_log.add_row(f"[{time.strftime('%H:%M:%S')}] {msg}")
        
        return Panel(
            success_log,
            title="[bold green]SUCCESS LOG[/bold green]",
            border_style="green",
            padding=(1, 1)
        )
    
    def create_achievement_panel(self, stats: dict) -> Panel:
        achievements_table = Table(show_header=False, box=None)
        achievements_table.add_column("Achievement", style="gold3", width=25)
        achievements_table.add_column("Status", style="green", width=10)
        
        if stats.get('accuracy', 0) >= 90:
            achievements_table.add_row("🏆 Code Master", "UNLOCKED")
        if stats.get('max_combo', 0) >= 50:
            achievements_table.add_row("🔥 Combo King", "UNLOCKED")
        if stats.get('perfect', 0) >= stats.get('total_actions', 1) * 0.7:
            achievements_table.add_row("⚡ Precision Expert", "UNLOCKED")
        if stats.get('score', 0) >= 10000:
            achievements_table.add_row("💎 High Scorer", "UNLOCKED")
        
        achievements_table.add_row("🎯 Bug Hunter", "UNLOCKED")
        achievements_table.add_row("🎵 Rhythm Hacker", "UNLOCKED")
        
        return Panel(
            achievements_table,
            title="[bold gold3]ACHIEVEMENTS[/bold gold3]",
            border_style="gold3",
            padding=(1, 1)
        )
    
    def get_performance_rank(self, stats: dict) -> tuple[str, str]:
        accuracy = stats.get('accuracy', 0)
        score = stats.get('score', 0)
        
        if accuracy >= 95 and score >= 20000:
            return "S+ LEGENDARY", "gold3"
        elif accuracy >= 90 and score >= 15000:
            return "S EXCELLENT", "yellow"
        elif accuracy >= 85 and score >= 10000:
            return "A GREAT", "green"
        elif accuracy >= 75 and score >= 5000:
            return "B GOOD", "blue"
        elif accuracy >= 60:
            return "C OKAY", "magenta"
        else:
            return "D NEEDS WORK", "red"
    
    def display(self, stats: dict):
        self.console.clear()
        
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=11),
            Layout(name="content"),
            Layout(name="footer", size=5)
        )
        
        layout["content"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        ascii_art = AsciiArt.get_victory_screen()[0]
        header_panel = Panel(
            Align.center(Text(ascii_art, style="bold green")),
            border_style="green",
            title="[bold green]MISSION ACCOMPLISHED[/bold green]"
        )
        
        rank, rank_color = self.get_performance_rank(stats)
        
        layout["header"].update(header_panel)
        layout["left"].update(self.create_success_log_panel(stats))
        layout["right"].update(self.create_achievement_panel(stats))
        
        footer_text = Text(
            f"PERFORMANCE RANK: {rank}\n"
            f"Final Score: {stats.get('score', 0):,} | "
            f"Accuracy: {stats.get('accuracy', 0):.1f}% | "
            f"Max Combo: {stats.get('max_combo', 0)}\n"
            "ESC to shutdown | Press q to return to the menu | ENTER to restart level",
            style=rank_color,
            justify="center"
        )
        footer_panel = Panel(footer_text, border_style=rank_color)
        layout["footer"].update(footer_panel)
        
        self.console.print(layout)

class LoadingScreen:
    def __init__(self, console: Console):
        self.console = console
        self.animation_frames = AsciiArt.get_loading_animation()
        
    def show_loading(self, message: str, duration: float = 3.0):
        start_time = time.time()
        frame_index = 0
        
        while time.time() - start_time < duration:
            frame = self.animation_frames[frame_index % len(self.animation_frames)]
            
            loading_text = Text(
                f"{frame} {message} {frame}",
                style="bold green",
                justify="center"
            )
            
            matrix_chars = " ".join(AsciiArt.get_matrix_rain()[:20])
            matrix_text = Text(matrix_chars, style="dim green")
            
            panel_content = Text("\n").join([matrix_text, loading_text, matrix_text])
            
            panel = Panel(
                Align.center(panel_content),
                border_style="green",
                title="[bold green]INITIALIZING BEATBUGGING SYSTEM[/bold green]"
            )
            
            self.console.clear()
            self.console.print(panel)
            
            time.sleep(0.1)
            frame_index += 1
