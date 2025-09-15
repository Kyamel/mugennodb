from dataclasses import field
from datetime import datetime
from pydantic. dataclasses import dataclass


@dataclass(slots=True)
class Tags:
    id: int
    name: str
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return f"Tags({self.name})"

    def __repr__(self) -> str:
        return f"Tags(id={self.id}, name='{self.name}', created_at={self.created_at})"