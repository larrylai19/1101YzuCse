from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from gtts import gTTS
import numpy as np
import cv2
import os

class MaskRecognition:
    def __init__(self):
        face_model = r'face_detector'
        prototxtPath = os.path.join(face_model, "deploy.prototxt")
        weightsPath = os.path.join(face_model, "res10_300x300_ssd_iter_140000.caffemodel")

        self.CONFIDENCE = 0.5
        self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        self.maskNet = load_model(os.path.join('model', 'model.h5'))

    def detect_and_predict_mask(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame,
                                    scalefactor = 1.0,  # 各通道數值的縮放比例
                                    size = (300, 300),  # 輸出圖像的尺寸 (W,H)
                                    mean = (104.0, 177.0, 123.0),  # 各通道減去的值，以降低光照的影響
                                    swapRB = True,  # 減均值順序是 (R,G,B)
        )
        
        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()
        
        locs, preds = [], []
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > self.CONFIDENCE:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                
                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                face = np.expand_dims(face, axis=0)
                pred = self.maskNet.predict(face)[0]

                preds.append(pred)
                locs.append((startX, startY, endX, endY))

        return locs, preds

    def processFrame(self, frame):
        locs, preds = self.detect_and_predict_mask(frame)
            
        l = []
        for box, pred in zip(locs, preds):
            startX, startY, endX, endY = box
            mask, withoutMask = pred
            l.append((mask, withoutMask))
            
            label = "Mask %4.2f" % mask if mask > withoutMask else "No Mask %4.2f" % withoutMask
            color = (0, 255, 0) if mask > withoutMask else (0, 0, 255)
            cv2.rectangle(frame, (startX + 20, startY), (endX, endY), color, 2)
            cv2.putText(frame, label, (startX + 10,endY + 25), cv2.FONT_HERSHEY_DUPLEX , 1, color)
        
        ifNoMask = False
        for (mask, withoutMask) in l:
            if mask <= withoutMask:
                ifNoMask = True
                break

        return ifNoMask, frame