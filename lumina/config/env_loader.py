from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import ValidationError

from .settings import Settings


def load_env(env_file: Optional[str] = None) -> Settings:
    """
    Load environment variables from an optional dotenv file and return validated Settings.

    - If env_file is provided, it is loaded with python-dotenv (no override).
    - Raises RuntimeError with guidance if required configuration is missing.
    """
    if env_file:
        # Load variables from the provided env file but do not override existing env.
        load_dotenv(env_file, override=False)

    try:
        settings = Settings.load(env_file=env_file)
    except (ValidationError, ValueError) as exc:
        # If the environment explicitly requests testing, allow tests to inspect
        # validation errors by re-raising the original exception.
        env = os.environ.get("ENV", os.environ.get("env", "development"))
        if env and env.lower() in ("testing", "test"):
            raise
        # Provide clear guidance to the user without printing secrets.
        raise RuntimeError(
            "Invalid configuration: required environment variables are missing or invalid. "
            "Ensure at least one LLM API key is set (OPENROUTER_API_KEY, GEMINI_API_KEY, or GROQ_API_KEY) "
            "or set ENV=testing to relax this requirement."
        ) from exc

    return settings
