import os

CAMERA_RES_WIDTH = 640
CAMERA_RES_HEIGHT = 480
CAMERA_FRAMERATE = 20

THRESHOLD = 75

SYMBOL_MIN_AREA = 7000
SYMBOL_MAX_AREA = 23000

SYMBOL_TYPES = ['1', '2', '3', '4', '5', 'A', 'B', 'C', 'D', 'E', 'Arrow', 'Circle']
IMG_DIR = os.path.dirname(os.path.abspath(__file__)) + '/images'
IMG_INV_DIR = os.path.dirname(os.path.abspath(__file__)) + '/images_inv'
