from abc import abstractmethod
from typing import List, Optional

from interfaces.disk import AbstractDisk


class AbstractRaid(AbstractDisk):
    @abstractmethod
    def __init__(
            self,
            name: Optional[str] = None,
            size: int = 0,
            disks: List[AbstractDisk] = (),
            is_rebuild: bool = False
    ):
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
    
    @property
    @abstractmethod
    def raid_type(self) -> str:
        ...

    @property
    @abstractmethod
    def is_valid_disk_count(self) -> bool:
        ...

    @property
    @abstractmethod
    def is_healthy(self) -> bool:
        ...

    @property
    @abstractmethod
    def list_disk(self) -> List[AbstractDisk]:
        ...

