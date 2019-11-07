import os

LOCALE = "UTF-8"

# Android BT connection settings
RFCOMM_CHANNEL = 8
# raspberryHotPotato: B8:27:EB:14:A1:9C
# MDPGrp14: B8:27:EB:12:0D:6F
RPI_MAC_ADDR = "B8:27:EB:14:A1:9C"
N7_MAC_ADDR = ""
UUID = "00000000-0000-1000-8000-00805F9B34FC"

# PC Wifi connection settings
# raspberryHotPotato: 192.168.3.1
# MDPGrp14: 192.168.14.14
WIFI_IP = "192.168.14.14"
WIFI_PORT = 3053

# Arduino USB connection settings
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

# Image Recognition Settings
CAMERA_RES_WIDTH = 540
CAMERA_RES_HEIGHT = 480
CAMERA_FRAMERATE = 32

MIN_CONTOUR_AREA = 2000 # Assuming at a distance of 20 - 25cm
MAX_CONTOUR_AREA = 9000 # Assuming min distance of 10 - 15cm
MATCH_CONFIDENCE_COUNT = 5
THRESHOLD = 75
MATCH_THRESHOLD = 0.23
ARROW_PIXEL_THRESHOLD = 10

SYMBOL_TYPES = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E', 'Arrow', 'Circle']
IMG_DIR = os.path.dirname(os.path.abspath(__file__)) + '/detector/train_images'

SYMBOL_ID_MAP = {
    'Arrow': 0,
    'Arrow_white': 1,
    'Arrow_red': 2,
    'Arrow_green': 3,
    'Arrow_blue': 4,
    'Circle': 5,
    '1': 6,
    '2': 7,
    '3': 8,
    '4': 9,
    '5': 10,
    'A': 11,
    'B': 12,
    'C': 13,
    'D': 14,
    'E': 15
}
