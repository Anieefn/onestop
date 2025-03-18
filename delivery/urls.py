from django.urls import path
from . import views
urlpatterns = [
    path('', views.handle_login, name='handle_login'),
    path('signup/', views.singup, name='handle_singup'),
    path('login/', views.add_post, name="add_post"),
]