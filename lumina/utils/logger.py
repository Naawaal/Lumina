from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from rich.console import Console
from rich.logging import RichHandler

if TYPE_CHECKING:
    from lumina.config.settings import Settings

# Color map for states (per spec)
_STATE_COLORS = {
    "Thinking": "yellow",
    "Generating": "magenta",
    "Searching": "cyan",
    "Speaking": "green",
    "Error": "white",
    "Idle": "white",
}


class LuminaLogger:
    """
    Lightweight logger wrapper using rich for pretty console output.

    Synchronous and test-friendly.
    """

    def __init__(
        self,
        name: str = "lumina",
        level: str = "INFO",
        *,
        file_logging: bool = False,
        file_path: Optional[Path] = None,
    ) -> None:
        self.console = Console()
        self.logger = logging.getLogger(name)
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(numeric_level)

        # Configure RichHandler once per logger
        if not any(isinstance(h, RichHandler) for h in self.logger.handlers):
            rich_handler = RichHandler(
                console=self.console, show_time=True, show_path=False, markup=True
            )
            rich_handler.setLevel(numeric_level)
            rich_handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(rich_handler)

        # Optional file logging
        self.file_handler: Optional[logging.Handler] = None
        if file_logging or level.upper() == "DEBUG":
            path = Path(file_path) if file_path is not None else Path("lumina.log")
            try:
                # Ensure parent dir exists
                path.parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                # Best-effort; do not fail logger creation
                pass
            fh = logging.FileHandler(path, encoding="utf-8")
            fh.setLevel(numeric_level)
            fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            self.logger.addHandler(fh)
            self.file_handler = fh
            # ensure the file exists
            try:
                path.touch(exist_ok=True)
            except Exception:
                pass

    def info(self, message: str, *args, **kwargs) -> None:
        self.logger.info(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        self.logger.debug(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs) -> None:
        # Keep error messages visible in red on console while preserving plain message in file logs
        self.logger.error(f"[red]{message}[/red]", *args, **kwargs)

    def state(self, state_name: str, message: str) -> None:
        """Log a message associated with a state using the configured color."""
        color = _STATE_COLORS.get(state_name, "white")
        # Console uses rich markup; file handlers will receive the same text but without color rendering
        self.logger.info(f"[{color}][{state_name}][/]{message}")

    @contextmanager
    def state_context(self, state_name: str, message: str):
        """
        Context manager that logs entering and exiting a state.
        Example:
            with logger.state_context("Thinking", "evaluating"):
                ...
        """
        enter_msg = f"entering {message}"
        exit_msg = f"exiting {message}"
        self.state(state_name, enter_msg)
        try:
            yield
        except Exception as exc:
            self.error(f"Exception in state [{state_name}]: {exc}")
            raise
        finally:
            self.state(state_name, exit_msg)


def get_logger(
    settings: Optional["Settings"] = None,
    *,
    name: str = "lumina",
    file_logging: bool = False,
    file_path: Optional[Path] = None,
) -> LuminaLogger:
    """
    Factory returning a configured LuminaLogger.

    - settings: optional Settings instance with attribute LOG_LEVEL; if present it's used.
    - file_logging: force file logging.
    - file_path: optional Path for logfile (defaults to ./lumina.log).
    """
    level = "INFO"
    if settings is not None:
        level = getattr(settings, "LOG_LEVEL", level) or level
    return LuminaLogger(
        name=name, level=level, file_logging=file_logging, file_path=file_path
    )


@contextmanager
def state_context(state_name: str, message: str, settings: Optional["Settings"] = None):
    """
    Module-level convenience context manager that uses a default logger instance.
    Example:
        with state_context("Thinking", "planning"):
            ...
    """
    logger = get_logger(settings)
    with logger.state_context(state_name, message):
        yield
