
# Coding Guidelines
To maintain a clean, readable, and maintainable codebase, please follow these rules:

## Index
  - [File Size](#file-size)
  - [Type Annotations and Validation](#type-annotations-and-validation)
  - [Async Style](#async-style)
  - [Prefer Duck Typing Over ABCs](#prefer-duck-typing-over-abstract-base-classes-abcs)
    - [Example: ABC (Avoid)](#abc-or-abstract-base-class-avoid)
    - [Example: Duck Typing (Preferred)](#duck-typing-with-protocols-recommended)
    - [Example: Duck Typing with dataclasses](#duck-typing-with-dataclasses-and-slots)

---

### File Size

Avoid writing files with more than **200 lines of code**. Keep modules focused and easy to navigate.

---

### Type Annotations and Validation

Use **Python type annotations** consistently, including arguments, return values, and important variables.

Validate with:

- `mypy  .` (entire project)
- `mypy -m mugennodb` (entire module)
- `mypy file.py` (single file)

This helps ensure type safety and clarity.

---

### Async Style

The project uses `asyncio` and `asyncpg` to handle database operations.

- Always write async functions using `async def`
- Use `await` for I/O calls, especially queries
- Avoid blocking calls inside async functions

Example:

```python
async def fetch_user(pool, user_id: int) -> dict:
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
```


## Prefer Duck Typing Over Abstract Base Classes (ABCs)

Avoid using `ABC` for defining interfaces. Instead, prefer **duck typing**: rely on the presence of methods or fields, not inheritance.

Avoid classes that are just containers for abstract methods. If you're just grouping functions, prefer a plain module.

### ABC or Abstract Base Class (Avoid)

```python
from abc import ABC, abstractmethod

class MangaRepository(ABC):
    @abstractmethod
    async def get_manga_by_id(self, manga_id: int) -> dict:
        pass

class PostgresMangaRepository(MangaRepository):
    async def get_manga_by_id(self, manga_id: int) -> dict:
        # Simulated database fetch
        return {"id": manga_id, "title": "One Piece"}

class MockMangaRepository(MangaRepository):
    async def get_manga_by_id(self, manga_id: int) -> dict:
        # Simulated mock data for testing
        return {"id": manga_id, "title": f"Fake Manga {manga_id}"}

async def show_manga(repo: MangaRepository, manga_id: int):
    manga = await repo.get_manga_by_id(manga_id)
    print(f"Manga: {manga['title']}")


# Usage
import asyncio

async def main():
    real_repo = PostgresMangaRepository()
    mock_repo = MockMangaRepository()

    await show_manga(real_repo, 1)  # Output: Manga: One Piece
    await show_manga(mock_repo, 42) # Output: Manga: Fake Manga 42

asyncio.run(main())
```

### Duck Typing with Protocols (Recommended)

Instead of relying on inheritance or abstract base classes, this project prefers duck typing combined with Python's `Protocol` from the `typing` module.  
This allows static type checking of expected methods or attributes without forcing inheritance.

Below is an example of two classes implementing the same protocol (interface) by simply having the required async method `get_manga_by_id`.  
The `show_manga` function accepts **any** object that satisfies this protocol, enabling flexibility and testability without inheritance.

```python
from typing import Protocol

class MangaRepository(Protocol):
    async def get_manga_by_id(self, manga_id: int) -> dict:
        ...

class PostgresMangaRepository:
    async def get_manga_by_id(self, manga_id: int) -> dict:
        # Simulated database fetch
        return {"id": manga_id, "title": "One Piece"}

class MockMangaRepository:
    async def get_manga_by_id(self, manga_id: int) -> dict:
        # Simulated mock data for testing
        return {"id": manga_id, "title": f"Fake Manga {manga_id}"}

async def show_manga(repo: MangaRepository, manga_id: int):
    manga = await repo.get_manga_by_id(manga_id)
    print(f"Manga: {manga['title']}")


# Usage
import asyncio

async def main():
    real_repo = PostgresMangaRepository()
    mock_repo = MockMangaRepository()

    await show_manga(real_repo, 1)  # Output: Manga: One Piece
    await show_manga(mock_repo, 42) # Output: Manga: Fake Manga 42

asyncio.run(main())
```

This pattern allows interchangeable implementations (real DB access, mocks, etc.) without inheritance, promoting clean, testable, and maintainable code.

### Duck Typing with dataclasses and slots

For simple data containers, use @dataclass(slots=True) to define lightweight, memory-efficient classes without inheritance.

``` python
from dataclasses import dataclass
from typing import Protocol

class HasName(Protocol):
    name: str

@dataclass(slots=True)
class User:
    id: int
    name: str

@dataclass(slots=True)
class FansubGroup:
    id: int
    name: str

async def welcome(entity: HasName) -> None:
    print(f"Welcome, {entity.name}!")


# Usage
import asyncio

async def main():
    await welcome(User(id=1, name="Alice"))
    await welcome(FansubGroup(id=42, name="ScanTeam"))

asyncio.run(main())
```

Using slots=True reduces memory consumption and prevents dynamic attribute assignment, making data classes safer and more performant.
This approach is idiomatic, clear, and works well with static type checkers like mypy.