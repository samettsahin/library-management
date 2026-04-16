from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(slots=True)
class Loan:
    user_id: str
    isbn: str
    borrowed_on: date
    due_on: date
    returned_on: date | None = None

    @classmethod
    def create(cls, user_id: str, isbn: str, borrowed_on: date, due_in_days: int = 14) -> "Loan":
        if due_in_days <= 0:
            msg = "due_in_days must be positive"
            raise ValueError(msg)
        return cls(
            user_id=user_id,
            isbn=isbn,
            borrowed_on=borrowed_on,
            due_on=borrowed_on + timedelta(days=due_in_days),
        )

    @property
    def is_active(self) -> bool:
        return self.returned_on is None

    def mark_returned(self, returned_on: date) -> None:
        if returned_on < self.borrowed_on:
            msg = "returned_on cannot be earlier than borrowed_on"
            raise ValueError(msg)
        self.returned_on = returned_on
