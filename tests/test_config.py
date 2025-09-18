import os

import pytest

from lumina.config.settings import Settings
from lumina.config import env_loader


def test_settings_loads_from_env(monkeypatch):
    # Provide one LLM API key and other variables
    monkeypatch.setenv("ENV", "development")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("OPENROUTER_API_KEY", "dummy-key")
    s = Settings.load()
    assert isinstance(s, Settings)
    assert s.OPENROUTER_API_KEY == "dummy-key"
    assert s.LOG_LEVEL == "DEBUG"


def test_missing_keys_raises(monkeypatch):
    # Ensure when no LLM keys present and ENV is non-testing, validation fails
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setenv("ENV", "development")
    # Settings.load raises ValueError when no keys provided
    with pytest.raises(ValueError):
        Settings.load()
    # env_loader.load_env should translate that into a RuntimeError for consumers
    with pytest.raises(RuntimeError):
        env_loader.load_env(env_file=None)
