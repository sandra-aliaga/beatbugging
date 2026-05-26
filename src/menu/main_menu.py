import os
import sys
import tty
import termios
import select
import time
import threading
import itertools
import random
from contextlib import contextmanager
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import difflib

import pygame
import numpy as np
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.console import Group

from music.generator import LogMusicGenerator


# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class LogFile:
    path: Path
    score: float
    name: str
    parent_dir: str
    size: int
    line_count: int = 0


class SimpleFuzzyMatcher:
    @staticmethod
    def calculate_ratio(query: str, filename: str) -> float:
        if not query:
            return 1.0
        ql = query.lower()
        fl = filename.lower()
        ratio = difflib.SequenceMatcher(None, ql, fl).ratio()
        if ql in fl:
            ratio += 0.4
        if fl.startswith(ql):
            ratio += 0.3
        return min(ratio, 1.0)

    @staticmethod
    def find_matches(query: str, files: List[LogFile], limit: int = 100) -> List[LogFile]:
        if not query.strip():
            return files[:limit]
        scored = []
        for f in files:
            score = SimpleFuzzyMatcher.calculate_ratio(query, f.name)
            if score > 0.1:
                scored.append((score, f))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [f for _, f in scored[:limit]]


# ── Audio ─────────────────────────────────────────────────────────────────────

def play_sound_and_wait(sound_path: str) -> None:
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(0.4)
        sound.play()
        while pygame.mixer.get_busy():
            time.sleep(0.1)
    except Exception:
        pass


class SoundManager:
    def __init__(self):
        self.last_click_time = 0.0
        self.click_delay = 0.2
        self.volume = 0.3
        self.menu_click_path = os.path.join(
            os.path.dirname(__file__), "res", "menu-click.mp3"
        )
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def play_menu_click(self) -> None:
        now = time.time()
        if now - self.last_click_time >= self.click_delay:
            self.last_click_time = now
            def _play():
                try:
                    sound = pygame.mixer.Sound(self.menu_click_path)
                    sound.set_volume(self.volume)
                    sound.play()
                except Exception:
                    pass
            threading.Thread(target=_play, daemon=True).start()


sound_manager = SoundManager()


# ── File scanning ─────────────────────────────────────────────────────────────

def _scan_dir(path: Path, label: Optional[str] = None) -> tuple[List[LogFile], int]:
    """Returns (files, skipped_count)."""
    results = []
    skipped = 0
    try:
        for p in path.rglob("*.log"):
            try:
                if not p.is_file():
                    continue
                stat = p.stat()
                line_count = 0
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                        for i, _ in enumerate(itertools.islice(fh, 200)):
                            line_count = i + 1
                except Exception:
                    skipped += 1
                    continue
                if line_count == 0:
                    skipped += 1
                    continue
                results.append(LogFile(
                    path=p,
                    score=1.0,
                    name=p.name,
                    parent_dir=label if label is not None else str(p.parent),
                    size=stat.st_size,
                    line_count=line_count,
                ))
            except (OSError, PermissionError):
                skipped += 1
                continue
    except (OSError, PermissionError):
        pass
    results.sort(key=lambda f: f.line_count, reverse=True)
    return results, skipped


# ── Input ─────────────────────────────────────────────────────────────────────

def _read_raw(fd: int) -> str:
    """Read one byte from raw fd, bypassing Python's TextIOWrapper buffer."""
    return os.read(fd, 1).decode("utf-8", errors="replace")


def read_key(fd: int) -> str:
    """Read one keypress using raw fd. Normalizes arrow sequences."""
    ch = _read_raw(fd)
    if ch == "\x1b":
        r, _, _ = select.select([fd], [], [], 0.05)
        if not r:
            return "ESC"
        ch2 = _read_raw(fd)
        if ch2 == "[":
            r, _, _ = select.select([fd], [], [], 0.05)
            if r:
                ch3 = _read_raw(fd)
                return {"A": "UP", "B": "DOWN", "C": "RIGHT", "D": "LEFT"}.get(
                    ch3, "ESC"
                )
        return "ESC"
    if ch in ("\r", "\n"):
        return "ENTER"
    if ch == "\x7f":
        return "BACKSPACE"
    if ch == "\x03":
        raise KeyboardInterrupt
    return ch


@contextmanager
def _raw_stdin():
    """Put stdin in cbreak (raw) mode and yield the file descriptor."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        yield fd
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ── Logos ─────────────────────────────────────────────────────────────────────

LOGO_A = """\
 ███████████  ██████████   █████████   ███████████    ███████████  █████  █████   █████████    █████████  █████ ██████   █████   █████████
░░███░░░░░███░░███░░░░░█  ███░░░░░███ ░█░░░███░░░█   ░░███░░░░░███░░███  ░░███   ███░░░░░███  ███░░░░░███░░███ ░░██████ ░░███   ███░░░░░███
 ░███    ░███ ░███  █ ░  ░███    ░███ ░   ░███  ░     ░███    ░███ ░███   ░███  ███     ░░░  ███     ░░░  ░███  ░███░███ ░███  ███     ░░░
 ░██████████  ░██████    ░███████████     ░███        ░██████████  ░███   ░███ ░███         ░███          ░███  ░███░░███░███ ░███
 ░███░░░░░███ ░███░░█    ░███░░░░░███     ░███        ░███░░░░░███ ░███   ░███ ░███    █████░███    █████ ░███  ░███  ░░██████ ░███    █████
 ░███    ░███ ░███ ░   █ ░███    ░███     ░███        ░███    ░███ ░███   ░███ ░░███  ░░███ ░░███  ░░███  ░███  ░███  ░░█████ ░░███  ░░███
 ███████████  ██████████ █████   █████    █████       ███████████  ░░████████   ░░█████████  ░░█████████  █████ █████  ░░█████ ░░█████████
░░░░░░░░░░░  ░░░░░░░░░░ ░░░░░   ░░░░░    ░░░░░       ░░░░░░░░░░░    ░░░░░░░░     ░░░░░░░░░    ░░░░░░░░░  ░░░░░ ░░░░░    ░░░░░   ░░░░░░░░░"""

LOGO_B = """\
 ███████████  ██████████   █████████   ███████████    ███████████  █████  █████   █████████    █████████  █████ ██████   █████   █████████
▒▒███▒▒▒▒▒███▒▒███▒▒▒▒▒█  ███▒▒▒▒▒███ ▒█▒▒▒███▒▒▒█   ▒▒███▒▒▒▒▒███▒▒███  ▒▒███   ███▒▒▒▒▒███  ███▒▒▒▒▒███▒▒███ ▒▒██████ ▒▒███   ███▒▒▒▒▒███
 ▒███    ▒███ ▒███  █ ▒  ▒███    ▒███ ▒   ▒███  ▒     ▒███    ▒███ ▒███   ▒███  ███     ▒▒▒  ███     ▒▒▒  ▒███  ▒███▒███ ▒███  ███     ▒▒▒
 ▒██████████  ▒██████    ▒███████████     ▒███        ▒██████████  ▒███   ▒███ ▒███         ▒███          ▒███  ▒███▒▒███▒███ ▒███
 ▒███▒▒▒▒▒███ ▒███▒▒█    ▒███▒▒▒▒▒███     ▒███        ▒███▒▒▒▒▒███ ▒███   ▒███ ▒███    █████▒███    █████ ▒███  ▒███ ▒▒██████ ▒███    █████
 ▒███    ▒███ ▒███ ▒   █ ▒███    ▒███     ▒███        ▒███    ▒███ ▒███   ▒███ ▒▒███  ▒▒███ ▒▒███  ▒▒███  ▒███  ▒███  ▒▒█████ ▒▒███  ▒▒███
 ███████████  ██████████ █████   █████    █████       ███████████  ▒▒████████   ▒▒█████████  ▒▒█████████  █████ █████  ▒▒█████ ▒▒█████████
▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒ ▒▒▒▒▒   ▒▒▒▒▒    ▒▒▒▒▒       ▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒     ▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒   ▒▒▒▒▒▒▒▒▒"""


# ── TitleScreen ───────────────────────────────────────────────────────────────

def _btn(label: str, selected: bool, color: str) -> Panel:
    """Render a menu button as a bordered panel."""
    if selected:
        inner = Text()
        inner.append("▶ ", style=f"bold {color}")
        inner.append(label, style=f"bold reverse {color}")
    else:
        inner = Text(f"  {label}  ", style=f"dim {color}")
    return Panel(
        Align.center(inner),
        border_style=f"bold {color}" if selected else f"dim {color}",
        expand=False,
    )


def run_title_screen() -> bool:
    """Returns True = play, False = exit."""
    console = Console()
    cursor = 0
    logo_idx = 0
    logo_lock = threading.Lock()
    running = True
    errors = random.randint(5000, 99999)

    def _toggle():
        nonlocal logo_idx
        while running:
            time.sleep(0.8)
            with logo_lock:
                logo_idx = 1 - logo_idx

    threading.Thread(target=_toggle, daemon=True).start()

    try:
        with _raw_stdin() as fd:
            with Live(console=console, screen=True, refresh_per_second=10) as live:
                while True:
                    with logo_lock:
                        logo = LOGO_A if logo_idx == 0 else LOGO_B

                    subtitle = Text(
                        f"[SYS://INIT] {errors} CRITICAL ERRORS DETECTED",
                        style="bold cyan",
                    )

                    btn_row = Table.grid(padding=(0, 2))
                    btn_row.add_column()
                    btn_row.add_column()
                    btn_row.add_row(
                        _btn("PLAY", cursor == 0, "green"),
                        _btn("EXIT", cursor == 1, "red"),
                    )

                    hint = Text(
                        "[ ↑/↓ ] NAVIGATE   [ ↵ ] EXECUTE   [ E ] QUIT",
                        style="dim green",
                    )

                    content = Group(
                        Align.center(Text(logo, style="green", no_wrap=True)),
                        Text(""),
                        Align.center(subtitle),
                        Text(""),
                        Align.center(btn_row),
                        Text(""),
                        Align.center(hint),
                    )
                    live.update(Panel(
                        Align.center(content, vertical="middle"),
                        border_style="green",
                    ))

                    r, _, _ = select.select([fd], [], [], 0.1)
                    if not r:
                        continue

                    key = read_key(fd)
                    if key == "UP":
                        cursor = (cursor - 1) % 2
                        sound_manager.play_menu_click()
                    elif key == "DOWN":
                        cursor = (cursor + 1) % 2
                        sound_manager.play_menu_click()
                    elif key == "ENTER":
                        sound_manager.play_menu_click()
                        running = False
                        return cursor == 0
                    elif key.upper() == "E" or key == "ESC":
                        running = False
                        return False
    finally:
        running = False


# ── FileBrowserScreen ─────────────────────────────────────────────────────────

_DATA_SELECTION_TITLE = """\
╺┳┓┏━┓╺┳╸┏━┓   ┏━┓┏━╸╻  ┏━╸┏━╸╺┳╸╻┏━┓┏┓╻
 ┃┃┣━┫ ┃ ┣━┫   ┗━┓┣╸ ┃  ┣╸ ┃   ┃ ┃┃ ┃┃┗┫
╺┻┛╹ ╹ ╹ ╹ ╹   ┗━┛┗━╸┗━╸┗━╸┗━╸ ╹ ╹┗━┛╹ ╹"""


def _build_search_panel(query: str, cursor_char: str) -> Panel:
    search_text = Text()
    search_text.append("  > ", style="cyan")
    search_text.append(query + cursor_char, style="green")
    return Panel(
        search_text,
        border_style="cyan" if query else "green",
        title="[cyan]Search[/cyan]",
        height=3,
    )


def _build_file_table(visible: List[LogFile], scroll_offset: int, cursor: int) -> Table:
    table = Table(show_header=False, box=None, padding=(0, 1), expand=True)
    table.add_column("cur", width=2, no_wrap=True)
    table.add_column("name", style="green")
    table.add_column("dir", style="dim")
    table.add_column("info", justify="right", style="cyan", no_wrap=True)
    for i, f in enumerate(visible):
        abs_idx = scroll_offset + i
        is_sel = abs_idx == cursor
        size_mb = f.size / (1024 * 1024)
        table.add_row(
            "▶" if is_sel else " ",
            f.name,
            f.parent_dir,
            f"{f.line_count}L {size_mb:.1f}MB",
            style="bold green reverse" if is_sel else "",
        )
    return table


def run_file_browser() -> Optional[LogFile]:
    """Returns selected LogFile, or None (back to title)."""
    console = Console()
    all_files: List[LogFile] = []
    scanning = True
    scan_lock = threading.Lock()
    scan_skipped = [0]
    query = ""
    cursor = 0
    scroll_offset = 0
    blink = True
    blink_time = time.time()

    def _scan():
        nonlocal scanning
        total_skipped = 0
        cwd = Path(os.getcwd())
        files, skipped = _scan_dir(cwd, label="./")
        total_skipped += skipped
        with scan_lock:
            all_files.extend(files)
        for p in [
            Path("/var/log"),
            Path.home() / ".local" / "share",
            Path("/tmp"),
        ]:
            if p.exists():
                files, skipped = _scan_dir(p)
                total_skipped += skipped
                with scan_lock:
                    all_files.extend(files)
        with scan_lock:
            scan_skipped[0] = total_skipped
        scanning = False

    threading.Thread(target=_scan, daemon=True).start()

    while True:  # re-enter after listen
        action = None
        selected_file: Optional[LogFile] = None
        listen_file: Optional[LogFile] = None

        with _raw_stdin() as fd:
            with Live(console=console, screen=True, refresh_per_second=10) as live:
                while True:
                    now = time.time()
                    if now - blink_time > 0.5:
                        blink = not blink
                        blink_time = now

                    with scan_lock:
                        current_files = list(all_files)
                        skipped = scan_skipped[0]

                    scan_done_empty = not scanning and not current_files
                    cursor_char = "█" if blink else " "

                    title_text = Text(_DATA_SELECTION_TITLE, style="green", no_wrap=True)

                    if scan_done_empty:
                        # Manual path mode
                        prompt = Text()
                        prompt.append("No log files found.\n\n", style="yellow")
                        prompt.append("Enter path: ", style="cyan")
                        prompt.append(query + cursor_char, style="green")
                        live.update(
                            Panel(
                                Align.center(
                                    Group(
                                        Align.center(title_text),
                                        Text(""),
                                        Align.center(prompt),
                                    ),
                                    vertical="middle",
                                ),
                                border_style="green",
                            )
                        )

                        r, _, _ = select.select([fd], [], [], 0.1)
                        if not r:
                            continue
                        key = read_key(fd)

                        if key == "ENTER" and query:
                            p = Path(query)
                            if p.is_file():
                                try:
                                    stat = p.stat()
                                    lc = 0
                                    with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                                        for i, _ in enumerate(itertools.islice(fh, 200)):
                                            lc = i + 1
                                    selected_file = LogFile(
                                        path=p,
                                        score=1.0,
                                        name=p.name,
                                        parent_dir=str(p.parent),
                                        size=stat.st_size,
                                        line_count=lc,
                                    )
                                    action = "selected"
                                    break
                                except Exception:
                                    pass
                        elif key == "BACKSPACE":
                            query = query[:-1]
                        elif key == "ESC" or key.upper() == "B":
                            action = "back"
                            break
                        elif len(key) == 1 and key.isprintable():
                            query += key
                        continue

                    # Normal file list mode
                    filtered = SimpleFuzzyMatcher.find_matches(query, current_files)
                    if filtered:
                        cursor = max(0, min(cursor, len(filtered) - 1))
                    else:
                        cursor = 0

                    term_height = console.height
                    list_height = max(3, term_height - 12)

                    if cursor < scroll_offset:
                        scroll_offset = cursor
                    elif cursor >= scroll_offset + list_height:
                        scroll_offset = cursor - list_height + 1

                    visible = filtered[scroll_offset : scroll_offset + list_height]

                    status = (
                        "⠋ Scanning..."
                        if scanning
                        else f"{len(filtered)}/{len(current_files)} files"
                        + (f" ({skipped} skipped)" if skipped > 0 else "")
                    )

                    file_panel = Panel(
                        _build_file_table(visible, scroll_offset, cursor),
                        border_style="green",
                        subtitle=f"[dim]{status}[/dim]",
                    )

                    footer_table = Table.grid(padding=(0, 1))
                    footer_table.add_column()
                    footer_table.add_column()
                    footer_table.add_column()
                    footer_table.add_row(
                        Panel("[green][B]ack[/green]", border_style="green", expand=False),
                        Panel("[green][L]isten[/green]", border_style="green", expand=False),
                        Panel("[bright_green][↵] Setup[/bright_green]", border_style="bright_green", expand=False),
                    )

                    layout = Layout()
                    layout.split_column(
                        Layout(Align.center(title_text), name="title", size=3),
                        Layout(_build_search_panel(query, cursor_char), name="search", size=3),
                        Layout(file_panel, name="files"),
                        Layout(Align.center(footer_table), name="footer", size=5),
                    )
                    live.update(layout)

                    r, _, _ = select.select([fd], [], [], 0.1)
                    if not r:
                        continue

                    key = read_key(fd)
                    ku = key.upper()

                    if key == "UP":
                        if cursor > 0:
                            cursor -= 1
                            sound_manager.play_menu_click()
                    elif key == "DOWN":
                        if cursor < len(filtered) - 1:
                            cursor += 1
                            sound_manager.play_menu_click()
                    elif key == "ENTER":
                        if filtered:
                            sound_manager.play_menu_click()
                            selected_file = filtered[cursor]
                            action = "selected"
                            break
                    elif ku == "L":
                        if filtered:
                            sound_manager.play_menu_click()
                            listen_file = filtered[cursor]
                            action = "listen"
                            break
                    elif key == "ESC" or ku == "B":
                        action = "back"
                        break
                    elif key == "BACKSPACE":
                        if query:
                            query = query[:-1]
                            cursor = 0
                            scroll_offset = 0
                    elif len(key) == 1 and key.isprintable():
                        query += key.lower()
                        cursor = 0
                        scroll_offset = 0

        if action == "selected":
            return selected_file
        elif action == "back":
            return None
        elif action == "listen" and listen_file:
            run_listen_screen(listen_file)
            # loop back → re-enter file browser


# ── SetupScreen ───────────────────────────────────────────────────────────────

def run_setup_screen(log_file: LogFile) -> Optional[dict]:
    """Returns game_config dict or None (back to file browser)."""
    console = Console()
    difficulty = "user"

    while True:  # re-enter after listen
        action = None

        with _raw_stdin() as fd:
            with Live(console=console, screen=True, refresh_per_second=10) as live:
                while True:
                    size_mb = log_file.size / (1024 * 1024)

                    file_info = Text()
                    file_info.append(f" {log_file.name} ", style="bold green")
                    file_info.append(f" {log_file.line_count} lines  {size_mb:.1f}MB", style="cyan")
                    file_panel = Panel(
                        Align.center(file_info),
                        border_style="green",
                        title="[green]Setup[/green]",
                    )

                    user_sel = difficulty == "user"
                    diff_table = Table.grid(padding=(0, 3))
                    diff_table.add_column()
                    diff_table.add_column()
                    diff_table.add_row(
                        Panel(
                            Align.center(Text(
                                "◀  User (Normal)" if user_sel else "   User (Normal)",
                                style="bold green" if user_sel else "green",
                            )),
                            border_style="bold green" if user_sel else "green",
                            expand=False,
                        ),
                        Panel(
                            Align.center(Text(
                                "Root (Hard)  ▶" if not user_sel else "Root (Hard)   ",
                                style="bold red" if not user_sel else "red",
                            )),
                            border_style="bold red" if not user_sel else "red",
                            expand=False,
                        ),
                    )
                    diff_panel = Panel(
                        Align.center(
                            Group(
                                Align.center(Text("Select difficulty:", style="cyan")),
                                Text(""),
                                Align.center(diff_table),
                                Text(""),
                                Align.center(Text("[←/→] Switch difficulty", style="dim")),
                            ),
                            vertical="middle",
                        ),
                        border_style="green",
                    )

                    action_table = Table.grid(padding=(0, 1))
                    action_table.add_column()
                    action_table.add_column()
                    action_table.add_column()
                    action_table.add_row(
                        Panel("[green][B]ack[/green]", border_style="green", expand=False),
                        Panel("[green][L]isten[/green]", border_style="green", expand=False),
                        Panel("[bright_green][↵] Start Game[/bright_green]", border_style="bright_green", expand=False),
                    )
                    action_panel = Panel(Align.center(action_table), border_style="green")

                    layout = Layout()
                    layout.split_column(
                        Layout(file_panel, name="file", size=3),
                        Layout(diff_panel, name="diff"),
                        Layout(action_panel, name="actions", size=5),
                    )
                    live.update(layout)

                    r, _, _ = select.select([fd], [], [], 0.1)
                    if not r:
                        continue

                    key = read_key(fd)
                    ku = key.upper()

                    if key == "LEFT":
                        difficulty = "user"
                        sound_manager.play_menu_click()
                    elif key == "RIGHT":
                        difficulty = "root"
                        sound_manager.play_menu_click()
                    elif key == "ENTER":
                        sound_manager.play_menu_click()
                        action = "start"
                        break
                    elif ku == "L":
                        sound_manager.play_menu_click()
                        action = "listen"
                        break
                    elif ku == "B" or key == "ESC":
                        action = "back"
                        break

        if action == "start":
            game_start_path = os.path.join(
                os.path.dirname(__file__), "res", "game-start.mp3"
            )
            play_sound_and_wait(game_start_path)
            return {"file": str(log_file.path), "difficulty": difficulty}
        elif action == "back":
            return None
        elif action == "listen":
            run_listen_screen(log_file)
            # loop back → re-enter setup


# ── ListenScreen ──────────────────────────────────────────────────────────────

def run_listen_screen(log_file: LogFile) -> None:
    """Stream log lines in sync with generated audio. ESC to return."""
    console = Console()

    state_lock = threading.Lock()
    state = {
        "actions": [],
        "total_duration": 0.0,
        "start_time": None,
        "lines_shown": 0,
        "log_lines": [],
        "ready": False,
        "error": None,
    }

    def _generate():
        try:
            gen = LogMusicGenerator(log_path=str(log_file.path))
            result = gen.generate_music()
            state["actions"] = result["gameplay_actions"]
            state["total_duration"] = max(
                (a["tiempo"] for a in state["actions"]), default=0.0
            )

            audio = result["audio_data"]
            if audio is not None and len(audio) > 0:
                def _play():
                    try:
                        if not pygame.mixer.get_init():
                            pygame.mixer.pre_init(
                                frequency=44100, size=-16, channels=1, buffer=1024
                            )
                            pygame.mixer.init()
                        cfg = pygame.mixer.get_init()
                        if cfg and cfg[2] == 2 and audio.ndim == 1:
                            a = np.column_stack((audio, audio)).astype(np.int16)
                        else:
                            a = audio.astype(np.int16)
                        pygame.sndarray.make_sound(a).play()
                        with state_lock:
                            state["start_time"] = time.time()
                    except Exception:
                        with state_lock:
                            state["start_time"] = time.time()
                    finally:
                        state["ready"] = True

                threading.Thread(target=_play, daemon=True).start()
            else:
                with state_lock:
                    state["start_time"] = time.time()
                state["ready"] = True
        except Exception as e:
            state["error"] = type(e).__name__ + ": " + str(e)
            with state_lock:
                state["start_time"] = time.time()
            state["ready"] = True

    threading.Thread(target=_generate, daemon=True).start()

    size_mb = log_file.size / (1024 * 1024)

    with _raw_stdin() as fd:
        with Live(console=console, screen=True, refresh_per_second=10) as live:
            while True:
                with state_lock:
                    st = state["start_time"]
                elapsed = time.time() - st if st is not None else 0.0
                total = state["total_duration"]

                # Append new log lines that are due
                if state["ready"] and not state["error"] and st is not None:
                    actions = state["actions"]
                    ls = state["lines_shown"]
                    while ls < len(actions) and actions[ls]["tiempo"] <= elapsed:
                        state["log_lines"].append(actions[ls]["line"])
                        ls += 1
                    state["lines_shown"] = ls

                # Progress bar
                if total > 0 and st is not None:
                    pct = min(100, int(elapsed / total * 100))
                    bar_w = 36
                    filled = int(pct / 100 * bar_w)
                    bar = "█" * filled + "░" * (bar_w - filled)
                    def _fmt(s: float) -> str:
                        return f"{int(s) // 60}:{int(s) % 60:02d}"
                    progress_str = f"{bar} {pct}% {_fmt(elapsed)}/{_fmt(total)}"
                    progress_style = "cyan"
                else:
                    if not state["ready"]:
                        progress_str = "Generating music..."
                    elif state["error"]:
                        progress_str = f"Error: {state['error']}"
                    else:
                        progress_str = "Starting playback..."
                    progress_style = "yellow"

                header_str = (
                    f"♪ LISTEN — {log_file.name} | "
                    f"{log_file.line_count} lines | {size_mb:.1f}MB"
                )
                # header=3, progress=3, footer=1, log panel borders=2
                log_capacity = max(5, console.height - 9)
                visible = state["log_lines"][-log_capacity:]
                log_text = Text("\n".join(visible), style="green", no_wrap=True)

                layout = Layout()
                layout.split_column(
                    Layout(
                        Panel(
                            Align.center(Text(header_str, style="bold green")),
                            border_style="green",
                        ),
                        name="header",
                        size=3,
                    ),
                    Layout(
                        Panel(
                            Align.center(Text(progress_str, style=progress_style)),
                            border_style="green",
                        ),
                        name="progress",
                        size=3,
                    ),
                    Layout(Panel(log_text, border_style="green"), name="log"),
                    Layout(
                        Align.center(Text("ESC → back", style="dim")),
                        name="footer",
                        size=1,
                    ),
                )
                live.update(layout)

                if st is not None and total > 0 and elapsed >= total:
                    break

                r, _, _ = select.select([fd], [], [], 0)
                if r:
                    ch = os.read(fd, 1)
                    if ch in (b"\x1b", b"\x03"):
                        if ch == b"\x03":
                            raise KeyboardInterrupt
                        break

                time.sleep(0.1)

    try:
        pygame.mixer.stop()
    except Exception:
        pass


# ── Entry point ───────────────────────────────────────────────────────────────

def run_menu() -> Optional[dict]:
    while True:
        try:
            play = run_title_screen()
        except KeyboardInterrupt:
            return None
        if not play:
            return None

        while True:
            try:
                log_file = run_file_browser()
            except KeyboardInterrupt:
                return None
            if log_file is None:
                break  # back to title

            try:
                game_config = run_setup_screen(log_file)
            except KeyboardInterrupt:
                return None
            if game_config is not None:
                return game_config
            # None = back to file browser → loop


if __name__ == "__main__":
    result = run_menu()
