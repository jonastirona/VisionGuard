from django.urls import path
from camera.views import video_feed

urlpatterns = [
    path('', video_feed, name='video_feed'),
    path('video_feed', video_feed, name='video_feed'),
]