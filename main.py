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
        self._input_lock = threading.Lock()
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
                # Key detected - no output needed for clean gameplay
                # Handle the key press
                self._handle_key_press(game_key)

        except Exception as e:
            pass  # Silent error handling for clean gameplay

        return True  # Continue listening

    def _handle_key_press(self, key):
        """Handle a key press and build coordinate"""
        with self._input_lock:
            if len(self.current_input) == 0:
                # First character - should be A,S,D,E,F
                if key in ['A', 'S', 'D', 'E', 'F']:
                    self.current_input = key
                    self.game_map.set_input(self.current_input)
            elif len(self.current_input) == 1:
                # Second character - should be J,K,L,M,N
                if key in ['J', 'K', 'L', 'M', 'N']:
                    self.current_input += key
                    self.game_map.set_input(self.current_input)

                    # COORDINATE COMPLETE! Check immediately!
                    self.coordinate_ready = True
                    self.last_coordinate = self.current_input

                    # LLAMAR DIRECTAMENTE A LA GAME ENGINE
                    if hasattr(self, 'game_engine') and self.game_engine:
                        current_time = time.time() - self.game_engine.start_time if hasattr(self.game_engine, 'start_time') else 0
                        self.game_engine.process_user_input(self.current_input, current_time)

                    # Clear input after delay
                    threading.Timer(1.0, self._clear_input).start()
                else:
                    # Wrong second key - reset
                    self.current_input = ""
                    self.game_map.set_input(self.current_input)
            else:
                # Input too long, reset
                self.current_input = ""
                self.game_map.set_input(self.current_input)

    def _clear_input(self):
        """Clear the input after coordinate is submitted"""
        with self._input_lock:
            self.current_input = ""
            self.game_map.set_input(self.current_input)
            self.coordinate_ready = False

    def _skip_current_note(self):
        """Skip current note for debugging purposes"""
        self.game_map.set_actual_line("ESC pressed - skipping current note (debug feature)")

    def get_coordinate_if_ready(self):
        """Get coordinate if one is ready, then mark as consumed"""
        with self._input_lock:
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
            pass
        except Exception as e:
            pass

    def reinit_audio(self):
        """Reinicializar el sistema de audio si es necesario"""
        try:
            if not pg.mixer.get_init():
                pg.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=256)
                pg.mixer.init()
                pass
        except Exception as e:
            pass

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
        
        # Reiniciar barras y contador
        self.game_map.set_progress(0)
        self.game_map.set_health(100)
        self.game_map.reset_success()
        
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
            # Set speed based on difficulty - reduced by 0.2 each
            if self.selected_difficulty == "root":
                game_speed = 1.6  # was 1.8
            else:  # user mode
                game_speed = 1.2  # was 1.4

            self.music_data = self.music_generator.generate_music(
                scale=Config.DEFAULT_SCALE,
                rate=Config.AUDIO_SAMPLE_RATE,
                speed=game_speed
            )
            
            # Crear acciones con timing ajustado a la velocidad de música
            raw_actions = []
            for action in self.music_data["gameplay_actions"]:
                # AJUSTAR EL TIMING a la velocidad de la música
                original_time = action["tiempo"]
                adjusted_time = original_time / game_speed  # Dividir por velocidad!


                raw_actions.append(GameAction(
                    tiempo=adjusted_time,
                    coordenada=action["coordenada"],
                    tipo=action["tipo"],
                    duracion=action["duracion"],
                    line=action.get("line", "")
                ))

            # Espaciar las notas si están muy juntas
            self.actions = self._space_out_actions(raw_actions)
            
            
        except Exception as e:
            # Silent error handling - create minimal data to continue
            self.actions = [
                GameAction(tiempo=2.0, coordenada='AJ', tipo='tap', duracion=0, line="Sample log entry 1"),
                GameAction(tiempo=4.0, coordenada='SK', tipo='tap', duracion=0, line="Sample log entry 2"),
                GameAction(tiempo=6.0, coordenada='DL', tipo='tap', duracion=0, line="Sample log entry 3"),
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

                # NO cambiar start_time aquí - ya está establecido
                pass
                sound.play()
                
                while pg.mixer.get_busy() and self.running:
                    time.sleep(0.1)
                        
            except Exception as e:
                # NO cambiar start_time en caso de error tampoco
                pass
        
        self.music_thread = threading.Thread(target=play_music, daemon=True)
        self.music_thread.start()
    
    def game_loop(self):
        """Complete game loop with fixed InputHandler"""
        try:
            # Longer loading for large files
            loading_time = 6.0 if len(self.actions) > 50 else 3.0
            self.loading_screen.show_loading("INITIALIZING BEATBUGGING SYSTEM", loading_time)

            # NO EMPEZAR MÚSICA TODAVÍA - esperar el momento exacto
            # SINCRONIZACIÓN REAL: Empezar música Y timer al mismo tiempo
            self.start_time = time.time()  # Tiempo de referencia
            self.start_music()  # Empezar música AHORA

            # Start keyboard capture - CONNECT TO GAME ENGINE
            self.input_handler.game_engine = self  # Connect!
            self.input_handler.start_capture()

            # Show difficulty mode info
            mode_text = "ROOT MODE (Speed: 1.6x)" if self.selected_difficulty == "root" else "USER MODE (Speed: 1.2x)"
            self.game_map.set_actual_line(f"♪ {mode_text} - Music synced!")
            pass

            # Use the configuration that works for map rendering
            with Live(self.game_map.build_layout(), screen=True, redirect_stderr=False) as live:
                game_duration = max([action.tiempo for action in self.actions]) + 10.0 if self.actions else 90.0
                start_time = time.time()

                while self.state == GameState.PLAYING and self.running:
                    # USAR EL TIEMPO REAL DE LA MÚSICA - NO DEL JUEGO
                    if hasattr(self, 'start_time') and self.start_time:
                        current_time = time.time() - self.start_time
                    else:
                        current_time = time.time() - start_time  # Fallback

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

    def _space_out_actions(self, actions):
        """Espaciar las acciones para evitar que aparezcan muy juntas"""
        if not actions:
            return actions

        # Ordenar por tiempo
        sorted_actions = sorted(actions, key=lambda a: a.tiempo)
        spaced_actions = []

        # Tiempo mínimo entre notas - MUY RÁPIDO
        min_gap = 0.8  # 0.8 segundos mínimo entre notas (súper rápido)

        last_time = 0
        for action in sorted_actions:
            # Si esta nota está muy cerca de la anterior, espaciarla
            if action.tiempo - last_time < min_gap:
                action.tiempo = last_time + min_gap

            spaced_actions.append(action)
            last_time = action.tiempo

        return spaced_actions

    def process_actions(self, current_time, elapsed_time=None):
        """MEJORADO: Una nota a la vez con espaciado adecuado"""
        if not self.actions:
            return

        # Limpiar mapa completamente
        for coord in self.game_map.grid_state:
            self.game_map.set_cell_state(coord, 0)

        # NUEVO: Permitir múltiples notas simultáneas como juego de ritmo real
        active_actions = []

        # Buscar todas las notas que deben estar visibles ahora
        for action in self.actions:
            if action.completada:
                continue

            timing_offset = current_time - action.tiempo

            # Mostrar notas solo 0.5 segundos antes - CASI SINCRONIZADO
            if -0.5 <= timing_offset <= Config.OKAY_WINDOW:
                active_actions.append((action, timing_offset))

        # Si tenemos notas activas, mostrarlas
        if active_actions:
            # Mostrar la primera nota como target en Line panel
            self.game_map.set_target_coordinate(active_actions[0][0].coordenada)

            # Procesar cada nota activa
            for current_action, timing_offset in active_actions:
                # NO SOBRESCRIBIR si ya está completada (amarilla)
                if current_action.completada:
                    continue  # Skip - keep yellow color

                # Estados visuales para ventana de 0.5 segundos - MUY RÁPIDO
                if timing_offset < -0.3:
                    # Apareciendo - apenas visible (0.2s)
                    self.game_map.set_cell_state(current_action.coordenada, 2)
                elif -0.4 <= timing_offset <= 0.4:
                    # Momento perfecto - VERDE por 0.8 segundos total
                    self.game_map.set_cell_state(current_action.coordenada, 3)
                else:
                    # Fuera del momento perfecto - azul normal
                    self.game_map.set_cell_state(current_action.coordenada, 2)

            # Mostrar info de la primera nota
            first_action = active_actions[0][0]
            first_offset = active_actions[0][1]

            # Show current action line
            self.game_map.set_actual_line(f"♪ Now playing: {first_action.coordenada} - {first_action.line[:30]}...")

            # Mostrar cuántas notas están activas
            coords_text = " | ".join([a[0].coordenada for a in active_actions[:3]])
            self.game_map.set_active_coords(f"Active: {coords_text}")

        else:
            # No hay notas activas
            self.game_map.set_actual_line("♪ Song complete! ♪")
            self.game_map.set_active_coords("FINAL SCORE")

        # REVISAR TODAS LAS NOTAS para misses automáticos
        for action in self.actions:
            if action.completada:
                continue

            timing_offset = current_time - action.tiempo

            # Miss automático si pasó mucho tiempo después del momento perfecto
            if timing_offset > Config.OKAY_WINDOW * 1.5:  # 3 segundos después
                action.completada = True
                action.missed = True
                self.combo_system.break_combo()

                # DAÑO por miss automático
                damage = abs(Config.HEALTH_CHANGES["MISS"])
                self.health_system.take_damage(damage)

                self.game_map.set_cell_state(action.coordenada, 5)  # Red for miss
                self.game_map.set_actual_line(f"♪ AUTO MISS! {action.coordenada} expired (-{damage} HP)")

        # Actualizar estadísticas
        completed = sum(1 for action in self.actions if action.completada)
        self.current_action_index = completed
        progress = int((completed / len(self.actions)) * 100) if self.actions else 100
        self.game_map.set_progress(progress)

        current_health = self.health_system.get_health_percentage()
        health_display = max(0, int(current_health))
        self.game_map.set_health(health_display)

        # Show game progress
        total_actions = len(self.actions)
        if total_actions == 0:
            self.game_map.set_active_coords("No actions loaded")
        else:
            self.game_map.set_active_coords(f"Progress: {completed}/{total_actions} | Health: {current_health:.0f}%")

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
        """Procesa el input del usuario cuando presiona teclas - SIMPLIFICADO"""
        if not self.actions:
            return

        # Process hit attempt

        # Buscar CUALQUIER acción con esa coordenada que no esté completada
        hit_successful = False

        for action in self.actions:
            if action.completada or action.coordenada != coordinate:
                continue

            timing_offset = current_time - action.tiempo

            # VENTANA SÚPER GENEROSA: ±3 segundos
            if -3.0 <= timing_offset <= 3.0:
                action.completada = True
                action.hit_successfully = True

                # ÉXITO!
                hit_successful = True

                # Visual feedback - AMARILLO para hit exitoso
                self.game_map.set_cell_state(action.coordenada, 4)  # Amarillo
                # FORZAR actualización visual inmediatamente
                pass
                threading.Timer(2.0, lambda coord=action.coordenada: self.game_map.set_cell_state(coord, 0)).start()

                # INCREMENT SUCCESS COUNTER!
                self.game_map.increment_success()

                # Show success feedback
                self.game_map.set_actual_line(f"♪ SUCCESS! {coordinate} hit!")

                # Puntaje y healing
                points = Config.BASE_POINTS["PERFECT"] if abs(timing_offset) <= 1.0 else Config.BASE_POINTS["GOOD"]
                self.score_system.add_score(points)

                # HEALING - debug
                heal_amount = Config.HEALTH_CHANGES["PERFECT"]
                pass
                self.health_system.heal(heal_amount)

                self.combo_system.add_hit()

                break
        # Si no hubo hit exitoso, mostrar miss
        if not hit_successful:
            # Mostrar qué notas están disponibles
            available_notes = [f"{a.coordenada}" for a in self.actions if not a.completada][:5]
            self.game_map.set_actual_line(f"♪ MISS! {coordinate} not available. Try: {', '.join(available_notes)}")

            # MÁS DAMAGE por miss manual
            damage = abs(Config.HEALTH_CHANGES["MISS"])
            pass
            self.combo_system.break_combo()
            self.health_system.take_damage(damage)

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
                pass
            elif result_name == "GOOD":
                pass
            elif result_name == "OKAY":
                pass
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
                    self.console.print("[yellow]Invalid option. Use ENTER, R or Q[/yellow]")
            except (KeyboardInterrupt, EOFError):
                self.running = False
                return
            
def main():
    engine = GameEngine()
    engine.state = GameState.MENU
    engine.run()

if __name__ == "__main__":
    main()
