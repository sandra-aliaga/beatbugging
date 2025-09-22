# Documentación del Módulo Music

Este módulo contiene las funcionalidades principales para convertir archivos de log en música y generar datos de gameplay para el juego BeatBugging.

## Archivos del Módulo

- `generator.py` - Generador principal de música desde logs
- `log_utils.py` - Utilidades para parsear y procesar archivos de log

---

## generator.py

### Clase Principal: `LogMusicGenerator`

Clase responsable de convertir archivos de log en música procedural y generar datos de gameplay correspondientes.

#### Constructor

```python
def __init__(self, log_path="none")
```

**Parámetros:**
- `log_path` (str): Ruta al archivo de log. Si es "none", se usará el log por defecto.

**Atributos inicializados:**
- `log_path`: Ruta del archivo de log
- `fileState`: Estado booleano del archivo (True si existe)
- `musicState`: Estado de la música (reservado para futuras funcionalidades)
- `default_path`: Ruta por defecto al archivo `test-app.log`
- `scale`: Escala musical seleccionada
- `freq`: Frecuencia base
- `rate`: Tasa de muestreo de audio
- `coords`: Diccionario de coordenadas (reservado)
- `waves`: Diccionario de funciones de ondas disponibles
- `grid_columns`: Lista de columnas del grid de juego ['A', 'S', 'D', 'E', 'F']
- `grid_rows`: Lista de filas del grid de juego ['J', 'K', 'L', 'M', 'N']

#### Métodos Públicos

##### `useDefaultLog()`
Configura el generador para usar el archivo de log por defecto (`logs/test-app.log`).

##### `generate_music(scale="minor", freq=440, rate=44100, speed=2.0)`
Método principal que genera música y datos de gameplay desde el archivo de log.

**Parámetros:**
- `scale` (str): Escala musical ("minor", "major", "pentatonic", "blues")
- `freq` (float): Frecuencia base en Hz (por defecto 440Hz = A4)
- `rate` (int): Tasa de muestreo en Hz (por defecto 44100Hz)
- `speed` (float): Multiplicador de velocidad (mayor valor = más rápido)

**Retorna:**
```python
{
    "audio_data": np.array,          # Datos de audio en formato int16
    "sample_rate": int,              # Tasa de muestreo utilizada
    "scale_used": str,               # Escala musical utilizada
    "speed_multiplier": float,       # Multiplicador de velocidad aplicado
    "gameplay_actions": list         # Lista de acciones para el gameplay
}
```

**Estructura de `gameplay_actions`:**
```python
{
    "line": str,           # Línea original del log
    "tiempo": float,       # Tiempo en segundos desde el inicio
    "coordenada": str,     # Coordenada del grid (ej: "A1", "S2")
    "tipo": str,           # Tipo de acción ("tap" o "hold")
    "duracion": float      # Duración de la acción (0 para tap)
}
```

#### Métodos Privados

##### `__generate_scale_notes()`
Genera las notas musicales para la escala seleccionada.

**Escalas disponibles:**
- `minor`: Escala menor natural - sonido melancólico [0, 2, 3, 5, 7, 8, 10]
- `major`: Escala mayor - sonido alegre/brillante [0, 2, 4, 5, 7, 9, 11]
- `pentatonic`: Pentatónica - sonido oriental/folk [0, 2, 4, 7, 9]
- `blues`: Escala blues - sonido jazzy [0, 3, 5, 6, 7, 10]

**Retorna:** Lista de diccionarios con `{"midi": int, "freq": float}`

##### Funciones de Ondas

Todas las funciones de onda reciben los mismos parámetros:
- `freq` (float): Frecuencia en Hz
- `duration` (float): Duración en segundos
- `volume` (float): Volumen (0.0 a 1.0)

###### `__sin_wave(freq, duration, volume=0.5)`
Genera una onda senoidal suave usando la fórmula: `volume * sin(2π * freq * t)`

###### `__square_wave(freq, duration, volume=0.5)`
Genera una onda cuadrada usando: `volume * sign(sin(2π * freq * t))`

###### `__saw_wave(freq, duration, volume=0.5)`
Genera una onda de diente de sierra usando: `volume * 0.5 * (t * freq - floor(t * freq + 0.5))`

###### `__triangle_wave(freq, duration, volume=0.5)`
Genera una onda triangular usando: `volume * 0.5 * |2 * (t * freq - floor(t * freq + 0.5))| - volume`

##### `_select_wave_severity(log_line)`
Selecciona el tipo de onda basado en la severidad del log.

**Mapeo de severidad:**
- `DEBUG` → `sin` (onda suave)
- `INFO` → `triangle` (onda moderada)
- `WARNING` → `square` (onda agresiva)
- `ERROR` → `saw` (onda muy agresiva)
- Otro → `triangle` (por defecto)

##### `_generate_wave_sample(wave_type, freq, duration, volume)`
Genera una muestra de audio usando el tipo de onda especificado.

##### `_generate_coordinate(note_info, original_line)`
Genera coordenadas del grid de juego basadas en el hash MIDI de la nota.

**Algoritmo:**
- `col_index = midi_hash % len(grid_columns)`
- `row_index = (midi_hash // len(grid_columns)) % len(grid_rows)`

##### `_determine_action_type(original_line, duration)`
Determina si la acción del juego debe ser "tap" o "hold".

**Lógica:**
- `ERROR` → siempre "hold"
- `WARNING` con duración > 0.5s → "hold"
- Otros casos → "tap"

#### Función Principal

##### `main()`
Función de prueba que:
1. Crea un generador con el log por defecto
2. Genera música en escala pentatónica a velocidad 2.0x
3. Muestra las acciones de gameplay generadas
4. Reproduce el audio usando pygame (opcional)

---

## log_utils.py

### Clase Principal: `LogMusic`

Clase utilitaria para leer, parsear y convertir archivos de log en datos musicales estructurados.

#### Atributos de Clase

- `path`: Ruta por defecto al archivo `test-app.log`
- `size`: Rango MIDI (0-127) para mapear hashes a notas
- `log_path`: Ruta del archivo de log actual

#### Constructor

```python
def __init__(self, log_path: str | Path | None = None)
```

**Parámetros:**
- `log_path`: Ruta al archivo de log. Si es None, usa la ruta por defecto.

**Excepciones:**
- `FileNotFoundError`: Si el archivo especificado no existe.

#### Métodos Públicos

##### `generate_music()`
Método de prueba que lee el archivo de log y muestra la cantidad de notas extraídas.

##### `read_log_file(log_path=None, default_path=None, encoding='utf-8')`
Lee un archivo de log y retorna las líneas como lista de strings.

**Parámetros:**
- `log_path`: Ruta primaria al archivo
- `default_path`: Ruta de respaldo
- `encoding`: Codificación del archivo (por defecto UTF-8)

**Retorna:** Lista de strings (líneas del log sin espacios en blanco)

**Comportamiento:**
1. Intenta leer `log_path` si existe
2. Si falla, intenta `default_path`
3. Si ambos fallan, retorna lista vacía
4. Filtra líneas vacías automáticamente

##### `parse_log_line(line: str) -> dict`
Parsea una línea de log individual y retorna un diccionario estructurado.

**Formatos soportados:**

1. **JSON válido**: Retorna el dict directamente
2. **Logcat (Android)**: Parsea formato tipo:
   ```
   2024-01-01 12:00:00.123 1234-5678 TAG PACKAGE LEVEL mensaje
   ```
   Campos extraídos: `fecha`, `pid_tid`, `tag`, `paquete`, `nivel`, `mensaje`

3. **Logs con timestamp en corchetes**:
   ```
   [2024-01-01 12:00:00] LEVEL mensaje
   ```
   Campos extraídos: `fecha`, `nivel`, `mensaje`

4. **Fallback**: `{"mensaje": line}` para cualquier otro formato

**Parámetros:**
- `line` (str): Línea de log a parsear

**Retorna:** Diccionario con los campos extraídos

##### `log_lines_to_dicts(log_lines)`
Convierte lista de líneas de log en lista de "notas musicales" estructuradas.

**Algoritmo de conversión:**
1. Parsea cada línea con `parse_log_line()`
2. Genera hash SHA-256 estable de todos los campos
3. Convierte hash a número entero
4. Mapea número a nota MIDI (0-127)
5. Convierte nota MIDI a frecuencia Hz usando A4=440Hz
6. Determina duración según nivel de log
7. Calcula volumen según longitud del mensaje

**Mapeo de duración por nivel:**
- `INFO` / `I`: 0.4 segundos
- `DEBUG` / `D`: 0.3 segundos  
- `WARNING` / `W`: 0.6 segundos
- `ERROR` / `E`: 0.8 segundos
- Otro: 0.5 segundos

**Cálculo de volumen:**
```python
volume = min(1.0, 0.5 + (len(mensaje) % 50) / 100)
```

**Retorna:** Lista de diccionarios con estructura:
```python
{
    "midi": int,        # Nota MIDI (0-127)
    "freq": float,      # Frecuencia en Hz
    "duration": float,  # Duración en segundos
    "volume": float,    # Volumen (0.0-1.0)
    "raw": dict         # Datos originales parseados
}
```

#### Patrones de Expresiones Regulares

##### `LOGCAT_PATTERN`
```regex
^(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)?\s*
(?P<pid_tid>\d+-\d+)?\s*
(?P<tag>[A-Za-z0-9._]+)?\s*
(?P<paquete>[A-Za-z0-9._]+)?\s*
(?P<nivel>[VDIWEF])?\s*
(?P<mensaje>.*)
```

##### `BRACKET_PATTERN`
```regex
^\[(?P<fecha>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+
(?P<nivel>[A-Z]+)\s+
(?P<mensaje>.*)
```

### Instancia Global

```python
log_music = LogMusic()
log_music.generate_music()
```

Se crea una instancia global que ejecuta una prueba básica del sistema.

---

## Flujo de Trabajo Completo

1. **Lectura de logs**: `LogMusic.read_log_file()` lee el archivo
2. **Parseo**: `LogMusic.parse_log_line()` estructura cada línea
3. **Conversión musical**: `LogMusic.log_lines_to_dicts()` convierte a notas
4. **Generación de escalas**: `LogMusicGenerator.__generate_scale_notes()` crea la escala
5. **Selección de ondas**: `LogMusicGenerator._select_wave_severity()` elige tipo de onda
6. **Generación de audio**: Funciones de onda crean muestras de audio
7. **Datos de gameplay**: Se generan coordenadas y tipos de acción
8. **Compilación final**: Se combinan todas las muestras en audio completo

## Dependencias

- `numpy`: Para generación de ondas y manipulación de arrays
- `pygame`: Para reproducción de audio
- `pathlib`: Para manejo de rutas de archivos
- `hashlib`: Para generar hashes estables
- `json`: Para parsear logs en formato JSON
- `re`: Para expresiones regulares en parseo de logs
- `time`: Para funciones de temporización
- `os`: Para operaciones del sistema de archivos

## Notas Técnicas

- **Formato de audio**: Int16, tasa de muestreo configurable (por defecto 44.1kHz)
- **Rango MIDI**: 0-127 (estándar MIDI)
- **Escalas musicales**: Intervalos basados en semitonos desde nota base
- **Hash estable**: SHA-256 para mapeo consistente log→nota
- **Grid de juego**: 5x5 (25 posiciones totales)
- **Tipos de acción**: "tap" (instantáneo) y "hold" (duración extendida)
