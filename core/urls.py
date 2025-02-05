from django.urls import path
from camera.views import stream_page, video_feed

urlpatterns = [
    path('', stream_page, name='stream_page'),
    path('video_feed', video_feed, name='video_feed'),
]