import cv2
import io
import socket
import struct
import time
import pickle
import zlib

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.setblocking(True)
# client_socket.connect(('192.168.0.24', 27500))
# connection = client_socket.makefile('wb')

cap = cv2.VideoCapture("v4l2src device=/dev/video2 io-mode=dmabuf ! videoscale ! videorate ! video/x-raw, width=1920, height=1080, framerate=30/1 ! videoconvert ! appsink")

#cam.set(3, 320);
#cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cap.read()
    print(img_counter)
    # result, frame = cv2.imencode('.jpg', frame, encode_param)
    # data = zlib.compress(pickle.dumps(frame, 0))
    # data = pickle.dumps(frame, 0)
    # size = len(data)


    # # print("{}: {}".format(img_counter, size))
    # client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
