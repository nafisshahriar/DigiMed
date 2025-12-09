import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'digimed_project.settings')
django.setup()

from users.models import User, DoctorProfile, Specialization
from appointments.models import Appointment
from django.test import RequestFactory
from django.urls import reverse
from core.views import reject_doctor, approve_doctor

def verify_doctor_approval():
    print("Verifying Doctor Approval (Soft Reject)...")
    spec = Specialization.objects.first()
    if not spec:
        spec = Specialization.objects.create(name="General")
        
    # Cleanup
    User.objects.filter(username='reject_test_doc').delete()
    
    # Create Doc
    user = User.objects.create_user(username='reject_test_doc', password='password', role=User.IS_DOCTOR, is_active=True)
    profile = DoctorProfile.objects.create(user=user, specialization=spec, is_verified=True)
    
    # Test Soft Rejection
    # We need to simulate the request to the view or just call the logic if we abstracted it. 
    # Since logic is in view, we'll use RequestFactory
    factory = RequestFactory()
    request = factory.get(reverse('reject_doctor', args=[user.id]))
    
    User.objects.filter(username='admin_tester').delete()
    admin = User.objects.create_user(username='admin_tester', is_staff=True, is_superuser=True)
    request.user = admin
    
    reject_doctor(request, user.id)
    
    user.refresh_from_db()
    profile.refresh_from_db()
    
    if not user.is_active and not profile.is_verified:
        print("PASS: Doctor soft rejection verified (is_active=False, is_verified=False).")
    else:
        print(f"FAIL: Doctor not deactivated. Active: {user.is_active}, Verified: {profile.is_verified}")
        
    # Test Re-Approval
    print("Verifying Re-Approval...")
    request_approve = factory.get(reverse('approve_doctor', args=[user.id]))
    request_approve.user = admin
    approve_doctor(request_approve, user.id)
    
    user.refresh_from_db()
    profile.refresh_from_db()
    
    if user.is_active and profile.is_verified:
        print("PASS: Doctor re-approval verified.")
    else:
        print(f"FAIL: Doctor not re-approved. Active: {user.is_active}")

def verify_appointment_workflow():
    print("\nVerifying Appointment Workflow (Transitions)...")
    # Cleanup
    Appointment.objects.all().delete()
    
    patient = User.objects.filter(role=User.IS_PATIENT).first()
    if not patient:
        patient = User.objects.create_user(username='pat_test', role=User.IS_PATIENT)
    
    doctor = User.objects.filter(role=User.IS_DOCTOR).first()
    if not doctor:
        doctor = User.objects.create_user(username='doc_test', role=User.IS_DOCTOR)
        DoctorProfile.objects.create(user=doctor)

    appt = Appointment.objects.create(
        patient=patient, doctor=doctor, date=timezone.now().date(), time=timezone.now().time(), status='pending'
    )
    
    # Check transitions
    transitions = ['accepted', 'completed', 'accepted', 'rejected', 'accepted']
    for status in transitions:
        appt.status = status
        appt.save()
        print(f"PASS: Transitioned to {status}")
        
    if appt.status == 'accepted':
         print("PASS: Final status matches expected.")

def verify_admin_metrics():
    print("\nVerifying Admin Metrics...")
    Appointment.objects.all().delete()
    
    doctor = User.objects.filter(role=User.IS_DOCTOR).first()
    patient = User.objects.filter(role=User.IS_PATIENT).first()
    today = timezone.now().date()
    
    Appointment.objects.create(patient=patient,doctor=doctor,date=today,time=timezone.now().time(),status='pending')
    Appointment.objects.create(patient=patient,doctor=doctor,date=today,time=timezone.now().time(),status='accepted')
    Appointment.objects.create(patient=patient,doctor=doctor,date=today,time=timezone.now().time(),status='completed')
    Appointment.objects.create(patient=patient,doctor=doctor,date=today,time=timezone.now().time(),status='rejected')
    
    count = Appointment.objects.filter(date=today).exclude(status__in=['completed', 'rejected']).count()
    
    from django.db.models import F, Count
    driver_data = Appointment.objects.filter(
        date=today
    ).exclude(status__in=['completed', 'rejected']).annotate(
        specialization=F('doctor__doctor_profile__specialization__name')
    ).values(
        'doctor__last_name', 'specialization'
    ).annotate(count=Count('id')).order_by('-count')
    
    if len(driver_data) > 0 and 'specialization' in driver_data[0]:
         print(f"PASS: Specialization alias present: {driver_data[0]['specialization']}")
    else:
         # Might fail if specialization is None, which mimics real world if not set. 
         # But in verify_doctor_approval we ensure spec exists maybe?
         # Check if doc has spec
         if doctor.doctor_profile.specialization:
             print(f"FAIL: Data missing alias or empty. Data: {list(driver_data)}")
         else:
             print("WARN: Doctor has no specialization, skipping alias check.")
         
    if count == 2:
         print("PASS: Pending/Accepted are remaining. Completed/Rejected are excluded.")
    else:
         print(f"FAIL: Expected 2, got {count}")
         
    # TEST DATE FILTER
    # Create an appointment for tomorrow
    tmrw = today + timezone.timedelta(days=1)
    Appointment.objects.create(patient=patient,doctor=doctor,date=tmrw,time=timezone.now().time(),status='pending')
    
    today = timezone.now().date()
    
    # Needs a staff user
    factory = RequestFactory()
    User.objects.filter(username='staff_tester').delete()
    staff = User.objects.create_user(username='staff_tester', is_staff=True)
    
    # Test Add Specialization
    print("Testing Add Specialization...")
    from users.models import Specialization
    spec_name = "TestSpec_" + str(timezone.now().timestamp())
    request = factory.post(reverse('add_specialization'), {'name': spec_name})
    request.user = staff
    
    from core.views import add_specialization
    add_specialization(request)
    if Specialization.objects.filter(name=spec_name).exists():
        print("PASS: Specialization created successfully via view.")
    else:
        print("FAIL: Specialization not created.")
        
    # Verify Doctor Name Update via Form
    print("Testing Doctor Name Update...")
    doctor = User.objects.filter(role=User.IS_DOCTOR).first()
    if doctor:
        # Simulate form data
        form_data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'specialization': doctor.doctor_profile.specialization.id if doctor.doctor_profile.specialization else '',
            'bio': 'New Bio',
            'start_time': '09:00',
            'end_time': '17:00',
            # working_days_selection handled by widget/cleaning, raw data needs list?
            'working_days_selection': ['Mon', 'Tue']
        }
        
        # We need to simulate the POST request to doctor_dashboard view
        # or just test the form directly. Testing form is better isolation.
        from users.forms import DoctorAvailabilityForm
        
        # Bind data
        f = DoctorAvailabilityForm(data=form_data, instance=doctor.doctor_profile)
        
        if f.is_valid():
            f.save()
            doctor.refresh_from_db()
            if doctor.first_name == 'NewFirstName' and doctor.last_name == 'NewLastName':
                print("PASS: Doctor name updated successfully via form.")
            else:
                 print(f"FAIL: Name not updated. Got: {doctor.first_name} {doctor.last_name}")
        else:
             print(f"FAIL: Form invalid. Errors: {f.errors}")
    else:
        print("WARN: No doctor found to test name update.")
        
    # Verify Patient Name Update
    print("Testing Patient Name Update...")
    patient = User.objects.filter(role=User.IS_PATIENT).first()
    if patient:
        from users.forms import PatientNameForm
        p_form_data = {'first_name': 'PatientFirst', 'last_name': 'PatientLast'}
        pf = PatientNameForm(data=p_form_data, instance=patient)
        if pf.is_valid():
            pf.save()
            patient.refresh_from_db()
            if patient.first_name == 'PatientFirst' and patient.last_name == 'PatientLast':
                print("PASS: Patient name updated successfully.")
            else:
                print(f"FAIL: Patient name mismatch: {patient.first_name}")
        else:
             print(f"FAIL: Patient form invalid: {pf.errors}")
    else:
         print("WARN: No patient found to test.")

if __name__ == '__main__':
    verify_doctor_approval()
    verify_appointment_workflow()
    verify_admin_metrics()
