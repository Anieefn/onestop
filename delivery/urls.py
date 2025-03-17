from django.urls import path
from . import views
urlpatterns = [
    path('', views.handle_login, name='handle_login'),
    path('signup/', views.singup, name='handle_singup'),
    path('login/', views.handle_singup, name='login_singup')
]