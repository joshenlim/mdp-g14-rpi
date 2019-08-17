import cv2 as cv
import numpy as np
import time
import os

import VideoStream

IM_WIDTH = 640
IM_HEIGHT = 480
FRAME_RATE = 10

frame_rate_calc = 1
freq = cv.getTickFrequency()

font = cv.FONT_HERSHEY_SIMPLEX

video_stream = VideoStream.VideoStream((IM_WIDTH, IM_HEIGHT), FRAME_RATE).start()
time.sleep(1)

cam_quit = 0

while cam_quit == 0:
    image = video_stream.read()
    t1 = cv.getTickCount()

    fps_text = 'FPS: ' + str(int(frame_rate_calc))
    cv.putText(image, fps_text, (10, 26), font, 0.7, (255, 0, 255), 2, cv.LINE_AA)
    cv.imshow("Symbol Detector", image)

    t2 = cv.getTickCount()
    frame_time = (t2 - t1) / freq
    frame_rate_calc = 1 / frame_time

    key = cv.waitKey(1) & 0xFF
    if key == ord("q"):
        cam_quit = 1
        
cv.destroyAllWindows()
video_stream.stop()
