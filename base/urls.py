from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.taskList, name="taskList"),
    path('task/<str:pk>/', views.taskdetail, name="taskdetail"),
    path('create/', views.create, name='create'),
    path('update/<str:pk>/', views.update, name="update"),
    path('delete/<str:pk>',views.delete,name='delete'),
]
