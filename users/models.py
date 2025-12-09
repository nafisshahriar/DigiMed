from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    IS_PATIENT = 'patient'
    IS_DOCTOR = 'doctor'
    IS_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (IS_PATIENT, 'Patient'),
        (IS_DOCTOR, 'Doctor'),
        (IS_ADMIN, 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=IS_PATIENT)
    
    def is_doctor(self):
        return self.role == self.IS_DOCTOR
    
    def is_patient(self):
        return self.role == self.IS_PATIENT
    
    def is_admin(self):
        return self.role == self.IS_ADMIN

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    
    # New Phase 2 Fields
    is_verified = models.BooleanField(default=False)
    start_time = models.TimeField(default='09:00')
    end_time = models.TimeField(default='17:00')
    working_days = models.CharField(max_length=100, default='Mon,Tue,Wed,Thu,Fri', help_text="Comma-separated days (e.g. Mon,Tue)")
    
    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True, help_text="Basic medical history summary")
    
    def __str__(self):
        return f"Patient: {self.user.username}"

