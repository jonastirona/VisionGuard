from django.urls import path
from camera.views import camera_stream

urlpatterns = [
    path('', camera_stream, name='camera_stream'),
    path('camera_stream', camera_stream, name='camera_stream'),
]