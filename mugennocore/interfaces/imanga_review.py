   from typing import Protocol, runtime_checkable

   @runtime_checkable
   class IMangaReview(Protocol):
        reviewId: int
        mangaId: int

        def __str__(self) -> str: ...
        def __repr__(self) -> str: ...