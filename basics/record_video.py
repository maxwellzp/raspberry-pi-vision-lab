from picamera2 import Picamera2
from libcamera import Transform
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from datetime import datetime
from time import sleep
from pathlib import Path

DATE_TIME_FILE_FORMAT = "%Y%m%d_%H%M%S"
RECORDING_TIME_SECONDS = 10

def build_filename(storage_dir):
    timestamp = datetime.now().strftime(DATE_TIME_FILE_FORMAT)
    return storage_dir / f"video_{timestamp}.h264"

def main():
    storage_dir = Path("storage/videos")
    try:
        storage_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print("Can't create a directory")
        return
    
    filename = build_filename(storage_dir)

    camera = Picamera2()
    config = camera.create_video_configuration(
        transform=Transform(hflip=1, vflip=1)
    )
    camera.configure(config)
    
    encoder = H264Encoder(bitrate=10_000_000)
    camera.start_recording(encoder, FileOutput(str(filename)))
    print(f"Recording {RECORDING_TIME_SECONDS} seconds...")
    sleep(RECORDING_TIME_SECONDS)

    camera.stop_recording()
    camera.stop()

    print(f"Video saved: {filename}")


if __name__ == "__main__":
    main()
