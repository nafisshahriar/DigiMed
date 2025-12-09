from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
    path('approve-doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('reject-doctor/<int:doctor_id>/', views.reject_doctor, name='reject_doctor'),
    path('add_specialization/', views.add_specialization, name='add_specialization'),
]
