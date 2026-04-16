from dataclasses import dataclass, field

from .author import Author


@dataclass(slots=True)
class Book:
    isbn: str
    title: str
    publication_year: int
    language: str
    genre: str
    page_count: int
    authors: list[Author] = field(default_factory=list)
    total_copies: int = 1
    available_copies: int = 1

    def __post_init__(self) -> None:
        if self.total_copies < 0:
            msg = "total_copies cannot be negative"
            raise ValueError(msg)
        if self.available_copies < 0 or self.available_copies > self.total_copies:
            msg = "available_copies must be between 0 and total_copies"
            raise ValueError(msg)

    def is_available(self) -> bool:
        return self.available_copies > 0

    def borrow_copy(self) -> None:
        if not self.is_available():
            msg = f"Book '{self.title}' is not currently available"
            raise ValueError(msg)
        self.available_copies -= 1

    def return_copy(self) -> None:
        if self.available_copies >= self.total_copies:
            msg = f"All copies of '{self.title}' are already in the library"
            raise ValueError(msg)
        self.available_copies += 1
