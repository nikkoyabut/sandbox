import gi
import cv2
import numpy as np
import threading
import queue
import time  # Add this line to import the time module

gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)


class VideoServer:
    def __init__(self):
        self.pipeline = Gst.parse_launch(
            "v4l2src device=\\\\\\\\?\\\\usb\\#vid_0c45\\&pid_6a09\\&mi_00\\#6\\&2382cd66\\&0\\&0000\\#\\{e5323777-f976-4f5b-9b55-b94699c46e44\\}\\\\global ! video/x-raw, width=640, height=480 ! appsink name=sink emit-signals=True" 
        )
        self.appsink = self.pipeline.get_by_name("sink")
        self.frame_queue = queue.Queue(maxsize=10)
        self.running = False

    def start_server(self):
        print("     Video Server started...")
        self.running = True
        self.pipeline.set_state(Gst.State.PLAYING)
        print("     GStreamer Pipeline created...")
        threading.Thread(target=self.produce_frames).start()


    def produce_frames(self):
        while self.running:
            sample = self.appsink.emit("pull-sample")
            if sample is not None:
                buffer = sample.get_buffer()
                if buffer:
                    print("          Received a sample buffer.")
                    # Your buffer handling code here
            else:
                print("          Sample is None. No frame available.")
            time.sleep(0.1)

    def consume_frames(self):
        while True:
            if not self.frame_queue.empty():
                print("Consume frames started...")
                frame = self.frame_queue.get()

                buffer_size = frame.get_size()
                _, data = frame.map(Gst.MapFlags.READ)
                np_data = np.ndarray(buffer=data, dtype=np.uint8, shape=(buffer_size,))
                frame.unmap(data)

                frame_data = np_data.reshape((480, 640, 3))

                cv2.imshow('Frame', frame_data)
                cv2.waitKey(1)

                frame.unref()

    def stop_server(self):
        self.running = False
        self.pipeline.set_state(Gst.State.NULL)

if __name__ == "__main__":
    print("START ================================================")

    print("Start Video Server...")
    video_server = VideoServer()
    video_server.start_server()

    threading.Thread(target=video_server.consume_frames).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        video_server.stop_server()
        print("END ================================================")


    def consume_frames(self):
        while True:
            if not self.frame_queue.empty():
                print("Consume frames started...")
                frame = self.frame_queue.get()

                buffer_size = frame.get_size()
                _, data = frame.map(Gst.MapFlags.READ)
                np_data = np.ndarray(buffer=data, dtype=np.uint8, shape=(buffer_size,))
                frame.unmap(data)

                frame_data = np_data.reshape((480, 640, 3))

                cv2.imshow('Frame', frame_data)
                cv2.waitKey(1)

                frame.unref()

if __name__ == "__main__":
    print("START ================================================")

    print("Start Video Server...")
    video_server = VideoServer()
    video_server.start_server()

    threading.Thread(target=video_server.consume_frames).start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        video_server.stop_server()
        print("END ================================================")
