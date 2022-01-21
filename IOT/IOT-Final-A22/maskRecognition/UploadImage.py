from urllib.parse import urlencode
from urllib.request import urlopen
from queue import Queue
import os
import threading
import time
import base64
import cv2

uploadAddress = 'http://127.0.0.1:5000/upload'

class UploadImage:
    def __init__(self) -> None:
        self.q = Queue()
        self.stop = False

    def addFrameToUpload(self, frame, fileName):
        self.q.put((frame, fileName))

    def uploadImg(self):
        while True:
            if self.q.empty():
                if self.stop:
                    break
                time.sleep(2)
                continue

            frame, fileName = self.q.get()

            cv2.imwrite('test.png', frame)

            with open('test.png', 'rb') as f:
                base64_data = base64.b64encode(f.read())

            post_data = urlencode({ 'img': base64_data, 'fileName': fileName }).encode('ascii')
            r = urlopen(uploadAddress, post_data)
            os.remove('test.png')