"""Resilient settings module that exposes Settings and ensures imports never fail.

Tries to import BaseSettings from pydantic_settings, then pydantic.
Falls back to a dataclass-based implementation reading from os.environ.
"""

from typing import Optional, Any, TYPE_CHECKING, List
import os
import dataclasses
import importlib

__all__: List[str] = ["Settings"]

# Try to import BaseSettings dynamically to avoid static import errors for linters.
# Prefer pydantic_settings (v2) then pydantic (v1). Use importlib so static analyzers
# that cannot resolve optional deps do not emit false positives.
try:
    _mod = importlib.import_module("pydantic_settings")
    _BaseSettings = getattr(_mod, "BaseSettings", None)
except ImportError:
    try:
        _mod = importlib.import_module("pydantic")
        _BaseSettings = getattr(_mod, "BaseSettings", None)
    except ImportError:
        _BaseSettings = None  # type: ignore  # pylint: disable=invalid-name


def _validate(instance: Any) -> None:
    """Enforce required API-key presence for non-testing envs."""
    env = getattr(instance, "ENV", None)
    if env != "testing":
        if not any(
            getattr(instance, k, None)
            for k in (
                "OPENROUTER_API_KEY",
                "GEMINI_API_KEY",
                "GROQ_API_KEY",
            )
        ):
            raise ValueError(
                "At least one LLM API key (OPENROUTER_API_KEY, GEMINI_API_KEY, or "
                "GROQ_API_KEY) must be set for ENV != 'testing'"
            )


if _BaseSettings is not None:
    # Use pydantic-based settings when available.
    class Settings(_BaseSettings):  # type: ignore
        """Application settings backed by pydantic BaseSettings.

        Attributes use UPPER_CASE to match environment variable names. Pylint
        invalid-name is disabled for this class by design because these fields
        intentionally map to environment variables.
        """

        # pylint: disable=invalid-name
        ENV: str = "development"
        LOG_LEVEL: str = "INFO"
        OPENROUTER_API_KEY: Optional[str] = None
        GEMINI_API_KEY: Optional[str] = None
        GROQ_API_KEY: Optional[str] = None
        SERPAPI_KEY: Optional[str] = None
        TTS_PROVIDER: str = "streamelements"
        STT_PROVIDER: str = "whisper"
        RAG_VECTOR_DB: str = "faiss"
        RAG_SEARCH_PROVIDER: str = "serpapi"

        class Config:  # type: ignore
            """Pydantic settings config."""

            # Do not auto-load dotenv here; callers may provide env_file but we no-op.
            env_prefix = ""

        @classmethod
        def load(cls, env_file: Optional[str] = None) -> "Settings":
            """Return a validated Settings instance.

            env_file is accepted for API compatibility but intentionally ignored;
            callers should load dotenv explicitly if desired.
            """
            if env_file:
                _ = env_file  # env_file intentionally not processed here
            inst = cls()  # type: ignore
            _validate(inst)
            return inst

else:
    # Lightweight dataclass fallback that reads from os.environ deterministically.
    @dataclasses.dataclass(frozen=True)
    class _DataclassSettings:
        """Dataclass fallback for environments without pydantic.

        Fields intentionally use UPPER_CASE to mirror environment variable names.
        Pylint invalid-name is disabled for this class by design.
        """

        # pylint: disable=invalid-name
        ENV: str = "development"
        LOG_LEVEL: str = "INFO"
        OPENROUTER_API_KEY: Optional[str] = None
        GEMINI_API_KEY: Optional[str] = None
        GROQ_API_KEY: Optional[str] = None
        SERPAPI_KEY: Optional[str] = None
        TTS_PROVIDER: str = "streamelements"
        STT_PROVIDER: str = "whisper"
        RAG_VECTOR_DB: str = "faiss"
        RAG_SEARCH_PROVIDER: str = "serpapi"

        @classmethod
        def load(cls, env_file: Optional[str] = None) -> "_DataclassSettings":
            """Create Settings from os.environ.

            env_file is accepted for API compatibility but not processed here.
            """
            if env_file:
                _ = env_file  # env_file intentionally not processed here

            def _get(name: str, default: Any) -> Any:
                val = os.environ.get(name, None)
                if val is None:
                    return default
                if val == "":
                    # Treat empty string as unset for optional keys.
                    return None if default is None else default
                return val

            inst = cls(
                ENV=_get("ENV", "development"),
                LOG_LEVEL=_get("LOG_LEVEL", "INFO"),
                OPENROUTER_API_KEY=_get("OPENROUTER_API_KEY", None),
                GEMINI_API_KEY=_get("GEMINI_API_KEY", None),
                GROQ_API_KEY=_get("GROQ_API_KEY", None),
                SERPAPI_KEY=_get("SERPAPI_KEY", None),
                TTS_PROVIDER=_get("TTS_PROVIDER", "streamelements"),
                STT_PROVIDER=_get("STT_PROVIDER", "whisper"),
                RAG_VECTOR_DB=_get("RAG_VECTOR_DB", "faiss"),
                RAG_SEARCH_PROVIDER=_get("RAG_SEARCH_PROVIDER", "serpapi"),
            )

            _validate(inst)
            return inst

    # Expose consistent Settings symbol when pydantic is unavailable.
    Settings = _DataclassSettings  # type: ignore[misc]
