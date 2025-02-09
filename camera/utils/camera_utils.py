import cv2

class VideoCamera:
    def __init__(self, source=0): # 0 for default camera, 1 for external camera
        self.cam = cv2.VideoCapture(source)
        if not self.cam.isOpened():
            raise IOError("Cannot access webcam")

    def get_frame(self):
        success, frame = self.cam.read()
        if not success:
            return None
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def __del__(self):
        self.cam.release()