import os
from pathlib import Path

from dotenv import load_dotenv

from . import _version

load_dotenv()

__version__ = _version.get_versions()["version"]

default_log_level = os.environ.get("ML_PROJECT_LOG_LEVEL")
if default_log_level is None:
    default_log_level = "INFO"

# NOTE: It is assuming that you installed with `pip install -e .`
#      If you installed with `pip install .`, then the path will be different.
PROJECT_DIR = Path(__file__).parent.parent.parent

DATA_DIR = os.environ.get("ML_PROJECT_DATA_DIR")
DATA_DIR = (
    PROJECT_DIR / "data" if DATA_DIR is None or DATA_DIR == "" else Path(DATA_DIR)
)

LOG_DIR = DATA_DIR / "logs"
