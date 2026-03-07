import cv2
from ultralytics import YOLO

from utils.camera import CameraManager


MODEL_PATH = "/home/maksim/raspberry-pi-vision-lab/ml/yolo/models/mandarin.pt"

def main():

    model = YOLO(MODEL_PATH)

    with CameraManager(resolution=(640, 480)) as camera:

        while True:

            frame = camera.capture_array()

            results = model(frame)

            annotated = results[0].plot()

            boxes = results[0].boxes
            count = len(boxes)

            cv2.putText(
                annotated,
                f"Mandarins: {count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow("Mandarin Detector", annotated)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
