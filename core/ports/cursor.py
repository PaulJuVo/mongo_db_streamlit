from typing import Protocol, TypeVar, Iterator

T = TypeVar("T", covariant=True)

class Cursor(Protocol[T]):
    def __iter__(self) -> Iterator[T]:
        ...

    def __next__(self) -> T:
        ...
