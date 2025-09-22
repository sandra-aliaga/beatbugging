import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.box import HEAVY, DOUBLE_EDGE

BORDER_COLOR = "green"
ACCENT_COLOR = "bright_green"
PRIMARY_COLOR = "green"
ACCENT_STYLE = f"bold {ACCENT_COLOR}"

# Estados expandidos: 0=inactivo, 1=early, 2=almost_early, 3=perfect, 4=almost_late, 5=late

CELL_PERFECT = [
    "╔═════╗",
    "║ COO ║",  # Para la coordenada
    "║█████║",
    "╚═════╝"
]

CELL_ALMOST_LATE = [
    "╔═════╗",
    "║ COO ║", 
    "║▓▓▓▓▓║",
    "╚═════╝"
]

CELL_ALMOST_EARLY = [
    "┌─────┐",
    "│ COO │",  
    "│▒▒▒▒▒│",
    "└─────┘"
]

CELL_EARLY = [
    "┌─────┐",
    "│ COO │",  
    "│░░░░░│",
    "└─────┘"
]

CELL_INACTIVE = [
    "┌─────┐",
    "│     │",  
    "│     │",
    "└─────┘"
]

class Map:
    def __init__(self, size=5):
        self.console = Console()
        self.size = size
        self.active_coords = "AJ - SK - DL - EM - FN"
        self.actual_line = "Nothing to debug..."
        self.progress_value = 0
        self.health_value = 100
        self.row_labels = ['J', 'K', 'L', 'M', 'N'][:size]
        self.col_labels = ['A', 'S', 'D', 'E', 'F'][:size]
        self.grid_state = {f"{col}{row}": 0 for row in self.row_labels for col in self.col_labels}

    def update_cell(self, coordinate: str, is_active: bool):
        if coordinate in self.grid_state:
            self.grid_state[coordinate] = 3 if is_active else 0
    
    def set_cell_state(self, coordinate: str, state: int):
        if coordinate in self.grid_state and 0 <= state <= 5:  # ✅ Ahora soporta estados 0-5
            self.grid_state[coordinate] = state
    
    def transition_cell(self, coordinate: str, target_state: int, steps: int = 1):
        if coordinate not in self.grid_state:
            return
        current = self.grid_state[coordinate]
        if current < target_state:
            self.grid_state[coordinate] = min(current + steps, target_state)
        elif current > target_state:
            self.grid_state[coordinate] = max(current - steps, target_state)
    
    def set_active_coords(self, coords_string: str):
        self.active_coords = coords_string
    
    def set_actual_line(self, line_string: str): 
        self.actual_line = line_string if len(line_string) < 35 else line_string[0:35] + "..."

    def set_progress(self, value: int): 
        self.progress_value = max(0, min(100, value))
    
    def set_health(self, value: int): 
        self.health_value = max(0, min(100, value))

    def _create_header_layout(self) -> Layout:
        header_layout = Layout(name="header")
        header_layout.split_column(
            Layout(Panel(Text("BEATBUGGING DEBUGGING SYSTEM",
                              justify="center",
                              style="bold green"),
                              box=HEAVY,
                              border_style=BORDER_COLOR),
                              name="title"),
            Layout(name="info_panels", ratio=1)
        )
        
        info_panel_grid = Table.grid(expand=True)
        info_panel_grid.add_column(ratio=1)
        info_panel_grid.add_column(ratio=1)
        
        coords_panel = Panel(Text(self.active_coords,
                                  justify="center",
                                  style=PRIMARY_COLOR),
                                  title=f"[{ACCENT_STYLE}]NEXT ACTIONS[/]",
                                  border_style=BORDER_COLOR)
        line_panel = Panel(Text(self.actual_line,
                                justify="left",
                                style=PRIMARY_COLOR),
                                title=f"[{ACCENT_STYLE}]DEBUGGING LINE...[/]",
                                border_style=BORDER_COLOR)
        
        info_panel_grid.add_row(coords_panel, line_panel)
        header_layout["info_panels"].update(info_panel_grid)
        
        return header_layout

    def _create_vertical_bar(self, value: int, height: int = 20) -> Text:
        
        filled_count = int((value / 100) * height)
        empty_count = height - filled_count
        
        fill_char = Text("██████", style="bright_green")
        empty_char = Text("░░░░░░", style="dim green")
        
        bar_chars = ([empty_char] * empty_count) + ([fill_char] * filled_count)
        return Text("\n").join(bar_chars)

    def _create_stats_panel(self) -> Panel:
        stats_grid = Table.grid(expand=True, padding=(0, 2))
        stats_grid.add_column(ratio=1, justify="center")
        stats_grid.add_column(ratio=1, justify="center")

        health_bar = self._create_vertical_bar(self.health_value)
        health_title = Text(f"HEALTH\n{self.health_value}%", 
                          justify="center", 
                          style="bold bright_green")
        health_display = Text.assemble(health_title, "\n\n", health_bar)

        progress_bar = self._create_vertical_bar(self.progress_value)
        progress_title = Text(f"PROGRESS\n{self.progress_value}%", 
                            justify="center", 
                            style="bold bright_green")
        progress_display = Text.assemble(progress_title, "\n\n", progress_bar)
        
        stats_grid.add_row(
            Align.center(health_display),
            Align.center(progress_display)
        )
        
        return Panel(
            Align.center(stats_grid, vertical="middle"),
            border_style=BORDER_COLOR,
            title=f"[{ACCENT_STYLE}]SYSTEM CORE[/]",
            box=DOUBLE_EDGE,
            expand=True
        )

    def _get_cell_display(self, coord: str, state: int):
        cell_templates = [
            CELL_INACTIVE,      # Estado 0: Inactivo 
            CELL_EARLY,         # Estado 1: Early - apenas visible
            CELL_ALMOST_EARLY,  # Estado 2: Almost Early - más visible
            CELL_PERFECT,       # Estado 3: Perfect - completamente visible
            CELL_ALMOST_LATE,   # Estado 4: Almost Late - desvaneciendo
            CELL_EARLY          # Estado 5: Late - muy tenue (reutiliza early)
        ]
        
        # Estilos con colores mejorados basados en timing
        styles = [
            "dim green",                    # Estado 0: Inactivo
            "dim blue",                     # Estado 1: Early
            "blue",                         # Estado 2: Almost Early  
            "bold blink bright_green",      # Estado 3: Perfect - ¡momento exacto!
            "yellow",                       # Estado 4: Almost Late
            "dim orange"                    # Estado 5: Late
        ]
        
        # Asegurar que el estado esté en rango válido
        state = max(0, min(state, len(cell_templates) - 1))
        
        cell = cell_templates[state].copy()
        style = styles[state]
        
        cell[1] = cell[1].replace("COO", coord[0] + "-" + coord[1])
        
        return [Text(line, style=style) for line in cell]

    def _create_map_display(self) -> Panel:
        map_table = Table(
            box=None,
            show_header=False,
            padding=0,
            pad_edge=False,
            expand=True
        )
        
        map_table.add_column(justify="center", style="green bold", width=3)
        
        for _ in self.col_labels:
            map_table.add_column(justify="center", width=8)

        for row_idx, row_label in enumerate(self.row_labels):
            for line_idx in range(4):
                row_content = []
                
                if line_idx == 2:
                    row_content.append(f" {row_label} ")
                else:
                    row_content.append("")
                
                for col_label in self.col_labels:
                    coord = f"{col_label}{row_label}"
                    state = self.grid_state.get(coord, 0)
                    cell_lines = self._get_cell_display(coord, state)
                    row_content.append(cell_lines[line_idx])
                
                map_table.add_row(*row_content)
            
            if row_idx < len(self.row_labels) - 1:
                map_table.add_row()

        col_header_row = [""] + [Text(f"   {label}   ", style="bold green") for label in self.col_labels]
        map_table.add_row(*col_header_row)

        return Panel(
            Align.center(map_table, vertical="middle"),
            border_style=BORDER_COLOR,
            title=f"[{ACCENT_STYLE}]BEATBUGGING MATRIX[/]",
            box=DOUBLE_EDGE,
            expand=True
        )

    def build_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(self._create_header_layout(), name="header", size=7), 
            Layout(name="main", ratio=1),
        )
        
        main_content_grid = Table.grid(expand=True, padding=1)
        main_content_grid.add_column(ratio=2)
        main_content_grid.add_column(ratio=1)
        
        main_content_grid.add_row(
            self._create_map_display(),
            self._create_stats_panel()
        )
        
        layout["main"].update(main_content_grid)
        return layout

    def run_demo(self):
        actions = ["AJ", "SK", "DL", "EM", "FN", "AJ", "SK", "DL"]
        
        with Live(self.build_layout(), screen=True, redirect_stderr=False, vertical_overflow="visible") as live:
            for i, coord in enumerate(actions):
                health = max(0, 100 - (i * 15))
                progress = (i + 1) * (100 / len(actions))
                self.set_health(health)
                self.set_progress(progress)
                
                for state in range(1, 4):
                    self.set_cell_state(coord, state)
                    self.set_actual_line(f"TRACE {i*128:04x}: Preparing node '{coord}'... State {state}")
                    live.update(self.build_layout())
                    time.sleep(0.2)
                
                self.set_actual_line(f"TRACE {i*128:04x}: ACTIVE! Press '{coord}' NOW!")
                if i < len(actions) - 1:
                    self.set_active_coords(f"UPCOMING: {actions[i+1]}")
                else:
                    self.set_active_coords(">> SEQUENCE COMPLETE <<")
                
                live.update(self.build_layout())
                time.sleep(0.5)
                
                self.set_cell_state(coord, 0)
                live.update(self.build_layout())
                time.sleep(0.3)
            
            time.sleep(2)


if __name__ == "__main__":
    game_map = Map(size=5)
    try:
        game_map.run_demo()
    except KeyboardInterrupt:
        print("\n[bold red]>> SESSION TERMINATED BY USER <<[/bold red]")

"""
Metodos para manejar estados:
- set_cell_state(coord, state): Establece directamente el estado (0-3)
- transition_cell(coord, target, steps): Transición gradual entre estados
- update_cell(coord, is_active): Compatibilidad - activa (3) o desactiva (0)
"""