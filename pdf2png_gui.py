#!/usr/bin/python
import os
import subprocess
from gi.repository import Gtk, Gdk


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PDF to PNG")
        self.set_border_width(10)
        self.set_size_request(200, 20)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)
        #label = Gtk.Label(label="Resolution Number")
        #vbox.pack_start(label, False, False, 0)
        self.entry = Gtk.Entry()
        self.entry.set_text("Resolution Number")
        vbox.pack_start(self.entry, True, True, 0)

        grid = Gtk.Grid()
        vbox.add(grid)
        def reveal_child(button):
            if self.entry.get_text().isdigit() is False:
                revealer.set_reveal_child(True)
            else:
                revealer.set_reveal_child(False)
        revealer = Gtk.Revealer()
        revealer.set_reveal_child(False)
        grid.attach(revealer, 0, 0, 1, 1)

        label = Gtk.Label("       Type only numbers")
        revealer.add(label)
        #button = Gtk.Button("Reveal")
        #button.connect("clicked", reveal_child)
        #grid.attach(button, 0, 1, 1, 1)

        #self.button1 = Gtk.Button(label="Select file")
        self.button1 = Gtk.ToolButton(stock_id=Gtk.STOCK_INDEX)
        self.button1.connect("clicked", self.button_clicked)
        self.button1.connect("clicked", reveal_child)
        vbox.pack_start(self.button1, True, True, 0)

    def button_clicked(self, widget):
        resolution_number = self.entry.get_text().isdigit()
        if resolution_number is False:
            #self.RaiseWarning()
            print("")
        else:
            chooser_dialog = Gtk.FileChooserDialog(title="Select file"
            ,action=Gtk.FileChooserAction.OPEN
            ,buttons=["Convert", Gtk.ResponseType.OK, "Cancel", Gtk.ResponseType.CANCEL])
            filter_pdf = Gtk.FileFilter()
            filter_pdf.set_name("PDF Files")
            filter_pdf.add_pattern("*.pdf")
            chooser_dialog.add_filter(filter_pdf)
            chooser_dialog.run()
            filename = chooser_dialog.get_filename()

            if filename is not None:
                self.pdf_to_png(chooser_dialog, filename)
            chooser_dialog.destroy()

    #def RaiseWarning(self):
        #display_user_input = self.entry.get_text()
        #dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            #Gtk.ButtonsType.OK, "Warning %r !" % display_user_input)
        #dialog.format_secondary_text(
            #"Please type a number in the field" )
        #dialog.run()
        #dialog.destroy()

    def pdf_to_png(self, chooser_dialog, pdffilepath):
        pdfname, ext = os.path.splitext(chooser_dialog.get_filename())
        resolution = self.entry.get_text()
        arglist = ["gs", "-dBATCH", "-dNOPAUSE", "-dFirstPage=1", "-dLastPage=1",
                  "-sOutputFile=%s.png" % pdfname, "-sDEVICE=png16m",
                  "-r%s" % resolution, pdffilepath]
        sp = subprocess.Popen(args=arglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sp.communicate()

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()