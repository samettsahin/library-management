from dataclasses import dataclass, field
from enum import StrEnum

from .author import Author


class BookStatus(StrEnum):
    AVAILABLE = "available"
    LOANED = "loaned"
    RESERVED = "reserved"
    LOST = "lost"


@dataclass
class Book:
    isbn: str
    title: str
    authors: list[Author]
    published_year: int
    language: str = "English"
    genre: str | None = None
    pages: int | None = None
    publisher: str | None = None
    copies_total: int = 1
    copies_available: int = 1
    tags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if not self.authors:
            raise ValueError("A book must have at least one author.")
        if self.copies_total < 1:
            raise ValueError("copies_total must be at least 1.")
        if not 0 <= self.copies_available <= self.copies_total:
            raise ValueError("copies_available must be between 0 and copies_total.")

    @property
    def status(self) -> BookStatus:
        return BookStatus.AVAILABLE if self.copies_available > 0 else BookStatus.LOANED

    @property
    def is_available(self) -> bool:
        return self.copies_available > 0

    def checkout(self) -> None:
        if not self.is_available:
            raise ValueError(f"Book '{self.title}' is not currently available.")
        self.copies_available -= 1

    def checkin(self) -> None:
        if self.copies_available >= self.copies_total:
            raise ValueError(f"All copies of '{self.title}' are already checked in.")
        self.copies_available += 1

    def add_tag(self, tag: str) -> None:
        self.tags.add(tag.strip().lower())

    def remove_tag(self, tag: str) -> None:
        self.tags.discard(tag.strip().lower())
