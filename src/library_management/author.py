from dataclasses import dataclass

from .person import Person


@dataclass(slots=True)
class Author(Person):
    author_id: str
    birth_year: int | None = None
    nationality: str | None = None
