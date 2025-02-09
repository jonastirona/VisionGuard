import cv2
import numpy as np

class VideoProcessor:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        return frame

    def get_processed_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        # Resize the frame to improve processing speed
        frame = cv2.resize(frame, (640, 480))
        frame = self.detect_faces(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def release(self):
        self.cap.release()