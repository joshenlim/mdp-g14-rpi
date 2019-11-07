# mdp-g14-rpi
Raspberry Pi Codebase for CZ3004 MDP

Ensure that OpenCV 3.3.0 is installed

## Set Up on Raspberry Pi
   Working on Raspbian Jessie (2016-02-26), with Python version 3.4.2. Ensure that OpenCV 3.3.0 is installed as well.

   Ensure that `picamera` version is at 1.1.0 (`sudo pip3 install "picamera[array]" == 1.1.0`)
   
   Ensure that `at-spi2-core` is installed (`sudo apt-get install at-spi2-core`)

## To run
- Symbol Threshold Extraction: `python3 -m src.detector.SymbolIsolator.py`

   Take photos of the physical Symbol Cards sequentially (1 - 5, A - E, Arrow, Circle) with the PiCamera and check threshold segmentation quality for each Symbol before approving to save the image. Symbol Images extracted via `THRESH_BINARY` will be saved into an output folder, and will be used for image recognition. Symbol Cards will have to be backed by a white backing for the contour detection to detect the edges of the card instead of the symbol for proper perspective distortion. Take note that running this will overwrite any images existing within the output folder - do a backup before running this.
   
- Main Program: `sudo python3 -m main`

   Begins a multithread session that will establish communications with N7 Tablet, Arduino and PC. Also starts a video stream that will attempt to detect symbols in front of it. Program will conclude the ID of the detected symbol depending on an arbitrary threshold value.
   Still a work in progress - multithread communication is commented out for now to test the detection alone.

## Connecting a new bluetooth device
`sudo hciconfig hci0 piscan`

`hcitool scan`
