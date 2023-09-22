from abc import ABC, abstractmethod
from typing import Optional


class AbstractDisk(ABC):
    @abstractmethod
    def __init__(self, name: Optional[str] = None, size: int = 0):
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

    @property
    @abstractmethod
    def size(self) -> int:
        ...

    @property
    @abstractmethod
    def is_resizable(self) -> bool:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...
