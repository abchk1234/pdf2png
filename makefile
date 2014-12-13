NAME = pdf2png
VERSION = 0.5
SHELL = /bin/bash
INSTALL = /usr/bin/install
MSGFMT = /usr/bin/msgfmt
SED = /bin/sed
DESTDIR =
bindir = /usr/bin
localedir = /usr/share/locale
icons = /usr/share/pixmaps
mandir = /usr/share/man/man1/
deskdir = /usr/share/applications
docdir = /usr/share/doc/$(NAME)
appdir = /usr/share/$(NAME)-$(VERSION)

all:

install: all
	$(INSTALL) -d $(DESTDIR)$(bindir)
	$(INSTALL) -d $(DESTDIR)$(icons)
	$(INSTALL) -d $(DESTDIR)$(deskdir)
	$(INSTALL) -d $(DESTDIR)$(docdir)
	$(INSTALL) -d $(DESTDIR)$(appdir)
	$(INSTALL) -m755 bin/pdf2png.py $(DESTDIR)$(bindir)/pdf2png
	$(INSTALL) -m644 install/pdf2png.png $(DESTDIR)$(icons)
	$(INSTALL) -m644 install/pdf2png.desktop $(DESTDIR)$(deskdir)
	$(INSTALL) -m644 README.md $(DESTDIR)$(docdir)
	$(INSTALL) -m644 COPYING $(DESTDIR)$(docdir)
	$(INSTALL) -m644 makefile $(DESTDIR)$(appdir)
