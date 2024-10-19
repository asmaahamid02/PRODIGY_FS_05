from django.urls import path
from .views import comment_create_view, comment_list_view, comment_delete_view

app_name = 'interactions'

urlpatterns = [
    path('<int:post_id>/comments/create', comment_create_view , name='create-comment'),
    path('<int:post_id>/comments/list', comment_list_view , name='list-comments'),
    path('<int:comment_id>/comments/delete', comment_delete_view , name='delete-comment'),
]
