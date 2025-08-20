from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class Manga:
    id: int
    country_id: int
    title_english: str
    title_native: str
    release_date: date
    finish_date: Optional[date]
    active_status: str
    comic_type: str
    cover: UUID
    mal_id: int
    created_at: datetime
    updated_at: datetime

    def update_info(
        self,
        title_english: Optional[str] = None,
        title_native: Optional[str] = None,
        release_date: Optional[date] = None,
        finish_date: Optional[date] = None,
        active_status: Optional[str] = None,
        comic_type: Optional[str] = None,
        cover: Optional[UUID] = None,
        mal_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        if title_english is not None:
            self.title_english = title_english
        if title_native is not None:
            self.title_native = title_native
        if release_date is not None:
            self.release_date = release_date
        if finish_date is not None:
            self.finish_date = finish_date
        if active_status is not None:
            self.active_status = active_status
        if comic_type is not None:
            self.comic_type = comic_type
        if cover is not None:
            self.cover = cover
        if mal_id is not None:
            self.mal_id = mal_id
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    def __str__(self) -> str:
        return (
            f"[Manga ID: {self.id}] "
            f"{self.title_english} ({self.title_native}) | "
            f"Type: {self.comic_type} | Status: {self.active_status} | "
            f"Release: {self.release_date.strftime('%Y-%m-%d')}"
            f"{f', Finish: {self.finish_date.strftime('%Y-%m-%d')}' if self.finish_date else ''} | "
            f"MAL ID: {self.mal_id} | "
            f"Country ID: {self.country_id} | "
            f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"Updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def __repr__(self) -> str:
        return (
            f"Manga(id={self.id}, title_english={self.title_english!r}, "
            f"title_native={self.title_native!r}, mal_id={self.mal_id}, "
            f"active_status={self.active_status!r}, comic_type={self.comic_type!r}, "
            f"release_date={self.release_date.isoformat()}, updated_at={self.updated_at.isoformat()})"
        )

    def detailed_info(self) -> str:
        return (
            f"Title English: {self.title_english}\n"
            f"Title Native: {self.title_native}\n"
            f"Status: {self.active_status}\n"
            f"Type: {self.comic_type}\n"
            f"Release Date: {self.release_date}\n"
            f"Finish Date: {self.finish_date}\n"
            f"MAL ID: {self.mal_id}\n"
            f"Last Updated: {self.updated_at}\n"
        )
