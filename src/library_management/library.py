from dataclasses import dataclass, field
from datetime import date, timedelta
from uuid import uuid4

from .book import Book
from .employee import Employee
from .loan import Loan
from .user import User


@dataclass
class Library:
    name: str
    address: str | None = None
    catalog: dict[str, Book] = field(default_factory=dict)
    users: dict[str, User] = field(default_factory=dict)
    employees: dict[str, Employee] = field(default_factory=dict)
    loans: dict[str, Loan] = field(default_factory=dict)

    def add_book(self, book: Book) -> None:
        if book.isbn in self.catalog:
            raise ValueError(f"Book with ISBN '{book.isbn}' already exists in catalog.")
        self.catalog[book.isbn] = book

    def remove_book(self, isbn: str) -> None:
        book = self.catalog.get(isbn)
        if book is None:
            raise ValueError(f"Book with ISBN '{isbn}' was not found.")
        if any(loan.book_isbn == isbn and not loan.is_returned for loan in self.loans.values()):
            raise ValueError("Cannot remove a book that is currently on loan.")
        del self.catalog[isbn]

    def register_user(self, user: User) -> None:
        if user.user_id in self.users:
            raise ValueError(f"User '{user.user_id}' is already registered.")
        self.users[user.user_id] = user

    def hire_employee(self, employee: Employee) -> None:
        if employee.employee_id in self.employees:
            raise ValueError(f"Employee '{employee.employee_id}' is already registered.")
        self.employees[employee.employee_id] = employee

    def lend_book(self, user_id: str, isbn: str, loan_days: int = 14) -> Loan:
        user = self.users.get(user_id)
        if user is None:
            raise ValueError(f"User '{user_id}' was not found.")

        book = self.catalog.get(isbn)
        if book is None:
            raise ValueError(f"Book with ISBN '{isbn}' was not found.")

        user.borrow_book(book)

        borrowed_on = date.today()
        loan = Loan(
            loan_id=self._next_loan_id(),
            user_id=user_id,
            book_isbn=isbn,
            borrowed_on=borrowed_on,
            due_on=borrowed_on + timedelta(days=loan_days),
        )
        self.loans[loan.loan_id] = loan
        return loan

    def return_book(self, user_id: str, isbn: str, returned_on: date | None = None) -> Loan:
        user = self.users.get(user_id)
        if user is None:
            raise ValueError(f"User '{user_id}' was not found.")

        book = self.catalog.get(isbn)
        if book is None:
            raise ValueError(f"Book with ISBN '{isbn}' was not found.")

        active_loan = next(
            (
                loan
                for loan in self.loans.values()
                if loan.user_id == user_id and loan.book_isbn == isbn and not loan.is_returned
            ),
            None,
        )
        if active_loan is None:
            raise ValueError(f"No active loan found for user '{user_id}' and ISBN '{isbn}'.")

        user.return_book(book)
        active_loan.mark_returned(returned_on)
        return active_loan

    def available_books(self) -> list[Book]:
        return [book for book in self.catalog.values() if book.is_available]

    @staticmethod
    def _next_loan_id() -> str:
        return uuid4().hex[:12]
