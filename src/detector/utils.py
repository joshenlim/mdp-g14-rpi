import cv2 as cv
import numpy as np

from src.config import THRESHOLD
from src.config import MIN_CONTOUR_AREA
from src.config import MAX_CONTOUR_AREA

def preprocess_frame(image):
    '''
    Returns the grayscaled, blurred and threshold camera image
    Currently threshold value of 40 seems to be working fine
    for all colors, but may need to look into adaptive thresholding
    depending on ambient light conditions
    '''

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(blur, THRESHOLD, 255, cv.THRESH_BINARY)
    return thresh
    
def flatten_image(image, pts, width, height):
    '''
    Flatten image of a symbol card into a top-down perspective
    Returns the flattened, re-sized, grayed image
    '''
    temp_rect = np.zeros((4, 2), dtype="float32")
    
    source = np.sum(pts, axis=2)

    top_left = pts[np.argmin(source)]
    btm_right = pts[np.argmax(source)]

    diff = np.diff(pts, axis=-1)

    top_right = pts[np.argmin(diff)]
    btm_left = pts[np.argmax(diff)]

    # Clockwise
    temp_rect[0] = top_left
    temp_rect[1] = top_right
    temp_rect[2] = btm_right
    temp_rect[3] = btm_left

    max_width = 260
    max_height = 260

    dst = np.array([[0,0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]], np.float32)

    M = cv.getPerspectiveTransform(temp_rect, dst)
    warp = cv.warpPerspective(image, M, (max_width, max_height))
    warp = cv.cvtColor(warp, cv.COLOR_BGR2GRAY)
    crop = warp[40:-40, 40:-40]

    return crop

def filter_contour_size(contours):
    filtered = filter(
        lambda x: cv.contourArea(x) >= MIN_CONTOUR_AREA and cv.contourArea(x) <= MAX_CONTOUR_AREA,
        contours)
    return list(filtered)

def extract_extreme_points(contour):
    extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
    extRight = tuple(contour[contour[:, :, 0].argmax()][0])
    extTop = tuple(contour[contour[:, :, 1].argmin()][0])
    extBottom = tuple(contour[contour[:, :, 1].argmax()][0])

    return extLeft, extTop, extRight, extBottom

def extract_detected_symbol_thresh(image, extLeft, extTop, extRight, extBottom):
    placeholder_box = np.zeros((4, 2), dtype="float32")
    placeholder_box[0] = (extLeft[0], extTop[1]) # Top Left
    placeholder_box[1] = (extRight[0], extTop[1]) # Top Right
    placeholder_box[2] = (extRight[0], extBottom[1]) # Bottom Left
    placeholder_box[3] = (extLeft[0], extBottom[1]) # Bottom Right

    placeholder_width = extRight[0] - extLeft[0]
    placeholder_height = extBottom[1] - extTop[1]

    dst = np.array([
        [0,0],
        [placeholder_width - 1, 0],
        [placeholder_width - 1, placeholder_height - 1],
        [0, placeholder_height - 1]
    ], np.float32)
    M = cv.getPerspectiveTransform(placeholder_box, dst)
    warp = cv.warpPerspective(image, M, (placeholder_width, placeholder_height))
    warp = cv.cvtColor(warp, cv.COLOR_BGR2GRAY)

    symbol_card_blur = cv.GaussianBlur(warp, (5, 5), 0)
    _, symbol_thresh = cv.threshold(symbol_card_blur, 100, 255, cv.THRESH_BINARY)
    
    return symbol_thresh
