# Contributing to Lumina

Thank you for your interest in contributing to Lumina.

## Development guidelines

- Follow PEP8 and use Black and isort before committing:

  - black .
  - isort .

- Run tests locally:

  - pytest -q

- Static type checks (optional):
  - mypy .

## Commit message convention

Use Conventional Commits. Examples:

- feat: add new feature
- fix: correct behavior
- docs: update documentation
- chore: maintenance

## Pull request checklist

- [ ] Tests added or updated
- [ ] Code formatted with black/isort
- [ ] Type checks pass (mypy) if applicable
- [ ] PR description explains the change and any relevant decisions
