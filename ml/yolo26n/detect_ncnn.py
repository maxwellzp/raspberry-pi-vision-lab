import cv2
from picamera2 import Picamera2
from libcamera import Transform

from ultralytics import YOLO

# Initialize the Picamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)},
    transform=Transform(hflip=1, vflip=1)
)
picam2.configure(config)
picam2.start()

# Load the YOLO26 model
model = YOLO("yolo26n.pt")

while True:
    # Capture frame-by-frame
    frame = picam2.capture_array()

    # Run YOLO26 inference on the frame
    results = model(frame)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the resulting frame
    cv2.imshow("Camera", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources and close windows
cv2.destroyAllWindows()