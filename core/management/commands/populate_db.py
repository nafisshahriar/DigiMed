from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User, DoctorProfile, PatientProfile, Specialization
from appointments.models import Appointment
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        Appointment.objects.all().delete()
        DoctorProfile.objects.all().delete()
        PatientProfile.objects.all().delete()
        Specialization.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write('Creating Specializations...')
        spec_names = ['Cardiology', 'Dermatology', 'Neurology', 'Pediatrics', 'General Practice']
        specs = {}
        for name in spec_names:
            specs[name] = Specialization.objects.create(name=name, description=f'Specialists in {name}')

        self.stdout.write('Creating Admin User...')
        if not User.objects.filter(username='admin_user').exists():
            User.objects.create_user(
                username='admin_user',
                email='admin@digimed.com',
                password='password123',
                role=User.IS_ADMIN,
                is_staff=True,
                is_superuser=True
            )

        self.stdout.write('Creating Doctors...')
        doctors = []
        for i in range(5):
            username = f'doctor{i+1}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='password123',
                role=User.IS_DOCTOR,
                first_name=f'Doctor',
                last_name=f'{i+1}',
                is_active=True # Auto activate for dummy data
            )
            spec_name = spec_names[i % len(spec_names)]
            DoctorProfile.objects.create(
                user=user,
                specialization=specs[spec_name],
                bio=f'Experienced specialist in {spec_name} with over 10 years of practice.',
                is_verified=True,
                working_days="Mon,Tue,Wed,Thu,Fri"
            )
            doctors.append(user)
            self.stdout.write(f'Created {username}')

        self.stdout.write('Creating Patients...')
        patients = []
        for i in range(5):
            username = f'patient{i+1}'
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='password123',
                role=User.IS_PATIENT,
                first_name=f'Patient',
                last_name=f'{i+1}'
            )
            PatientProfile.objects.create(
                user=user,
                date_of_birth=timezone.now().date() - timedelta(days=365*25),
                address=f'Home Address {i+1}',
                medical_history='No significant history.'
            )
            patients.append(user)
            self.stdout.write(f'Created {username}')

        self.stdout.write('Creating Appointments...')
        statuses = ['pending', 'accepted', 'rejected', 'completed']
        for _ in range(10):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            days_offset = random.randint(-5, 10)
            appt_date = timezone.now().date() + timedelta(days=days_offset)
            appt_time = timezone.now().replace(hour=random.randint(9, 17), minute=0, second=0).time()
            
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=appt_date,
                time=appt_time,
                status=random.choice(statuses),
                symptoms='Routine checkup and consultation.'
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
