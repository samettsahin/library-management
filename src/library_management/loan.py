from dataclasses import dataclass
from datetime import date


@dataclass
class Loan:
    loan_id: str
    user_id: str
    book_isbn: str
    borrowed_on: date
    due_on: date
    returned_on: date | None = None

    @property
    def is_returned(self) -> bool:
        return self.returned_on is not None

    def mark_returned(self, return_date: date | None = None) -> None:
        if self.is_returned:
            raise ValueError("Loan has already been returned.")
        self.returned_on = return_date or date.today()

    def is_overdue(self, today: date | None = None) -> bool:
        if self.is_returned:
            return False
        return (today or date.today()) > self.due_on
