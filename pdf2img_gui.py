#!/usr/bin/python
import os
import subprocess
from gi.repository import Gtk, Gdk


class MainWindow(Gtk.Window):

    def about_dialog(self, widget):
        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_name("About")
        aboutdialog.set_version("v0.2")
        aboutdialog.set_comments("Convert PDF book to multiple images\nin various formats with a single mouse click")
        aboutdialog.set_website("http://linux.sytes.net/")
        aboutdialog.set_website_label("Developer Website")
        aboutdialog.set_authors(["Aaron Caffrey"])
        aboutdialog.run()
        aboutdialog.destroy()

    #def comboboxtext_changed(self, comboboxtext):
            #active = comboboxtext.get_active_text()

    def button_clicked(self, widget):
        resolution_number = self.entry.get_text().isdigit()
        if resolution_number is not False:
            chooser_dialog = Gtk.FileChooserDialog(title="Select PDF file"
            ,action=Gtk.FileChooserAction.OPEN
            ,buttons=["Convert", Gtk.ResponseType.OK, "Cancel", Gtk.ResponseType.CANCEL])
            filter_pdf = Gtk.FileFilter()
            filter_pdf.set_name("PDF Filter")
            filter_pdf.add_pattern("*.pdf")
            chooser_dialog.add_filter(filter_pdf)
            chooser_dialog.run()
            filename = chooser_dialog.get_filename()

            if filename is not None:
                self.pdf_to_png(chooser_dialog, filename)
            chooser_dialog.destroy()
        else:
            self.RaiseWarning()

    def RaiseWarning(self):
        display_user_input = self.entry.get_text()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, "Warning %r !" % display_user_input)
        dialog.format_secondary_text(
            "Please type a number in the field" )
        dialog.run()
        dialog.destroy()

    def pdf_to_png(self, chooser_dialog, pdffilepath):
        pdfname, ext = os.path.splitext(chooser_dialog.get_filename())
        resolution = self.entry.get_text()
        arglist = ["gs", "-dBATCH", "-dNOPAUSE", "-dFirstPage=%s" % self.spinbutton.get_text(), "-dLastPage=%s" % self.spinbutton2.get_text(),
                  "-sOutputFile=%s" % pdfname + " page %01d." + "%s" % self.comboboxtext2.get_active_text(), "-sDEVICE=%s" % self.comboboxtext.get_active_text(),
                  "-r%s" % resolution, pdffilepath]
        sp = subprocess.Popen(args=arglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sp.communicate()

    def __init__(self):
        Gtk.Window.__init__(self, title="PDF to IMG")
        self.set_border_width(10)
        self.set_size_request(200, 20)
        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1))

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=13)
        self.add(vbox)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        vbox.add(grid)

        label = Gtk.Label(label="Resolution Number")
        grid.attach(label, Gtk.PositionType.LEFT, 1, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_text("100")
        self.entry.set_max_length(4)
        grid.attach(self.entry, Gtk.PositionType.LEFT, 2, 1, 1)

        label = Gtk.Label(label="About")
        grid.attach(label, Gtk.PositionType.RIGHT, 1, 1, 1)

        self.button_about = Gtk.ToolButton(stock_id=Gtk.STOCK_ABOUT)
        self.button_about.connect("clicked", self.about_dialog)
        grid.attach(self.button_about, Gtk.PositionType.RIGHT, 2, 1, 1)

        label = Gtk.Label(label="From page:")
        grid.attach(label, Gtk.PositionType.LEFT, 3, 1, 1)
        adjustment = Gtk.Adjustment(value=1, lower=1, upper=9999, step_increment=1)
        self.spinbutton = Gtk.SpinButton(adjustment=adjustment, climb_rate=1, digits=0)
        grid.attach(self.spinbutton, Gtk.PositionType.LEFT, 4, 1, 1)

        label = Gtk.Label(label="To:")
        grid.attach(label, Gtk.PositionType.RIGHT, 3, 1, 1)
        adjustment = Gtk.Adjustment(value=1, lower=1, upper=9999, step_increment=1)
        self.spinbutton2 = Gtk.SpinButton(adjustment=adjustment, climb_rate=1, digits=0)
        grid.attach(self.spinbutton2, Gtk.PositionType.RIGHT, 4, 1, 1)

        label = Gtk.Label(label="Image format")
        grid.attach(label, Gtk.PositionType.LEFT, 5, 1, 1)
        self.comboboxtext2 = Gtk.ComboBoxText()
        self.comboboxtext2.append("png", "png")
        self.comboboxtext2.append("jpg", "jpg")
        self.comboboxtext2.append("bmp", "bmp")
        self.comboboxtext2.append("tiff", "tiff")
        self.comboboxtext2.set_active(0)
        #self.comboboxtext2.connect("changed", self.comboboxtext_changed)
        grid.attach(self.comboboxtext2, Gtk.PositionType.LEFT, 6, 1, 1)

        label = Gtk.Label(label="sDevice")
        grid.attach(label, Gtk.PositionType.RIGHT, 5, 1, 1)
        self.comboboxtext = Gtk.ComboBoxText()
        self.comboboxtext.append("png16m", "png16m")
        self.comboboxtext.append("pngalpha", "pngalpha")
        self.comboboxtext.append("pnggray", "pnggray")
        self.comboboxtext.append("jpeg", "jpeg")
        self.comboboxtext.append("jpegcmyk", "jpegcmyk")
        self.comboboxtext.append("jpeggray", "jpeggray")
        self.comboboxtext.append("bmp16m", "bmp16m")
        self.comboboxtext.append("bmpgray", "bmpgray")
        self.comboboxtext.append("tiff24nc", "tiff24nc")
        self.comboboxtext.append("tiffgray", "tiffgray")
        self.comboboxtext.set_active(0)
        #self.comboboxtext.connect("changed", self.comboboxtext_changed)
        grid.attach(self.comboboxtext, Gtk.PositionType.RIGHT, 6, 1, 1)

        label = Gtk.Label(label="Select PDF file")
        vbox.add(label)
        #self.button1 = Gtk.Button(label="Select file")
        self.button1 = Gtk.ToolButton(stock_id=Gtk.STOCK_INDEX)
        self.button1.connect("clicked", self.button_clicked)
        vbox.pack_start(self.button1, True, True, 0)

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()