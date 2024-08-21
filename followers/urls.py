from django.urls import path
from .views import follow_view, get_followers_view, get_following_view

app_name = 'followers'

urlpatterns = [
    path('<str:username>/follow', follow_view , name='follow'),
    path('<str:username>/followers-list', get_followers_view , name='followers_list'),
    path('<str:username>/following-list', get_following_view , name='following_list'),
]
