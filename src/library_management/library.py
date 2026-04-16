from dataclasses import dataclass, field
from datetime import date

from .book import Book
from .employee import Employee
from .loan import Loan
from .user import User


@dataclass(slots=True)
class Library:
    name: str
    address: str
    books: dict[str, Book] = field(default_factory=dict)
    users: dict[str, User] = field(default_factory=dict)
    employees: dict[str, Employee] = field(default_factory=dict)
    active_loans: dict[tuple[str, str], Loan] = field(default_factory=dict)
    loan_history: list[Loan] = field(default_factory=list)

    def add_book(self, book: Book) -> None:
        self.books[book.isbn] = book

    def register_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def hire_employee(self, employee: Employee) -> None:
        self.employees[employee.employee_id] = employee

    def find_book(self, isbn: str) -> Book:
        try:
            return self.books[isbn]
        except KeyError as exc:
            msg = f"Book with ISBN {isbn} not found"
            raise ValueError(msg) from exc

    def find_user(self, user_id: str) -> User:
        try:
            return self.users[user_id]
        except KeyError as exc:
            msg = f"User {user_id} not registered"
            raise ValueError(msg) from exc

    def borrow_book(self, user_id: str, isbn: str, borrowed_on: date, due_in_days: int = 14) -> Loan:
        user = self.find_user(user_id)
        book = self.find_book(isbn)

        if (user_id, isbn) in self.active_loans:
            msg = "User already has an active loan for this book"
            raise ValueError(msg)

        loan = Loan.create(user_id=user_id, isbn=isbn, borrowed_on=borrowed_on, due_in_days=due_in_days)
        book.borrow_copy()
        user.add_loan(loan)
        self.active_loans[(user_id, isbn)] = loan
        self.loan_history.append(loan)
        return loan

    def return_book(self, user_id: str, isbn: str, returned_on: date) -> Loan:
        book = self.find_book(isbn)
        user = self.find_user(user_id)

        loan = user.return_loan(isbn=isbn, returned_on=returned_on)
        book.return_copy()
        self.active_loans.pop((user_id, isbn), None)
        return loan
