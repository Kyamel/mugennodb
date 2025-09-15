from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass(slots=True)
class AttachmentTypes:
    id: int
    name: str
    mime_type: Optional[str] = None
    icon_url: Optional[str] = None

    def __str__(self) -> str:
        return f"AttachmentTypes({self.name})"

    def __repr__(self) -> str:
        return f"AttachmentTypes'(id={self.id}, name='{self.name}', mime_type='{self.mime_type}')"
