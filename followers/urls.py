from django.urls import path
from .views import follow_view

app_name = 'followers'

urlpatterns = [
    path('<str:username>/follow', follow_view , name='follow')
]
