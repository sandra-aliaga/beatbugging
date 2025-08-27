import json
from pathlib import Path
import hashlib
import json
import hashlib
from pathlib import Path

class LogMusic:

    path = Path(__file__).resolve().parents[2] / "logs" / "default.log"
    size = 128  # Rango MIDI (0–127)

    def __init__(self, log_path: str | Path | None = None):
        chosen = Path(log_path) if log_path is not None else self.__class__.path
        if not chosen.is_file():
            raise FileNotFoundError(f"No se encontró el log: {chosen}")
        self.log_path = chosen

    def generate_music(self):
        log_lines = self.read_log_file(self.log_path)
        log_notes = self.log_lines_to_dicts(log_lines)
        # Aquí se generarían los sonidos reales
        for note in log_notes:
            print(note)

    def read_log_file(self, log_path=None, default_path=None, encoding='utf-8'):
        primary = Path(log_path) if log_path is not None else self.log_path
        fallback = Path(default_path) if default_path is not None else self.__class__.path

        if primary.exists() and primary.is_file():
            chosen = primary
        elif fallback.exists() and fallback.is_file():
            chosen = fallback
        else:
            return []

        with chosen.open('r', encoding=encoding, errors='replace') as f:
            return [line.strip() for line in f if line.strip()]

    def log_lines_to_dicts(self, log_lines):
        """
        Convierte cada línea del log en una nota musical:
        log → cadena → hash → entero → número MIDI → frecuencia Hz → nota
        """
        result = []

        for line in log_lines:
            # 1. Preparamos el texto base para hashear
            try:
                entry = json.loads(line)
                hash_input = json.dumps(entry, sort_keys=True)
                keyword = "JSON"
                mensaje = line
            except json.JSONDecodeError:
                parts = line.split(maxsplit=2)
                if len(parts) >= 3:
                    fecha, keyword, mensaje = parts[0], parts[1], parts[2]
                elif len(parts) == 2:
                    fecha, keyword, mensaje = parts[0], parts[1], ""
                else:
                    fecha, keyword, mensaje = "N/A", "UNKNOWN", line

                hash_input = f"{fecha}|{keyword}|{len(mensaje)}|{len(mensaje.split())}"

            # 2. Hash → número entero
            digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
            number = int.from_bytes(digest, byteorder="big")

            # 3. Convertir a nota MIDI
            midi_note = number % self.__class__.size

            # 4. Convertir a frecuencia Hz
            freq = 440.0 * (2 ** ((midi_note - 69) / 12))

            # 5. Determinar duración según severidad o longitud
            if keyword.upper().startswith("INFO"):
                duration = 0.4
            elif keyword.upper().startswith("DEBUG"):
                duration = 0.3
            elif keyword.upper().startswith("WARNING"):
                duration = 0.6
            elif keyword.upper().startswith("ERROR"):
                duration = 0.8
            else:
                duration = 0.5

            # 6. Determinar volumen (más largo el mensaje → más fuerte)
            volume = min(1.0, 0.5 + (len(mensaje) % 50) / 100)

            # 7. Construir objeto nota
            note = {
                "midi": midi_note,
                "freq": round(freq, 2),
                "duration": duration,
                "volume": round(volume, 2)
            }

            result.append(note)

        return result


log_music = LogMusic()
log_music.generate_music()

