from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('<str:username>/',views.UserTaskList.as_view(),name='user_tasks'),
    path('<str:username>/create',views.UserTaskCreate.as_view(),name='task_create'),
    path('<str:username>/<int:pk>/',views.UserTaskUpdate.as_view(),name='task_detail'),
    path('<str:username>/<int:pk>/delete/',views.UserTaskDelete.as_view(),name='task_delete'),
    path('',views.background,name='background'),
]
