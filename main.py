import cv2
from djitellopy import Tello
import threading

# Initialize Tello drone
tello = Tello()
tello.connect()


tello.streamon()

# Get video stream
video_stream = tello.get_frame_read()

tello.takeoff()
# Read and display video frames
while True:
    # Get the latest video frame
    frame = video_stream.frame

    # Display the video frame
    cv2.imshow("Tello Video Stream", frame)
    cv2.waitKey(1)
