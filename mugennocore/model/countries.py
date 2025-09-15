from datetime import datetime
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class Countries:
    id: int
    locale_code: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        return f"Countries({self.locale_code})"

    def __repr__(self) -> str:
        return f"Countries(id={self.id}, locale_code='{self.locale_code}', created_at={self.created_at}, updated_at={self.updated_at})"