from picamera2 import Picamera2

picam2 = Picamera2()

# Can capture multiple images with a time delay
# picam2.start_and_capture_files("/tmp/test{:d}.jpg", initial_delay=5, delay=5, num_files=10)

picam2.start_and_capture_files("/tmp/test{:d}.jpg", initial_delay=0, delay=0, num_files=10)
