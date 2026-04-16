# library-management

A minimal Python domain model for a library system.

Implemented classes (separate files):
- `Library`
- `Book`
- `User`
- `Author`
- `Employee`
- `Loan` (supporting class)
- `Person` (base class for people)

Tooling:
- Project metadata in `pyproject.toml` (uv-compatible layout)
- `.gitignore` for Python/venv/tool caches
- Ruff configuration for linting
- Pytest tests for core borrowing/return behaviors
