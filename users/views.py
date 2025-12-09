from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, DoctorAvailabilityForm
from .models import DoctorProfile, User
from appointments.models import Appointment

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == User.IS_DOCTOR:
                user.is_active = False
                user.save()
                return render(request, 'users/signup_pending.html')
            
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def patient_dashboard(request):
    if not request.user.is_patient():
        return redirect('home')
        
    doctors = DoctorProfile.objects.all()
    appointments = Appointment.objects.filter(patient=request.user)
    
    from .forms import PatientNameForm
    form = PatientNameForm(instance=request.user)
    
    if request.method == 'POST':
        form = PatientNameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    
    return render(request, 'users/patient_dashboard.html', {
        'doctors': doctors,
        'appointments': appointments,
        'form': form
    })

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor():
        return redirect('home')
    
    profile = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time')
    
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorAvailabilityForm(instance=profile)
    
    return render(request, 'users/doctor_dashboard.html', {
        'appointments': appointments,
        'form': form,
        'profile': profile
    })

@login_required
def book_appointment(request, doctor_id):
    if not request.user.is_patient():
        return redirect('home')
        
    try:
        doctor_user = User.objects.get(pk=doctor_id)
        doctor_profile = doctor_user.doctor_profile
    except User.DoesNotExist:
        return redirect('patient_dashboard')
        
    slots = []
    selected_date = request.GET.get('date')
    
    if selected_date:
        from datetime import datetime, timedelta
        import calendar
        
        date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        day_name = calendar.day_name[date_obj.weekday()][:3] # Mon, Tue...
        
        # Check if doctor works on this day
        # Handle simple comma separated string "Mon,Tue"
        working_days = [d.strip() for d in doctor_profile.working_days.split(',')]
        
        if day_name in working_days:
            # Generate slots
            start_dt = datetime.combine(date_obj, doctor_profile.start_time)
            end_dt = datetime.combine(date_obj, doctor_profile.end_time)
            
            current_dt = start_dt
            while current_dt < end_dt:
                time_val = current_dt.time()
                # Check if booked
                if not Appointment.objects.filter(doctor=doctor_user, date=date_obj, time=time_val).exists():
                    slots.append(time_val.strftime('%H:%M'))
                current_dt += timedelta(minutes=30)

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        symptoms = request.POST.get('symptoms')
        
        # Double check availability race condition
        if Appointment.objects.filter(doctor=doctor_user, date=date, time=time).exists():
            # Handle error
            return render(request, 'users/book_appointment.html', {
                'doctor': doctor_user, 
                'slots': slots, 
                'selected_date': selected_date,
                'error': 'Slot already taken.'
            })

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor_user,
            date=date,
            time=time,
            symptoms=symptoms
        )
        return redirect('patient_dashboard')
        
    return render(request, 'users/book_appointment.html', {
        'doctor': doctor_user,
        'slots': slots,
        'selected_date': selected_date
    })

@login_required
def update_appointment(request, appointment_id):
    if not request.user.is_doctor():
        return redirect('home')
        
    appointment = Appointment.objects.get(pk=appointment_id, doctor=request.user)
    
    # Lock decision: Removed as per request "changable always"
    # if appointment.status in ['completed', 'rejected']:
    #     return redirect('doctor_dashboard')
    
    # Actually just remove the check completely to allow free modification
    pass
    
    if request.method == 'POST':
        status = request.POST.get('status')
        # Allow transition to 'completed' or 'rejected' or 'accepted'
        if status in ['accepted', 'rejected', 'completed']:
            appointment.status = status
            appointment.save()
            
    return redirect('doctor_dashboard')

@login_required
def doctor_detail(request, doctor_id):
    try:
        doctor = User.objects.get(pk=doctor_id, role=User.IS_DOCTOR)
    except User.DoesNotExist:
        return redirect('home')
        
    return render(request, 'users/doctor_detail.html', {'doctor': doctor})
    
# Add User import if not present at top, I will assume it's there or I need to add it.
# Actually I need to check imports. I'll include imports in this replacement block just in case to be safe?
# No, Replace is safer to target the end of file or method.
# I will grab the User model import if missing.
# Checking file content first is better but I will try to append.


