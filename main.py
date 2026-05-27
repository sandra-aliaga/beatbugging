import threading
import time
import pygame as pg
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import sys
import os
import select
import queue
import tty
import termios

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import Config
from settings import Settings

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
    missed: bool = False
    hit_successfully: bool = False


class GameEngine:
    def __init__(self):
        self.console = Settings.make_console()
        self.state = GameState.MENU
        self.music_generator = LogMusicGenerator()
        self.game_map = Map(size=Config.GRID_SIZE)
        # Sistemas de juego con OpacityTimingSystem real
        self.score_system = ScoreSystem()
        self.combo_system = ComboSystem()
        self.health_system = HealthSystem(max_health=Config.MAX_HEALTH)
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
        self.selected_log_file = None
        self.selected_difficulty = "user"
        self.selected_scale = Settings.scale
        
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
                scale=self.selected_scale,
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
        self.health_system = HealthSystem(max_health=Config.MAX_HEALTH)
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
        """Complete game loop using stdin for input (works on X11 and Wayland)."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        inp = {"buf": ""}
        _FIRST = set('asdef')
        _SECOND = set('jklmn')

        try:
            tty.setcbreak(fd)
            try:
                loading_time = 6.0 if len(self.actions) > 50 else 3.0
                self.loading_screen.show_loading("INITIALIZING BEATBUGGING SYSTEM", loading_time)

                self.start_time = time.time()
                self.start_music()

                mode_text = "ROOT MODE (Speed: 1.6x)" if self.selected_difficulty == "root" else "USER MODE (Speed: 1.2x)"
                self.game_map.set_actual_line(f"♪ {mode_text} - Music synced!")

                live_console = Settings.make_console(style="on black")
                with Live(self.game_map.build_layout(), console=live_console, screen=True, redirect_stderr=False) as live:
                    game_duration = max([action.tiempo for action in self.actions]) + 10.0 if self.actions else 90.0

                    while self.state == GameState.PLAYING and self.running:
                        current_time = time.time() - self.start_time

                        # select() con timeout 0: check instantáneo sin O_NONBLOCK
                        # (O_NONBLOCK afecta la file description compartida con stdout)
                        r, _, _ = select.select([fd], [], [], 0)
                        if r:
                            raw = os.read(fd, 1)
                            c = raw.decode('utf-8', errors='replace').lower()
                            if c in ('\x1b', '\x03'):
                                raise KeyboardInterrupt
                            if c in _FIRST:
                                inp["buf"] = c.upper()
                                self.game_map.set_input(inp["buf"])
                            elif c in _SECOND and len(inp["buf"]) == 1:
                                inp["buf"] += c.upper()
                                self.game_map.set_input(inp["buf"])
                                coord = inp["buf"]
                                self.process_user_input(coord, current_time)
                                inp["buf"] = ""
                                self.game_map.clear_input()

                        self.process_actions(current_time, current_time)

                        current_health = self.health_system.get_health_percentage()
                        if self.health_system.is_dead() or current_health <= 0:
                            self.state = GameState.GAME_OVER
                            break

                        if current_time >= game_duration:
                            self.state = GameState.VICTORY
                            break

                        self.update_display(live)
                        time.sleep(0.1)

            except KeyboardInterrupt:
                self.console.print("\n[red]Game interrupted[/red]")
            except Exception as e:
                self.console.print(f"[red]Error in game loop: {e}[/red]")
            finally:
                self.stop_music()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def run(self):
        try:
            while self.running:
                if self.state == GameState.MENU:
                    game_config = run_menu()
                    if game_config:
                        # Guardar el archivo y dificultad seleccionados
                        self.selected_log_file = game_config.get('file')
                        self.selected_difficulty = game_config.get('difficulty', 'user')
                        self.selected_scale = game_config.get('scale', Settings.scale)

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

        sorted_actions = sorted(actions, key=lambda a: a.tiempo)
        spaced_actions = []
        min_gap = 0.8
        last_time = 0.0

        for action in sorted_actions:
            new_time = max(action.tiempo, last_time + min_gap)
            spaced_actions.append(GameAction(
                tiempo=new_time,
                coordenada=action.coordenada,
                tipo=action.tipo,
                duracion=action.duracion,
                line=action.line,
                completada=action.completada,
                tiempo_inicio_hold=action.tiempo_inicio_hold,
            ))
            last_time = new_time

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
            if -0.5 <= timing_offset <= Config.OKAY_WINDOW:
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

        
    
    def _wait_end_screen_input(self, render_frame=None) -> str:
        """Wait for input on end screens. If render_frame is given, animate via Live.

        render_frame: callable(angle: float) -> renderable, called each tick.
        Returns 'restart', 'menu', or 'quit'.
        """
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            # Drain stdin so leftover keys don't trigger an immediate exit
            while select.select([fd], [], [], 0)[0]:
                os.read(fd, 64)

            def _classify(ch: str):
                if ch in ('\x1b', '\x03'):  return 'menu'
                if ch in ('\r', '\n'):      return 'restart'
                if ch == 'q':                return 'quit'
                if ch == 'm':                return 'menu'
                return None

            if render_frame is None:
                while True:
                    r, _, _ = select.select([fd], [], [], 0.2)
                    if not r:
                        continue
                    action = _classify(os.read(fd, 1).decode('utf-8', errors='replace').lower())
                    if action:
                        return action

            start = time.time()
            with Live(console=self.console, screen=True, refresh_per_second=15) as live:
                while True:
                    angle = (time.time() - start) * 0.6
                    live.update(render_frame(angle))
                    r, _, _ = select.select([fd], [], [], 0.08)
                    if not r:
                        continue
                    action = _classify(os.read(fd, 1).decode('utf-8', errors='replace').lower())
                    if action:
                        return action
        except KeyboardInterrupt:
            return 'quit'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def show_game_over(self):
        self.stop_music()

        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions)
        }

        self.game_over_animation.show_game_over_animation()

        action = self._wait_end_screen_input(
            render_frame=lambda angle: self.game_over_screen.build(stats, angle)
        )
        if action == 'restart':
            self.reset_game()
            self.start_game()
        elif action == 'menu':
            self.state = GameState.MENU
        elif action == 'quit':
            self.running = False

    def show_victory(self):
        self.stop_music()

        stats = {
            **self.score_system.get_stats(),
            'health': self.health_system.get_health_percentage(),
            'total_actions': len(self.actions),
            'time_taken': getattr(self, 'current_time', 0)
        }

        self.victory_animation.show_victory_animation()

        action = self._wait_end_screen_input(
            render_frame=lambda angle: self.victory_screen.build(stats, angle)
        )
        if action == 'restart':
            self.reset_game()
            self.start_game()
        elif action == 'menu':
            self.state = GameState.MENU
        elif action == 'quit':
            self.running = False
            
def main():
    import traceback, datetime
    from pathlib import Path
    log_dir = Path.home() / ".local" / "share" / "beatbugging"
    log_path = log_dir / "error.log"

    try:
        Settings.load()
        engine = GameEngine()
        engine.state = GameState.MENU
        engine.run()
    except Exception:
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a") as f:
            f.write(f"\n--- {datetime.datetime.now().isoformat()} ---\n")
            traceback.print_exc(file=f)
        print(f"\n[ERROR] El programa terminó con un error inesperado.")
        print(f"Revisa el log en: {log_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
