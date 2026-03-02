import os
import numpy as np
import cv2
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

from utils.camera import CameraManager

KNOWN_DIR = "ml/face/known_faces"
THRESHOLD = 0.5

def load_known_faces():
    known = {}
    for file in os.listdir(KNOWN_DIR):
        if file.endswith(".npy"):
            name = file.replace(".npy", "")
            known[name] = np.load(os.path.join(KNOWN_DIR, file))
    return known

def main():
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0)

    known_faces = load_known_faces()

    with CameraManager() as camera:
        while True:
            frame = camera.capture_array()
            faces = app.get(frame)

            for face in faces:
                box = face.bbox.astype(int)
                embedding = face.embedding

                name = "Unknown"
                for known_name, known_embedding in known_faces.items():
                    sim = cosine_similarity(
                        [embedding],
                        [known_embedding]
                    )[0][0]

                    if sim > THRESHOLD:
                        name = f"{known_name} ({sim:.2f})"

                cv2.rectangle(frame, box[:2], box[2:], (0,255,0), 2)
                cv2.putText(
                    frame,
                    name,
                    (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0,255,0),
                    2
                )

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) == ord("q"):
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

