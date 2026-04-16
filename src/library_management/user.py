from dataclasses import dataclass, field
from enum import StrEnum

from .book import Book


class UserType(StrEnum):
    STUDENT = "student"
    ACADEMIC = "academic"
    GUEST = "guest"


@dataclass
class User:
    user_id: str
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    user_type: UserType = UserType.GUEST
    max_books: int = 3
    active: bool = True
    borrowed_isbns: set[str] = field(default_factory=set)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def can_borrow(self) -> bool:
        return self.active and len(self.borrowed_isbns) < self.max_books

    def borrow_book(self, book: Book) -> None:
        if not self.can_borrow():
            raise ValueError(f"User '{self.full_name}' cannot borrow more books.")
        book.checkout()
        self.borrowed_isbns.add(book.isbn)

    def return_book(self, book: Book) -> None:
        if book.isbn not in self.borrowed_isbns:
            raise ValueError(f"User '{self.full_name}' did not borrow '{book.title}'.")
        book.checkin()
        self.borrowed_isbns.remove(book.isbn)
