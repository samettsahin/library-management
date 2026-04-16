from .author import Author
from .book import Book, BookStatus
from .employee import Employee, EmployeeRole
from .library import Library
from .loan import Loan
from .user import User, UserType


def main() -> None:
    print("library-management domain models are ready to use.")


__all__ = [
    "Author",
    "Book",
    "BookStatus",
    "Employee",
    "EmployeeRole",
    "Library",
    "Loan",
    "User",
    "UserType",
    "main",
]
