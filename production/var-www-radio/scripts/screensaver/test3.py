#!/usr/bin/python

import os
import sys
 
import gtk
from gtk import gdk
 
# the secret sauce is to get the "window id" out of $XSCREENSAVER_WINDOW

class ScreenSaverWindow(gtk.Window):
 
    def __init__(self):
        gtk.Window.__init__(self)
        pass
 
    def do_realize(self):
        if self.flags() & gtk.REALIZED:
            return
       
        ident = os.environ.get('XSCREENSAVER_WINDOW')
        if not ident is None:
            self.window = gtk.gdk.window_foreign_new(int(ident, 16))
            self.window.set_events(gtk.gdk.EXPOSURE_MASK |
                                   gtk.gdk.STRUCTURE_MASK)
            x, y, w, h, depth = self.window.get_geometry()
            self.size_allocate(gtk.gdk.Rectangle(x, y, w, h))
            self.set_default_size(w, h)
            self.set_decorated(False)
 
        else:
            self.window = gtk.gdk.Window(
                self.get_parent_window(),
                width=self.allocation.width,
                height=self.allocation.height,
                window_type=gtk.gdk.WINDOW_TOPLEVEL,
                wclass=gtk.gdk.INPUT_OUTPUT,
                event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK)

        # run in both cases
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.set_flags(self.flags() | gtk.REALIZED)

 
window = ScreenSaverWindow()
#window.set_title('Floaters')
#window.set_default_size(1024, 768)
window.connect('delete-event', gtk.main_quit)
window.realize()
 
window.modify_bg(gtk.STATE_NORMAL, gdk.color_parse("black"))
 
label = gtk.Label()
label.set_markup("<span foreground=\"white\"><big>Hello, world</big></span>")
label.show()
window.add(label)
 
window.show()
 
gtk.main()


