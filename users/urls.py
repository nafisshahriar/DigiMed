from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Dashboards
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    
    # Appointments
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
]
