from django.urls import path, re_path
from . import views

app_name = 'imagestat'

urlpatterns = [
    path('', views.images, name='images'),
    path('/comments/<int:id>/', views.commentsbyimagetotal, name='comments'),
]