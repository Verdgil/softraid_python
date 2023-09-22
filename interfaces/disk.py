from abc import ABC, abstractmethod
from typing import Optional


class AbstractDisk(ABC):
    @abstractmethod
    def __init__(self, size: int = 0, name: Optional[str] = None):
        ...

    @abstractmethod
    def read(self, position: int, count: int) -> bytearray:
        ...

    @abstractmethod
    def write(self, data: bytearray, position: int) -> None:
        ...

    @abstractmethod
    def resize(self, increase_size: int) -> None:
        ...

    @abstractmethod
    @property
    def size(self) -> int:
        ...

    @abstractmethod
    @property
    def is_resizable(self) -> bool:
        ...

    @abstractmethod
    @property
    def name(self) -> str:
        ...
