from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.taskList, name="taskList"),
    path('activation_link', views.activateEmail, name="activate_link"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('task/<str:pk>/', views.taskdetail, name="taskdetail"),
    path('create/', views.create, name='create'),
    path('update/<str:pk>/', views.update, name="update"),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name='logout'),
]
