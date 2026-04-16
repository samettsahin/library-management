from dataclasses import dataclass


@dataclass(frozen=True)
class Author:
    first_name: str
    last_name: str
    birth_year: int | None = None
    nationality: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
