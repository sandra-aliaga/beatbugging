#!/usr/bin/env python3
"""
Motor de juego principal para BeatBugging con indicadores visuales mejorados
"""

import pygame as pg
import sys
import os
import time
import math
from typing import List, Dict, Optional

# Agregar paths para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(__file__))

from music.generator import LogMusicGenerator

class GameEngine:
    def __init__(self, log_path: str = "default", difficulty: str = "user"):
        # Inicializar pygame
        pg.init()
        pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Configuración de pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("BeatBugging - Sistema de Depuración Musical")
        
        # Configuración de juego
        self.clock = pg.time.Clock()
        self.fps = 60
        self.running = True
        self.paused = False
        
        # Estado del juego
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.health = 100
        self.perfect_hits = 0
        self.good_hits = 0
        self.ok_hits = 0
        self.miss_hits = 0
        
        # Timing más generoso para jugabilidad
        self.perfect_window = 200  # ±200ms
        self.good_window = 400     # ±400ms  
        self.ok_window = 600       # ±600ms
        
        # Generar música y acciones
        self.music_generator = LogMusicGenerator(log_path)
        if log_path == "default":
            self.music_generator.useDefaultLog()
        
        # Grid 5x5 con coordenadas claras
        self.grid_size = 5
        self.cell_size = 80
        self.grid_x = 50
        self.grid_y = 150
        
        # Mapeo de teclas más intuitivo
        self.key_mapping = {
            # Fila superior (columnas A-E)
            pg.K_a: (0, 0), pg.K_s: (1, 0), pg.K_d: (2, 0), pg.K_f: (3, 0), pg.K_g: (4, 0),
            # Filas J-N (usar teclas de abajo)
            pg.K_z: (0, 1), pg.K_x: (1, 1), pg.K_c: (2, 1), pg.K_v: (3, 1), pg.K_b: (4, 1),
            pg.K_q: (0, 2), pg.K_w: (1, 2), pg.K_e: (2, 2), pg.K_r: (3, 2), pg.K_t: (4, 2),
            pg.K_1: (0, 3), pg.K_2: (1, 3), pg.K_3: (2, 3), pg.K_4: (3, 3), pg.K_5: (4, 3),
            pg.K_y: (0, 4), pg.K_u: (1, 4), pg.K_i: (2, 4), pg.K_o: (3, 4), pg.K_p: (4, 4)
        }
        
        # Estado de las celdas
        self.cell_states = {}
        for x in range(5):
            for y in range(5):
                self.cell_states[(x, y)] = {
                    'active': False,
                    'hit': False,
                    'glow': 0,
                    'pulse': 0,
                    'show_key': False,
                    'key_name': self.get_key_name(x, y)
                }
        
        # Acciones de juego
        self.gameplay_actions = []
        self.current_action_index = 0
        self.game_start_time = 0
        
        # Colores neón
        self.colors = {
            'background': (5, 5, 15),
            'grid_line': (0, 100, 100),
            'cell_normal': (10, 10, 30),
            'cell_active': (0, 255, 255),
            'cell_hit': (0, 255, 0),
            'cell_miss': (255, 50, 50),
            'text_normal': (200, 200, 200),
            'text_glow': (0, 255, 255),
            'perfect': (255, 255, 0),
            'good': (0, 255, 0),
            'ok': (255, 165, 0),
            'miss': (255, 0, 0)
        }
        
        # Fuentes
        self.font_large = pg.font.Font(None, 48)
        self.font_medium = pg.font.Font(None, 32)
        self.font_small = pg.font.Font(None, 24)
        self.font_key = pg.font.Font(None, 20)
        
        print("🎮 Motor de juego inicializado")
        print("📋 Controles:")
        print("   A S D F G (fila superior)")
        print("   Z X C V B (segunda fila)")
        print("   Q W E R T (tercera fila)")
        print("   1 2 3 4 5 (cuarta fila)")
        print("   Y U I O P (fila inferior)")
        print("   ESPACIO: Pausa | ESC: Salir")
    
    def get_key_name(self, x: int, y: int) -> str:
        """Obtiene el nombre de la tecla para una posición del grid"""
        key_grid = [
            ['A', 'S', 'D', 'F', 'G'],
            ['Z', 'X', 'C', 'V', 'B'],
            ['Q', 'W', 'E', 'R', 'T'],
            ['1', '2', '3', '4', '5'],
            ['Y', 'U', 'I', 'O', 'P']
        ]
        return key_grid[y][x]
    
    def prepare_game(self):
        """Prepara el juego generando música y acciones"""
        print("🎵 Generando música desde logs...")
        
        try:
            # Generar música con velocidad más lenta
            music_data = self.music_generator.generate_music(
                scale="pentatonic", 
                rate=44100, 
                speed=0.5  # Muy lento para ser jugable
            )
            
            self.gameplay_actions = music_data['gameplay_actions']
            
            # Convertir audio para pygame
            if len(music_data['audio_data']) > 0:
                # Convertir a estéreo si es necesario
                audio_array = music_data['audio_data']
                if len(audio_array.shape) == 1:
                    stereo_array = audio_array.reshape(-1, 1)
                    stereo_array = stereo_array.repeat(2, axis=1)
                else:
                    stereo_array = audio_array
                
                self.music_sound = pg.sndarray.make_sound(stereo_array.astype('int16'))
            else:
                self.music_sound = None
            
            print(f"✅ Generadas {len(self.gameplay_actions)} acciones de juego")
            print(f"🎼 Escala musical: {music_data['scale_used']}")
            
        except Exception as e:
            print(f"❌ Error generando música: {e}")
            self.gameplay_actions = []
            self.music_sound = None
    
    def start_music(self):
        """Inicia la reproducción de música"""
        if self.music_sound:
            try:
                self.music_sound.play()
                print("🎵 Música iniciada")
            except Exception as e:
                print(f"❌ Error reproduciendo música: {e}")
        
        self.game_start_time = time.time()
    
    def update_game_state(self):
        """Actualiza el estado del juego"""
        if self.paused:
            return
        
        current_time = time.time() - self.game_start_time
        
        # Actualizar células activas basado en las acciones
        for action in self.gameplay_actions[self.current_action_index:]:
            action_time = action['tiempo']
            
            # Mostrar acción 1 segundo antes
            if action_time - 1.0 <= current_time <= action_time + 0.5:
                coord = action['coordenada']
                if coord and len(coord) >= 2:
                    try:
                        # Convertir coordenada de letra-número a x,y
                        col = ord(coord[0].upper()) - ord('A')
                        row = ord(coord[1].upper()) - ord('J')
                        
                        if 0 <= col < 5 and 0 <= row < 5:
                            cell_key = (col, row)
                            self.cell_states[cell_key]['active'] = True
                            self.cell_states[cell_key]['show_key'] = True
                            
                            # Efecto de pulso
                            pulse_factor = math.sin(time.time() * 8) * 0.5 + 0.5
                            self.cell_states[cell_key]['pulse'] = pulse_factor
                    except (IndexError, ValueError):
                        pass
            else:
                # Desactivar célula si ya pasó el tiempo
                coord = action['coordenada']
                if coord and len(coord) >= 2:
                    try:
                        col = ord(coord[0].upper()) - ord('A')
                        row = ord(coord[1].upper()) - ord('J')
                        
                        if 0 <= col < 5 and 0 <= row < 5:
                            cell_key = (col, row)
                            if current_time > action_time + 0.5:
                                self.cell_states[cell_key]['active'] = False
                                self.cell_states[cell_key]['show_key'] = False
                    except (IndexError, ValueError):
                        pass
        
        # Avanzar índice de acciones
        while (self.current_action_index < len(self.gameplay_actions) and 
               current_time > self.gameplay_actions[self.current_action_index]['tiempo'] + 1.0):
            self.current_action_index += 1
        
        # Reducir efectos visuales
        for cell_state in self.cell_states.values():
            if cell_state['glow'] > 0:
                cell_state['glow'] -= 5
            if cell_state['hit']:
                cell_state['glow'] = max(0, cell_state['glow'] - 3)
                if cell_state['glow'] <= 0:
                    cell_state['hit'] = False
    
    def handle_key_press(self, key):
        """Maneja la presión de teclas"""
        if key in self.key_mapping:
            cell_pos = self.key_mapping[key]
            current_time = time.time() - self.game_start_time
            
            # Buscar acción más cercana para esta célula
            best_action = None
            best_time_diff = float('inf')
            
            for action in self.gameplay_actions:
                coord = action['coordenada']
                if coord and len(coord) >= 2:
                    try:
                        col = ord(coord[0].upper()) - ord('A')
                        row = ord(coord[1].upper()) - ord('J')
                        
                        if (col, row) == cell_pos:
                            time_diff = abs(current_time - action['tiempo'])
                            if time_diff < best_time_diff and time_diff <= 1.0:  # 1 segundo de ventana
                                best_time_diff = time_diff
                                best_action = action
                    except (IndexError, ValueError):
                        continue
            
            if best_action:
                self.process_hit(cell_pos, best_time_diff)
            else:
                self.process_miss(cell_pos)
    
    def process_hit(self, cell_pos, time_diff):
        """Procesa un hit exitoso"""
        self.cell_states[cell_pos]['hit'] = True
        self.cell_states[cell_pos]['glow'] = 255
        
        # Determinar calidad del hit
        points = 0
        hit_quality = ""
        
        if time_diff <= self.perfect_window / 1000:
            points = 100
            hit_quality = "PERFECT!"
            self.perfect_hits += 1
            self.combo += 1
            self.cell_states[cell_pos]['glow'] = 255
            color = self.colors['perfect']
        elif time_diff <= self.good_window / 1000:
            points = 50
            hit_quality = "GOOD"
            self.good_hits += 1
            self.combo += 1
            color = self.colors['good']
        elif time_diff <= self.ok_window / 1000:
            points = 25
            hit_quality = "OK"
            self.ok_hits += 1
            self.combo = max(0, self.combo - 1)
            color = self.colors['ok']
        else:
            self.process_miss(cell_pos)
            return
        
        # Actualizar score con multiplicador de combo
        combo_multiplier = min(1 + (self.combo // 10) * 0.1, 3.0)
        self.score += int(points * combo_multiplier)
        self.max_combo = max(self.max_combo, self.combo)
        
        print(f"🎯 {hit_quality} +{int(points * combo_multiplier)} (combo x{self.combo})")
    
    def process_miss(self, cell_pos):
        """Procesa un miss"""
        self.miss_hits += 1
        self.combo = 0
        self.health = max(0, self.health - 5)
        self.cell_states[cell_pos]['glow'] = 100
        
        print("❌ MISS! -5 health")
    
    def draw_grid(self):
        """Dibuja el grid 5x5 con efectos visuales"""
        for x in range(5):
            for y in range(5):
                cell_x = self.grid_x + x * (self.cell_size + 10)
                cell_y = self.grid_y + y * (self.cell_size + 10)
                
                cell_key = (x, y)
                cell_state = self.cell_states[cell_key]
                
                # Color base de la célula
                if cell_state['active']:
                    # Efecto de pulso para células activas
                    pulse = cell_state['pulse']
                    base_color = self.colors['cell_active']
                    color = tuple(min(255, int(c * (0.7 + 0.3 * pulse))) for c in base_color)
                elif cell_state['hit']:
                    glow = cell_state['glow']
                    color = tuple(min(255, int(c + glow * 0.3)) for c in self.colors['cell_hit'])
                else:
                    color = self.colors['cell_normal']
                
                # Dibujar célula
                pg.draw.rect(self.screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))
                pg.draw.rect(self.screen, self.colors['grid_line'], (cell_x, cell_y, self.cell_size, self.cell_size), 2)
                
                # Mostrar nombre de tecla si está activa
                if cell_state['show_key'] or cell_state['active']:
                    key_name = cell_state['key_name']
                    text_color = self.colors['text_glow'] if cell_state['active'] else self.colors['text_normal']
                    
                    # Texto de la tecla más grande y visible
                    key_text = self.font_medium.render(key_name, True, text_color)
                    text_rect = key_text.get_rect(center=(cell_x + self.cell_size//2, cell_y + self.cell_size//2))
                    
                    # Sombra para mejor visibilidad
                    shadow_text = self.font_medium.render(key_name, True, (0, 0, 0))
                    shadow_rect = text_rect.copy()
                    shadow_rect.x += 2
                    shadow_rect.y += 2
                    
                    self.screen.blit(shadow_text, shadow_rect)
                    self.screen.blit(key_text, text_rect)
    
    def draw_ui(self):
        """Dibuja la interfaz de usuario"""
        # Panel de información
        ui_x = self.screen_width - 350
        ui_y = 50
        
        # Score
        score_text = self.font_large.render(f"SCORE: {self.score:,}", True, self.colors['text_glow'])
        self.screen.blit(score_text, (ui_x, ui_y))
        
        # Combo
        combo_color = self.colors['perfect'] if self.combo > 10 else self.colors['text_normal']
        combo_text = self.font_medium.render(f"COMBO: x{self.combo}", True, combo_color)
        self.screen.blit(combo_text, (ui_x, ui_y + 50))
        
        # Health bar
        health_y = ui_y + 100
        health_text = self.font_small.render("SYSTEM HEALTH:", True, self.colors['text_normal'])
        self.screen.blit(health_text, (ui_x, health_y))
        
        # Barra de vida
        bar_width = 200
        bar_height = 20
        health_ratio = self.health / 100
        
        health_bg = pg.Rect(ui_x, health_y + 25, bar_width, bar_height)
        pg.draw.rect(self.screen, (50, 50, 50), health_bg)
        
        if self.health > 70:
            health_color = self.colors['good']
        elif self.health > 30:
            health_color = self.colors['ok']
        else:
            health_color = self.colors['miss']
        
        health_fill = pg.Rect(ui_x, health_y + 25, bar_width * health_ratio, bar_height)
        pg.draw.rect(self.screen, health_color, health_fill)
        pg.draw.rect(self.screen, self.colors['grid_line'], health_bg, 2)
        
        # Progreso
        actions_remaining = len(self.gameplay_actions) - self.current_action_index
        progress_text = self.font_small.render(f"ACCIONES RESTANTES: {actions_remaining}", True, self.colors['text_normal'])
        self.screen.blit(progress_text, (ui_x, ui_y + 170))
        
        # Próximas acciones
        next_y = ui_y + 200
        next_title = self.font_small.render("PRÓXIMAS ACCIONES:", True, self.colors['text_glow'])
        self.screen.blit(next_title, (ui_x, next_y))
        
        current_time = time.time() - self.game_start_time
        for i, action in enumerate(self.gameplay_actions[self.current_action_index:self.current_action_index + 3]):
            time_until = action['tiempo'] - current_time
            coord = action['coordenada']
            
            if time_until > 0:
                preview_text = self.font_small.render(f"{coord}: {time_until:.1f}s", True, self.colors['text_normal'])
                self.screen.blit(preview_text, (ui_x, next_y + 25 + i * 20))
        
        if self.paused:
            pause_text = self.font_large.render("=== PAUSADO ===", True, self.colors['text_glow'])
            pause_rect = pause_text.get_rect(center=(self.screen_width//2, 100))
            self.screen.blit(pause_text, pause_rect)
    
    def run(self):
        """Ejecuta el bucle principal del juego"""
        self.prepare_game()
        
        if not self.gameplay_actions:
            print("❌ No hay acciones de juego generadas")
            return
        
        print("🚀 Iniciando juego...")
        self.start_music()
        
        while self.running:
            # Eventos
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                    elif event.key == pg.K_SPACE:
                        self.paused = not self.paused
                        print("⏸️ Pausa" if self.paused else "▶️ Continuar")
                    else:
                        self.handle_key_press(event.key)
            
            # Actualizar
            self.update_game_state()
            
            # Dibujar
            self.screen.fill(self.colors['background'])
            self.draw_grid()
            self.draw_ui()
            
            pg.display.flip()
            self.clock.tick(self.fps)
            
            # Verificar condiciones de fin
            if self.health <= 0:
                print("💀 Game Over - Sistema Comprometido")
                break
            elif self.current_action_index >= len(self.gameplay_actions):
                print("🏆 ¡Misión Completada!")
                break
        
        # Mostrar estadísticas finales
        total_actions = len(self.gameplay_actions)
        accuracy = ((self.perfect_hits + self.good_hits + self.ok_hits) / max(1, total_actions)) * 100
        
        print("\n📊 ESTADÍSTICAS FINALES:")
        print(f"Score Final: {self.score:,}")
        print(f"Combo Máximo: {self.max_combo}")
        print(f"Precisión: {accuracy:.1f}%")
        print(f"Perfect: {self.perfect_hits} | Good: {self.good_hits} | OK: {self.ok_hits} | Miss: {self.miss_hits}")
        
        pg.quit()

def main():
    """Función principal para pruebas"""
    game = GameEngine()
    game.run()

if __name__ == "__main__":
    main()