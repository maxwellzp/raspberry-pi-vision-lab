import cv2
from utils.camera import CameraManager
from ml.yolo.detect_onnx import YOLODetector


def main():
    detector = YOLODetector(
        model_path="ml/yolo/models/yolov8n.onnx",
        conf_threshold=0.5
    )

    with CameraManager(resolution=(640, 480)) as camera:

        while True:
            frame = camera.capture_array()

            frame = detector.detect(frame)

            cv2.imshow("YOLO ONNX", frame)

            if cv2.waitKey(1) == 27:
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
