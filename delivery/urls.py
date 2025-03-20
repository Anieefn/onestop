from django.urls import path
from . import views
urlpatterns = [
    path('', views.handle_login, name='handle_login'),
    path('signup/', views.singup, name='singup'),
    path('handle_signup/', views.handle_singup, name='handle_singup'),
    path('stock/<str:userid>/', views.stock_view, name='stock_view'),
    path('update/<int:userid>/<int:pid>/', views.update_stock, name='update_stock'),
    path('delete/<int:userid>/<int:pid>/', views.delete_user, name='delete_user'),
    ################ admin ###############
    path('home/', views.home, name='home'),
]