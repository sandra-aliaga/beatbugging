import threading
import time
import pygame as pg
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import sys
import os
import queue
from pynput import keyboard

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config

from music.generator import LogMusicGenerator
from cli.map import Map
from game.timing_system import ScoreSystem, ComboSystem, HealthSystem, HitResult
from game.opacity_timing import OpacityTimingSystem
from game.screens import GameOverAnimation, GameOverScreen, VictoryAnimation, VictoryScreen, LoadingScreen
from menu.main_menu import run_menu
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
    def __init__(self, game_map):
        self.game_map = game_map
        self.running = True
        self.current_input = ""
        self.input_thread = None
        self.coordinate_ready = False
        self.last_coordinate = None
        self.input_queue = queue.Queue()
        self.last_input_time = time.time()
        self.key_events = queue.Queue()

    def start_capture(self):
        """Start global keyboard capture using pynput"""
        self.running = True
        self.game_map.set_actual_line("pynput ready! Press keys: A,S,D,E,F then J,K,L,M,N")

        # Start pynput listener
        self.listener = keyboard.Listener(on_press=self._on_key_press)
        self.listener.start()

    def stop_capture(self):
        """Stop keyboard capture"""
        self.running = False
        if hasattr(self, 'listener'):
            self.listener.stop()

    def _on_key_press(self, key):
        """Handle pynput key press events"""
        if not self.running:
            return False  # Stop listener

        try:
            # Map pynput keys to our game keys
            valid_keys = {
                'a': 'A', 's': 'S', 'd': 'D', 'e': 'E', 'f': 'F',
                'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N'
            }

            # Get the character representation
            key_char = None
            if hasattr(key, 'char') and key.char:
                key_char = key.char.lower()

            if key_char in valid_keys:
                game_key = valid_keys[key_char]
                # Show immediate feedback in debug line
                self.game_map.set_actual_line(f"pynput detected: {game_key}")
                # Handle the key press
                self._handle_key_press(game_key)

        except Exception as e:
            self.game_map.set_actual_line(f"pynput error: {str(e)}")

        return True  # Continue listening

    def _handle_key_press(self, key):
        """Handle a key press and build coordinate"""
        # ALWAYS update debug line to show we detected a key
        self.game_map.set_actual_line(f"Key detected: {key} | Current input: '{self.current_input}'")

        if len(self.current_input) == 0:
            # First character - should be A,S,D,E,F
            if key in ['A', 'S', 'D', 'E', 'F']:
                self.current_input = key
                self.game_map.set_input(self.current_input)
                # Debug: update debug line to show key press
                self.game_map.set_actual_line(f"First key: {key} | Need row key (J,K,L,M,N)")
        elif len(self.current_input) == 1:
            # Second character - should be J,K,L,M,N
            if key in ['J', 'K', 'L', 'M', 'N']:
                self.current_input += key
                self.game_map.set_input(self.current_input)
                # Coordinate is ready
                self.coordinate_ready = True
                self.last_coordinate = self.current_input
                # Debug: show coordinate completed
                self.game_map.set_actual_line(f"Coordinate complete: {self.current_input} - submitting!")
                # Clear input after a short delay
                threading.Timer(0.5, self._clear_input).start()
            else:
                # Wrong second key
                self.game_map.set_actual_line(f"Wrong key {key}! Need J,K,L,M,N after {self.current_input}")
        else:
            # Input too long, reset
            self.current_input = ""
            self.game_map.set_input(self.current_input)
            self.game_map.set_actual_line(f"Input reset. Key {key} - start with A,S,D,E,F")

    def _clear_input(self):
        """Clear the input after coordinate is submitted"""
        self.current_input = ""
        self.game_map.set_input(self.current_input)
        self.coordinate_ready = False

    def _skip_current_note(self):
        """Skip current note for debugging purposes"""
        self.game_map.set_actual_line("ESC pressed - skipping current note (debug feature)")

    def get_coordinate_if_ready(self):
        """Get coordinate if one is ready, then mark as consumed"""
        if self.coordinate_ready and self.last_coordinate:
            coord = self.last_coordinate
            self.coordinate_ready = False
            return coord
        return None

    def update(self):
        """Update method for compatibility - now just returns coordinate if ready"""
        coord = self.get_coordinate_if_ready()
        return [coord] if coord else []

    def get_coordinate_from_keys(self):
        """Get coordinate if ready - for compatibility"""
        return self.get_coordinate_if_ready()

    def _restore_input(self):
        """Stop capture when game ends"""
        self.stop_capture()

class GameEngine:
    def __init__(self):
        self.console = Console()
        self.state = GameState.MENU
        self.music_generator = LogMusicGenerator()
        self.game_map = Map(size=Config.GRID_SIZE)
        self.input_handler = InputHandler(self.game_map)  # Pass game_map reference
        
        # Sistemas de juego con OpacityTimingSystem real
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem(max_health=300)  
        self.opacity_timing = OpacityTimingSystem()  
        
        self.game_over_animation = GameOverAnimation(self.console)
        self.game_over_screen = GameOverScreen(self.console)
        self.victory_animation = VictoryAnimation(self.console)
        self.victory_screen = VictoryScreen(self.console)
        self.loading_screen = LoadingScreen(self.console)
        
        self.music_data = None
        self.actions: List[GameAction] = []
        self.current_action_index = 0
        self.start_time = 0
        self.current_time = 0
        
        self.running = True
        self.music_thread = None
        self.game_thread = None
        self.selected_log_file = None  # Archivo seleccionado del menú
        self.selected_difficulty = "user"  # Dificultad seleccionada del menú
        
        # Restore pygame audio - now that we know it doesn't break the map
        try:
            pg.mixer.pre_init(
                frequency=Config.AUDIO_SAMPLE_RATE,
                size=-Config.AUDIO_BIT_DEPTH,
                channels=Config.AUDIO_CHANNELS,
                buffer=Config.AUDIO_BUFFER_SIZE
            )
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
            # NO hacer quit() aquí para que el audio se pueda reiniciar
            print("Music stopped cleanly")
        except Exception as e:
            print(f"Error stopping music: {e}")

    def reinit_audio(self):
        """Reinicializar el sistema de audio si es necesario"""
        try:
            if not pg.mixer.get_init():
                pg.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=256)
                pg.mixer.init()
                print("Audio reinitialized")
        except Exception as e:
            print(f"Error reinitializing audio: {e}")

    def reset_game(self):
        self.current_time = 0.0
        self.current_action_index = 0
        self.state = GameState.PLAYING
        
        # Reinicializar audio si es necesario
        self.reinit_audio()
        
        # Reiniciar sistemas con OpacityTimingSystem
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem(max_health=Config.MAX_HEALTH)
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
        """Initialize and start the game with the selected log file"""
        self.state = GameState.PLAYING
        # Clear console for clean start
        self.console.clear()
        
        # Initialize music generator with the selected file
        if self.selected_log_file:
            self.music_generator = LogMusicGenerator(log_path=self.selected_log_file)
        else:
            self.music_generator = LogMusicGenerator()
        
        # Generate music and gameplay actions with difficulty-based speed
        try:
            # Set speed based on difficulty
            if self.selected_difficulty == "root":
                game_speed = 1.8
            else:  # user mode
                game_speed = 1.4

            self.music_data = self.music_generator.generate_music(
                scale=Config.DEFAULT_SCALE,
                rate=Config.AUDIO_SAMPLE_RATE,
                speed=game_speed
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
                self.start_time = time.time()
        
        self.music_thread = threading.Thread(target=play_music, daemon=True)
        self.music_thread.start()
    
    def game_loop(self):
        """Complete game loop with fixed InputHandler"""
        try:
            self.loading_screen.show_loading("INITIALIZING BEATBUGGING SYSTEM", 3.0)
            self.start_music()

            # Start keyboard capture
            self.input_handler.start_capture()

            # Show difficulty mode info
            mode_text = "ROOT MODE (Speed: 1.8x)" if self.selected_difficulty == "root" else "USER MODE (Speed: 1.4x)"
            self.game_map.set_actual_line(f"Starting {mode_text}")

            # Use the configuration that works for map rendering
            with Live(self.game_map.build_layout(), screen=True, redirect_stderr=False) as live:
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
            self.console.print("\n[red]Game interrupted[/red]")
        except Exception as e:
            self.console.print(f"[red]Error in game loop: {e}[/red]")
        finally:
            self.stop_music()
            self.input_handler._restore_input()
    
    def run(self):
        try:
            while self.running:
                if self.state == GameState.MENU:
                    game_config = run_menu()
                    if game_config:
                        # Guardar el archivo y dificultad seleccionados
                        self.selected_log_file = game_config.get('file')
                        self.selected_difficulty = game_config.get('difficulty', 'user')

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
            self.console.print("\n[bold red]Game interrupted by user[/bold red]")
        finally:
            self.stop_music()
            pg.mixer.quit()  # Cerrar completamente el audio al salir
            pg.quit()
            self.console.print("[bold green]¡THANKS for BeatBugging![/bold green]")

    
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

            # Update target coordinate in Line panel
            self.game_map.set_target_coordinate(current_action.coordenada)

            # Timing window usando configuración - MUCHO más tiempo visible
            timing_window = Config.OKAY_WINDOW * 8  # 8 segundos para ver la nota venir
            if -timing_window <= timing_offset <= timing_window * 0.67:
                # Estados visuales más claros
                if timing_offset < -timing_window * 0.33:
                    # Muy temprano - apenas visible
                    self.game_map.set_cell_state(current_action.coordenada, 1)
                elif timing_offset < timing_window * 0.17:
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

            elif timing_offset > timing_window * 0.67:
                # Miss automático después del timing window - COMO ANTES
                current_action.completada = True
                current_action.missed = True
                self.combo_system.break_combo()
                self.health_system.take_damage(abs(Config.HEALTH_CHANGES["MISS"]))
                self.game_map.set_cell_state(current_action.coordenada, 5)  # Red for miss
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

        # Debug: show game stats
        total_actions = len(self.actions)
        if total_actions == 0:
            self.game_map.set_active_coords("ERROR: No actions loaded! Check log file.")
        else:
            self.game_map.set_active_coords(f"Actions: {completed}/{total_actions} | Health: {current_health:.0f}%")

        # Check game end conditions
        if self.health_system.is_dead() or current_health <= 0:
            self.state = GameState.GAME_OVER
            return

        # Victoria cuando todas las notas están completadas - ONLY if we have actions
        if total_actions > 0 and completed >= total_actions:
            self.state = GameState.VICTORY
    
    def _opacity_to_visual_state(self, opacity: float, timing_state: str) -> int:
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

            # Ventana de hit usando configuración
            if -Config.OKAY_WINDOW <= timing_offset <= Config.OKAY_WINDOW:
                action.completada = True
                action.hit_successfully = True

                # Visual feedback - make cell flash green for HIT
                self.game_map.set_cell_state(action.coordenada, 3)
                # Reset visual feedback after 1 second
                threading.Timer(1.0, lambda: self.game_map.set_cell_state(action.coordenada, 0)).start()
                # Mark that user attempted this action
                action.user_attempted = True

                # Puntaje basado en precisión usando configuración
                if abs(timing_offset) <= Config.PERFECT_WINDOW:
                    points = Config.BASE_POINTS["PERFECT"]
                    self.game_map.set_active_coords(f"PERFECT! +{points} pts")
                elif abs(timing_offset) <= Config.GOOD_WINDOW:
                    points = Config.BASE_POINTS["GOOD"]
                    self.game_map.set_active_coords(f"GOOD! +{points} pts")
                else:
                    points = Config.BASE_POINTS["OKAY"]
                    self.game_map.set_active_coords(f"OKAY! +{points} pts")

                self.score_system.add_score(points)
                # Determinar healing basado en precisión
                if abs(timing_offset) <= Config.PERFECT_WINDOW:
                    heal_amount = Config.HEALTH_CHANGES["PERFECT"]
                elif abs(timing_offset) <= Config.GOOD_WINDOW:
                    heal_amount = Config.HEALTH_CHANGES["GOOD"]
                else:
                    heal_amount = Config.HEALTH_CHANGES["OKAY"]

                self.health_system.heal(heal_amount)
                self.combo_system.add_hit()
                break
            else:
                # Miss - visual feedback
                self.game_map.set_cell_state(action.coordenada, 5)  # Show miss state (red)
                # Reset visual feedback after 1.5 seconds
                threading.Timer(1.5, lambda: self.game_map.set_cell_state(action.coordenada, 0)).start()
                self.game_map.set_active_coords(f"MISS! Wrong timing for {action.coordenada}")
                action.user_attempted = True  # Mark as attempted
                action.completada = True  # Complete with miss
                action.missed = True
                self.combo_system.break_combo()
                self.health_system.take_damage(abs(Config.HEALTH_CHANGES["MISS"]))
                break

        # If coordinate doesn't match any active action
        if coordinate and not any(action.coordenada == coordinate and not action.completada for action in self.actions):
            self.game_map.set_active_coords(f"MISS! Wrong coordinate: {coordinate}")
            self.combo_system.break_combo()
            self.health_system.take_damage(abs(Config.HEALTH_CHANGES["MISS"]))

    def update_display(self, live):
        live.update(self.game_map.build_layout())

    def update_game_logic_old(self):
        current_coord = self.input_handler.get_current_coordinate()
        
        # Verificar acciones como era antes
        for i in range(self.current_action_index, min(self.current_action_index + 5, len(self.actions))):
            action = self.actions[i]
            timing_offset = self.current_time - action.tiempo
            
            # Ventana de tiempo usando configuración
            if not action.completada and abs(timing_offset) <= Config.OKAY_WINDOW:
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
                
            elif timing_offset > Config.OKAY_WINDOW and not action.completada:
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
                    self.console.print("[yellow] Invalid option. Use Q, ENTER or ESC[/yellow]")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
    
    def show_victory(self):
        self.stop_music()
        
        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions),
            'time_taken': getattr(self, 'current_time', 0)
        }
        
        self.victory_animation.show_victory_animation()
        
        os.system("cls" if os.name == "nt" else "clear")
        
        self.victory_screen.display(stats)
        
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
                    print("Invalid option. Use ENTER, R or Q")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
            
def main():
    engine = GameEngine()
    engine.state = GameState.MENU
    engine.run()

if __name__ == "__main__":
    main()
