#!/usr/bin/python
import os
import sys
import subprocess
from gi.repository import Gtk, Gdk, GdkPixbuf

program_icon = "/usr/share/pixmaps/pdf2png.png"

class MainWindow(Gtk.Window):

    @staticmethod
    def about_dialog(self, widget):
        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_logo_icon_name(Gtk.STOCK_ABOUT)
        aboutdialog.set_program_name("pdf2png")
        aboutdialog.set_version("v0.5")
        aboutdialog.set_comments("Convert PDF to multiple images in various formats\nlike PNG with a single mouse click\n")
        aboutdialog.set_website("https://github.com/abchk1234/pdf2png")
        aboutdialog.set_website_label("Website\n")
        aboutdialog.set_authors(["Aaron", "\nSpecial thanks to:\nAaditya"])
        aboutdialog.set_license("""This program is free software;
you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the
License, or (at your option) any later version.
See http://www.gnu.org/licenses/gpl.html
for more details.""")
        aboutdialog.run()
        aboutdialog.destroy()

    def comboboxtext2_changed(self, comboboxtext2):
            active = comboboxtext2.get_active_text()
            if active == "png16m" or active == "pngalpha" or active == "pnggray":
                self.comboboxtext2.set_active(0)
            if active == "jpeg" or active == "jpegcmyk" or active == "jpeggray":
                self.comboboxtext2.set_active(1)
            if active == "bmp16m" or active == "bmpgray":
                self.comboboxtext2.set_active(2)
            if active == "tiff24nc" or active == "tiffgray":
                self.comboboxtext2.set_active(3)

    def comboboxtext_changed(self, comboboxtext):
            active = comboboxtext.get_active_text()
            if active == "png":
                self.comboboxtext.set_active(0)
            if active == "jpg":
                self.comboboxtext.set_active(3)
            if active == "bmp":
                self.comboboxtext.set_active(6)
            if active == "tiff":
                self.comboboxtext.set_active(8)

    def button_clicked(self, widget):
        if int(self.spinbutton.get_text()) > int(self.spinbutton2.get_text()):
            dialog_reversed_numbers = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
                Gtk.ButtonsType.OK, "Reversed Numbers")
            dialog_reversed_numbers.format_secondary_text(
                "From page {0} To {1} = OK\nFrom page {2} To {3} = Not working"
                .format(self.spinbutton2.get_text(),self.spinbutton.get_text(),
                    self.spinbutton.get_text(), self.spinbutton2.get_text()))
            dialog_reversed_numbers.run()
            dialog_reversed_numbers.destroy()
        else:
            resolution_number = self.entry.get_text().isdigit()
            if resolution_number is not False:
                chooser_dialog = Gtk.FileChooserDialog(title="Select PDF file"
                ,action=Gtk.FileChooserAction.OPEN
                ,buttons=["Convert", Gtk.ResponseType.OK, "Cancel", Gtk.ResponseType.CANCEL])
                filter_pdf = Gtk.FileFilter()
                filter_pdf.set_name("PDF Filter")
                filter_pdf.add_pattern("*.pdf")
                chooser_dialog.add_filter(filter_pdf)
                response = chooser_dialog.run()
                filename = chooser_dialog.get_filename()

                if response == Gtk.ResponseType.OK:
                    self.pdf_to_img(chooser_dialog, filename)
                if response == Gtk.ResponseType.CANCEL:
                    pass
                chooser_dialog.destroy()
            else:
                self.RaiseWarning()

    def RaiseWarning(self):
        display_user_input = self.entry.get_text()
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK, "Warning {0} !".format(display_user_input))
        dialog.format_secondary_text(
            "Please type a number in the field" )
        dialog.run()
        dialog.destroy()

    def pdf_to_img(self, chooser_dialog, pdffilepath):
        pdffile = chooser_dialog.get_filename()
        pdfname, ext = os.path.splitext(pdffile)
        resolution = self.entry.get_text()
        if os.path.exists('/usr/bin/gs'):
            arglist = ["gs", "-dBATCH", "-dNOPAUSE", "-dFirstPage={0}".format(self.spinbutton.get_text()), "-dLastPage={0}".format(self.spinbutton2.get_text()), "-sOutputFile={0}-page%d.{1}".format(pdfname, self.comboboxtext2.get_active_text()), "-sDEVICE={0}".format(self.comboboxtext.get_active_text()),"-r{0}".format(resolution), pdffilepath]
            sp = subprocess.Popen(args=arglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = sp.communicate()
        else:
            err = 'gs (GhostScript) not available for conversion'
        if err:
            dialog2 = Gtk.MessageDialog(chooser_dialog, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Warning!")
            dialog2.format_secondary_text("{0}".format(err))
            dialog2.run()
            dialog2.destroy()
            return
        # The output is in the form of page1, page2, .., even though input pages may have been from 3 to 5
        # So we move the output pages in terms of input ones
        # Pages are renamed in reverse order so they do not overlap
        # previous pages get overwritten, ie, if there was a page 1 before, it would get probably get overwritten..
        x = int(self.spinbutton.get_text()) # input page no. lower value
        y = int(self.spinbutton2.get_text()) # input page no. upper value
        z = y - x + 1 # no of pages to be renamed
        e = self.comboboxtext2.get_active_text() # extension of output file
        while y >= x:
            if y == 1:
                break # single (first) page
            else:
                os.system('mv -f "{0}-page{1}.{2}"'.format(pdfname, z, e) + ' "{0}-page{1}.{2}"'.format(pdfname, y, e))
            z = z - 1
            y = y - 1

        dialog2 = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, "Processed!")
        dialog2.format_secondary_text("Converted page(s) placed with the original file.\nTry refreshing the folder if they do not appear.")
        dialog2.run()
        dialog2.destroy()

        # Open the directory in which the pdf file and converted images are
        #pdfdir = os.path.dirname(pdffile)
        #subprocess.call(["exo-open", pdfdir])

    def __init__(self):
        Gtk.Window.__init__(self, title="PDF to PNG")

        if os.path.isfile(program_icon):
            self.set_icon_from_file(program_icon)

        self.set_border_width(6)
        self.set_size_request(200, 20)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        grid = Gtk.Grid()
        grid.set_row_spacing(7)
        grid.set_column_spacing(5)
        vbox.add(grid)

        label = Gtk.Label(label=" Resolution ")
        grid.attach(label, Gtk.PositionType.LEFT, 1, 1, 1)

        self.entry = Gtk.Entry()
        self.entry.set_width_chars(1)
        self.entry.set_text("300")
        self.entry.set_max_length(4)
        grid.attach(self.entry, Gtk.PositionType.LEFT, 2, 1, 1)

        label = Gtk.Label(label="About")
        grid.attach(label, Gtk.PositionType.RIGHT, 1, 1, 1)

        self.button_about = Gtk.ToolButton(stock_id=Gtk.STOCK_ABOUT)
        self.button_about.connect("clicked", self.about_dialog, "about")
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
        self.comboboxtext2.connect("changed", self.comboboxtext_changed)
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
        self.comboboxtext.connect("changed", self.comboboxtext2_changed)
        grid.attach(self.comboboxtext, Gtk.PositionType.RIGHT, 6, 1, 1)

        label = Gtk.Label(label="Select PDF file")
        vbox.add(label)
        self.button1 = Gtk.ToolButton(stock_id=Gtk.STOCK_INDEX)
        self.button1.connect("clicked", self.button_clicked)
        vbox.pack_start(self.button1, True, True, 0)

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
