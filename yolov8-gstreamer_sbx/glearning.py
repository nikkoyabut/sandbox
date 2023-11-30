from threading import Thread
from time import sleep

import gi

gi.require_version("Gst", "1.0")

from gi.repository import Gst, GLib


Gst.init()

main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

# pipeline = Gst.parse_launch("v4l2src ! decodebin ! videoconvert ! autovideosink")
# pipeline = Gst.parse_launch("ksvideosrc ! decodebin ! videoconvert ! autovideosink")
pipeline = Gst.parse_launch('mfvideosrc device-path="\\\\\?\\usb\#vid_0c45\&pid_6a09\&mi_00\#6\&2382cd66\&0\&0000\#\{e5323777-f976-4f5b-9b55-b94699c46e44\}\\global" ! video/x-raw,width=640,height=480 ! autovideosink ! decodebin ! videoconvert ! autovideosink')
pipeline.set_state(Gst.State.PLAYING)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    pass

pipeline.set_state(Gst.State.NULL)
main_loop.quit()