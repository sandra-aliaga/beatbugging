import threading
import time
import pygame as pg
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from music.generator import LogMusicGenerator
from cli.map import Map
from game.timing_system import ScoreSystem, AdvancedTimingSystem, ComboSystem, HealthSystem, DifficultyManager, HitResult
from game.screens import GameOverScreen, VictoryScreen, LoadingScreen
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    PAUSED = "paused"

@dataclass
class GameAction:
    tiempo: float
    coordenada: str
    tipo: str
    duracion: float
    completada: bool = False
    tiempo_inicio_hold: Optional[float] = None

class InputHandler:
    def __init__(self):
        self.pressed_keys = set()
        self.key_mapping = {
            'a': 'A', 's': 'S', 'd': 'D', 'e': 'E', 'f': 'F',
            'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N'
        }
        self.current_combination = set()
        self.last_input = ""
        
    def update(self):
        # En el juego real, esto será reemplazado por input en tiempo real
        pass
    
    def on_key_press(self, letter):
        pass
    
    def on_key_release(self, letter):
        pass
    
    def get_current_coordinate(self):
        # Para demo, simularemos inputs aleatorios
        return None
    
    def process_input(self, input_str):
        """Procesa input del usuario para determinar coordenada"""
        input_str = input_str.lower().strip()
        if len(input_str) == 2:
            col = input_str[0].upper()
            row = input_str[1].upper()
            if col in ['A', 'S', 'D', 'E', 'F'] and row in ['J', 'K', 'L', 'M', 'N']:
                return f"{col}{row}"
        return None

class GameEngine:
    def __init__(self):
        self.console = Console()
        self.state = GameState.MENU
        self.music_generator = LogMusicGenerator()
        self.game_map = Map(size=5)
        self.input_handler = InputHandler()
        
        # Sistemas de juego con velocidad NORMAL (como era antes)
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.timing_system = AdvancedTimingSystem(bpm=120.0)  # BPM normal
        self.health_system = HealthSystem()
        self.difficulty_manager = DifficultyManager()
        
        # Pantallas como estaban antes
        self.game_over_screen = GameOverScreen(self.console)
        self.victory_screen = VictoryScreen(self.console)
        self.loading_screen = LoadingScreen(self.console)
        
        self.music_data = None
        self.actions: List[GameAction] = []
        self.current_action_index = 0
        self.start_time = 0
        self.current_time = 0
        
        # Variables como estaban antes
        self.health = 100
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        
        self.running = True
        self.music_thread = None
        self.game_thread = None
        
        pg.init()
        # Configuración mono como era antes
        pg.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
        pg.mixer.init()
        
        # Verificar si el sistema forzó estéreo
        mixer_config = pg.mixer.get_init()
        self.force_stereo = mixer_config and mixer_config[2] == 2
        if self.force_stereo:
            print("⚠️ Sistema forzó configuración estéreo, se adaptará el audio mono automáticamente")
    
    def stop_music(self):
        """Detener toda la música y sonidos"""
        try:
            pg.mixer.stop()
            pg.mixer.music.stop()
        except:
            pass
    
    def reset_game(self):
        """Reiniciar todos los valores del juego para una nueva partida"""
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.health = 100
        self.current_time = 0.0
        self.current_action_index = 0
        
        # Reiniciar sistemas
        self.score_system = ScoreSystem()
        self.timing_system = AdvancedTimingSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem()
        self.difficulty_manager = DifficultyManager()
        
        # Limpiar grid
        for coord in self.game_map.grid_state:
            self.game_map.update_cell(coord, False)
        
        # Reiniciar barras
        self.game_map.set_progress(0)
        self.game_map.set_health(100)
        
        # Regenerar acciones usando el método correcto
        if hasattr(self, 'music_generator'):
            # Generar nueva música y acciones
            sound_array, sample_rate = self.music_generator.generate_music()
            self.actions = self.music_generator.generate_game_actions(sound_array, sample_rate)
            for action in self.actions:
                action.completada = False
                action.tiempo_inicio_hold = None
        else:
            # Si no hay generador, crear acciones de prueba
            self.actions = []
        
    def start_menu(self):
        # Iniciar directamente el juego sin menú interno
        self.console.print("[bold green]Iniciando BeatBugging...[/bold green]")
        self.start_game()
    
    def start_game(self):
        self.state = GameState.PLAYING
        self.console.clear()
        
        # Mostrar pantalla de carga
        self.loading_screen.show_loading("Parsing error logs and generating music...", 2.0)
        
        # Aplicar configuración de dificultad
        self.difficulty_manager.apply_to_score_system(self.score_system)
        self.difficulty_manager.apply_to_health_system(self.health_system)
        
        # Generar música con velocidad NORMAL (como era antes)
        self.music_data = self.music_generator.generate_music(
            scale="minor", 
            rate=44100, 
            speed=1.0  # Velocidad normal como era antes
        )
        
        self.actions = [
            GameAction(
                tiempo=action["tiempo"],
                coordenada=action["coordenada"],
                tipo=action["tipo"],
                duracion=action["duracion"]
            )
            for action in self.music_data["gameplay_actions"]
        ]
        
        self.loading_screen.show_loading("Initializing debugging environment...", 1.0)
        
        # Reset de sistemas como era antes
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.timing_system = AdvancedTimingSystem(bpm=120.0)  # BPM normal
        self.difficulty_manager.apply_to_score_system(self.score_system)
        self.difficulty_manager.apply_to_health_system(self.health_system)
        
        self.current_action_index = 0
        
        # Sync variables
        self.health = self.health_system.current_health
        self.score = self.score_system.score
        self.combo = self.combo_system.current_combo
        
        self.start_music()
        self.game_loop()
    
    def start_music(self):
        def play_music():
            try:
                sound_array = self.music_data['audio_data']
                
                # Debug info
                print(f"Audio shape: {sound_array.shape}, dtype: {sound_array.dtype}")
                print(f"Pygame mixer config: {pg.mixer.get_init()}")
                
                # Asegurar que el audio es mono y del tipo correcto
                if sound_array.ndim > 1:
                    sound_array = sound_array[:, 0]
                    print("Convertido de 2D a 1D (mono)")
                
                # Asegurar que es int16 para pygame
                if sound_array.dtype != np.int16:
                    if sound_array.dtype == np.float64 or sound_array.dtype == np.float32:
                        sound_array = sound_array * 32767
                    sound_array = sound_array.astype(np.int16)
                    print(f"Convertido a int16, nuevo shape: {sound_array.shape}")
                
                # Si el sistema forzó estéreo, convertir mono a estéreo
                if self.force_stereo:
                    sound_array = np.column_stack((sound_array, sound_array))
                    print(f"Audio convertido a estéreo - Shape: {sound_array.shape}")
                
                # Verificar que el mixer esté inicializado
                if not pg.mixer.get_init():
                    print("⚠️ Reinicializando mixer de pygame...")
                    pg.mixer.quit()
                    pg.mixer.init(frequency=44100, size=-16, channels=2)
                
                # Crear sonido con pygame
                sound = pg.sndarray.make_sound(sound_array)
                sound.play()
                print("Audio reproduciendose...")
                
                while pg.mixer.get_busy():
                    time.sleep(0.1)
                    
                print("Reproduccion completada")
                self.state = GameState.PLAYING
                print("Iniciando juego!")
                
            except Exception as e:
                print(f"❌ Error reproduciendo música: {e}")
                import traceback
                traceback.print_exc()
                # Continuar sin música
                self.state = GameState.PLAYING
        
        self.music_thread = threading.Thread(target=play_music, daemon=True)
        self.music_thread.start()
        self.timing_system.start()
    
    def game_loop(self):
        with Live(self.game_map.build_layout(), screen=True, redirect_stderr=False) as live:
            while self.state == GameState.PLAYING and self.running:
                self.current_time = self.timing_system.get_current_time()
                
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.state = GameState.MENU
                            return
                        elif event.key == pg.K_SPACE:
                            if self.timing_system.is_paused:
                                self.timing_system.resume()
                            else:
                                self.timing_system.pause()
                    elif event.type == pg.QUIT:
                        self.running = False
                        return
                
                self.input_handler.update()
                self.update_game_logic()
                self.update_display(live)
                
                # Sync variables
                self.health = self.health_system.current_health
                self.score = self.score_system.score
                self.combo = self.combo_system.current_combo
                self.max_combo = self.combo_system.max_combo
                
                if self.health_system.is_dead():
                    self.state = GameState.GAME_OVER
                    break  # Salir del game loop para mostrar game over
                
                if self.current_action_index >= len(self.actions):
                    self.state = GameState.VICTORY
                    break  # Salir del game loop para mostrar victory
                
                # Frame rate NORMAL como era antes
                time.sleep(0.016)  # ~60fps normal
    
    def update_game_logic(self):
        current_coord = self.input_handler.get_current_coordinate()
        
        # Verificar acciones como era antes
        for i in range(self.current_action_index, min(self.current_action_index + 5, len(self.actions))):
            action = self.actions[i]
            timing_offset = self.current_time - action.tiempo
            
            # Ventana de tiempo NORMAL como era antes
            if not action.completada and abs(timing_offset) <= 0.5:
                if current_coord == action.coordenada:
                    if action.tipo == "tap":
                        self.process_hit(action, i, timing_offset)
                    elif action.tipo == "hold":
                        if action.tiempo_inicio_hold is None:
                            action.tiempo_inicio_hold = self.current_time
                        
                        hold_duration = self.current_time - action.tiempo_inicio_hold
                        if hold_duration >= action.duracion:
                            self.process_hit(action, i, timing_offset)
                        
                        self.game_map.update_cell(action.coordenada, True)
                
            elif timing_offset > 0.5 and not action.completada:
                self.process_miss(action, i)
        
        while (self.current_action_index < len(self.actions) and 
               self.actions[self.current_action_index].completada):
            self.current_action_index += 1
    
    def process_hit(self, action: GameAction, index: int, timing_offset: float):
        action.completada = True
        self.game_map.update_cell(action.coordenada, True)
        
        hit_result = self.score_system.evaluate_hit(timing_offset)
        
        if hit_result.result != HitResult.MISS:
            self.combo_system.add_hit()
            self.health_system.heal(hit_result.health_change)
            result_name = hit_result.result.name
            if result_name == "PERFECT":
                print(f"✨ PERFECT! {action.coordenada}")
            elif result_name == "GOOD":
                print(f"GOOD! {action.coordenada}")
            elif result_name == "OKAY":
                print(f"👍 OKAY! {action.coordenada}")
        else:
            self.combo_system.break_combo()
            self.health_system.take_damage(-hit_result.health_change)
            print(f"❌ MISS! {action.coordenada}")
    
    def process_miss(self, action: GameAction, index: int):
        action.completada = True
        
        miss_result = self.score_system.evaluate_hit(1.0)
        self.combo_system.break_combo()
        self.health_system.take_damage(-miss_result.health_change)
        
        print(f"❌ MISS! Perdiste {action.coordenada}")
    
    def update_display(self, live):
        # Limpiar celdas
        for action in self.game_map.grid_state:
            self.game_map.update_cell(action, False)
        
        # Mostrar próximas acciones como era antes
        for i in range(self.current_action_index, min(self.current_action_index + 3, len(self.actions))):
            action = self.actions[i]
            if not action.completada:
                # Iluminar las casillas como era antes
                if (self.current_time >= action.tiempo - 0.5 and 
                    self.current_time <= action.tiempo + 0.5):
                    self.game_map.update_cell(action.coordenada, True)
        
        # Actualizar barras
        progress = min(100, int((self.current_action_index / len(self.actions)) * 100))
        self.game_map.set_progress(progress)
        self.game_map.set_health(self.health_system.get_health_percentage())
        
        # Mostrar próximas coordenadas
        next_actions = []
        for i in range(self.current_action_index, min(self.current_action_index + 3, len(self.actions))):
            action = self.actions[i]
            if not action.completada:
                next_actions.append(f"{action.coordenada}({action.tipo})")
        
        coord_text = " - ".join(next_actions) if next_actions else "¡Sistema limpio!"
        self.game_map.set_active_coords(coord_text)
        
        # Status como era antes
        combo_rank = self.combo_system.get_combo_rank()
        status_text = (f"Score: {self.score:,} | "
                      f"Combo: {self.combo} ({combo_rank}) | "
                      f"Accuracy: {self.score_system.get_accuracy():.1f}% | "
                      f"Time: {self.current_time:.1f}s")
        
        live.update(self.game_map.build_layout(status_text))
    
    def show_game_over(self):
        self.stop_music()  # Detener música
        
        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions)
        }
        
        self.game_over_screen.display(stats)
        
        # Mostrar opciones con arte ASCII bonito
        self.console.print("\n")
        game_over_art = (
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║                                                              ║\n"
            "║   ██████   █████  ███    ███ ███████      ██████  ██    ██  ║\n"
            "║  ██       ██   ██ ████  ████ ██          ██    ██ ██    ██  ║\n"
            "║  ██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██  ║\n"
            "║  ██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██   ║\n"
            "║   ██████  ██   ██ ██      ██ ███████      ██████    ████    ║\n"
            "║                                                              ║\n"
            "║  ██    ██ ███████ ██████      ███████ ███    ██ ██████       ║\n"
            "║  ██    ██ ██      ██   ██     ██      ████   ██ ██   ██      ║\n"
            "║  ██    ██ █████   ██████      █████   ██ ██  ██ ██   ██      ║\n"
            "║   ██  ██  ██      ██   ██     ██      ██  ██ ██ ██   ██      ║\n"
            "║    ████   ███████ ██   ██     ███████ ██   ████ ██████       ║\n"
            "║                                                              ║\n"
            "╚══════════════════════════════════════════════════════════════╝"
        )
        
        self.console.print(Text(game_over_art, style="bold red"))
        
        # Menu de opciones con estilo ASCII
        menu_options = (
            "\n╔══════════════════════════════════════════════════════════════╗\n"
            "║                    QUE QUIERES HACER?                       ║\n"
            "║                                                              ║\n"
            "║  [1] ENTER ──────────── Volver al menu principal            ║\n"
            "║  [2] R ──────────────── Jugar otra vez                      ║\n"
            "║  [3] Q ──────────────── Salir del juego                     ║\n"
            "║                                                              ║\n"
            "╚══════════════════════════════════════════════════════════════╝"
        )
        
        self.console.print(Text(menu_options, style="bold green"))
        
        while True:
            try:
                user_input = input("\n> ").strip().lower()
                if user_input == "" or user_input == "1":
                    self.state = GameState.MENU
                    return
                elif user_input == "r" or user_input == "2":
                    # Reiniciar el juego
                    self.reset_game()
                    self.start_game()
                    return
                elif user_input == "q" or user_input == "3":
                    self.running = False
                    return
                else:
                    self.console.print("[yellow]❓ Opción inválida. Usa ENTER, R o Q[/yellow]")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
    
    def show_victory(self):
        self.stop_music()  # Detener música
        
        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions),
            'time_taken': self.current_time
        }
        
        self.victory_screen.display(stats)
        
        # Mostrar opciones con arte ASCII bonito
        self.console.print("\n")
        victory_art = (
            "╔══════════════════════════════════════════════════════════════╗\n"
            "║                                                              ║\n"
            "║ ██    ██ ██  ██████ ████████  ██████  ██████  ██  █████     ║\n"
            "║ ██    ██ ██ ██         ██    ██    ██ ██   ██ ██ ██   ██    ║\n"
            "║ ██    ██ ██ ██         ██    ██    ██ ██████  ██ ███████    ║\n"
            "║  ██  ██  ██ ██         ██    ██    ██ ██   ██ ██ ██   ██    ║\n"
            "║   ████   ██  ██████    ██     ██████  ██   ██ ██ ██   ██    ║\n"
            "║                                                              ║\n"
            "║           ███████ ██   ██  ██████ ███████ ██                 ║\n"
            "║           ██      ██   ██ ██      ██      ██                 ║\n"
            "║           █████    ██ ██  ██      █████   ██                 ║\n"
            "║           ██        ███   ██      ██                         ║\n"
            "║           ███████   ██     ██████ ███████ ██                 ║\n"
            "║                                                              ║\n"
            "╚══════════════════════════════════════════════════════════════╝"
        )
        
        self.console.print(Text(victory_art, style="bold green"))
        
        # Estadisticas con estilo ASCII
        stats_display = (
            f"\n╔══════════════════════════════════════════════════════════════╗\n"
            f"║                     ESTADISTICAS FINALES                    ║\n"
            f"║                                                              ║\n"
            f"║  Puntuacion Final: {stats.get('score', 0):,}                              ║\n"
            f"║  Precision: {stats.get('accuracy', 0):.1f}%                                       ║\n"
            f"║  Combo Maximo: {stats.get('max_combo', 0)}                                    ║\n"
            f"║                                                              ║\n"
            f"╚══════════════════════════════════════════════════════════════╝"
        )
        
        self.console.print(Text(stats_display, style="bold yellow"))
        
        # Menu de opciones con estilo ASCII
        menu_options = (
            "\n╔══════════════════════════════════════════════════════════════╗\n"
            "║                    QUE QUIERES HACER?                       ║\n"
            "║                                                              ║\n"
            "║  [1] ENTER ──────────── Volver al menu principal            ║\n"
            "║  [2] R ──────────────── Jugar otra vez                      ║\n"
            "║  [3] Q ──────────────── Salir del juego                     ║\n"
            "║                                                              ║\n"
            "╚══════════════════════════════════════════════════════════════╝"
        )
        
        self.console.print(Text(menu_options, style="bold green"))
        
        while True:
            try:
                user_input = input("\n> ").strip().lower()
                if user_input == "" or user_input == "1":
                    self.state = GameState.MENU
                    return
                elif user_input == "r" or user_input == "2":
                    # Reiniciar el juego
                    self.reset_game()
                    self.start_game()
                    return
                elif user_input == "q" or user_input == "3":
                    self.running = False
                    return
                else:
                    self.console.print("[yellow]❓ Opción inválida. Usa ENTER, R o Q[/yellow]")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
    
    def run(self):
        try:
            while self.running:
                if self.state == GameState.MENU:
                    self.start_menu()
                elif self.state == GameState.GAME_OVER:
                    self.show_game_over()
                elif self.state == GameState.VICTORY:
                    self.show_victory()
                else:
                    time.sleep(0.1)
        
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Juego interrumpido por el usuario[/bold red]")
        finally:
            self.stop_music()  # Asegurar que se detenga la música
            pg.quit()
            self.console.print("[bold green]¡Gracias por jugar BeatBugging![/bold green]")

def main():
    engine = GameEngine()
    engine.run()

if __name__ == "__main__":
    main()
