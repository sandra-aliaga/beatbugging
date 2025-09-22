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
from game.timing_system import ScoreSystem, ComboSystem, HealthSystem, HitResult
from game.opacity_timing import OpacityTimingSystem
from game.screens import GameOverAnimation, GameOverScreen, VictoryScreen, LoadingScreen
from rich.console import Console
from rich.text import Text
from rich.live import Live

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
    line: str = ""
    completada: bool = False
    tiempo_inicio_hold: Optional[float] = None

class InputHandler:
    def __init__(self):
        self.recent_presses = []
        self.running = True
        # NO modificamos el terminal - eso rompe Rich

    def update(self):
        """Simple input that doesn't break Rich - for now just return empty"""
        return []

    def get_recent_key_press(self, window_seconds=0.1):
        """Obtiene la tecla presionada más recientemente en la ventana de tiempo"""
        current_time = time.time()
        recent = [key for key, t in self.recent_presses if current_time - t <= window_seconds]
        return recent[-1] if recent else None

    def add_key_press(self, key):
        """Agregar una tecla presionada manualmente"""
        self.recent_presses.append((key, time.time()))

    def get_coordinate_from_keys(self):
        """Combina teclas presionadas para formar coordenadas como AJ, SK, etc."""
        current_time = time.time()
        recent_keys = [key for key, t in self.recent_presses if current_time - t <= 0.3]

        if len(recent_keys) >= 2:
            # Buscar columna (A,S,D,E,F) y fila (J,K,L,M,N)
            cols = [k for k in recent_keys if k in ['A', 'S', 'D', 'E', 'F']]
            rows = [k for k in recent_keys if k in ['J', 'K', 'L', 'M', 'N']]

            if cols and rows:
                return f"{cols[-1]}{rows[-1]}"

        return None

    def _restore_input(self):
        """No-op since we don't modify terminal"""
        pass

class GameEngine:
    def __init__(self):
        self.console = Console()
        self.state = GameState.MENU
        self.music_generator = LogMusicGenerator()
        self.game_map = Map(size=5)
        self.input_handler = InputHandler()  # Now safe - doesn't modify terminal
        
        # Sistemas de juego con OpacityTimingSystem real
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem(max_health=300)  
        self.opacity_timing = OpacityTimingSystem()  
        
        self.game_over_animation = GameOverAnimation(self.console)
        self.game_over_screen = GameOverScreen(self.console)
        self.victory_screen = VictoryScreen(self.console)
        self.loading_screen = LoadingScreen(self.console)
        
        self.music_data = None
        self.actions: List[GameAction] = []
        self.current_action_index = 0
        self.start_time = 0
        self.current_time = 0
        
        self.health = 200  
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        
        self.running = True
        self.music_thread = None
        self.game_thread = None
        
        # Restore pygame audio - now that we know it doesn't break the map
        try:
            pg.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=256)
            pg.mixer.init()
            self.force_stereo = False
        except Exception as e:
            self.force_stereo = False
        

        self.temp_screen = None
    
    def stop_music(self):
        """Detener toda la música y sonidos correctamente"""
        try:
            pg.mixer.stop()
            pg.mixer.music.stop()
            pg.mixer.quit()
            print("Música detenida correctamente")
        except Exception as e:
            print(f"Error al detener música: {e}")
    
    def reset_game(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.health = 200 
        self.current_time = 0.0
        self.current_action_index = 0
        self.state = GameState.PLAYING
        
        # Reiniciar sistemas con OpacityTimingSystem
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem(max_health=300)  # Increased to 300
        self.opacity_timing = OpacityTimingSystem()
        
        # Limpiar grid
        for coord in self.game_map.grid_state:
            self.game_map.set_cell_state(coord, 0)
        
        # Reiniciar barras
        self.game_map.set_progress(0)
        self.game_map.set_health(100)
        
        # Recrear acciones
        if hasattr(self, 'music_data') and self.music_data:
            gameplay_actions = self.music_data.get('gameplay_actions', [])
            self.actions = []
            for action_data in gameplay_actions:
                action = GameAction(
                    tiempo=action_data['tiempo'],
                    coordenada=action_data['coordenada'],
                    tipo=action_data['tipo'],
                    duracion=action_data['duracion'],
                    line=action_data.get('line', ''),
                    completada=False,
                    tiempo_inicio_hold=None
                )
                self.actions.append(action)
        else:
            self.actions = []
        
    def start_game(self):
        """Initialize and start the game directly"""
        self.state = GameState.PLAYING
        # Clear console for clean start
        self.console.clear()
        
        # Generate music and gameplay actions
        try:
            self.music_data = self.music_generator.generate_music(
                scale="minor", 
                rate=22050,  # Match mixer frequency
                speed=1.0
            )
            
            self.actions = [
                GameAction(
                    tiempo=action["tiempo"],
                    coordenada=action["coordenada"],
                    tipo=action["tipo"],
                    duracion=action["duracion"],
                    line=action.get("line", "")
                )
                for action in self.music_data["gameplay_actions"]
            ]
            
            # Silently generated actions - no print
            
        except Exception as e:
            # Silent error handling - create minimal data to continue
            self.actions = [
                GameAction(tiempo=2.0, coordenada='AJ', tipo='tap', duracion=0, line="DEBUG: Test log line 1"),
                GameAction(tiempo=4.0, coordenada='SK', tipo='tap', duracion=0, line="INFO: Test log line 2"),
                GameAction(tiempo=6.0, coordenada='DL', tipo='tap', duracion=0, line="ERROR: Test log line 3"),
            ]
            self.music_data = {'audio_data': None}
        
        # Reset game systems con OpacityTimingSystem
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem()
        self.opacity_timing = OpacityTimingSystem()
        self.current_action_index = 0
        
        # Sync stats
        self.health = self.health_system.current_health
        self.score = self.score_system.score
        self.combo = self.combo_system.current_combo
        
        # Start game loop (music will start after loading screen)
        self.game_loop()
    
    def start_music(self):
        def play_music():
            try:
                sound_array = self.music_data['audio_data']
                
                # Verificar que tenemos datos
                if len(sound_array) == 0:
                    self.start_time = time.time()
                    return
                
                # Garantizar que es mono 1D
                if sound_array.ndim > 1:
                    sound_array = sound_array.flatten()
                
                # Convertir a int16 si no lo es
                if sound_array.dtype != np.int16:
                    sound_array = sound_array.astype(np.int16)
                
                # Crear sonido mono SIN reshape - directo como 1D array
                # Crear sonido con pygame - convertir a estéreo si es necesario
                mixer_config = pg.mixer.get_init()
                if mixer_config and mixer_config[2] == 2 and sound_array.ndim == 1:
                    # Convertir mono a estéreo para pygame
                    sound_array = np.column_stack((sound_array, sound_array))
                
                sound = pg.sndarray.make_sound(sound_array)
                
                self.start_time = time.time()
                sound.play()
                
                while pg.mixer.get_busy() and self.running:
                    time.sleep(0.1)
                        
            except Exception as e:
                print(f"Error en audio: {e}")
                self.start_time = time.time()
        
        self.music_thread = threading.Thread(target=play_music, daemon=True)
        self.music_thread.start()
    
    def game_loop(self):
        """Complete game loop with fixed InputHandler"""
        try:
            self.loading_screen.show_loading("INITIALIZING BEATBUGGING SYSTEM", 3.0)
            self.start_music()

            # Use the configuration that works for map rendering
            with Live(self.game_map.build_layout(), screen=True, redirect_stderr=False, vertical_overflow="visible") as live:
                game_duration = max([action.tiempo for action in self.actions]) + 10.0 if self.actions else 90.0
                start_time = time.time()

                while self.state == GameState.PLAYING and self.running:
                    current_time = time.time() - start_time

                    # Process input (safe now)
                    pressed_keys = self.input_handler.update()
                    if pressed_keys:
                        coordinate = self.input_handler.get_coordinate_from_keys()
                        if coordinate:
                            self.process_user_input(coordinate, current_time)

                    self.process_actions(current_time, current_time)

                    # Check death
                    current_health = self.health_system.get_health_percentage()
                    if self.health_system.is_dead() or current_health <= 0:
                        self.state = GameState.GAME_OVER
                        break

                    # Check victory
                    if current_time >= game_duration:
                        self.state = GameState.VICTORY
                        break

                    # Update display
                    self.update_display(live)
                    time.sleep(0.1)

        except KeyboardInterrupt:
            self.console.print("\n[red]Juego interrumpido[/red]")
        except Exception as e:
            self.console.print(f"[red]Error en game loop: {e}[/red]")
        finally:
            self.stop_music()
            self.input_handler._restore_input()
    
    def run(self):
        try:
            while self.running:
                if self.state == GameState.MENU:
                    from src.menu.main_menu import run_menu
                    game_config = run_menu()
                    if game_config:
                        # Use the file and difficulty from menu
                        print(f"Starting game with: {game_config}")
                        self.reset_game()
                        self.start_game()
                        # Después de start_game(), el estado ya cambió y game_loop() se ejecutó
                        # No necesitamos hacer nada más aquí
                    else:
                        self.running = False

                elif self.state == GameState.PLAYING:
                    # Si llegamos aquí, significa que algo está mal
                    # El juego debería manejarse completamente en start_game() -> game_loop()
                    break

                elif self.state == GameState.GAME_OVER:
                    self.show_game_over()

                elif self.state == GameState.VICTORY:
                    self.show_victory()

        except KeyboardInterrupt:
            self.console.print("\n[bold red]Juego interrumpido por el usuario[/bold red]")
        finally:
            self.stop_music()
            pg.quit()
            self.console.print("[bold green]¡Gracias por jugar BeatBugging![/bold green]")

    
    def process_actions(self, current_time, elapsed_time=None):
        """ULTRA SIMPLE: Solo una nota a la vez, timing muy generoso"""
        if not self.actions:
            return

        # Limpiar mapa completamente
        for coord in self.game_map.grid_state:
            self.game_map.set_cell_state(coord, 0)

        # Buscar SOLO la próxima nota sin completar
        current_action = None
        for action in self.actions[self.current_action_index:]:
            if not action.completada:
                current_action = action
                break

        if current_action:
            timing_offset = current_time - current_action.tiempo

            # TIMING MUY GENEROSO: 3 segundos antes, 2 segundos después
            if -3.0 <= timing_offset <= 2.0:
                # Estados visuales más claros
                if timing_offset < -1.0:
                    # Muy temprano - apenas visible
                    self.game_map.set_cell_state(current_action.coordenada, 1)
                elif timing_offset < 0.5:
                    # Momento perfecto - muy visible y parpadea
                    self.game_map.set_cell_state(current_action.coordenada, 3)
                else:
                    # Tardío pero aún válido
                    self.game_map.set_cell_state(current_action.coordenada, 2)

                # Mostrar la línea del log que se está debuggeando
                if current_action.line:
                    # Truncar la línea si es muy larga para que quepa en pantalla
                    log_line = current_action.line[:60] + "..." if len(current_action.line) > 60 else current_action.line
                    self.game_map.set_actual_line(f"DEBUGGING: {log_line}")
                else:
                    self.game_map.set_actual_line(f"GET READY... {current_action.coordenada}")

                self.game_map.set_active_coords(f"HIT: {current_action.coordenada} | TIMING: {timing_offset:.1f}s")

            elif timing_offset > 2.0:
                # Miss automático después de 2 segundos
                current_action.completada = True
                self.combo_system.break_combo()
                self.health_system.take_damage(10)
                self.game_map.set_actual_line("MISSED! Get ready for next...")
        else:
            # No hay más notas
            self.game_map.set_actual_line("♪ Song complete! ♪")
            self.game_map.set_active_coords("FINAL SCORE")

        # Actualizar estadísticas
        completed = sum(1 for action in self.actions if action.completada)
        self.current_action_index = completed
        progress = int((completed / len(self.actions)) * 100) if self.actions else 100
        self.game_map.set_progress(progress)

        current_health = self.health_system.get_health_percentage()
        self.game_map.set_health(max(0, int(current_health)))

        # Sync stats
        self.health = int(self.health_system.current_health)
        self.score = self.score_system.score
        self.combo = self.combo_system.current_combo

        # Check game end conditions
        if self.health_system.is_dead() or current_health <= 0:
            self.state = GameState.GAME_OVER
            return

        # Victoria cuando todas las notas están completadas
        if completed >= len(self.actions):
            self.state = GameState.VICTORY
    
    def _opacity_to_visual_state(self, opacity: float, timing_state: str) -> int:
        """Convierte opacidad y estado de timing a estados visuales del mapa"""
        # Mapear estados de timing a números para mejor visualización
        timing_states_map = {
            "early": 1,
            "almost_early": 2, 
            "perfect": 3,
            "almost_late": 4,
            "late": 5,
            "miss": 0
        }
        
        # Si está en estado miss o opacidad muy baja, no mostrar
        if timing_state == "miss" or opacity <= 0.1:
            return 0  # INACTIVE
        
        # Usar el mapeo directo del estado de timing
        return timing_states_map.get(timing_state, 0)
    
    def process_user_input(self, coordinate: str, current_time: float):
        """Procesa el input del usuario cuando presiona teclas"""
        if not self.actions:
            return

        # Buscar acción activa en esa coordenada
        for action in self.actions:
            if action.completada or action.coordenada != coordinate:
                continue

            timing_offset = current_time - action.tiempo

            # Ventana de hit más estricta: -1s a +1s
            if -1.0 <= timing_offset <= 1.0:
                action.completada = True
                action.hit_successfully = True
                self.game_map.update_cell(action.coordenada, True)

                # Puntaje basado en precisión
                if abs(timing_offset) <= 0.5:
                    points = 300
                elif abs(timing_offset) <= 1.0:
                    points = 150
                else:
                    points = 50

                self.score_system.add_score(points)
                self.health_system.heal(5)
                self.combo_system.add_hit()
                break
            else:
                # Miss
                self.combo_system.break_combo()
                self.health_system.take_damage(15)
                break

    def update_display(self, live):
        """Actualiza el display del juego de manera simple y efectiva"""
        # Solo actualizar el layout sin reconstruirlo completamente
        live.update(self.game_map.build_layout())

    def update_game_logic_old(self):
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
                print(f"PERFECT! {action.coordenada}")
            elif result_name == "GOOD":
                print(f"GOOD! {action.coordenada}")
            elif result_name == "OKAY":
                print(f"OKAY! {action.coordenada}")
        else:
            self.combo_system.break_combo()
            self.health_system.take_damage(-hit_result.health_change)
            # Miss sin log para pantalla limpia
    
    def process_miss(self, action: GameAction, index: int):
        action.completada = True
        
        miss_result = self.score_system.evaluate_hit(1.0)
        self.combo_system.break_combo()
        self.health_system.take_damage(-miss_result.health_change)
        
    
    def show_game_over(self):
        self.stop_music()
        
        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions)
        }
        
        self.game_over_animation.show_game_over_animation()
        self.game_over_screen.display(stats)

        while True:
            try:
                user_input = input("\n> ").strip().lower()
                if user_input == "q":
                    self.state = GameState.MENU
                    return
                elif user_input == "" or user_input == "enter":
                    # reiniciar nivel
                    self.reset_game()
                    self.start_game()
                    return
                elif user_input == "esc":
                    # salir del juego
                    self.running = False
                    return
                else:
                    self.console.print("[yellow] Opción inválida. Usa Q, ENTER o ESC[/yellow]")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
    
    def show_victory(self):
        self.stop_music()  # Detener música
        
        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions),
            'time_taken': getattr(self, 'current_time', 0)
        }
        
        self.victory_screen.display(stats)
        
        print("\n")
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
        
        print(victory_art)
        
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
        
        print(stats_display)
        
        menu_options = (
            "\n╔══════════════════════════════════════════════════════════════╗\n"
            "║                    QUE QUIERES HACER?                       ║\n"
            "║                                                              ║\n"
            "║  [ENTER] ──────────── Volver al menu principal              ║\n"
            "║  [R] ──────────────── Jugar otra vez                        ║\n"
            "║  [Q] ──────────────── Salir del juego                       ║\n"
            "║                                                              ║\n"
            "╚══════════════════════════════════════════════════════════════╝"
        )
        
        print(menu_options)
        
        # Usar input() normal - SIN pygame
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
                    print("❓ Opción inválida. Usa ENTER, R o Q")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
            
def main():
    # Start with menu for proper integration
    engine = GameEngine()
    engine.state = GameState.MENU
    engine.run()

if __name__ == "__main__":
    main()
