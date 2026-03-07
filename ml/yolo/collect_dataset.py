import os
import cv2
from datetime import datetime
from utils.camera import CameraManager


SAVE_DIR = "ml/yolo/datasets/mandarin/images"

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    counter = len(os.listdir(SAVE_DIR))

    print("Press 's' to save a frame")
    print("Press 'q' to quit")

    with CameraManager(resolution=(640, 480), hflip=True, vflip=True) as camera:
        while True:
            frame = camera.capture_array()

            cv2.imshow("Dataset Collector", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                filename = f"mandarin_{counter:04d}.jpg"
                path = os.path.join(SAVE_DIR, filename)
                cv2.imwrite(path, frame)
                print(f"[SAVED] {filename}")
                counter += 1

            elif key == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()