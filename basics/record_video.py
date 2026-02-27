from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from datetime import datetime
from time import sleep
from pathlib import Path
import logging

DATE_TIME_FILE_FORMAT = "%Y%m%d_%H%M%S"
RECORDING_TIME_SECONDS = 10

def build_filename(storage_dir):
    timestamp = datetime.now().strftime(DATE_TIME_FILE_FORMAT)
    return storage_dir / f"video_{timestamp}.h264"

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
    storage_dir = Path("storage/videos")
    logs_dir = Path("logs")
    try:
        storage_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print("Can't create a directory")
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
        config = camera.create_video_configuration(
        transform=Transform(hflip=1, vflip=1))
        camera.configure(config)

        encoder = H264Encoder(bitrate=10_000_000)

        camera.start_recording(encoder, FileOutput(str(filename)))
        logging.info(f"Recording {RECORDING_TIME_SECONDS} seconds...")
        sleep(RECORDING_TIME_SECONDS)

        camera.stop_recording()
        camera.stop()

        logging.info(f"Video saved: {filename}")
    except Exception as e:
        logging.error(f"Camera error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
