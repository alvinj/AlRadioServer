#!/usr/bin/python

import os
import sys
 
import gtk
from gtk import gdk
 
# the secret sauce is to get the "window id" out of $XSCREENSAVER_WINDOW
# 1) http://pastebin.com/nSCiq1P3
# 2) http://stackoverflow.com/questions/4598581/python-clutter-set-display

class ScreenSaverWindow(gtk.Window):
 
    def __init__(self):
        gtk.Window.__init__(self)
        pass
 
    def realize(self):
        f = open("/var/www/radio/scripts/screensaver/out.txt", "w")
        if self.flags() & gtk.REALIZED:
            return
       
        window_xid = os.getenv("XSCREENSAVER_WINDOW")
        f.write('window_xid: ' + str(window_xid) + "\n")
 
        if window_xid != None:
            f.write('window_xid != None:')
            end_index = window_xid.find(" ")
            if end_index > 0:
                window_xid = int(window_xid[:end_index], 0)
                f.write('window_xid: ' + str(window_xid) + "\n")
            else:
                window_xid = int(window_xid, 0)
                f.write('window_xid: ' + str(window_xid) + "\n")
 
            if window_xid != 0:
                f.write('window_xid != 0:' + "\n")
                self.window = gdk.window_foreign_new(window_xid)
 
                if self.window != None:
                    f.write('self.window != None:')
                    self.window.set_events (gdk.EXPOSURE_MASK | gdk.STRUCTURE_MASK)
 
        if self.window == None:
            f.write('self.window == None:' + "\n")
            self.window = gdk.Window(None, 1024, 768, gdk.WINDOW_TOPLEVEL,
                                     (gdk.EXPOSURE_MASK | gdk.STRUCTURE_MASK),
                                     gdk.INPUT_OUTPUT)
 
        if self.window != None:
            f.write('self.window != None:' + "\n")
            #self.window.add_filter(lambda *args: self.filter_event(args))
            self.set_flags(self.flags() | gtk.REALIZED)

        f.close
 
f = open("/var/www/radio/scripts/screensaver/out.txt", "a")
window = ScreenSaverWindow()
f.write("1\n")
window.set_title('Floaters')
f.write("2\n")
window.connect('delete-event', gtk.main_quit)
f.write("3\n")
#window.set_default_size(1024, 768)
window.realize()
f.write("4\n")
 
window.modify_bg(gtk.STATE_NORMAL, gdk.color_parse("black"))
f.write("5\n")
 
label = gtk.Label()
f.write("6\n")
label.set_markup("<span foreground=\"white\"><big>Hello, world</big></span>")
f.write("7\n")
label.show()
f.write("8\n")
window.add(label)
f.write("9\n")
 
window.show()
f.write("10\n")
 
gtk.main()
f.write("11\n")

f.close()
