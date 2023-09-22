from typing import List, Optional

from exceptions.size_exceptions import DiskSizeError, RaidDiskCountError, RaidCorruptedError, DiskResizeError

from interfaces.disk import AbstractDisk
from interfaces.raid import AbstractRaid


class Raid0(AbstractRaid):
    _magic_string = b"RAID0"

    def __init__(
            self,
            name: Optional[str] = None,
            size: int = 0,
            disks: List[AbstractDisk] = (),
            is_rebuild: bool = False
    ):
        self._size = sum([disk.size for disk in disks]) - len(disks)*len(self._magic_string)
        self._name = name
        if len(disks) <= 1:
            raise RaidDiskCountError()

        for disk in disks:
            if disk.size != disks[0].size:
                raise DiskSizeError()

        self._disks = disks.copy()
        self._disk_count = len(disks)
        if not is_rebuild:
            for disk in self._disks:
                disk.write(bytearray(self._magic_string), 0)

    def append_disks(self, disks: List[AbstractDisk]) -> None:
        data = self.read(0, self._size)
        new_raid = Raid0(
            disks=self._disks+disks
        )
        self._disks = new_raid._disks.copy()
        self._disk_count = new_raid._disk_count
        self.write(data, 0)

    def remove_disk(self, disk: AbstractDisk) -> None:
        raise NotImplemented()

    def check_raid(self) -> None:
        pass

    @property
    def raid_type(self) -> str:
        return "RAID0"

    @property
    def is_valid_disk_count(self) -> bool:
        return len(self._disks) > 0

    @property
    def is_healthy(self) -> bool:
        return True

    @property
    def list_disk(self) -> List[AbstractDisk]:
        return self._disks

    def read(self, position: int, count: int) -> bytearray:
        data = bytearray()
        for current_position in range(position, count):
            disk, position_in_disk = self._flat_position_to_disk_position(current_position)
            data += (
                self._disks[disk].read(
                    position_in_disk + len(self._magic_string), 1
                )
            )
        return data

    def write(self, data: bytearray, position: int) -> None:
        if len(data) > self._size:
            raise DiskSizeError()
        for index, byte in enumerate(data):
            disk, position_in_disk = self._flat_position_to_disk_position(position + index)
            bytes_to_write = bytearray()
            bytes_to_write.append(byte)
            self._disks[disk].write(bytes_to_write, position_in_disk + len(self._magic_string))

    def resize(self, increase_size: int) -> None:
        if not self.is_resizable:
            raise DiskResizeError(f"raid is unresizable because one disk isn't resizable")

        for disk in self._disks:
            disk.resize(increase_size)

        self._size += len(self._disks)*increase_size

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

    def _flat_position_to_disk_position(self, position: int) -> tuple[int, int]:
        res = position % self._disk_count, position//self._disk_count
        return res
