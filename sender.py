import cv2
import time
import collections
import time

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

def show_camera():

    cap = cv2.VideoCapture("v4l2src device=/dev/video2 ! video/x-raw,format=YUY2,width=1920,height=1080,framerate=30/1 ! appsink")
    out = cv2.VideoWriter("appsrc ! videoconvert ! video/x-raw,format=YUY2,width=1920,height=1080,framerate=30/1 ! jpegenc ! rtpjpegpay ! udpsink host=192.168.0.24 port=5000")
    img_counter = 0
    fpsm = fpsmeter()
    if cap.isOpened():
        while True:
            ret_val, img = cap.read()
            out.write(img)
            fpsm.addtick()
            print("FPS: ",fpsm.FPS())
            cv2.imshow('ImageWindow_1',img)
            cv2.waitKey(1)
            img_counter += 1
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()