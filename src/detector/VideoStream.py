from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera

class VideoStream:
    def __init__(self, resolution=(640, 480), framerate=30):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.camera.vflip = False
        self.camera.hflip = False
        self.raw_capture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.raw_capture, format='bgr', use_video_port=True)
        self.frame = []
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        for frame in self.stream:
            self.frame = frame.array
            # print('frame update', self.frame[0][0])
            self.raw_capture.truncate(0)

            if self.stopped:
                self.stream.close()
                self.raw_capture.close()
                self.camera.close()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True        
