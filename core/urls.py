from django.urls import path, include
from django.views.generic import TemplateView
from camera.views import video_feed

urlpatterns = [
    path('', video_feed, name='video_feed'),
    path('stream/', TemplateView.as_view(template_name='stream.html')),
]