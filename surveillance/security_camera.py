import logging
import cv2
import time

from utils.logger import setup_logging
from surveillance import config
from utils.camera import CameraManager

def main():
    setup_logging(config.LOG_FILE)
    logging.info("Security camera started")

    config.EVENTS_DIR.mkdir(exist_ok=True)

    background = None
    last_event_time = 0

    with CameraManager(resolution=config.RESOLUTION) as camera:

        while True:
            frame = camera.capture_array()
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if background is None:
                background = gray
                continue

            delta = cv2.absdiff(background, gray)
            thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(
                thresh,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            motion_detected = False

            for contour in contours:
                if cv2.contourArea(contour) < config.MIN_AREA:
                    continue

                motion_detected = True

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            current_time = time.time()

            if motion_detected and (current_time - last_event_time > config.COOLDOWN_SECONDS):
                logging.info("Motion detected")

                if config.SAVE_IMAGES:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    image_path =config.EVENTS_DIR / f"motion_{timestamp}.jpg"
                    cv2.imwrite(str(image_path), frame)
                    logging.info(f"Saved event: {image_path}")
                
                last_event_time = current_time
            
            cv2.imshow("Secutiry Camera", frame)

            if cv2.waitKey(1) == 27:
                break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
