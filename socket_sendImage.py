

from SpinnakerCamera import CSpinnakerCamera
from matplotlib import pyplot as plt
import cv2
import json
import collections

import io
import socket
import struct
import time
import pickle
import zlib

class fpsmeter:

    def __init__(self):
        self.q = collections.deque(maxlen=100)#type: typing.Deque

    def addtick(self):
        self.q.append(time.time())

    def FPS(self):
        fps = 0
        if len(self.q) > 2:
            t1 = self.q[0]
            t2 = self.q[-1]
            fps = 1.0 * (len(self.q) - 1) / (t2 - t1)
        return fps
    
    
CAMERA_CONFIG = json.load(open("cameraconfig.json",'r'))

camera = CSpinnakerCamera(
            in_cameraId=CAMERA_CONFIG['cameraId'],
            in_grabImageCols=CAMERA_CONFIG['grabImageCols'],
            in_grabImageRows=CAMERA_CONFIG['grabImageRows'],
            in_offsetX=CAMERA_CONFIG['offsetX'],
            in_offsetY=CAMERA_CONFIG['offsetY'],
            in_frameRate=CAMERA_CONFIG['frameRate'],
            in_firstShutter=CAMERA_CONFIG['firstShutter'],
            in_firstGain=CAMERA_CONFIG['firstGain'],
            in_videoMode=CAMERA_CONFIG['videoMode'],
            in_binningHorizontal=CAMERA_CONFIG['binningHorizontal'],
            in_binningVertical=CAMERA_CONFIG['binningVertical'])

cameraReady = False
fpsm = fpsmeter()

while not cameraReady:
    print("Initialize Camera")
    cameraReady = camera.initCamera()
    time.sleep(1)
print('camera ready')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setblocking(True)
client_socket.connect(('192.168.0.24', 13500))
connection = client_socket.makefile('wb')
print('socket connection successful')
for img_counter in range(10000):
    
    frame = camera.grabImage()
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    
    fpsm.addtick()
    print("FPS: ",fpsm.FPS())
    
    data = pickle.dumps(frame, 0)
    size = len(data)
    
    client_socket.sendall(struct.pack(">L", size) + data)
#     print("{}: {}".format(img_counter, size))

    