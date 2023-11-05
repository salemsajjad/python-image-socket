import numpy as np
import base64
import pickle
import cv2
import time


original = cv2.imread('1.jpg')
encoded  = cv2.imencode(".jpg", original, [int(cv2.IMWRITE_JPEG_QUALITY), 50])[1]
tic = time.time() 

b64 = base64.b64encode(encoded)

# ps  = pickle.dumps(encoded, 0)

recieved = np.frombuffer(base64.b64decode(b64), dtype=np.uint8)
image = cv2.imdecode(recieved, cv2.IMREAD_COLOR)
cv2.imshow('image', image)
cv2.waitKey()
