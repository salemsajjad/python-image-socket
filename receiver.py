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

    cap = cv2.VideoCapture("udpsrc port=5000 ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG,framerate=30/1 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink")
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    img_counter = 0
    time.sleep(5)
    fpsm = fpsmeter()
    if cap.isOpened():
        while True:
            ret_val, img = cap.read()
            fpsm.addtick()
            print("FPS: ",fpsm.FPS())
            cv2.imshow('ImageWindow_1',img)
            cv2.waitKey(1)
            img_counter += 1
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()