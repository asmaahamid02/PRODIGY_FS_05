from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.index_view , name='index')
]

