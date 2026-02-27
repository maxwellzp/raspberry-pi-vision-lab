from picamera2 import Picamera2
from libcamera import Transform
from datetime import datetime
from time import sleep
from pathlib import Path
import logging

DATE_TIME_FILE_FORMAT = "%Y%m%d_%H%M%S"

def build_filename(storage_dir):
    timestamp = datetime.now().strftime(DATE_TIME_FILE_FORMAT)
    return storage_dir / f"photo_{timestamp}.jpg"

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
    storage_dir = Path("storage/photos")
    logs_dir = Path("logs")
    try:
        storage_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Can't create storage/photos directory: {e}")
        return
    filename = build_filename(storage_dir)

    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Can't create logs directory: {e}")
        return
    log_file = logs_dir / "app.log"
    setup_logging(log_file)
    try:
        camera = Picamera2()

        config = camera.create_still_configuration(
        transform=Transform(hflip=1, vflip=1))

        camera.configure(config)
        camera.start()
        sleep(3)

        camera.capture_file(str(filename))
        camera.stop()

        logging.info(f"Photo saved: {filename}")
    except Exception as e:
        logging.error(f"Camera error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
