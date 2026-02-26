from picamera2 import Picamera2
from libcamera import Transform
from datetime import datetime
from time import sleep
from pathlib import Path

DATE_TIME_FILE_FORMAT = "%Y%m%d_%H%M%S"

def build_filename(storage_dir):
    timestamp = datetime.now().strftime(DATE_TIME_FILE_FORMAT)
    return storage_dir / f"photo_{timestamp}.jpg"

def main():
    storage_dir = Path("storage/photos")
    try:
        storage_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print("Can't create a directory")
        return

    camera = Picamera2()
    config = camera.create_still_configuration(
        transform=Transform(hflip=1, vflip=1)
    )
    camera.configure(config)
    filename = build_filename(storage_dir)

    camera.start()
    sleep(3)

    camera.capture_file(str(filename))
    camera.stop()

    print(f"Photo saved: {filename}")


if __name__ == "__main__":
    main()
