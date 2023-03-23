from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('register/', views.register, name='register'),
    path('for-got-password/', views.forgot, name='for_got_password'),
    path('logout/', views.user_logout, name='logout'),
    path('my-account/', views.myaccount, name='my-account'),
]