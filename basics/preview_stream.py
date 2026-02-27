from picamera2 import Picamera2
from libcamera import Transform
import cv2
import logging
from pathlib import Path

def setup_logging(log_file) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def main():
    logs_dir = Path("logs")
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Can't create logs directory: {e}")
        return
    log_file = logs_dir / "app.log"
    setup_logging(log_file)

    camera = Picamera2()
    cv2.namedWindow("Raspberry Pi 5 Camera", cv2.WINDOW_NORMAL)
    config = camera.create_preview_configuration(
        main={
            "format": "RGB888", 
            "size": (1280, 720)
            },
        transform=Transform(hflip=1, vflip=1)
        )
    camera.configure(config)
    camera.start()

    logging.info("Press ESC to exit")

    while True:
        frame = camera.capture_array()

        cv2.imshow("Raspberry Pi 5 Camera", frame)

        if cv2.waitKey(1) == 27:
            break
    
    cv2.destroyAllWindows()
    camera.stop()

if __name__ == "__main__":
    main()
