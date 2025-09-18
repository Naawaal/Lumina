# Lumina

Hindi-first AI assistant Lumina.

## Overview

Lumina is a small demonstration project showing configuration using Pydantic,
dotenv-based environment loading, and a simple rich-based logger with
state contexts.

## Quickstart

1. Ensure you have Python >= 3.10 installed.
2. Create and activate a virtual environment:

   python -m venv .venv

   # Windows

   .venv\Scripts\activate

   # Unix / macOS

   source .venv/bin/activate

3. Install the package in editable mode:

   pip install -e .

4. Copy the example env and edit values:

   cp .env.example .env

   # then edit .env and add at least one LLM API key for non-testing usage

5. Run the demo:

   python main.py

## Testing

Run tests with:

    pytest -q

## Files of note

- pyproject.toml — project metadata and dependencies
- .env.example — example environment variables to copy to .env
- main.py — simple demonstration that loads settings and exercises logging
- lumina/config — settings and env loader implemented with Pydantic and python-dotenv
- lumina/utils/logger.py — rich-backed logger with state contexts
