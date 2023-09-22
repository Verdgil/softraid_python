import os.path
from typing import Optional

import utils.utils
from exceptions.size_exceptions import DiskSizeError
from interfaces.disk import AbstractDisk


class FileDisk(AbstractDisk):
    def __init__(
            self,
            name: Optional[str] = None,
            size: int = 1024 ** 2,
    ):
        self._file_name = name if name else utils.utils.get_random_name()
        self._size = size
        self._data = None
        if self._file_exist():
            self._read_file()
        else:
            self._data = bytearray(size)
            self._write_file()
        self._name = name

    def read(self, position: int, count: int) -> bytearray:
        return self._data[position:(position + count)]

    def write(self, data: bytearray, position: int) -> None:
        if position + len(data) > self._size:
            raise DiskSizeError
        self._data[position:(position+len(data))] = data
        self._write_file()

    def resize(self, increase_size: int) -> None:
        self._data += bytearray(increase_size)
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

    def _read_file(self):
        with open(self._file_name, "rb") as file:
            self._data = bytearray(file.read())

    def _write_file(self):
        with open(self._file_name, "wb") as file:
            file.write(bytes(self._data))

    def _file_exist(self):
        return os.path.exists(self._file_name)
