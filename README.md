# library-management

Simple library domain model built with Python and uv.

## Classes

- `Library` - manages books, users, employees, and loans.
- `Book` - stores book metadata and copy availability.
- `User` - represents a person who borrows books.
- `Author` - stores author details.
- `Employee` - represents library workers.
- `Loan` - tracks borrow/return dates.

All classes are organized in separate files under:

- `/home/runner/work/library-management/library-management/src/library_management`

## Linting (Ruff)

```bash
uv run --group dev ruff check .
```
