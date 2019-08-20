import cv2 as cv
import numpy as np

from config import THRESHOLD
from config import SYMBOL_MIN_AREA
from config import SYMBOL_MAX_AREA

def filter_contours(contours):
    filtered = []
    for contour in contours:
        size = cv.contourArea(contour)
        if ((size < SYMBOL_MAX_AREA) and (size > SYMBOL_MIN_AREA)):
            filtered.append(contour)
    return filtered

def preprocess_frame(image):
    '''
    Returns the grayscaled, blurred and threshold camera image
    Currently threshold value of 40 seems to be working fine
    for all colors, but may need to look into adaptive thresholding
    depending on ambient light conditions

    TO-DO: Figure out adaptive thresholding cause 40 seems to low
    easily distorted by ambient lighting, and still doesnt work perfectly
    for red symbols, and also think - 100 is actually working when detecting
    the bounding boxes for symbols, why? And right now the detection is still very noisy
    '''

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5, 5), 0)

    # img_width, img_height = np.shape(image)[:2]
    # background_level = gray[int(img_height / 100)][int(img_width / 2)]
    # thresh_level = background_level + BACKGROUND_TRESH

    _, thresh = cv.threshold(blur,THRESHOLD, 255, cv.THRESH_BINARY)

    return thresh

def find_symbol(thresh_image):
    '''
    Find symbols in a thresholded camera image
    '''
    _, contours, hierarchy = cv.findContours(thresh_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)

    if len(contours) > 0:
        symbol = contours[0]
        x, y, w, h = cv.boundingRect(symbol)
        return [x, y, w, h]
    else:
        return None
        
    # index_sort = sorted(range(lens(contours)), key=lambda i : cv.contourArea(contours[i]), reverse=True)

def perspective_transform(image, contour, width, height):
    extLeft = tuple(contour[contour[:, :, 0].argmin()][0])
    extRight = tuple(contour[contour[:, :, 0].argmax()][0])
    extTop = tuple(contour[contour[:, :, 1].argmin()][0])
    extBottom = tuple(contour[contour[:, :, 1].argmax()][0])

    #cv.circle(image, extLeft, 8, (255, 0, 0), 2)
    #cv.circle(image, extRight, 8, (255, 0, 0), -1)
    #cv.circle(image, extTop, 8, (255, 0, 0), -1)
    #cv.circle(image, extBottom, 8, (255, 0, 0), -1)

    #cv.circle(image, (extLeft[0], extTop[1]), 8, (0, 255, 0), 2)
    #cv.circle(image, (extRight[0], extTop[1]), 8, (0, 255, 0), 2)
    #cv.circle(image, (extRight[0], extBottom[1]), 8, (0, 255, 0), 2)
    #cv.circle(image, (extLeft[0], extBottom[1]), 8, (0, 255, 0), 2)

    #cv.imshow("test", image)

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

    return warp
    

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
