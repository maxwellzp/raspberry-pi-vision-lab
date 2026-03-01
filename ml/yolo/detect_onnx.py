import cv2
import numpy as np
import onnxruntime as ort

class YOLODetector:
    """
    YOLOv8 ONNX object detector using ONNX Runtime.
    Designed for real-time inference on Raspberry Pi 5.
    """

    def __init__(self, model_path: str, conf_threshold: float = 0.5):
        # Confidence threshold for filtering detections
        self.conf_threshold = conf_threshold

        # Load ONNX model
        self.session = ort.InferenceSession(
            model_path,
            providers=["CPUExecutionProvider"]
        )


        # Get model input details
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape

        # YOLOv8 default input size
        self.img_size = 640

        # COCO class names
        self.class_names = self._load_coco_classes()
    
    def _load_coco_classes(self):
        """
        Returns list of COCO dataset class names.
        """
        return [
            "person", "bicycle", "car", "motorcycle", "airplane",
            "bus", "train", "truck", "boat", "traffic light",
            "fire hydrant", "stop sign", "parking meter", "bench",
            "bird", "cat", "dog", "horse", "sheep", "cow",
            "elephant", "bear", "zebra", "giraffe",
            "backpack", "umbrella", "handbag", "tie",
            "suitcase", "frisbee", "skis", "snowboard",
            "sports ball", "kite", "baseball bat", "baseball glove",
            "skateboard", "surfboard", "tennis racket",
            "bottle", "wine glass", "cup", "fork", "knife",
            "spoon", "bowl", "banana", "apple", "sandwich",
            "orange", "broccoli", "carrot", "hot dog", "pizza",
            "donut", "cake", "chair", "couch", "potted plant",
            "bed", "dining table", "toilet", "tv", "laptop",
            "mouse", "remote", "keyboard", "cell phone",
            "microwave", "oven", "toaster", "sink",
            "refrigerator", "book", "clock", "vase",
            "scissors", "teddy bear", "hair drier", "toothbrush"
        ]
    
    def preprocess(self, frame):
        """
        Prepare image for YOLO model:
        - resize
        - normalize
        - convert HWC -> CHW
        - add batch dimension
        """
        img = cv2.resize(frame, (self.img_size, self.img_size))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img
    
    def postprocess(self, outputs, frame):
        """
        Convert model output into bounding boxes.
        Apply confidence filtering and NMS.
        """
        predictions = outputs[0][0]
        predictions = np.transpose(predictions)

        h, w, _ = frame.shape

        boxes = []
        confidences = []
        class_ids = []

        for pred in predictions:
            scores = pred[4:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > self.conf_threshold:
                x, y, width, height = pred[0:4]

                x1 = int((x - width / 2) * w / self.img_size)
                y1 = int((y - height / 2) * h / self.img_size)
                x2 = int((x + width / 2) * w / self.img_size)
                y2 = int((y + height / 2) * h / self.img_size)

                boxes.append([x1, y1, x2 - x1, y2 - y1])
                confidences.append(float(confidence))
                class_ids.append(class_id)

        # Apply Non-Maximum Suppression (NMS)
        indices = cv2.dnn.NMSBoxes(
            boxes,
            confidences,
            self.conf_threshold,
            0.4
        )

        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w_box, h_box = boxes[i]
                class_id = class_ids[i]
                confidence = confidences[i]

                label = self.class_names[class_id]

                cv2.rectangle(
                    frame, 
                    (x, y), 
                    (x + w_box, y + h_box), 
                    (0, 255, 0), 
                    2
                )

                cv2.putText(
                    frame,
                    f"{label} {confidence:.2f}",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )
        
        return frame
    
    def detect(self, frame):
        """
        Full inference pipeline:
        preprocess -> inference -> postprocess
        """
        input_tensor = self.preprocess(frame)
        outputs = self.session.run(None, {self.input_name: input_tensor})
        return self.postprocess(outputs, frame)
