from django.http import StreamingHttpResponse
from camera.utils.camera_utils import VideoCamera
from camera.utils.audio_utils import AudioStream
from django.shortcuts import render

def gen(camera, audio):
    while True:
        video_frame = camera.get_frame()
        audio_frame = audio.get_frame()

        if video_frame is None or audio_frame is None:
            break

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n\r\n'
               b'--audio\r\n'
               b'Content-Type: audio/wav\r\n\r\n' + audio_frame + b'\r\n\r\n')

def stream_page(request):
    return render(request, 'stream.html')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera(), AudioStream()),
                    content_type='multipart/x-mixed-replace; boundary=frame')