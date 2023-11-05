import cv2
import io
import socket
import struct
import time
import pickle
import zlib


gst ="v4l2src device=/dev/video0 ! video/x-raw, width=1920, height=1080, format=UYVY, framerate=30/1 ! appsink"
# def gstreamer_pipeline(
#     capture_width=1920,
#     capture_height=1080,
#     display_width=1920,
#     display_height=1080,
#     framerate=30,
#     flip_method=0,
# ):
#     return (
#         "nvarguscamerasrc ! "
#         "video/x-raw(memory:NVMM), "
#         "width=(int)%d, height=(int)%d, "
#         "format=(string)NV12, framerate=(fraction)%d/1 ! "
#         "nvvidconv flip-method=%d ! "
#         "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
#         "videoconvert ! "
#         "video/x-raw, format=(string)BGR ! appsink"
#         % (
#             capture_width,
#             capture_height,
#             framerate,
#             flip_method,
#             display_width,
#             display_height,
#         )
#     )


def show_camera():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setblocking(True)
    client_socket.connect(('192.168.0.24', 27500))
    connection = client_socket.makefile('wb')

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gst)
    cap = cv2.VideoCapture(gst, cv2.CAP_GSTREAMER)
    img_counter = 0
    if cap.isOpened():
        while True:
            ret_val, img = cap.read()
            data = pickle.dumps(img, 0)
            size = len(data)


            print("{}: {}".format(img_counter, size))
            client_socket.sendall(struct.pack(">L", size) + data)
            img_counter += 1
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()