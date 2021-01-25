from django.urls import path, re_path
from . import views

app_name = 'imagestat'

urlpatterns = [
    path('', views.index, name='index'),
    path('images', views.images, name='images'),
    path('comments/<int:id>/', views.commentsbyimagetotal, name='comments_total'),
    path('image/comments/<int:id>/', views.commentsbyimage, name='comments'),
    path('users', views.users, name='users'),
    path('users/activity/<int:id>', views.useractivity, name='user_activity'),
    path('users/all', views.usersbydate, name='users_by_date'),
    path('comments/all', views.commentsbydate, name='comments_by_date'),
    path('images/all', views.imagesbydate, name='images_by_date'),
    path('activity', views.totalactivity, name='activity'),
]