from time import time
from MaskRecognition import MaskRecognition
from UploadImage import UploadImage
from datetime import datetime
import threading
import time
import cv2
import random
import os

def main(cap, uploadHP):
    maskRecognition = MaskRecognition()

    while True:
        reg, frame = cap.read()

        if not reg:
            print('No frame!')
            continue

        ifNoMask, frame = maskRecognition.processFrame(frame)

        cv2.imshow('Frame', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == ord("q"):
            break

        if ifNoMask:
            now = datetime.now()
            fileName = now.strftime('%Y-%m-%d %H-%M-%S.jpg')
            uploadHP.addFrameToUpload(frame, fileName)

            if random.random() > 0.5:
                audioPath = os.path.join('audios', 'Larry.mp3')
                os.system(f'omxplayer -o local -p {audioPath} > /dev/null 2>&1')
            else:
                audioPath = os.path.join('audios', 'Daniel.mp3')
                os.system(f'omxplayer -o local -p {audioPath} > /dev/null 2>&1')

            print('Detect no mask.')

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    uploadHP = UploadImage()
    uploadThread = threading.Thread(target = uploadHP.uploadImg)
    uploadThread.start()
    try:
        main(cap, uploadHP)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print('Waiting for upload image...')
        uploadHP.stop = True
        uploadThread.join()
        print('Upload image complete.')