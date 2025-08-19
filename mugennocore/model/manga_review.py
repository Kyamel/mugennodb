   from dataclasses import dataclass

   @dataclass(slots=True)
   class MangaReview:
        reviewId: int
        mangaId: int