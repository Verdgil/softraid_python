from typing import List, Optional

from exceptions.size_exceptions import DiskSizeError, RaidDiskCountError, RaidCorruptedError, DiskResizeError

from interfaces.disk import AbstractDisk
from interfaces.raid import AbstractRaid


class Raid1(AbstractRaid):
    _magic_string = b"RAID1"

    def __init__(
            self,
            name: Optional[str] = None,
            size: int = 0,
            disks: List[AbstractDisk] = (),
            is_rebuild: bool = False
    ):
        self._size = min([disk.size for disk in disks]) - len(self._magic_string)
        self._name = name
        if len(disks) <= 1:
            raise RaidDiskCountError()

        for disk in disks:
            if disk.size != disks[0].size:
                raise DiskSizeError()

        self._disks = disks.copy()

        if not is_rebuild:
            for disk in self._disks:
                disk.write(bytearray(self._magic_string), 0)

    def append_disks(self, disks: List[AbstractDisk]) -> None:
        for disk in disks:
            if disk.size != self._disks[0].size:
                raise DiskSizeError()

        for disk in disks:
            disk.write(self._disks[0].read(0, self._disks[0].size), 0)

    def remove_disk(self, disk: AbstractDisk) -> None:
        if disk not in self._disks:
            return None

        if len(self._disks) == 1:
            raise RaidDiskCountError()

        self._disks.remove(disk)
        disk.write(bytearray(disk.size*b"\x00"), 0)

    @property
    def raid_type(self) -> str:
        return "RAID1"

    @property
    def is_valid_disk_count(self) -> bool:
        return len(self._disks) >= 1

    @property
    def is_healthy(self) -> bool:
        try:
            self.check_raid()
        except RaidCorruptedError as e:
            return False

        return len(self._disks) > 1

    @property
    def list_disk(self) -> List[AbstractDisk]:
        return self._disks

    def read(self, position: int, count: int) -> bytearray:
        return self._disks[0].read(position + len(self._magic_string), count)

    def check_raid(self) -> None:
        if len(self._disks) <= 1:
            return None

        data = self._disks[0].read(0, self._disks[0].size)
        for disk in self._disks:
            tmp_data = disk.read(0, disk.size)
            for ind, byte in enumerate(tmp_data):
                if (byte ^ data[ind]) != 0:
                    raise RaidCorruptedError()

    def write(self, data: bytearray, position: int) -> None:
        for disk in self._disks:
            disk.write(data, position + len(self._magic_string))

    def resize(self, increase_size: int) -> None:
        if not self.is_resizable:
            raise DiskResizeError(f"raid is unresizable because one disk isn't resizable")

        for disk in self._disks:
            disk.resize(increase_size)

        self._size += increase_size

    @property
    def size(self) -> int:
        return self._size

    @property
    def is_resizable(self) -> bool:
        for disk in self._disks:
            if not disk.is_resizable:
                return False
        return True

    @property
    def name(self) -> str:
        return self._name
