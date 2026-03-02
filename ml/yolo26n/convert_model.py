from ultralytics import YOLO
from pathlib import Path

# Path to original model
model_path = "ml/yolo26n/models/yolo26n.pt"

# Output directory
output_dir = Path("ml/yolo26n/models")

# Load model
model = YOLO(model_path)

model.export(
    format="ncnn", 
    project=str(output_dir),
        name="yolo26n_ncnn"
    )

ncnn_model = YOLO("ml/yolo26n/models/yolo26n_ncnn_model")

results = ncnn_model("https://ultralytics.com/images/bus.jpg")
print(results)
