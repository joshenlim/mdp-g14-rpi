import os

CAMERA_RES_WIDTH = 640
CAMERA_RES_HEIGHT = 480
CAMERA_FRAMERATE = 30

THRESHOLD = 75
MATCH_THRESHOLD = 0.23

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
