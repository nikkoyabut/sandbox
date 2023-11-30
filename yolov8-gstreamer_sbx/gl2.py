import gi
import cv2
import numpy as np
import threading
import queue  # Import the queue module explicitly

# Ensure Gst version is specified
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Define the video server class
class VideoServer:
    def __init__(self):
        self.pipeline = Gst.Pipeline()
        self.frame_queue = queue.Queue(maxsize=10)  # Fixed bucket size in FIFO mode
        self.running = False

    def start_server(self):
        print("    Video Server started...")
        self.running = True

        # Create GStreamer elements
        source = Gst.ElementFactory.make("v4l2src", "video-source")
        capsfilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        caps = Gst.Caps.from_string("video/x-raw, width=640, height=480")  # Adjust resolution as needed
        capsfilter.set_property("caps", caps)
        videoconvert = Gst.ElementFactory.make("videoconvert", "video-convert")
        queue = Gst.ElementFactory.make("queue", "queue")

        print("    GStreamer Elements Created...")

        # Add elements to the pipeline
        self.pipeline.add(source)
        self.pipeline.add(capsfilter)
        self.pipeline.add(videoconvert)
        self.pipeline.add(queue)

        print("    GStreamer Elements Added to Pipeline...")

        # Link the elements
        source.link(capsfilter)
        capsfilter.link(videoconvert)
        videoconvert.link(queue)

        print("    GStreamer Elements Linked...")

        # Start the pipeline
        self.pipeline.set_state(Gst.State.PLAYING)

        print("    GStreamer Pipeline started...")

        # Start producer thread
        threading.Thread(target=self.produce_frames).start()

        print("    GStreamer Producer started...")

    def stop_server(self):
        self.running = False
        self.pipeline.set_state(Gst.State.NULL)

    def produce_frames(self):
        print("        produce frames started ..")
        while self.running:
            # Retrieve frames from the pipeline
            sample = self.frame_queue.get()
            buffer = sample.get_buffer()
            print("        producing frames ..")

            # Convert GStreamer buffer to numpy array or process it as needed
            # Example: numpy_data = buffer.extract_dup(0, buffer.get_size())

            # Add frame data to the queue (simulate producing frames)
            self.frame_queue.put(buffer)

    def consume_frames(self):
        while True:
            if not self.frame_queue.empty():
                # Retrieve frames from the queue and display
                frame = self.frame_queue.get()

                # Convert the GStreamer buffer to a numpy array
                buffer_size = frame.get_size()
                _, data = frame.map(Gst.MapFlags.READ)
                np_data = np.ndarray(buffer=data, dtype=np.uint8, shape=(buffer_size,))
                frame.unmap(data)

                # Reshape the numpy array according to the frame resolution
                frame_data = np_data.reshape((480, 640, 3))  # Adjust resolution as needed

                # Display the frame using OpenCV
                cv2.imshow('Frame', frame_data)
                cv2.waitKey(1)  # Refresh the window

                # Release the frame
                frame.unref()

# Usage example
if __name__ == "__main__":
    print(".")
    print("...")
    print(".....")
    print("START ================================================")


    print("Start Video Server...")
    video_server = VideoServer()
    video_server.start_server()

    # Start a consumer thread (for displaying or processing frames)
    threading.Thread(target=video_server.consume_frames).start()

    # Keep the program running until interrupted
    try:
        while True:
            pass
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        video_server.stop_server()
        print("END ================================================")
        print(".....")
        print("...")
        print(".")
