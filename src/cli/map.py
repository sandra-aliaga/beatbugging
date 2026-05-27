import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.box import HEAVY, DOUBLE_EDGE

from settings import Settings

# Estados expandidos: 0=inactivo, 1=early, 2=almost_early, 3=perfect, 4=almost_late, 5=late

CELL_PERFECT = [
    "╔═════╗",
    "║ COO ║",
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

CELL_MISS = [
    "╔═════╗",
    "║ COO ║",
    "║✗✗✗✗✗║",
    "╚═════╝"
]

CELL_INACTIVE = [
    "┌─────┐",
    "│     │",
    "│     │",
    "└─────┘"
]

class Map:
    def __init__(self, size=5):
        self.console = Settings.make_console()
        self.size = size
        self.active_coords = "AJ - SK - DL - EM - FN"
        self.actual_line = "Nothing to debug..."
        self.progress_value = 0
        self.health_value = 100
        self.row_labels = ['J', 'K', 'L', 'M', 'N'][:size]
        self.col_labels = ['A', 'S', 'D', 'E', 'F'][:size]
        self.grid_state = {f"{col}{row}": 0 for row in self.row_labels for col in self.col_labels}

        self.current_input = ""
        self.input_status = "Type coordinate (e.g. AJ, SK)..."
        self.target_coordinate = "EM"
        self.success_count = 0

    def update_cell(self, coordinate: str, is_active: bool):
        if coordinate in self.grid_state:
            self.grid_state[coordinate] = 3 if is_active else 0

    def set_cell_state(self, coordinate: str, state: int):
        if coordinate in self.grid_state and 0 <= state <= 5:
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

    def set_input(self, input_text: str):
        self.current_input = input_text

    def set_input_status(self, status: str):
        self.input_status = status

    def clear_input(self):
        self.current_input = ""

    def set_target_coordinate(self, coordinate: str):
        self.target_coordinate = coordinate

    def increment_success(self):
        self.success_count += 1

    def reset_success(self):
        self.success_count = 0

    def _create_header_layout(self) -> Layout:
        header_layout = Layout(name="header")
        header_layout.split_column(
            Layout(Panel(Text("BEATBUGGING DEBUGGING SYSTEM",
                              justify="center",
                              style="primary.bold"),
                              box=HEAVY,
                              border_style="primary"),
                              name="title"),
            Layout(name="info_panels", ratio=1)
        )

        info_panel_grid = Table.grid(expand=True)
        info_panel_grid.add_column(ratio=1)
        info_panel_grid.add_column(ratio=1)

        coords_panel = Panel(Text(self.active_coords,
                                  justify="center",
                                  style="primary"),
                                  title="[accent.bold]NEXT ACTIONS[/]",
                                  border_style="primary")
        line_panel = Panel(Text(self.actual_line,
                                justify="left",
                                style="primary"),
                                title="[accent.bold]DEBUGGING LINE...[/]",
                                border_style="primary")

        info_panel_grid.add_row(coords_panel, line_panel)
        header_layout["info_panels"].update(info_panel_grid)

        return header_layout

    def _create_vertical_bar(self, value: int, height: int = 18) -> Text:
        filled_count = int((value / 100) * height)
        empty_count = height - filled_count

        fill_char = Text("██████", style="accent")
        empty_char = Text("░░░░░░", style="muted")

        bar_chars = ([empty_char] * empty_count) + ([fill_char] * filled_count)
        return Text("\n").join(bar_chars)

    def _create_stats_panel(self) -> Panel:
        stats_grid = Table.grid(expand=True, padding=(0, 2))
        stats_grid.add_column(ratio=1, justify="center")
        stats_grid.add_column(ratio=1, justify="center")

        health_bar = self._create_vertical_bar(self.health_value)
        health_title = Text(f"HEALTH\n{self.health_value}%",
                          justify="center",
                          style="accent.bold")
        health_display = Text.assemble(health_title, "\n\n", health_bar)

        progress_bar = self._create_vertical_bar(self.progress_value)
        progress_title = Text(f"PROGRESS\n{self.progress_value}%",
                            justify="center",
                            style="accent.bold")
        progress_display = Text.assemble(progress_title, "\n\n", progress_bar)

        stats_grid.add_row(
            Align.center(health_display),
            Align.center(progress_display)
        )

        return Panel(
            Align.center(stats_grid, vertical="middle"),
            border_style="primary",
            title="[accent.bold]SYSTEM CORE[/]",
            box=DOUBLE_EDGE,
            expand=True
        )

    def _get_cell_display(self, coord: str, state: int):
        cell_templates = [
            CELL_INACTIVE,
            CELL_EARLY,
            CELL_ALMOST_EARLY,
            CELL_PERFECT,
            CELL_ALMOST_LATE,
            CELL_MISS
        ]

        styles = [
            "muted",                                    # 0: inactive — follows theme
            "dim blue",                                 # 1: early
            "blue",                                     # 2: almost_early
            "bold blink bright_green on black",         # 3: perfect HIT — semantic green
            "bold bright_cyan on black",                # 4: SUCCESS HIT — semantic cyan
            "bold blink bright_red on black",           # 5: MISS — semantic red
        ]

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

        map_table.add_column(justify="center", style="primary.bold", width=3)

        for _ in self.col_labels:
            map_table.add_column(justify="center", width=8)

        col_header_row = [""] + [Text(f"   {label}   ", style="primary.bold") for label in self.col_labels]
        map_table.add_row(*col_header_row)

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

        return Panel(
            Align.center(map_table, vertical="middle"),
            border_style="primary",
            title="[accent.bold]BEATBUGGING MATRIX[/]",
            box=DOUBLE_EDGE,
            expand=True
        )

    def _create_line_panel(self) -> Panel:
        line_grid = Table.grid(expand=True, padding=(0, 1))
        line_grid.add_column(justify="left", width=8)
        line_grid.add_column(justify="left", ratio=1)
        line_grid.add_column(justify="right", width=12)

        line_grid.add_row(
            Text("Line:", style="accent.bold"),
            Text(self.target_coordinate, style="bold yellow"),
            Text(f"Success: {self.success_count}", style="accent.bold")
        )

        return Panel(
            line_grid,
            border_style="primary",
            height=3,
            expand=True
        )

    def _create_terminal_panel(self) -> Panel:
        terminal_grid = Table.grid(expand=True, padding=(0, 1))
        terminal_grid.add_column(justify="left", ratio=1)

        display_input = self.current_input + "_" if len(self.current_input) < 2 else self.current_input
        prompt_text = f"[user@01010]$ {display_input}"

        terminal_grid.add_row(
            Text(prompt_text, style="primary.bold")
        )

        return Panel(
            terminal_grid,
            border_style="primary",
            height=3,
            expand=True
        )

    def build_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(self._create_header_layout(), name="header", size=7),
            Layout(name="input_panels", size=4),
            Layout(name="main", ratio=1)
        )

        input_content_grid = Table.grid(expand=True, padding=1)
        input_content_grid.add_column(ratio=1)
        input_content_grid.add_column(ratio=1)

        input_content_grid.add_row(
            self._create_line_panel(),
            self._create_terminal_panel()
        )

        layout["input_panels"].update(input_content_grid)

        main_content_grid = Table.grid(expand=True, padding=1)
        main_content_grid.add_column(ratio=2)
        main_content_grid.add_column(ratio=1)

        main_content_grid.add_row(
            self._create_map_display(),
            self._create_stats_panel()
        )

        layout["main"].update(main_content_grid)
        return layout
