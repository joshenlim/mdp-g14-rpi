import numpy as np
import cv2 as cv

from src.config import SYMBOL_TYPES
from src.config import SYMBOL_ID_MAP

class Symbol:
    '''
    Holds information about the Symbol Images, each symbol image
    will have an image and name
    '''
    def __init__(self):
        self.id = 0
        self.name = ''
        self.contour = None

def load_symbols(filepath):
    '''
    Loads the thresholded symbol images from directory, stores
    them into a list of Symbol objects
    '''
    symbols = []
    for i, symbol in enumerate(SYMBOL_TYPES):
        symbols.append(Symbol())
        symbols[i].name = symbol
        symbols[i].id = SYMBOL_ID_MAP[symbol]
        filename = '{}.jpg'.format(symbol)
        
        symbol_img = cv.imread(filepath + '/' + filename)
        train_symbol_gray = cv.cvtColor(symbol_img, cv.COLOR_BGR2GRAY)
        _, train_symbol_thresh = cv.threshold(train_symbol_gray, 127, 255, 0)
        _, train_symbol_ctrs, _ = cv.findContours(train_symbol_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        train_symbol_ctrs = sorted(train_symbol_ctrs, key=cv.contourArea, reverse=True)
        symbols[i].contour = train_symbol_ctrs[0]
        
    return symbols
