import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align

class Map:
    def __init__(self, size=5, active_coords="AJ - SK - DL - EM - FN"):
        self.console = Console()
        self.size = size
        self.active_coords = active_coords 
        self.row_labels = ['J', 'K', 'L', 'M', 'N'][:size]  # Filas del generador
        self.col_labels = ['A', 'S', 'D', 'E', 'F'][:size]  # Columnas del generador
        
        self.grid_state = {
            f"{col}{row}": False
            for row in self.row_labels
            for col in self.col_labels
        }
        
        self.progress_value = 0
        self.health_value = 100

    def update_cell(self, coordinate: str, is_active: bool):
        if coordinate in self.grid_state:
            self.grid_state[coordinate] = is_active

    def set_active_coords(self, coords_string: str):
        self.active_coords = coords_string

    def set_progress(self, value: int):
        self.progress_value = max(0, min(100, value))

    def set_health(self, value: int):
        self.health_value = max(0, min(100, value))

    def _create_header_panel(self) -> Panel:
        return Panel(
            Text("Fixing...", justify="center", style="bold green"),
            border_style="green",
            height=3
        )

    def _create_status_panel(self, status_text: str) -> Panel:
        current_time = time.strftime("%H:%M:%S")
        line_text = status_text if status_text != "" else f"Line 17: {current_time} [DEBUG]... {status_text}"
        return Panel(
            Text(line_text, justify="center", style="green"),
            border_style="green",
            height=3
        )

    def _create_coordinates_panel(self) -> Panel:
        return Panel(
            Text(self.active_coords, justify="center", style="green"),
            border_style="green",
            height=3
        )

    def _create_map_display(self) -> Panel:
        CELL_PART_ACTIVE = "██████"
        CELL_PART_INACTIVE = "░░░░░░"
        
        map_table = Table(box=None, show_header=False, padding=0, pad_edge=False)
        
        map_table.add_column(justify="center", style="green bold", width=3)

        for _ in self.col_labels:
            map_table.add_column(justify="center")
        
        for row_label in self.row_labels:
            top_parts = [" "]
            middle_parts = [f" {row_label} "] 
            bottom_parts = [" "]
            
            for col_label in self.col_labels:
                coordinate = f"{col_label}{row_label}"
                is_active = self.grid_state.get(coordinate, False)
                
                cell_chars = CELL_PART_ACTIVE if is_active else CELL_PART_INACTIVE
                style = "green" if is_active else "dim green"
                cell_text = Text(cell_chars, style=style)
                
                top_parts.append(cell_text)
                middle_parts.append(cell_text)
                bottom_parts.append(cell_text)
            
            map_table.add_row(*top_parts)
            map_table.add_row(*middle_parts)
            map_table.add_row(*bottom_parts)
        
        empty_row = [" "] + [Text("") for _ in self.col_labels]
        map_table.add_row(*empty_row)
        
        col_labels_row = [" "]
        for label in self.col_labels:

            centered_label = f"   {label}   "
            col_labels_row.append(Text(centered_label, style="green bold"))
        map_table.add_row(*col_labels_row)
        
        centered_map = Align.center(map_table, vertical="middle")
        
        return Panel(centered_map, border_style="green")

    def _create_progress_bar(self, value: int, max_value: int = 100) -> str:

        bar_width = 50
        filled = int((value / max_value) * bar_width)
        empty = bar_width - filled
        return "█" * filled + "░" * empty

    def _create_bars_panel(self) -> Panel:

        progress_bar = self._create_progress_bar(self.progress_value)
        progress_text = Text(f"Progress: {progress_bar} {self.progress_value}%", style="green")
        
        # Barra de vida
        health_bar = self._create_progress_bar(self.health_value)
        # Color de la barra de vida según el valor
        if self.health_value > 60:
            health_style = "green"
        elif self.health_value > 30:
            health_style = "yellow"
        else:
            health_style = "red"
        health_text = Text(f"Health:   {health_bar} {self.health_value}%", style=health_style)
        
        # Combinar ambas barras en un layout
        bars_table = Table(box=None, show_header=False, padding=0)
        bars_table.add_column()
        bars_table.add_row(progress_text)
        bars_table.add_row(health_text)
        
        return Panel(bars_table, border_style="green", height=4)

    def build_layout(self, status_text="System Ready...") -> Layout:
        """Construye el layout completo de la interfaz."""
        layout = Layout()
        
        layout.split_column(
            Layout(self._create_header_panel(), name="header", size=3),
            Layout(self._create_status_panel(status_text), name="status", size=3),
            Layout(self._create_coordinates_panel(), name="coords", size=3),
            Layout(self._create_map_display(), name="map"),
            Layout(self._create_bars_panel(), name="bars", size=4)
        )
        
        return layout

    def run_demo(self):
        """Ejecuta una demostración animada."""
        checkerboard_pattern = [
            "ha", "ka", "ua",
            "js", "ys",
            "hd", "kd", "ud",
            "jf", "yf",
            "hg", "kg", "ug"
        ]
        
        with Live(self.build_layout(), screen=True, redirect_stderr=False) as live:
            # Estado inicial
            live.update(self.build_layout("Initializing sequence..."))
            time.sleep(1)
            
            # Activar el patrón de tablero
            for coord in checkerboard_pattern:
                self.update_cell(coord, is_active=True)
            live.update(self.build_layout("Pattern loaded..."))
            time.sleep(2)
            
            # Demostración animada con cambios en las barras
            statuses = [
                ("Scanning sectors...", 40, 70),
                ("Processing data...", 60, 65),
                ("Analyzing patterns...", 80, 60),
                ("Optimization complete.", 100, 75)
            ]
            
            for status, progress, health in statuses:
                self.set_progress(progress)
                self.set_health(health)
                live.update(self.build_layout(status))
                time.sleep(1.5)
            
            self.set_active_coords("ha - js - kd - yf - ug")
            live.update(self.build_layout("Coordinates updated."))
            time.sleep(2)
            
            for _ in range(3):
                # Desactivar algunas celdas
                for coord in ["js", "yf", "kd"]:
                    self.update_cell(coord, is_active=False)
                self.set_health(self.health_value - 5)
                live.update(self.build_layout("System check..."))
                time.sleep(0.3)
                
                # Reactivarlas
                for coord in ["js", "yf", "kd"]:
                    self.update_cell(coord, is_active=True)
                self.set_health(self.health_value + 5)
                live.update(self.build_layout("System stable..."))
                time.sleep(0.3)
            
            live.update(self.build_layout("Sequence complete. System idle."))
            time.sleep(2)


if __name__ == "__main__":
    # === EJEMPLO DE USO PARA INTEGRACIÓN CON LÓGICA DE JUEGO ===
    
    # Crear el mapa con coordenadas personalizadas
    game_map = Map(size=5, active_coords="ah - sj - kd - dh - fu")
    
    # --- Ejemplos de cómo cambiar celdas individualmente ---
    # game_map.activate_cell("ha")     # Activa la celda ha (la pone verde)
    # game_map.deactivate_cell("ha")   # Desactiva la celda ha (la pone gris)
    
    # --- Ejemplos de cómo cambiar múltiples celdas ---
    # game_map.activate_multiple_cells(["ha", "js", "kd", "yf", "ug"])
    # game_map.deactivate_multiple_cells(["ha", "js"])
    
    # --- Ejemplo de cómo limpiar todo el mapa ---
    # game_map.clear_all_cells()
    
    # --- Ejemplo de cómo verificar el estado de una celda ---
    # if game_map.get_cell_state("ha"):
    #     print("La celda ha está activa")
    
    # --- Ejemplo de cómo actualizar las barras ---
    # game_map.set_progress(50)  # Poner progreso al 50%
    # game_map.set_health(80)    # Poner vida al 80%
    
    # --- Ejemplo de cómo cambiar las coordenadas mostradas ---
    # game_map.set_active_coords("ha - js - kf - yg - ud")

    
    try:
        # Ejecutar la demostración por defecto
        game_map.run_demo()
    except KeyboardInterrupt:
        print("\n[bold red]Demo interrupted by user.[/bold red]")