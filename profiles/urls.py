from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', views.profile_view , name='profile'),
    path('update/', views.update_profile_view , name='update'),
    path('change_password/', views.change_password_view , name='change_password'),
]

