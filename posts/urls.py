from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index_view , name='index'),
    path('create/', views.post_create_view , name='create'),
    path('delete/<int:post_id>', views.post_delete_view , name='delete'),
]

