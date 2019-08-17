# mdp-g14-rpi
Raspberry Pi Codebase for CZ3004 MDP

Python Version = 3.4.2
Ensure that OpenCV is installed

## To run
- Symbol Threshold Extraction: `python3 SymbolIsolator.py`
Take photos of the physical Symbol Cards sequentially (1 - 5, A - E, Arrow, Circle) with the PiCamera and check threshold segmentation quality for each Symbol before approving to save the image. Symbol Images extracted via `THRESH_BINARY` and `TRESH_BINARY_INV` will be saved into an output folder in the root directory, and will be used for image recognition.
