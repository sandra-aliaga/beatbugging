import json
from pathlib import Path
import hashlib
import json
import hashlib
from pathlib import Path
import re

class LogMusic:

    path = Path(__file__).resolve().parents[2] / "logs" / "test-app.log"
    size = 128  # Rango MIDI (0–127)
    log_path = None

    def __init__(self, log_path: str | Path | None = None):
        chosen = Path(log_path) if log_path is not None else self.__class__.path
        if not chosen.is_file():
            raise FileNotFoundError(f"No se encontró el log: {chosen}")
        self.log_path = chosen

    def generate_music(self):
        log_lines = self.read_log_file(self.log_path)
        log_notes = self.log_lines_to_dicts(log_lines)
        print("Cantidad de notas extraidas: " + str(len(log_notes)))

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

    def parse_log_line(self, line: str) -> dict:
        """
        Parsea una línea de log y devuelve un diccionario estructurado.
        
        Formatos soportados:
        1. JSON válido → dict directamente.
        2. Logcat (Android) → fecha, pid_tid, tag, paquete, nivel, mensaje.
        3. Logs con timestamp en corchetes [YYYY-MM-DD HH:MM:SS] NIVEL mensaje.
        4. Fallback: {"mensaje": line}
        """

        # --- 1. Intentar JSON ---
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            pass

        # --- 2. Intentar formato Logcat ---
        LOGCAT_PATTERN = re.compile(
            r"^(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)?\s*"
            r"(?P<pid_tid>\d+-\d+)?\s*"
            r"(?P<tag>[A-Za-z0-9._]+)?\s*"
            r"(?P<paquete>[A-Za-z0-9._]+)?\s*"
            r"(?P<nivel>[VDIWEF])?\s*"
            r"(?P<mensaje>.*)"
        )
        m = LOGCAT_PATTERN.match(line)
        if m and any(m.groupdict().values()):
            parsed = {k: v for k, v in m.groupdict().items() if v}
            if parsed:  # solo devolver si no está vacío
                return parsed

        # --- 3. Intentar formato diferente, puede modificarse---
        BRACKET_PATTERN = re.compile(
            r"^\[(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+"
            r"(?P<nivel>[A-Z]+)\s+"
            r"(?P<mensaje>.*)"
        )
        m = BRACKET_PATTERN.match(line)
        if m:
            return {k: v for k, v in m.groupdict().items() if v}

        # --- 4. Fallback ---
        return {"mensaje": line}

    def log_lines_to_dicts(self, log_lines):
        """
        Convierte cada línea de log en una 'nota musical'.
        Usa parse_log_line() para estructurar los campos.
        
        Flujo:
        1. Parsear línea con parse_log_line → dict con campos disponibles.
        2. Generar hash estable basado en los campos del log.
        3. Mapear hash → número entero → nota MIDI → frecuencia Hz.
        4. Determinar duración y volumen según nivel/mensaje.
        5. Devolver lista de notas.
        """

        result = []

        for line in log_lines:
            entry = self.parse_log_line(line)

            # --- 1. String único para hashear ---
            hash_input = "|".join(f"{k}:{v}" for k, v in sorted(entry.items()))

            # --- 2. Hash → número entero ---
            digest = hashlib.sha256(hash_input.encode("utf-8")).digest()
            number = int.from_bytes(digest, byteorder="big")

            # --- 3. Convertir a nota MIDI ---
            midi_note = number % self.__class__.size

            # --- 4. Convertir a frecuencia Hz ---
            freq = 440.0 * (2 ** ((midi_note - 69) / 12))

            # --- 5. Determinar duración según nivel ---
            nivel = entry.get("nivel", "").upper()
            if nivel.startswith("INFO") or nivel == "I":
                duration = 0.4
            elif nivel.startswith("DEBUG") or nivel == "D":
                duration = 0.3
            elif nivel.startswith("WARNING") or nivel == "W":
                duration = 0.6
            elif nivel.startswith("ERROR") or nivel == "E":
                duration = 0.8
            else:
                duration = 0.5

            # --- 6. Volumen según longitud del mensaje ---
            mensaje = entry.get("mensaje", "")
            volume = min(1.0, 0.5 + (len(mensaje) % 50) / 100)

            # --- 7. Construir objeto nota ---
            note = {
                "midi": midi_note,
                "freq": round(freq, 2),
                "duration": duration,
                "volume": round(volume, 2),
                "raw": entry
            }

            result.append(note)

        return result


log_music = LogMusic()
log_music.generate_music()

