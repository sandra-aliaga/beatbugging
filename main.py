import threading
import time
import pygame as pg
import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import sys
import os
import select  # Para input no bloqueante
import termios
import tty
import keyboard

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from music.generator import LogMusicGenerator
from cli.map import Map
from game.timing_system import ScoreSystem, ComboSystem, HealthSystem, HitResult
from game.opacity_timing import OpacityTimingSystem  # 🎯 Importar el sistema de opacidad real
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
    completada: bool = False
    tiempo_inicio_hold: Optional[float] = None

class InputHandler:
    def __init__(self):
        self.recent_presses = []  # Para trackear presses recientes
        self.running = True
        self.old_settings = None
        self._setup_nonblocking_input()

    def _setup_nonblocking_input(self):
        """Configura input no bloqueante para terminal"""
        try:
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
        except:
            pass  # Si falla, usar método alternativo

    def _restore_input(self):
        """Restaura configuración de input"""
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_pressed_keys(self):
        """Obtiene teclas presionadas usando select no bloqueante"""
        pressed_keys = []
        try:
            if select.select([sys.stdin], [], [], 0.0)[0]:
                key = sys.stdin.read(1).upper()
                if key and key in 'ASDEFJKLMN':
                    self.recent_presses.append((key, time.time()))
                    pressed_keys.append(key)
        except:
            pass
        return pressed_keys

    def update(self):
        """Actualiza y obtiene input"""
        return self.get_pressed_keys()

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

class GameEngine:
    def __init__(self):
        self.console = Console()
        self.state = GameState.MENU
        self.music_generator = LogMusicGenerator()
        self.game_map = Map(size=5)
        self.input_handler = InputHandler()
        
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
        
        # SOLO inicializar audio, NO pygame completo para evitar ventanas
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
            print("🔇 Música detenida correctamente")
        except Exception as e:
            print(f"Error al detener música: {e}")
    
    def reset_game(self):
        """Reiniciar todos los valores del juego para una nueva partida"""
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.health = 200  # ✅ Más vida inicial
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
                    completada=False,
                    tiempo_inicio_hold=None
                )
                self.actions.append(action)
        else:
            self.actions = []
        
    def start_game(self):
        """Initialize and start the game directly"""
        self.state = GameState.PLAYING
        self.console.clear()
        
        # Show simple loading message
        self.console.print("[bold green]🎮 BEATBUGGING INICIANDO...[/bold green]")
        self.console.print("[dim]Los errores de logs se convierten en música y patrones visuales...[/dim]")
        
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
                    duracion=action["duracion"]
                )
                for action in self.music_data["gameplay_actions"]
            ]
            
            # Silently generated actions - no print
            
        except Exception as e:
            # Silent error handling - create minimal data to continue
            self.actions = [
                GameAction(tiempo=2.0, coordenada='AJ', tipo='tap', duracion=0),
                GameAction(tiempo=4.0, coordenada='SK', tipo='tap', duracion=0),
                GameAction(tiempo=6.0, coordenada='DL', tipo='tap', duracion=0),
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
        """Main game loop SIN ventana pygame, solo audio"""
        try:
        
            self.loading_screen.show_loading("INITIALIZING BEATBUGGING SYSTEM", 3.0)
            
            self.start_music()
            
            with Live(self.game_map.build_layout(), refresh_per_second=4) as live:
                # Calcular duración basada en las acciones generadas
                game_duration = max([action.tiempo for action in self.actions]) + 10.0 if self.actions else 90.0
                start_time = time.time()
                
                while self.state == GameState.PLAYING and self.running:
                    current_time = time.time() - start_time

                    # Procesar input del usuario
                    pressed_keys = self.input_handler.update()
                    if pressed_keys:
                        coordinate = self.input_handler.get_coordinate_from_keys()
                        if coordinate:
                            print(f"[DEBUG] Tecla presionada: {coordinate} en tiempo {current_time:.2f}")
                            self.process_user_input(coordinate, current_time)

                    self.process_actions(current_time, current_time)  # game_time and absolute_time

                    # VERIFY DEATH FIRST - priority over victory
                    current_health = self.health_system.get_health_percentage()
                    if self.health_system.is_dead() or current_health <= 0:
                        self.console.print(f"[red]GAME OVER: Health depleted ({current_health:.1f}%)[/red]")
                        print(f"[DEBUG] Setting state to GAME_OVER, health: {current_health}")  # Debug
                        self.state = GameState.GAME_OVER
                        break

                    # Terminar juego después de la duración establecida SOLAMENTE
                    # No verificar mixer porque puede no estar activo al inicio
                    if current_time >= game_duration:
                        self.state = GameState.VICTORY
                        break

                    # Actualizar pantalla
                    self.update_display(live)

                    # Control de FPS mejorado para mejor responsividad
                    time.sleep(0.1)  # ✅ 10 FPS para mejor gameplay
                        
        except KeyboardInterrupt:
            self.console.print("\n[red]Juego interrumpido[/red]")
        except Exception as e:
            self.console.print(f"[red]Error en game loop: {e}[/red]")
        finally:
            self.stop_music()
            self.input_handler._restore_input()  # Restaurar configuración de terminal
            # NO hay display pygame que cerrar
            
        # Mostrar pantalla final SIN pygame
        if self.state == GameState.GAME_OVER:
            self.show_game_over()
        elif self.state == GameState.VICTORY:
            self.show_victory()
    
    def run(self):
        try:
            while self.running:
                if self.state == GameState.MENU:
                    from src.menu.main_menu import run_menu
                    selected_file = run_menu()
                    if selected_file:
                        self.reset_game()
                        self.start_game()
                    else:
                        self.running = False

                elif self.state == GameState.PLAYING:
                    self.start_game()

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
        """Procesar acciones - usar lógica simple del mapa"""
        if not self.actions:
            return

        # Limpiar mapa primero
        for coord in self.game_map.grid_state:
            self.game_map.set_cell_state(coord, 0)

        # Mostrar próximas acciones usando timing system simple
        upcoming_coords = []
        for action in self.actions[self.current_action_index:self.current_action_index + 10]:
            if not action.completada:
                timing_offset = current_time - action.tiempo
                # Ventana de aparición más amplia: -4s a +3s
                if -4.0 <= timing_offset <= 3.0:
                    if abs(timing_offset) <= 0.5:
                        self.game_map.set_cell_state(action.coordenada, 3)  # PERFECT
                    elif abs(timing_offset) <= 1.5:
                        self.game_map.set_cell_state(action.coordenada, 2)  # GOOD
                    else:
                        self.game_map.set_cell_state(action.coordenada, 1)  # OK
                    upcoming_coords.append(action.coordenada)
                elif timing_offset > 3.0:  # Miss solo después de 3 segundos
                    action.completada = True
                    self.combo_system.break_combo()
                    self.health_system.take_damage(10)

        # Actualizar coordenadas activas
        self.game_map.set_active_coords(" - ".join(upcoming_coords[:3]))

        # Actualizar barras
        completed = sum(1 for action in self.actions if action.completada)
        self.current_action_index = completed
        progress = int((completed / len(self.actions)) * 100) if self.actions else 0
        self.game_map.set_progress(progress)

        current_health = self.health_system.get_health_percentage()
        self.game_map.set_health(max(0, int(current_health)))

        # Sync stats
        self.health = int(self.health_system.current_health)
        self.score = self.score_system.score
        self.combo = self.combo_system.current_combo

        # Check victory/death
        if self.health_system.is_dead() or current_health <= 0:
            self.state = GameState.GAME_OVER
            return

        # Victory cuando termine la música
        total_music_time = max([action.tiempo for action in self.actions]) if self.actions else 90.0
        if elapsed_time and elapsed_time >= total_music_time:
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

            # Ventana de hit: -2s a +2s
            if -2.0 <= timing_offset <= 2.0:
                action.completada = True
                action.hit_successfully = True
                self.game_map.update_cell(action.coordenada, True)

                # Puntaje basado en precisión
                if abs(timing_offset) <= 0.5:
                    points = 300
                    print(f"✨ PERFECT! {coordinate} (+{points} pts)")
                elif abs(timing_offset) <= 1.0:
                    points = 150
                    print(f"👍 GOOD! {coordinate} (+{points} pts)")
                else:
                    points = 50
                    print(f"👌 OK! {coordinate} (+{points} pts)")

                self.score_system.add_score(points)
                self.health_system.heal(5)
                self.combo_system.add_hit()
                break
            else:
                # Miss
                self.combo_system.break_combo()
                self.health_system.take_damage(15)
                print(f"❌ MISS! {coordinate}")
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
                print(f"✨ PERFECT! {action.coordenada}")
            elif result_name == "GOOD":
                print(f"GOOD! {action.coordenada}")
            elif result_name == "OKAY":
                print(f"👍 OKAY! {action.coordenada}")
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

                key = keyboard.read_key()

                if key == "q":
                    self.state = GameState.MENU
                    return
                elif key == "enter":
                    # reiniciar nivel
                    self.reset_game()
                    self.start_game()
                    return
                elif key == "esc":
                    # salir del juego
                    self.running = False
                    return
                else:
                    self.console.print("[yellow] Opción inválida. Usa ESC, Q o ENTER[/yellow]")
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
    engine = GameEngine()
    engine.state = GameState.MENU
    engine.run()

if __name__ == "__main__":
    main()
