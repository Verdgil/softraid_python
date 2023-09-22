from exceptions.size_exceptions import DiskSizeError
from interfaces.disk import AbstractDisk


def convert(input_disk: AbstractDisk, output_disk: AbstractDisk) -> AbstractDisk:
    if input_disk.size > output_disk.size and not output_disk.is_resizable:
        raise DiskSizeError("")

    output_disk.write(input_disk.read(0, input_disk.size), 0)

