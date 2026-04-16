from dataclasses import dataclass, field
from datetime import date

from .loan import Loan
from .person import Person


@dataclass(slots=True)
class User(Person):
    user_id: str
    email: str
    max_active_loans: int = 5
    loans: list[Loan] = field(default_factory=list)

    @property
    def active_loans(self) -> list[Loan]:
        return [loan for loan in self.loans if loan.is_active]

    def can_borrow(self) -> bool:
        return len(self.active_loans) < self.max_active_loans

    def add_loan(self, loan: Loan) -> None:
        if not self.can_borrow():
            msg = f"{self.full_name} has reached the borrowing limit"
            raise ValueError(msg)
        self.loans.append(loan)

    def return_loan(self, isbn: str, returned_on: date) -> Loan:
        for loan in self.active_loans:
            if loan.isbn == isbn:
                loan.mark_returned(returned_on)
                return loan

        msg = f"No active loan for ISBN {isbn}"
        raise ValueError(msg)
