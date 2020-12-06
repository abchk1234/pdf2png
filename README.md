About
=======

pdf2png converts PDF files to various image formats with a simple graphical interface. Written in python and uses ghostscript.

It currently supports 4 different image extensions: PNG, JPEG, BMP and TIFF.

## How To

Increasing or decreasing the resolution will change the image quality.

After typing correct numbers for the From page and To page, click on Select PDF file to open a dialog window. Browse and select the wanted PDF file. Click on Convert to extract and output the selected pages.

The converted image(s) are placed in the same directory where the pdf resides.

## Credits

Forked from WifiExtender's <a href="https://github.com/wifiextender/pdf2png">pdf2png</a>, so Thanks to him :)

This has minor chnages from his version like no tray icon and no over-riding of the system theme.

## Requirements

* python 3
* ghostscript
* python-gobject (for debian its python-gi)

## Installation

(as root)
~~~~
 # make install
~~~~
(or)
~~~~
 $ sudo make install
~~~~

For Arch Linux users check out <a href="https://aur.archlinux.org/packages/pdf2png/">pdf2png</a> in the AUR.
