from picamera2 import Picamera2

picamera = Picamera2()

print(picamera.sensor_modes)

# [
#     {
#         "format": SRGGB10_CSI2P,
#         "unpacked": "SRGGB10",
#         "bit_depth": 10,
#         "size": (1536, 864),
#         "fps": 120.13,
#         "crop_limits": (768, 432, 3072, 1728),
#         "exposure_limits": (9, 77208145, 20000),
#     },
#     {
#         "format": SRGGB10_CSI2P,
#         "unpacked": "SRGGB10",
#         "bit_depth": 10,
#         "size": (2304, 1296),
#         "fps": 56.03,
#         "crop_limits": (0, 0, 4608, 2592),
#         "exposure_limits": (13, 112015096, 20000),
#     },
#     {
#         "format": SRGGB10_CSI2P,
#         "unpacked": "SRGGB10",
#         "bit_depth": 10,
#         "size": (4608, 2592),
#         "fps": 14.35,
#         "crop_limits": (0, 0, 4608, 2592),
#         "exposure_limits": (26, 220416802, 20000),
#     },
# ]
