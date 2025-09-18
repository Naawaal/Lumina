# Setup and Installation

This document supplements README.md with step-by-step setup instructions.

## Requirements

- Python 3.10 or newer
- git (optional)

## Create a virtual environment

From the project root:

Windows:
python -m venv .venv
.venv\Scripts\activate

macOS / Linux:
python -m venv .venv
source .venv/bin/activate

## Install the package

Install in editable/development mode so tests and local changes are available:

    pip install -e .

## Prepare environment variables

Copy the example env and edit values:

    cp .env.example .env
    # Edit .env and provide at least one LLM API key for non-testing usage:
    # OPENROUTER_API_KEY, GEMINI_API_KEY, or GROQ_API_KEY

## Running the demo

Run the simple demo entrypoint:

    python main.py

This will:

- Load environment variables from .env (if present)
- Validate settings
- Instantiate a rich-backed logger
- Demonstrate state contexts (Thinking, Generating, Searching, Speaking)

## Testing

Run unit tests with pytest:

    pytest -q

## Notes

- The configuration loader uses python-dotenv to read a provided .env file.
- Settings are validated with pydantic.BaseSettings.
- The logger uses rich for pretty console output and can optionally write to lumina.log.
