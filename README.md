pdf2img
=======
<img src="img/pdf2img.png" alt="" /><img src="img/pdf2img-two.png" alt="" />

The conversion of PDF to image has never been easier task, but with pdf2img you have the opportunity to do this with a single mouse click. pdf2img supports up to 4 different image extensions and 10 different sdevices.

Once you download the program, before starting it copy img/pdf2img_icon.png to /usr/share/icons

    sudo cp img/pdf2img_icon.png /usr/share/icons

##How To

Increasing or decreasing the resolution will change the image quality.

Once given correct numbers for the From page and To page, click on Select PDF file to open a dialog window to browse and select the wanted PDF book, and click on Convert to convert the selected pages.

It would convert the pdf and output the image(s) in the same directory where the pdf resides.

##Credits

Forked from WifiExtender's <a href="https://github.com/wifiextender/pdf2png">pdf2png</a>, so Thanks to him :)

This has minor chnages from his version like no tray icon and some colorised fields.

For Arch Linux users check out <a href="https://aur.archlinux.org/packages/pdf2img-git/">pdf2img-git</a> in the AUR.
## Requirements

* python 
* ghostscript
* python-gobject (for debian is python-gi)
* webkitgtk, pywebkitgtk
