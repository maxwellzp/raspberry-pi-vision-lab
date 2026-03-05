from picamera2 import Picamera2

picam2 = Picamera2()

config = picam2.create_preview_configuration()
picam2.configure(config)

picam2.start()


# • Picamera2.create_preview_configuration will generate a configuration suitable for displaying camera preview images on
# the display, or prior to capturing a still image
# • Picamera2.create_still_configuration will generate a configuration suitable for capturing a high-resolution still image
# • Picamera2.create_video_configuration will generate a configuration suitable for recording video files


# The configuration-generating methods all choose an appropriate number of buffers for their use cases:
# • create_preview_configuration requests four sets of buffers
# • create_still_configuration requests just one set of buffers (as these are normally large full resolution buffers)
# • create_video_configuration requests six buffers, as the extra work involved in encoding and outputting the video streams
# makes it more susceptible to jitter or delays, which is alleviated by the longer queue of buffers.


# When a Picamera2 object is created, it contains three embedded configurations, in the following fields:
# • preview_configuration - the same configuration as is returned by the create_preview_configuration method
# • still_configuration - the same configuration as is returned by the create_still_configuration method
# • video_configuration - the same configuration as is returned by the create_video_configuration method

