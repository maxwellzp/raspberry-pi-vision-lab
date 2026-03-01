from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
EVENTS_DIR = BASE_DIR / "storage/events"

RESOLUTION = (640, 480)

MIN_AREA = 1500

LOG_FILE = LOGS_DIR / "security_camera.log"

SAVE_IMAGES = True
COOLDOWN_SECONDS = 5

