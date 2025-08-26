import os
import json
from pathlib import Path
import hashlib

class LogMusic:

    path = Path(__file__).resolve().parents[2] / "logs" / "default.log"
    size = 128
    """
    # Escala cromática
    log_music.log_lines_to_dicts(logs, size=12)
    # → [{3}, {7}, {0}]

    # Piano completo
    log_music.log_lines_to_dicts(logs, size=88)
    # → [{61}, {92}, {12}]

    # Notas MIDI
    log_music.log_lines_to_dicts(logs, size=128)
    # → [{61}, {92}, {12}]
    """

    def __init__(self, log_path: str | Path | None = None):
        chosen = Path(log_path) if log_path is not None else self.__class__.path
        if not chosen.is_file():
            raise FileNotFoundError(f"No se encontró el log: {chosen}")
        self.log_path = chosen


    def generate_music(self):
        log_lines = self.read_log_file(self.log_path)
        log_hashes = self.log_lines_to_dicts(log_lines)
        # Aquí iría la lógica para generar música a partir de los logs
        for log_hash in log_hashes:
            print(log_hash)

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
        result = []
        for line in log_lines:
            try:
                entry = json.loads(line)
                hash_input = json.dumps(entry, sort_keys=True)
            except json.JSONDecodeError:
                parts = line.split(maxsplit=2)
                if len(parts) >= 3:
                    fecha, keyword, mensaje = parts[0], parts[1], parts[2]
                elif len(parts) == 2:
                    fecha, keyword, mensaje = parts[0], parts[1], ""
                else:
                    fecha, keyword, mensaje = "N/A", "UNKNOWN", line

                hash_input = f"{fecha}|{keyword}|{len(mensaje)}|{len(mensaje.split())}"

            # Hash -> entero -> módulo para rango fijo
            digest = hashlib.sha256(hash_input.encode("utf-8")).digest()

            number = int.from_bytes(digest, byteorder="big") % self.__class__.size

            result.append({number})

        return result

# Ejemplo de uso:
log_music = LogMusic()
log_music.generate_music()
