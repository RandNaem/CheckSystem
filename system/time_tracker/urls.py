from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('success/', views.success, name='success'),
    path('failure/', views.failure, name='failure'),
    # path('video_feed/', views.video_feed, name='video_feed'),
]