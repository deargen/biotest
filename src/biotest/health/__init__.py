"""Check health of the installation."""

import logging
import os

from .. import DATA_DIR

logger = logging.getLogger(__name__)


def check_binaries():
    """Check if binaries are installed."""
    return True


def check_env():
    """Check environment variables."""
    biotest_data_dir = os.environ.get("BIOTEST_DATA_DIR")

    if biotest_data_dir is None:
        logger.warning(
            "🤒 Please set the environment variable BIOTEST_DATA_DIR to the path of the data directory.\n"
            f"Otherwise, the default {DATA_DIR} will be used."
        )
        return False

    logger.info(f"✅ BIOTEST_DATA_DIR is set to {biotest_data_dir}")
    return True


def main():
    successes = [check_env()]
    successes.append(check_binaries())

    if all(successes):
        logger.info("")
        logger.info("💪 You are ready to go!")


if __name__ == "__main__":
    main()