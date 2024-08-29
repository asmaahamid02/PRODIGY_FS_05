from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('update/', views.update_profile_view , name='update'),
    path('change_password/', views.change_password_view , name='change_password'),
    path('suggested_users/', views.suggested_users_view , name='suggested_users'),
    path('<str:username>/', views.profile_view , name='profile'),
]

