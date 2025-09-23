import os
from pathlib import Path

class GameConfig:
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent
    SRC_DIR = PROJECT_ROOT / "src"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # Audio Settings
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_BUFFER_SIZE = 1024
    AUDIO_CHANNELS = 1
    AUDIO_BIT_DEPTH = 16
    
    # Game Settings
    DEFAULT_BPM = 120.0
    DEFAULT_SCALE = "minor"
    DEFAULT_SPEED_MULTIPLIER = 2.0
    FRAME_RATE = 60
    
    # Timing Windows (in seconds) - Very generous for learning
    PERFECT_WINDOW = 0.8
    GOOD_WINDOW = 1.5
    OKAY_WINDOW = 2.0
    
    # Scoring
    BASE_POINTS = {
        "PERFECT": 300,
        "GOOD": 200,
        "OKAY": 100,
        "MISS": 0
    }
    
    MAX_COMBO_MULTIPLIER = 3.0
    COMBO_INCREMENT = 0.1
    
    # Health System
    MAX_HEALTH = 100
    CRITICAL_HEALTH_THRESHOLD = 20
    
    HEALTH_CHANGES = {
        "PERFECT": 3,
        "GOOD": 2,
        "OKAY": 1,
        "MISS": -15
    }
    
    # Grid Settings
    GRID_SIZE = 5
    GRID_COLUMNS = ['A', 'S', 'D', 'E', 'F']
    GRID_ROWS = ['J', 'K', 'L', 'M', 'N']
    
    # Visual Settings
    PRIMARY_COLOR = "#00ff00"
    SECONDARY_COLOR = "#39ff14"
    ERROR_COLOR = "#ff0000"
    WARNING_COLOR = "#ffff00"
    INFO_COLOR = "#00ffff"
    
    # Controls
    COLUMN_KEYS = ['a', 's', 'd', 'e', 'f']
    ROW_KEYS = ['j', 'k', 'l', 'm', 'n']
    
    PAUSE_KEY = 'space'
    QUIT_KEY = 'escape'
    CONFIRM_KEY = 'return'
    
    # Log Parsing
    SUPPORTED_LOG_FORMATS = [
        "JSON",
        "LOGCAT",  # Android
        "BRACKET",  # [YYYY-MM-DD HH:MM:SS] LEVEL message
        "PLAIN"
    ]
    
    LOG_SEVERITY_MAPPING = {
        "DEBUG": {"wave": "sin", "duration": 0.3, "color": "dim green"},
        "INFO": {"wave": "triangle", "duration": 0.4, "color": "green"},
        "WARNING": {"wave": "square", "duration": 0.6, "color": "yellow"},
        "ERROR": {"wave": "saw", "duration": 0.8, "color": "red"}
    }
    
    # Difficulty Settings
    DIFFICULTIES = {
        "EASY": {
            "timing_tolerance": 1.5,
            "health_multiplier": 1.5,
            "score_multiplier": 0.8,
            "damage_reduction": 0.6,
            "description": "Relaxed timing, more health"
        },
        "NORMAL": {
            "timing_tolerance": 1.0,
            "health_multiplier": 1.0,
            "score_multiplier": 1.0,
            "damage_reduction": 1.0,
            "description": "Balanced experience"
        },
        "HARD": {
            "timing_tolerance": 0.7,
            "health_multiplier": 0.7,
            "score_multiplier": 1.3,
            "damage_reduction": 1.5,
            "description": "Tight timing, higher rewards"
        },
        "EXPERT": {
            "timing_tolerance": 0.5,
            "health_multiplier": 0.5,
            "score_multiplier": 1.8,
            "damage_reduction": 2.0,
            "description": "For elite debuggers only"
        }
    }
    
    # Musical Scales
    SCALES = {
        "minor": {
            "intervals": [0, 2, 3, 5, 7, 8, 10],
            "description": "Natural minor - melancholic debugging"
        },
        "major": {
            "intervals": [0, 2, 4, 5, 7, 9, 11],
            "description": "Major scale - bright and optimistic"
        },
        "pentatonic": {
            "intervals": [0, 2, 4, 7, 9],
            "description": "Pentatonic - oriental coding vibes"
        },
        "blues": {
            "intervals": [0, 3, 5, 6, 7, 10],
            "description": "Blues scale - jazzy bug hunting"
        },
        "dorian": {
            "intervals": [0, 2, 3, 5, 7, 9, 10],
            "description": "Dorian mode - sophisticated debugging"
        }
    }
    
    # Achievement System
    ACHIEVEMENTS = {
        "FIRST_STEPS": {
            "name": "First Steps",
            "description": "Complete your first debugging session",
            "condition": lambda stats: stats.get('score', 0) > 0
        },
        "COMBO_MASTER": {
            "name": "Combo Master",
            "description": "Achieve a 50+ combo",
            "condition": lambda stats: stats.get('max_combo', 0) >= 50
        },
        "PERFECTIONIST": {
            "name": "Perfectionist",
            "description": "Get 70% perfect hits",
            "condition": lambda stats: (stats.get('perfect', 0) / max(stats.get('total_actions', 1), 1)) >= 0.7
        },
        "ACCURACY_EXPERT": {
            "name": "Accuracy Expert",
            "description": "Achieve 90%+ accuracy",
            "condition": lambda stats: stats.get('accuracy', 0) >= 90
        },
        "HIGH_SCORER": {
            "name": "High Scorer",
            "description": "Score 10,000+ points",
            "condition": lambda stats: stats.get('score', 0) >= 10000
        },
        "LEGEND": {
            "name": "Debugging Legend",
            "description": "Score 50,000+ points with 95%+ accuracy",
            "condition": lambda stats: stats.get('score', 0) >= 50000 and stats.get('accuracy', 0) >= 95
        }
    }
    
    # ASCII Art Templates
    ASCII_TEMPLATES = {
        "loading_chars": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
        "matrix_chars": "01アカサタナハマヤラワ",
        "separator": "=" * 60,
        "border_h": "─",
        "border_v": "│",
        "corner_tl": "┌",
        "corner_tr": "┐",
        "corner_bl": "└",
        "corner_br": "┘"
    }
    
    @classmethod
    def get_default_log_path(cls):
        return cls.LOGS_DIR / "default.log"
    
    @classmethod
    def get_test_log_path(cls):
        return cls.LOGS_DIR / "test-app.log"
    
    @classmethod
    def validate_config(cls):
        """Validate that all required directories and files exist"""
        errors = []
        
        if not cls.SRC_DIR.exists():
            errors.append(f"Source directory not found: {cls.SRC_DIR}")
        
        if not cls.LOGS_DIR.exists():
            errors.append(f"Logs directory not found: {cls.LOGS_DIR}")
        
        if not cls.get_default_log_path().exists():
            errors.append(f"Default log file not found: {cls.get_default_log_path()}")
        
        return errors

# Environment-specific overrides
class DevelopmentConfig(GameConfig):
    DEBUG = True
    VERBOSE_LOGGING = True
    SHOW_FPS = True

class ProductionConfig(GameConfig):
    DEBUG = False
    VERBOSE_LOGGING = False
    SHOW_FPS = False

# Select configuration based on environment
ENV = os.getenv('BEATBUGGING_ENV', 'development')
if ENV == 'production':
    Config = ProductionConfig
else:
    Config = DevelopmentConfig
