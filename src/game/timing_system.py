import time
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class HitResult(Enum):
    PERFECT = "perfect"
    GOOD = "good"
    OKAY = "okay"
    MISS = "miss"

@dataclass
class HitTiming:
    result: HitResult
    timing_offset: float
    points: int
    health_change: int

class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_hits = 0
        self.good_hits = 0
        self.okay_hits = 0
        self.misses = 0
        
        self.timing_windows = {
            HitResult.PERFECT: 0.1,
            HitResult.GOOD: 0.2,
            HitResult.OKAY: 0.3,
            HitResult.MISS: float('inf')
        }
        
        self.base_points = {
            HitResult.PERFECT: 300,
            HitResult.GOOD: 200,
            HitResult.OKAY: 100,
            HitResult.MISS: 0
        }
        
        self.health_changes = {
            HitResult.PERFECT: 5,  # More healing for good hits
            HitResult.GOOD: 3,
            HitResult.OKAY: 2,
            HitResult.MISS: -2  # Much less damage - was -8
        }
    
    def add_score(self, points: int):
        """Agrega puntos directamente al score"""
        self.score += points
    
    def evaluate_hit(self, timing_offset: float) -> HitTiming:
        abs_offset = abs(timing_offset)
        
        for result in [HitResult.PERFECT, HitResult.GOOD, HitResult.OKAY]:
            if abs_offset <= self.timing_windows[result]:
                return self._process_hit(result, timing_offset)
        
        return self._process_hit(HitResult.MISS, timing_offset)
    
    def _process_hit(self, result: HitResult, timing_offset: float) -> HitTiming:
        if result == HitResult.MISS:
            self.combo = 0
            self.misses += 1
            points = 0
        else:
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            
            if result == HitResult.PERFECT:
                self.perfect_hits += 1
            elif result == HitResult.GOOD:
                self.good_hits += 1
            elif result == HitResult.OKAY:
                self.okay_hits += 1
            
            combo_multiplier = min(1 + (self.combo - 1) * 0.1, 3.0)
            points = int(self.base_points[result] * combo_multiplier)
        
        self.score += points
        health_change = self.health_changes[result]
        
        return HitTiming(result, timing_offset, points, health_change)
    
    def get_accuracy(self) -> float:
        total_hits = self.perfect_hits + self.good_hits + self.okay_hits + self.misses
        if total_hits == 0:
            return 100.0
        
        weighted_score = (
            self.perfect_hits * 100 +
            self.good_hits * 75 +
            self.okay_hits * 50 +
            self.misses * 0
        )
        
        return (weighted_score / (total_hits * 100)) * 100
    
    def get_stats(self) -> dict:
        return {
            "score": self.score,
            "combo": self.combo,
            "max_combo": self.max_combo,
            "accuracy": self.get_accuracy(),
            "perfect": self.perfect_hits,
            "good": self.good_hits,
            "okay": self.okay_hits,
            "miss": self.misses
        }

class AdvancedTimingSystem:
    def __init__(self, bpm: float = 120.0):
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm
        self.start_time = None
        self.paused_time = 0
        self.is_paused = False
        
    def start(self):
        self.start_time = time.time()
        self.is_paused = False
        
    def pause(self):
        if not self.is_paused and self.start_time is not None:
            self.paused_time += time.time() - self.start_time
            self.is_paused = True
    
    def resume(self):
        if self.is_paused:
            self.start_time = time.time()
            self.is_paused = False
    
    def get_current_time(self) -> float:
        if self.start_time is None:
            return 0.0
        
        if self.is_paused:
            return self.paused_time
        
        return (time.time() - self.start_time) + self.paused_time
    
    def get_current_beat(self) -> float:
        return self.get_current_time() / self.beat_duration
    
    def time_to_beat(self, game_time: float) -> float:
        return game_time / self.beat_duration
    
    def beat_to_time(self, beat: float) -> float:
        return beat * self.beat_duration

class ComboSystem:
    def __init__(self):
        self.current_combo = 0
        self.max_combo = 0
        self.combo_thresholds = [10, 25, 50, 100, 200]
        self.combo_bonuses = [1.2, 1.5, 2.0, 3.0, 5.0]
        
    def add_hit(self):
        self.current_combo += 1
        self.max_combo = max(self.max_combo, self.current_combo)
    
    def break_combo(self):
        self.current_combo = 0
    
    def get_multiplier(self) -> float:
        for i, threshold in enumerate(self.combo_thresholds):
            if self.current_combo >= threshold:
                continue
            if i == 0:
                return 1.0
            return self.combo_bonuses[i-1]
        
        return self.combo_bonuses[-1]
    
    def get_combo_rank(self) -> str:
        if self.current_combo >= 200:
            return "LEGENDARY"
        elif self.current_combo >= 100:
            return "GODLIKE"
        elif self.current_combo >= 50:
            return "AMAZING"
        elif self.current_combo >= 25:
            return "EXCELLENT"
        elif self.current_combo >= 10:
            return "GREAT"
        else:
            return "GOOD"

class HealthSystem:
    def __init__(self, max_health: int = 100, critical_threshold: int = 20):
        self.max_health = max_health
        self.current_health = max_health
        self.critical_threshold = critical_threshold
        self.damage_reduction = 0.5  # Reduced from 0.7 to 0.5 - even less damage
        
    def take_damage(self, amount: int):
        """Recibe daño - amount debe ser positivo"""
        actual_damage = int(abs(amount) * self.damage_reduction)
        self.current_health = max(0, self.current_health - actual_damage)
        # Damage sin log para pantalla limpia
    
    def heal(self, amount: int):
        """Cura vida - amount debe ser positivo"""
        heal_amount = abs(amount)
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + heal_amount)
        gained = self.current_health - old_health
        if gained > 0:
            # Heal sin log para pantalla limpia
            pass
    
    def change_health(self, amount: int):
        """Cambia vida - positivo cura, negativo daña"""
        if amount > 0:
            self.heal(amount)
        elif amount < 0:
            self.take_damage(-amount)
    
    def is_critical(self) -> bool:
        return self.current_health <= self.critical_threshold
    
    def is_dead(self) -> bool:
        return self.current_health <= 0
    
    def get_health_percentage(self) -> float:
        return (self.current_health / self.max_health) * 100
    
    def set_damage_reduction(self, reduction: float):
        self.damage_reduction = max(0.0, min(1.0, reduction))

class DifficultyManager:
    def __init__(self):
        self.difficulties = {
            "easy": {
                "timing_tolerance": 1.5,
                "health_multiplier": 1.5,
                "score_multiplier": 0.8,
                "damage_reduction": 0.6
            },
            "normal": {
                "timing_tolerance": 1.0,
                "health_multiplier": 1.0,
                "score_multiplier": 1.0,
                "damage_reduction": 1.0
            },
            "hard": {
                "timing_tolerance": 0.7,
                "health_multiplier": 0.7,
                "score_multiplier": 1.3,
                "damage_reduction": 1.5
            },
            "expert": {
                "timing_tolerance": 0.5,
                "health_multiplier": 0.5,
                "score_multiplier": 1.8,
                "damage_reduction": 2.0
            }
        }
        
        self.current_difficulty = "normal"
    
    def set_difficulty(self, difficulty: str):
        if difficulty in self.difficulties:
            self.current_difficulty = difficulty
    
    def get_settings(self) -> dict:
        return self.difficulties[self.current_difficulty]
    
    def apply_to_score_system(self, score_system: ScoreSystem):
        settings = self.get_settings()
        
        for result in score_system.timing_windows:
            if result != HitResult.MISS:
                score_system.timing_windows[result] *= settings["timing_tolerance"]
        
        for result in score_system.base_points:
            score_system.base_points[result] = int(
                score_system.base_points[result] * settings["score_multiplier"]
            )
    
    def apply_to_health_system(self, health_system: HealthSystem):
        settings = self.get_settings()
        health_system.max_health = int(100 * settings["health_multiplier"])
        health_system.current_health = health_system.max_health
        health_system.set_damage_reduction(1.0 / settings["damage_reduction"])
