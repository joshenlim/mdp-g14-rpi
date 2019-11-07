from src.detector.SymbolDetector import SymbolDetector
from imutils.video import FPS
detector = SymbolDetector(width=650, height=480, framerate=32)
detector.start()
fps = FPS().start()

frame_count = 0

while frame_count < 10000:
    frame = detector.get_frame()
    symbol_match = detector.detect(frame)
    if symbol_match is not None:
        print('Symbol Match ID: ' + str(symbol_match))
    fps.update()
    frame_count = frame_count + 1

fps.stop()
print('Elapsed Time: ' + str(fps.elapsed()))
print('Frames per Sec: ' + str(fps.fps()))
