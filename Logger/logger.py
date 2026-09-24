import os
from datetime import datetime


def get_log_directory():

    local_app_data = os.environ.get("LOCALAPPDATA")

    if local_app_data:
        log_directory = os.path.join(local_app_data, "Loom")
    else:
        # Fallback for non-Windows environments
        log_directory = os.path.join(
            os.path.expanduser("~"),
            ".loom"
        )

    os.makedirs(log_directory, exist_ok=True)

    return log_directory


def get_log_file():


    return os.path.join(
        get_log_directory(),
        "loom.log"
    )


def get_error_type(error):
    """
    Convert a Loom error into a readable category.
    """

    error_name = type(error).__name__

    if error_name == "LoomLexerError":
        return "LEXER"

    if error_name == "LoomParseError":
        return "PARSER"

    if error_name == "LoomRuntimeError":
        return "RUNTIME"

    return "SYSTEM"


def log_error(error, file_path=None):
    """
    Append an error to Loom's persistent local error log.

    Logging failures are intentionally ignored so that
    the logger can never crash Loom itself.
    """

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    error_type = get_error_type(error)
    message = str(error)

    if file_path:
        entry = (
            f"{timestamp} | "
            f"{error_type:<7} | "
            f"File: {file_path} | "
            f"{message}\n"
        )
    else:
        entry = (
            f"{timestamp} | "
            f"{error_type:<7} | "
            f"{message}\n"
        )

    try:
        with open(
            get_log_file(),
            "a",
            encoding="utf-8"
        ) as log_file:

            log_file.write(entry)

    except OSError:
        pass