from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True)
class Country:
    """Representa um País do banco de dados."""

    id: int
    lang: str
    locale_code: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        """Retorna uma representação simples e legível do país."""
        return f"{self.locale_code.upper()} ({self.lang})"

    def __repr__(self) -> str:
        """Retorna uma representação detalhada e inequívoca do país."""
        return (
            f"Country(id={self.id}, lang={self.lang!r}, "
            f"locale_code={self.locale_code!r}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )