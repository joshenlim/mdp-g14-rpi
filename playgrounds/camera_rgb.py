from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()
camera.resolution = (640, 480)

output = PiRGBArray(camera)
camera.capture(output, 'bgr')
src = output.array

print('Capture %dx%d image' %(src.shape[1], src.shape[0]))
for i in range(1, 10):
    s = ''
    for j in range(1, 10):
      s = s + repr(src[i, j, 1]) + ' '
    print(s)
