import string
import random

from interfaces.raid import AbstractRaid
from utils.raid_config import RaidConfig


def get_config(raid: AbstractRaid, spaces: "") -> RaidConfig:
    result_conf = RaidConfig(f"{raid.raid_type}:\n")
    for disk in raid.list_disk:
        if isinstance(disk, AbstractRaid):
            result_conf += get_config(disk, spaces+"--")
        result_conf.add_disk(disk, spaces)
    return result_conf


def get_random_name(file_dir: str = "./disks") -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(8)) + ".img"
