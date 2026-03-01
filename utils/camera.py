from picamera2 import Picamera2
from libcamera import Transform

class CameraManager:
    def __init__(self, resolution=(640, 480), hflip=True, vflip=True):
        self.resolution = resolution
        self.hflip = hflip
        self.vflip = vflip
        self.camera = None
    
    def __enter__(self):
        self.camera = Picamera2()

        config = self.camera.create_preview_configuration(
            main={
                "format": "RGB888",
                "size": self.resolution
            },
            transform=Transform(
                hflip=int(self.hflip),
                vflip=int(self.vflip)
            )
        )

        self.camera.configure(config)
        self.camera.start()

        return self.camera
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.camera:
            self.camera.stop()
