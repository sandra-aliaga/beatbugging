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

        footer_text = Text("[↵] Restart   [M] Back to menu   [Q] Quit", style="green")
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
            "[↵] Restart   [M] Back to menu   [Q] Quit",
            style=rank_color,
            justify="center"
        )
        footer_panel = Panel(footer_text, border_style=rank_color)
        layout["footer"].update(footer_panel)
        
        self.console.print(layout)


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