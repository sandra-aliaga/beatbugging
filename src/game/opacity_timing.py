import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional, Dict, Any
import time

class TimingState(Enum):
    """Enum para los 6 estados de timing en orden temporal"""
    EARLY = "early"
    ALMOST_EARLY = "almost_early"
    PERFECT = "perfect"
    ALMOST_LATE = "almost_late"
    LATE = "late"
    MISS = "miss"

@dataclass
class TimingResult:
    """Resultado del cálculo de timing incluyendo estado y efectos visuales"""
    state: TimingState
    opacity: float
    time_offset: float
    points: int
    color_hint: str
    should_display: bool

class OpacityTimingSystem:
    """Sistema de timing basado en opacidad para BeatBugging"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.states_config = self.config["timing_states"]
        self.global_settings = self.config["global_settings"]
        
    def _get_default_config_path(self) -> str:
        """Obtiene la ruta del archivo de configuración"""
        current_dir = os.path.dirname(__file__)
        return os.path.join(current_dir, "..", "config", "timing_states.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Configuración por defecto si no existe el archivo
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Configuración por defecto si no existe el archivo JSON"""
        return {
            "timing_states": {
                "early": {"time_range": [-4.0, -2.0], "opacity": 0.2, "color_hint": "dim_blue"},  # ✅ 2 segundos de early
                "almost_early": {"time_range": [-2.0, -1.0], "opacity": 0.5, "color_hint": "blue"},  # ✅ 1 segundo de almost_early
                "perfect": {"time_range": [-1.0, 1.0], "opacity": 1.0, "color_hint": "bright_green"},  # ✅ 2 segundos de ventana perfecta!
                "almost_late": {"time_range": [1.0, 2.0], "opacity": 0.6, "color_hint": "yellow"},  # ✅ 1 segundo de almost_late
                "late": {"time_range": [2.0, 3.0], "opacity": 0.3, "color_hint": "orange"},  # ✅ 1 segundo de late
                "miss": {"time_range": [3.0, 5.0], "opacity": 0.0, "color_hint": "red"}  # ✅ 2 segundos antes de miss
            },
            "global_settings": {
                "anticipation_window": 2.0,
                "reaction_window": 2.0,
                "scoring_weights": {
                    "early": 50, "almost_early": 150, "perfect": 300,
                    "almost_late": 100, "late": 25, "miss": 0
                }
            }
        }
    
    def calculate_timing_state(self, current_time: float, target_time: float) -> TimingResult:
        """
        Calcula el estado de timing actual basado en el tiempo.
        
        Args:
            current_time: Tiempo actual del juego
            target_time: Tiempo objetivo del bug/acción
            
        Returns:
            TimingResult con el estado, opacidad y efectos visuales
        """
        # Calcular offset temporal (positivo = tarde, negativo = temprano)
        time_offset = current_time - target_time
        
        # Buscar en qué estado estamos
        for state_name, state_config in self.states_config.items():
            time_range = state_config["time_range"]
            min_time, max_time = time_range[0], time_range[1]
            
            if min_time <= time_offset < max_time:
                state = TimingState(state_name)
                opacity = state_config["opacity"]
                color_hint = state_config["color_hint"]
                points = self.global_settings["scoring_weights"][state_name]
                
                # Determinar si debe mostrarse
                should_display = opacity > 0.0
                
                return TimingResult(
                    state=state,
                    opacity=opacity,
                    time_offset=time_offset,
                    points=points,
                    color_hint=color_hint,
                    should_display=should_display
                )
        
        # Si no está en ningún rango, está fuera de la ventana de tiempo
        return TimingResult(
            state=TimingState.MISS,
            opacity=0.0,
            time_offset=time_offset,
            points=0,
            color_hint="dim_red",
            should_display=False
        )
    
    def is_within_anticipation_window(self, current_time: float, target_time: float) -> bool:
        """Verifica si el bug debe aparecer (dentro de la ventana de anticipación)"""
        time_until_target = target_time - current_time
        return time_until_target <= self.global_settings["anticipation_window"]
    
    def is_within_reaction_window(self, current_time: float, target_time: float) -> bool:
        """Verifica si aún es posible reaccionar al bug"""
        time_since_target = current_time - target_time
        return time_since_target <= self.global_settings["reaction_window"]
    
    def get_opacity_for_timing(self, current_time: float, target_time: float) -> float:
        """Obtiene solo la opacidad para un timing dado (función de conveniencia)"""
        result = self.calculate_timing_state(current_time, target_time)
        return result.opacity
    
    def get_interpolated_opacity(self, current_time: float, target_time: float) -> float:
        """
        Calcula una opacidad interpolada suavemente entre estados.
        Esto crea transiciones más fluidas en lugar de cambios abruptos.
        """
        time_offset = current_time - target_time
        
        # Encontrar los dos estados más cercanos para interpolar
        for i, (state_name, state_config) in enumerate(self.states_config.items()):
            time_range = state_config["time_range"]
            min_time, max_time = time_range[0], time_range[1]
            
            if min_time <= time_offset < max_time:
                # Calcular progreso dentro del estado (0.0 a 1.0)
                if max_time == min_time:
                    progress = 0.0
                else:
                    progress = (time_offset - min_time) / (max_time - min_time)
                
                current_opacity = state_config["opacity"]
                
                # Interpolar con el siguiente estado si es posible
                state_list = list(self.states_config.items())
                if i < len(state_list) - 1:
                    next_state_config = state_list[i + 1][1]
                    next_opacity = next_state_config["opacity"]
                    
                    # Interpolación lineal suave
                    interpolated_opacity = current_opacity + (next_opacity - current_opacity) * progress
                    return max(0.0, min(1.0, interpolated_opacity))
                
                return current_opacity
        
        return 0.0  # Fuera de rango
    
    def can_score_points(self, current_time: float, target_time: float) -> bool:
        """Verifica si presionar en este momento daría puntos"""
        result = self.calculate_timing_state(current_time, target_time)
        return result.points > 0
    
    def get_visual_feedback(self, current_time: float, target_time: float) -> Dict[str, Any]:
        """
        Obtiene información completa para efectos visuales.
        Útil para el sistema de renderizado.
        """
        result = self.calculate_timing_state(current_time, target_time)
        
        return {
            "state": result.state.value,
            "opacity": result.opacity,
            "color": result.color_hint,
            "should_display": result.should_display,
            "points_if_pressed": result.points,
            "time_offset": result.time_offset,
            "interpolated_opacity": self.get_interpolated_opacity(current_time, target_time)
        }

# Función de conveniencia para uso directo
def get_bug_opacity(current_time: float, target_time: float, timing_system: Optional[OpacityTimingSystem] = None) -> float:
    """
    Función simple para obtener la opacidad de un bug en un momento dado.
    
    Args:
        current_time: Tiempo actual del juego
        target_time: Tiempo objetivo cuando el bug debe presionarse
        timing_system: Sistema de timing (opcional, se crea uno por defecto)
    
    Returns:
        float: Opacidad entre 0.0 (invisible) y 1.0 (completamente visible)
    """
    if timing_system is None:
        timing_system = OpacityTimingSystem()
    
    return timing_system.get_opacity_for_timing(current_time, target_time)

# Demo/Test del sistema
def demo_timing_system():
    """Función de demostración del sistema de timing"""
    print("🎮 Demo del Sistema de Timing con Opacidad")
    print("=" * 50)
    
    timing_system = OpacityTimingSystem()
    target_time = 10.0  # Bug objetivo a los 10 segundos
    
    print(f"Objetivo del bug: {target_time}s")
    print("\nSimulación temporal:")
    
    # Simular desde 2 segundos antes hasta 2 segundos después
    for t in range(8 * 10, 12 * 10 + 1):  # 8.0s a 12.0s con pasos de 0.1s
        current_time = t / 10.0
        result = timing_system.calculate_timing_state(current_time, target_time)
        
        # Crear barra visual de opacidad
        opacity_bar = "█" * int(result.opacity * 10) + "░" * (10 - int(result.opacity * 10))
        
        print(f"Tiempo: {current_time:4.1f}s | {result.state.value:12} | "
              f"Opacidad: {result.opacity:.1f} [{opacity_bar}] | "
              f"Puntos: {result.points:3d}")
    
    print("\n🔍 Casos de uso:")
    
    # Casos específicos
    test_cases = [
        (8.5, "Bug apareciendo (early)"),
        (9.7, "Preparándose (almost_early)"),
        (10.0, "¡MOMENTO EXACTO! (perfect)"),
        (10.2, "Todavía bien (almost_late)"),
        (10.7, "Se está yendo (late)"),
        (11.5, "Perdido (miss)")
    ]
    
    for test_time, description in test_cases:
        result = timing_system.calculate_timing_state(test_time, target_time)
        print(f"  {test_time}s - {description}: Opacidad {result.opacity:.1f}, Puntos {result.points}")

if __name__ == "__main__":
    demo_timing_system()