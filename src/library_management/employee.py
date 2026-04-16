from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from .book import Book

if TYPE_CHECKING:
    from .library import Library


class EmployeeRole(StrEnum):
    LIBRARIAN = "librarian"
    ASSISTANT = "assistant"
    MANAGER = "manager"


@dataclass
class Employee:
    employee_id: str
    first_name: str
    last_name: str
    email: str
    role: EmployeeRole = EmployeeRole.ASSISTANT
    active: bool = True

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def register_book(self, library: "Library", book: Book) -> None:
        library.add_book(book)

    def remove_book(self, library: "Library", isbn: str) -> None:
        library.remove_book(isbn)
