from typing import Optional

from interfaces.disk import AbstractDisk


class RAMDisk(AbstractDisk):
    def __init__(self, size: int = 1024**3, name: Optional[str] = None):
        self._size = size
        self._ram = bytearray(size)
        self._name = name

    def read(self, position: int, count: int) -> bytearray:
        return self._ram[position:(position + count)]

    def write(self, data: bytearray, position: int) -> None:
        self._ram[position:len(data)] = data

    def resize(self, increase_size: int) -> None:
        self._ram += bytearray(increase_size)
        self._size += increase_size

    @property
    def size(self) -> int:
        return self._size

    @property
    def is_resizable(self) -> bool:
        return True

    @property
    def name(self) -> str:
        return self._name
