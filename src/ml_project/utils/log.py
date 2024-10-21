import inspect
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme

from ml_project import LOG_DIR, PROJECT_DIR, __version__, default_log_level

# 옵션으로 `from accelerate.logging import get_logger`
# 사용하시면 로깅할 때 main_process_only=False, in_order=True 등 옵션 사용 가능합니다
# https://huggingface.co/docs/accelerate/package_reference/logging
logger = logging.getLogger(__name__)

console = Console(
    theme=Theme(
        {
            "logging.level.error": "bold red blink",
            "logging.level.critical": "red blink",
            "logging.level.warning": "yellow",
            "logging.level.success": "green",
        }
    )
)


def setup_logging(
    console_level: int | str = default_log_level,
    output_files: list[str] | None = None,
    file_levels: list[int] | None = None,
):
    """
    Setup logging with RichHandler and FileHandler.

    You should call this function at the beginning of your script.

    Args:
        console_level: Logging level for console. Defaults to INFO or env var ML_PROJECT_LOG_LEVEL.
        output_files: List of output file paths, relative to LOG_DIR. If None, use default.
        file_levels: List of logging levels for each output file. If None, use default.
    """
    if output_files is None:
        output_files = ["{date:%Y%m%d-%H%M%S}-{name}-{levelname}-{version}.log"]
    if file_levels is None:
        file_levels = [logging.INFO]

    assert len(output_files) == len(
        file_levels
    ), "output_files and file_levels must have the same length"

    # NOTE: Initialise with NOTSET level and null device, and add stream handler separately.
    # This way, the root logging level is NOTSET (log all), and we can customise each handler's behaviour.
    # If we set the level during the initialisation, it will affect to ALL streams,
    # so the file stream cannot be more verbose (lower level) than the console stream.
    logging.basicConfig(
        format="",
        level=logging.NOTSET,
        stream=open(os.devnull, "w"),  # noqa: SIM115
    )

    # If you want to suppress logs from other modules, set their level to WARNING or higher
    # logging.getLogger('slowfast.utils.checkpoint').setLevel(logging.WARNING)

    console_handler = RichHandler(
        level=console_level,
        show_time=True,
        show_level=True,
        show_path=True,
        rich_tracebacks=True,
        tracebacks_show_locals=True,
        console=console,
    )
    console_format = logging.Formatter(
        fmt="%(name)s - %(message)s",
        datefmt="%m/%d %H:%M:%S",
    )
    console_handler.setFormatter(console_format)

    f_format = logging.Formatter(
        fmt="%(asctime)s - %(name)s: %(lineno)4d - %(levelname)s - %(message)s",
        datefmt="%y/%m/%d %H:%M:%S",
    )

    function_caller_module = inspect.getmodule(inspect.stack()[1][0])
    if function_caller_module is None:
        name_or_path = "unknown"
    elif function_caller_module.__name__ == "__main__":
        if function_caller_module.__file__ is None:
            name_or_path = function_caller_module.__name__
        else:
            name_or_path = function_caller_module.__file__.replace(
                str(PROJECT_DIR) + "/", ""
            ).replace("/", ".")
            # Remove .py extension
            name_or_path = Path(name_or_path).with_suffix("")

    else:
        name_or_path = function_caller_module.__name__

    log_path_map = {
        "name": name_or_path,
        "version": __version__,
        "date": datetime.now(timezone.utc),
    }

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)

    log_paths = []
    for output_file, file_level in zip(output_files, file_levels, strict=True):
        log_path_map["levelname"] = logging.getLevelName(file_level)
        log_path = LOG_DIR / output_file.format_map(log_path_map)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        f_handler = logging.FileHandler(log_path)
        f_handler.setLevel(file_level)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        root_logger.addHandler(f_handler)

    logger.info(f"ml-project {__version__}")

    for log_path in log_paths:
        logger.info(f"Logging to {log_path}")


def main():
    logger.info("Hello, world!")
    raise Exception("Test exception")  # noqa: TRY002


if __name__ == "__main__":
    try:
        setup_logging()
        main()
    except Exception:
        logger.exception("Exception occurred")
