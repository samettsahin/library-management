from dataclasses import dataclass


@dataclass(slots=True)
class Person:
    first_name: str
    last_name: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
