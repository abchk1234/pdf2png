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
	$(INSTALL) -m755 pdf2png $(DESTDIR)$(bindir)
	$(INSTALL) -m644 pdf2png.png $(DESTDIR)$(icons)
	$(INSTALL) -m644 pdf2png.desktop $(DESTDIR)$(appdir)
