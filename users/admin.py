from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorProfile, PatientProfile, Specialization

admin.site.register(Specialization)

class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False

@admin.action(description='Activate selected doctors')
def approve_doctors(modeladmin, request, queryset):
    for profile in queryset:
        profile.user.is_active = True
        profile.user.save()
        profile.is_verified = True
        profile.save()

class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_verified')
    list_filter = ('is_verified', 'specialization')
    actions = [approve_doctors]

class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    
    # Optional: Display inline profiles based on role, but simpler to just show them or register separately.
    inlines = [DoctorProfileInline, PatientProfileInline]

admin.site.register(User, CustomUserAdmin)
admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(PatientProfile)
