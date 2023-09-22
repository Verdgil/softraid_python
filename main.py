from disks import FileDisk, RAMDisk
from raid import Raid0, Raid1

raid = Raid0(
    disks=[
        FileDisk("./disks_image/1.img", size=8),
        FileDisk("./disks_image/2.img", size=8),
    ]
)


# raid.write(bytearray(b"abcdef"), 0)
print(raid.read(0, 6))
pass
