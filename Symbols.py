import numpy as np
import cv2 as cv

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
