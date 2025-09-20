import time
import os
import pygame as pg
import numpy as np
from .log_utils import LogMusic

class LogMusicGenerator:
    
    def __init__(self, log_path="none"):
        self.log_path = log_path
        self.fileState = False
        self.musicState = False
        self.default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs", "test-app.log")
        self.scale = ""
        self.freq = ""
        self.rate = ""
        self.coords = {}
        self.waves = {
            "sin": self.__sin_wave,
            "square": self.__square_wave,
            "saw": self.__saw_wave,
            "triangle": self.__triangle_wave
        }
        
        self.grid_columns = ['A', 'S', 'D', 'E', 'F']
        self.grid_rows = ['J', 'K', 'L', 'M', 'N']
        
        if self.log_path != "none":
            if os.path.isfile(self.log_path):
                self.fileState = True
                
                with open(self.log_path, "r") as f:
                    self.log_data = f.read()
            else:
                self.log_data = ""
        else:
            self.log_data = ""
    
    def useDefaultLog(self):
        self.log_path = self.default_path
        self.fileState = True
        
        if os.path.isfile(self.log_path):
            with open(self.log_path, "r") as f:
                self.log_data = f.read()
        else:
            self.log_data = ""
            
    def __generate_scale_notes(self):
        
        scales = {
            "minor": [0, 2, 3, 5, 7, 8, 10],  # Escala menor natural - sonido melancólico
            "major": [0, 2, 4, 5, 7, 9, 11],  # Escala mayor - sonido alegre/brillante
            "pentatonic": [0, 2, 4, 7, 9],    # Pentatónica - sonido oriental/folk
            "blues": [0, 3, 5, 6, 7, 10]      # Escala blues - sonido jazzy
        }
        
        if self.scale not in scales:
            self.scale = "minor"
            
        base_notes = scales[self.scale]
        notes = []

        for octave in range(3, 5):
            for interval in base_notes:
                # MIDI note 60 = C4 (Do central)
                midi_note = 60 + (octave - 4) * 12 + interval
                # Conversión MIDI a frecuencia Hz usando A4=440Hz como referencia
                freq = 440.0 * (2 ** ((midi_note - 69) / 12))
                notes.append({"midi": midi_note, "freq": freq})
        
        return notes
    
    def __sin_wave(self, freq, duration, volume=0.5):

        frames = int(duration * self.rate)  # Número de samples de audio
        t = np.linspace(0, duration, frames, False)  # Array de tiempo
        
        wave = volume * np.sin(2 * np.pi * freq * t)  # Fprmula onda senoidal
        return (wave * 32767).astype(np.int16)  # Convertir a formato audio 16-bit
    
    def __square_wave(self, freq, duration, volume=0.5):

        frames = int(duration * self.rate)
        t = np.linspace(0, duration, frames, False)
        wave = volume * np.sign(np.sin(2 * np.pi * freq * t))  # Solo valores +1 o -1
        return (wave * 32767).astype(np.int16)
    
    def __saw_wave(self, freq, duration, volume=0.5):

        frames = int(duration * self.rate)
        t = np.linspace(0, duration, frames, False)

        wave = volume * 0.5 *(t * freq - np.floor(t * freq + 0.5)) # quite un * 2 para q sea mas suave, ahora es ese 0.5 al lafo de volume
        return (wave * 32767).astype(np.int16)
    
    def __triangle_wave(self, freq, duration, volume=0.5):

        frames = int(duration * self.rate)
        t = np.linspace(0, duration, frames, False)

        wave = volume * 0.5 * np.abs(2 * (t * freq - np.floor(t * freq + 0.5))) - volume # lo mismo que saw
        return (wave * 32767).astype(np.int16)

    def _select_wave_severity(self, log_line):

        if "DEBUG" in log_line.upper():
            return "sin"
        elif "INFO" in log_line.upper():
            return "triangle"
        elif "WARNING" in log_line.upper():
            return "square"
        elif "ERROR" in log_line.upper():
            return "saw"
        else:
            return "triangle"

    def _generate_wave_sample(self, wave_type, freq, duration, volume):
        
        if wave_type in self.waves:
            return self.waves[wave_type](freq, duration, volume)
        else:
            return self.waves["sin"](freq, duration, volume)
    
    def _generate_coordinate(self, note_info, original_line):

        midi_hash = note_info["midi"]
        
        col_index = midi_hash % len(self.grid_columns)
        row_index = (midi_hash // len(self.grid_columns)) % len(self.grid_rows)
        
        column = self.grid_columns[col_index]
        row = self.grid_rows[row_index]
        
        return f"{column}{row}"
    
    def _determine_action_type(self, original_line, duration):

        # Determinar tipo de acción según severidad y duración
        if "ERROR" in original_line.upper():
            return "hold"  # Errores requieren hold para más atención
        elif "WARNING" in original_line.upper() and duration > 0.5:
            return "hold"  # Warnings largos también hold
        else:
            return "tap"   # DEBUG, INFO, y warnings cortos son tap
    
    def generate_music(self, scale="minor", freq=440, rate=44100, speed = 2.0):
        
        """
        FLUJO COMPLETO:
        1. Lee logs → LogMusic convierte a JSON
        2. Para cada nota JSON: detecta severidad → selecciona onda → genera audio
        3. Combina todas las muestras en secuencia musical
        """
        print("GENERANDO...")
        
        self.scale = scale
        self.freq = freq
        self.rate = rate
        
        if not self.fileState:
            self.useDefaultLog()
        
        log_music = LogMusic(self.log_path)
        log_lines = log_music.read_log_file()
        note_data = log_music.log_lines_to_dicts(log_lines)
        
        scale_notes = self.__generate_scale_notes()
        
        audio_samples = []
        gameplay_actions = []
        current_time = 0.0
        
        for i, note_info in enumerate(note_data):

            original_line = log_lines[i] if i < len(log_lines) else ""
            wave_type = self._select_wave_severity(original_line)
            

            midi_note_hash = note_info["midi"]
            scale_index = midi_note_hash % len(scale_notes)
            musical_freq = scale_notes[scale_index]["freq"]
            
            accelerated_duration = note_info["duration"] / speed
            accelerated_volume = note_info["volume"] * 0.4 
            
            sample = self._generate_wave_sample(wave_type, musical_freq, accelerated_duration, accelerated_volume)
            audio_samples.append(sample)
            
            # Generar datos de gameplay
            coordinate = self._generate_coordinate(note_info, original_line)
            action_type = self._determine_action_type(original_line, accelerated_duration)
            action_duration = accelerated_duration if action_type == "hold" else 0
            
            gameplay_action = {
                "tiempo": round(current_time, 2),
                "coordenada": coordinate,
                "tipo": action_type,
                "duracion": round(action_duration, 2)
            }
            
            gameplay_actions.append(gameplay_action)
            current_time += accelerated_duration
        
        if audio_samples:
            full_audio = np.concatenate(audio_samples)
        else:
            full_audio = np.array([], dtype=np.int16)
        
        return {
            "audio_data": full_audio,
            "sample_rate": self.rate,
            "scale_used": self.scale,
            "speed_multiplier": speed,
            "gameplay_actions": gameplay_actions
        }


def main():
    """
    FUNCIÓN DE PRUEBA:
    - Genera música desde default.log
    - Muestra estadísticas del proceso
    - Reproduce el audio generado (opcional)
    """
    
    # Crear generador (usará default.log automáticamente)
    generator = LogMusicGenerator()

    result = generator.generate_music(scale="pentatonic", rate=44100, speed=2.0)

    for i, action in enumerate(result['gameplay_actions']):
        print(f"  {i+1}. {action}")
    
    try:
        print(f"\nReproduciendo audio...")
        pg.mixer.init(frequency=result['sample_rate'], size=-16, channels=2, buffer=1024)
        
        sound_array = result['audio_data']
        # Convertir a estéreo si es mono
        if sound_array.ndim == 1:
            sound_array = np.column_stack((sound_array, sound_array))
        sound = pg.sndarray.make_sound(sound_array)
        
        print("   ▶ Presiona Enter para reproducir, Ctrl+C para salir")
        input()
        sound.play()
        pg.mixer.music.set_volume(0.5)  # Ajustar volumen
        
        while pg.mixer.get_busy():
            time.sleep(0.1)
            
        print(" Reproducción completada")
        
    except Exception as e:
        print(f"     No se pudo reproducir audio: {e}")
        print(f"    Audio generado correctamente (datos disponibles)")
    
    print("\n Prueba completada!")


if __name__ == "__main__":
    main()