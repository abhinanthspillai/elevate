from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('browse/', views.challenge_list, name='list'),
    path('<int:pk>/', views.challenge_detail, name='detail'),
    path('<int:pk>/join/', views.join_challenge, name='join'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    
    # Mentor/Admin paths
    path('create/', views.challenge_create, name='create'),
    path('<int:pk>/edit/', views.challenge_edit, name='edit'),
    path('<int:pk>/delete/', views.challenge_delete, name='delete'),
    path('<int:pk>/tasks/', views.manage_tasks, name='manage_tasks'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
