from pydantic.dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class StaffRoles:
    id: int
    name: str
    description: Optional[str] = None

    def __str__(self) -> str:
        return f"StaffRoles({self.name})"

    def __repr__(self) -> str:
        return f"StaffRoles(id={self.id}, name='{self.name}', description='{self.description}')"