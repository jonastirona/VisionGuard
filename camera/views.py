# Python
from django.shortcuts import render

def camera_stream(request):
    """
    Render a template with an HTML5 <video> element (or a custom player)
    that connects to the streaming socket server on port 8000.
    """
    context = {"stream_port": 8000}
    return render(request, "camera/stream.html", context)