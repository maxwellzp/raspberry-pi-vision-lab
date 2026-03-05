from picamera2.encoders import H264Encoder, Quality
from picamera2 import Picamera2
import time

picam2 = Picamera2()

picam2.configure(picam2.create_video_configuration())

# H264Encoder
# The H264Encoder class implements an H.264 encoder using the Pi’s in-built hardware, 
# accessed through the V4L2 kernel drivers, supporting up to 1080p30.

# JpegEncoder
# The JpegEncoder class implements a multi-threaded software JPEG encoder, which can 
# also be used as a motion JPEG (“MJPEG”) encoder

# MJPEGEncoder
# The MJPEGEncoder class implements an MJPEG encoder using the Raspberry Pi’s in-built 
# hardware, accessed through the V4L2 kernel drivers. 

# “Null” Encoder
# The base Encoder class can be used as the “null” encoder, that is, an encoder that 
# does nothing at all. It outputs exactly the same frames as were passed to it, without any compression or processing whatsoever. It could be used to record YUV or RGB frames (according to the output format of the stream being recorded), or even, as in the following example, the raw Bayer frames that are being output by the image sensor.

encoder = H264Encoder()

# • Quality.VERY_LOW
# • Quality.LOW
# • Quality.MEDIUM - this is the default for both functions if the parameter is not specified
# • Quality.HIGH
# • Quality.VERY_HIGH

picam2.start_recording(encoder, 'test.h264', quality=Quality.HIGH)
time.sleep(10)
picam2.stop_recording()
