from picamera2 import Picamera2, Preview
from libcamera import Transform

picam2 = Picamera2()

# The supported transforms are:
# • Transform() - the identity transform, which is the default
# • Transform(hflip=1) - horizontal flip
# • Transform(vflip=1) - vertical flip
# • Transform(hflip=1, vflip=1) - horizontal and vertical flip (equivalent to a 180 degree rotation)

picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600, transform=Transform(hflip=1))

picam2.start()
