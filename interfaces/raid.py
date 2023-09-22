from abc import abstractmethod
from typing import List, Optional

from disk import AbstractDisk


class AbstractRaid(AbstractDisk):
    @abstractmethod
    def __init__(self, size: int = 0, name: Optional[str] = None,
                 disks: List[AbstractDisk] = (), is_rebuild: bool = False):
        ...

    @abstractmethod
    def append_disks(self, disks: List[AbstractDisk]) -> None:
        ...

    @abstractmethod
    def remove_disk(self, disk: AbstractDisk) -> None:
        ...

    @abstractmethod
    def check_raid(self) -> None:
        ...
    
    @abstractmethod
    @property
    def raid_type(self) -> str:
        ...

    @abstractmethod
    @property
    def is_valid_disk_count(self) -> bool:
        ...

    @abstractmethod
    @property
    def is_healthy(self) -> bool:
        ...

    @abstractmethod
    @property
    def list_disk(self) -> List[AbstractDisk]:
        ...

