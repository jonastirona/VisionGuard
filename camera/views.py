from django.http import StreamingHttpResponse
from camera.utils.camera_utils import VideoProcessor

def gen(camera):
    while True:
        frame = camera.get_processed_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoProcessor()),
                    content_type='multipart/x-mixed-replace; boundary=frame')