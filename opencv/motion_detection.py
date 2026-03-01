from picamera2 import Picamera2
from libcamera import Transform
from pathlib import Path
import cv2
import time
import logging
from utils.logger import setup_logging

def main():
    # Logger initialization
    logs_dir = Path("logs")
    setup_logging(logs_dir / "motion.log")

    # Motion directory setup
    storage_dir = Path("storage/motion")
    storage_dir.mkdir(parents=True, exist_ok=True)

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

    cv2.namedWindow("Motion Detection", cv2.WINDOW_NORMAL)
    logging.info("Motion detection started. Press ESC to exit.")

    prev_frame = None
    last_saved_time = 0

    while True:
        # Capture the current frame from the camera as an array
        frame = camera.capture_array()

        # Convert the frame to black and white for easier processing 
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # # Apply Gaussian Blur to reduce noise and improve accuracy
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Save the previous version of the frame as "prev_frame"
        if prev_frame is None:
            prev_frame = gray
            continue

        # Compute the absolute difference between the current frame and the previous one
        frame_delta = cv2.absdiff(prev_frame, gray)
        
        # Apply a threshold to highlight significant changes (pixels > 25 become 255/white)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # Dilate the thresholded image to fill in holes and join nearby regions
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Find contours (outlines) of the moving objects
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        motion_detected = False
        
        # Iterate through detected contours
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue

            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_detected:
            current_time = time.time()

            # Save the frame only if the 2-second cooldown period has passed
            if current_time - last_saved_time > 2:
                filename = storage_dir / f"motion_{int(current_time)}.jpg"
            
                cv2.imwrite(str(filename), frame)
            
            
                logging.info(f"Motion detected! Saved: {filename}")
                last_saved_time = current_time
        cv2.imshow("Motion Detection", frame)

        prev_frame = gray

        if cv2.waitKey(1) == 27: # the 'ESC' key
            break

    camera.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
