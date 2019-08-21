import numpy as np
import cv2 as cv

from config import SYMBOL_TYPES
from config import SYMBOL_ID_MAP

class Symbols:
    '''
    Holds information about the Symbol Images, each symbol image
    will have an image and name
    '''
    def __init__(self):
        self.img = []
        self.id = 0
        self.name = ''

def load_symbols(filepath):
    '''
    Loads the thresholded symbol images from directory, stores
    them into a list of Symbol objects
    '''
    symbols = []
    for i, symbol in enumerate(SYMBOL_TYPES):
        symbols.append(Symbols())
        symbols[i].name = symbol
        symbols[i].id = SYMBOL_ID_MAP[symbol]
        filename = '{}.jpg'.format(symbol)
        symbols[i].img = cv.imread(filepath + '/' + filename)
        
    return symbols
