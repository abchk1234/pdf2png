SHELL = /bin/bash
INSTALL = /usr/bin/install
MSGFMT = /usr/bin/msgfmt
SED = /bin/sed
DESTDIR =
bindir = /usr/bin
localedir = /usr/share/locale
icons = /usr/share/pixmaps
appdir = /usr/share/applications
mandir = /usr/share/man/man1/

all:

install: all
	$(INSTALL) -d $(DESTDIR)$(bindir)
	$(INSTALL) -d $(DESTDIR)$(icons)
	$(INSTALL) -d $(DESTDIR)$(appdir)
	$(INSTALL) -m755 bin/pdf2png.py $(DESTDIR)$(bindir)/pdf2png
	$(INSTALL) -m644 install/pdf2png.png $(DESTDIR)$(icons)
	$(INSTALL) -m644 install/pdf2png.desktop $(DESTDIR)$(appdir)
