#!/usr/bin/env python

import gtk
import os

gtk.gdk.window_process_all_updates()

# os.environ.get('XSCREENSAVER_WINDOW')
window_xid = os.getenv ("XSCREENSAVER_WINDOW")

window_xid = 0x2000006
gdk_window = gtk.gdk.window_foreign_new(window_xid)

print(gdk_window.get_geometry())

