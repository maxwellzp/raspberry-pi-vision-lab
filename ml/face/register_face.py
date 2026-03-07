import os
import numpy as np
import cv2
from insightface.app import FaceAnalysis

from utils.camera import CameraManager

SAVE_DIR = "ml/face/known_faces"
NAME = "maksim"

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0)

    embeddings = []

    with CameraManager() as camera:
        print("Look at the camera... Press 's' to save a photo")

        while True:
            frame = camera.capture_array()
            faces = app.get(frame)

            for face in faces:
                box = face.bbox.astype(int)
                cv2.rectangle(frame, box[:2], box[2:], (0,255,0), 2)

            cv2.imshow("Register Face", frame)

            key = cv2.waitKey(1)

            if key == ord("s") and faces:
                embeddings.append(faces[0].embedding)
                print(f"Saved: {len(embeddings)}")

            if key == ord("q"):
                break

    if embeddings:
        mean_embedding = np.mean(embeddings, axis=0)
        np.save(f"{SAVE_DIR}/{NAME}.npy", mean_embedding)
        print("Face photo saved!")

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
