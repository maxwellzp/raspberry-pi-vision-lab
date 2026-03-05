from picamera2 import Picamera2

picam2 = Picamera2()

# For simple image capture
picam2.start_and_capture_file("test.jpg")
