import numpy as np
import cv2 as cv

from config import SYMBOL_TYPES

class Symbols:
    '''
    Holds information about the Symbol Images, each symbol image
    will have an image and name
    '''
    def __init__(self):
        self.img = []
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
        filename = '{}.jpg'.format(symbol)
        symbols[i].img = cv.imread(filepath + '/' + filename)
        
    return symbols
