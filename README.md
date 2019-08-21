# mdp-g14-rpi
Raspberry Pi Codebase for CZ3004 MDP

Python Version = 3.4.2
Ensure that OpenCV is installed

## To run
- Symbol Threshold Extraction: `python3 -m src.detector.SymbolIsolator.py`

   Take photos of the physical Symbol Cards sequentially (1 - 5, A - E, Arrow, Circle) with the PiCamera and check threshold segmentation quality for each Symbol before approving to save the image. Symbol Images extracted via `THRESH_BINARY` will be saved into an output folder, and will be used for image recognition. Symbol Cards will have to be backed by a white backing for the contour detection to detect the edges of the card instead of the symbol for proper perspective distortion. Take note that running this will overwrite any images existing within the output folder - do a backup before running this.
   
- Symbol Detection: `python3 -m src.detector.SymbolDetector.py`

   Begin a video stream that will attempt to detect symbols in front of it. Program will conclude the ID of the detected symbol depending on an arbitrar threshold value. Detection is done by contour matching with OpenCV's methods, which attempts to match the contour of the detected symbol from each frame in the video stream and the contours from the training images.
