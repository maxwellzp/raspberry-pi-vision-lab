from picamera2 import Picamera2
import logging
from libcamera import Transform
from pathlib import Path
import cv2
import time
from utils.logger import setup_logging

def main():
    # Logger initialization
    logs_dir = Path("logs")
    setup_logging(logs_dir / "face_detection.log")

    # Camera configuration
    camera = Picamera2()
    config = camera.create_preview_configuration(
        main={
            "format": "RGB888", 
            "size": (640, 480)},
        transform=Transform(hflip=1, vflip=1)
    )
    camera.configure(config)
    camera.start()

    # Load pre-trained Haar Cascade classifier for face detection
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        logging.error("Failed to load Haar Cascade. Check if OpenCV is installed correctly.")
        return
    
    cv2.namedWindow("Face Detection", cv2.WINDOW_NORMAL)
    logging.info("Face detection started. Press ESC to exit.")

    prev_time = time.time()
    face_present = False

    while True:
        # Capture a new frame from the camera as an RGB array
        frame = camera.capture_array()

        # Convert the frame to grayscale, as the face detector requires it
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect faces in the grayscale image
        # scaleFactor: how much the image size is reduced at each image scale
        # minNeighbors: how many neighbors each candidate rectangle should have to retain it
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30)
        )

        current_face_state = len(faces) > 0

        if current_face_state and not face_present:
            logging.info("Face detected")

        if not current_face_state and face_present:
            logging.info("Face lost")

        face_present = current_face_state

        # Draw a rectangle around every detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Calculate Frames Per Second (FPS)
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Display the FPS counter on the frame
        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        cv2.imshow("Face Detection", frame)

        if cv2.waitKey(1) == 27: # the 'ESC' key
            break
    
    camera.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
