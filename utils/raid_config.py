from __future__ import annotations
from interfaces.disk import AbstractDisk


class RaidConfig:
    ret_str = ""

    def __init__(self, header: str = ""):
        self.ret_str += header

    def add_disk(self, disk: AbstractDisk, spaces: "") -> None:
        self.ret_str += f"{spaces} {disk.name(disk.size)}\n"

    def __iadd__(self, other: RaidConfig) -> RaidConfig:
        self.ret_str += other.ret_str
        return self

    def __str__(self) -> str:
        return self.ret_str


