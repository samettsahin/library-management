from dataclasses import dataclass

from .person import Person


@dataclass(slots=True)
class Employee(Person):
    employee_id: str
    role: str
