from disks import FileDisk, RAMDisk
from raid import Raid0, Raid1

# raid = Raid0(
#     disks=[
#         Raid1(disks=[
#             FileDisk("./disks_image/1.img", size=32),
#             FileDisk("./disks_image/2.img", size=32),
#         ]),
#         Raid1(disks=[
#             FileDisk("./disks_image/3.img", size=32),
#             FileDisk("./disks_image/4.img", size=32),
#         ]),
#     ]
# )

raid = Raid0(
    disks=[
        FileDisk("./disks_image/1.img", size=32),
        FileDisk("./disks_image/2.img", size=32),
        FileDisk("./disks_image/3.img", size=32),
        FileDisk("./disks_image/4.img", size=32),
    ]
)

# raid.write(bytearray(b"abcdef"), 0)
print(raid.read(0, 6))
# raid.append_disks(disks=[
#     FileDisk("./disks_image/3.img", size=32),
#     FileDisk("./disks_image/4.img", size=32),
# ])
pass
