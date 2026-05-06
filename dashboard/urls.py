from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('mentor/', views.mentor_dashboard, name='mentor_dashboard'),
    path('admin_panel/', views.admin_dashboard, name='admin_dashboard'),
]
