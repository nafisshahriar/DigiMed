from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from appointments.models import Appointment

def home(request):
    return render(request, 'home.html')

@login_required
def dashboard_redirect(request):
    if request.user.is_doctor():
        return redirect('doctor_dashboard')
    elif request.user.is_patient():
        return redirect('patient_dashboard')
    elif request.user.is_superuser or request.user.is_staff:
        return redirect('admin_analytics')
    return redirect('home')

@login_required
def admin_analytics(request):
    if not request.user.is_staff:
        return redirect('home')
        
    # Pending Doctors
    from users.models import DoctorProfile
    from django.utils import timezone
    
    pending_doctors = DoctorProfile.objects.filter(is_verified=False)
    
    from django.utils.dateparse import parse_date
    import datetime
    
    today = timezone.now().date()
    selected_date = request.GET.get('date')
    if selected_date:
        parsed = parse_date(selected_date)
        if parsed:
            today = parsed
    
    # "Remaining Appointments Today" (or Selected Date)
    remaining_appointments_count = Appointment.objects.filter(
        date=today
    ).exclude(status__in=['completed', 'rejected']).count()
    
    # Appointments per Doctor (Today's remaining)
    from django.db.models import F
    appointments_by_doctor = Appointment.objects.filter(
        date=today
    ).exclude(status__in=['completed', 'rejected']).annotate(
        specialization=F('doctor__doctor_profile__specialization__name')
    ).values(
        'doctor__last_name', 'doctor__first_name', 'specialization'
    ).annotate(count=Count('id')).order_by('-count')
    
    # Appointments per Day
    appointments_by_day = Appointment.objects.filter(
         date__gte=timezone.now().date() - timezone.timedelta(days=7)
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    total_appointments_chart = sum(item['count'] for item in appointments_by_day) or 1
    
    from users.models import Specialization
    specializations = Specialization.objects.all().order_by('name')
    
    return render(request, 'core/admin_analytics.html', {
        'total_appointments': remaining_appointments_count,
        'appointments_by_doctor': appointments_by_doctor,
        'appointments_by_day': appointments_by_day,
        'total_appointments_chart': total_appointments_chart,
        'pending_doctors': pending_doctors,
        'specializations': specializations,
        'today': today,
    })

@login_required
def approve_doctor(request, doctor_id):
    if not request.user.is_staff:
        return redirect('home')
        
    try:
        from users.models import DoctorProfile
        profile = DoctorProfile.objects.get(user_id=doctor_id)
        profile.is_verified = True
        profile.save()
        profile.user.is_active = True
        profile.user.save()
    except Exception: # Catch any db error or import error
        pass
        
    return redirect('admin_analytics')

@login_required
def add_specialization(request):
    if not request.user.is_staff or request.method != 'POST':
        return redirect('admin_analytics')
    
    from users.models import Specialization
    name = request.POST.get('name')
    if name:
        Specialization.objects.get_or_create(name=name)
    
    return redirect('admin_analytics')
def reject_doctor(request, doctor_id):
    if not request.user.is_staff:
        return redirect('home')
        
    try:
        from users.models import User
        user = User.objects.get(pk=doctor_id)
        # Soft Reject: Deactivate and Unverify
        if user.role == User.IS_DOCTOR:
            user.is_active = False 
            user.save()
            if hasattr(user, 'doctor_profile'):
                user.doctor_profile.is_verified = False
                user.doctor_profile.save()
            # Do NOT delete.
    except User.DoesNotExist:
        pass
        
    return redirect('admin_analytics')
