from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DoctorProfile, PatientProfile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role',)
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if user.role == User.IS_DOCTOR:
                # Default profile creation
                DoctorProfile.objects.create(user=user)
            elif user.role == User.IS_PATIENT:
                PatientProfile.objects.create(user=user)
        return user

class DoctorAvailabilityForm(forms.ModelForm):
    DAYS_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    working_days_selection = forms.MultipleChoiceField(choices=DAYS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    remove_picture = forms.BooleanField(required=False, label="Remove Profile Picture")

    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'bio', 'profile_picture', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'profile_picture': forms.FileInput(), # Use standard input to hide "Currently" text
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk: # Check if instance exists and is saved (pk check)
             if self.instance.working_days:
                self.initial['working_days_selection'] = self.instance.working_days.split(',')
             if self.instance.user:
                self.initial['first_name'] = self.instance.user.first_name
                self.initial['last_name'] = self.instance.user.last_name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.working_days = ",".join(self.cleaned_data['working_days_selection'])
        
        # Save User fields
        user = instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        
        # Handle Picture Removal
        if self.cleaned_data.get('remove_picture'):
            instance.profile_picture = None
        
        if commit:
            instance.save()
        return instance

class PatientNameForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
