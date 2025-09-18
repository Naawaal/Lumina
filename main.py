"""Demo entrypoint for Lumina showing configuration + logger usage."""

import sys
from typing import Optional

from lumina.config.env_loader import load_env
from lumina.utils.logger import get_logger


def main() -> None:
    """Load configuration, create logger, and demonstrate state transitions."""
    try:
        # Load .env from project root if present
        settings = load_env(".env")
    except RuntimeError as exc:
        # If configuration is invalid, log and exit
        logger = get_logger(None)
        logger.error(str(exc))
        raise SystemExit(1) from exc

    logger = get_logger(settings)

    # Demonstrate simple stateful logging
    logger.info("Starting Lumina demo")

    with logger.state_context("Thinking", "planning demo"):
        logger.info("Evaluating available actions")

    with logger.state_context("Generating", "creating sample output"):
        logger.info("Assembling response tokens (simulated)")

    with logger.state_context("Searching", "simulated search"):
        logger.info("Search step completed (no external calls)")

    with logger.state_context("Speaking", "presenting output"):
        logger.info("Would speak the response (simulated)")

    logger.info("Lumina demo finished")


if __name__ == "__main__":
    # Run main and convert exceptions into exit codes
    try:
        main()
    except SystemExit as e:
        # Propagate exit code
        code: Optional[int] = getattr(e, "code", 1)
        sys.exit(code)
