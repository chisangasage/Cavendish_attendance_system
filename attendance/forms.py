from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Course, Enrollment, AttendanceSession, AttendanceRecord

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    student_id = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        role = self.cleaned_data.get('role')
        
        if role == 'student' and not student_id:
            raise forms.ValidationError("Student ID is required for student accounts.")
        
        if student_id and UserProfile.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("This Student ID is already registered.")
        
        return student_id

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name', 'description', 'lecturer']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']
    
    def __init__(self, *args, **kwargs):
        lecturer = kwargs.pop('lecturer', None)
        super().__init__(*args, **kwargs)
        
        if lecturer:
            self.fields['course'].queryset = Course.objects.filter(lecturer=lecturer)
        
        self.fields['student'].queryset = User.objects.filter(profile__role='student')

class AttendanceSessionForm(forms.ModelForm):
    class Meta:
        model = AttendanceSession
        fields = ['course', 'session_date', 'session_time', 'topic']
        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'session_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        lecturer = kwargs.pop('lecturer', None)
        super().__init__(*args, **kwargs)
        
        if lecturer:
            self.fields['course'].queryset = Course.objects.filter(lecturer=lecturer)

class AttendanceMarkingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students', [])
        super().__init__(*args, **kwargs)
        
        for student in students:
            self.fields[f'status_{student.id}'] = forms.ChoiceField(
                choices=AttendanceRecord.STATUS_CHOICES,
                initial='absent',
                widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
            )
            self.fields[f'remarks_{student.id}'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Optional remarks'})
            )

class AttendanceFilterForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False, empty_label="All Courses")
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(AttendanceRecord.STATUS_CHOICES),
        required=False
    )
