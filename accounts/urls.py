from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view , name='login'),
    path('register/', views.register_view , name='register'),
    path('logout/', views.logout_view , name='logout'),
    path('profile/<str:username>/', views.profile_view , name='profile'),
    path('update_profile/', views.update_profile_view , name='update_profile'),
    path('change_password/', views.change_password_view , name='change_password'),
]

