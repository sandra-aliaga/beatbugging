#!/usr/bin/env python3
"""
Pantalla de lanzamiento del juego BeatBugging
"""

import sys
import os
import pygame as pg

# Agregar paths para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.dirname(__file__))

from game_engine import GameEngine

def launch_game(log_path=None, difficulty="user"):
    """
    Lanza el juego con el archivo de log especificado
    """
    try:
        # Inicializar pygame
        pg.init()
        
        # Crear el motor del juego
        if log_path and os.path.exists(log_path):
            game = GameEngine(log_path, difficulty)
        else:
            game = GameEngine("default", difficulty)
        
        print(f"🎮 Iniciando BeatBugging...")
        print(f"📁 Archivo: {log_path if log_path else 'default.log'}")
        print(f"⚙️  Dificultad: {difficulty}")
        print(f"🎹 Controles: A,S,D,F,G (columnas) J,K,L,N,M (filas)")
        print(f"⏸️  ESPACIO: Pausa | ESC: Salir")
        print(f"🎯 ¡Presiona las teclas cuando veas las luces!")
        
        # Ejecutar el juego
        game.run()
        
    except Exception as e:
        print(f"❌ Error al ejecutar el juego: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pg.quit()

if __name__ == "__main__":
    launch_game()