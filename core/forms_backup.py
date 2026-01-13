from django import forms
from accounts.models import User
from .models import Class, Student, Subject


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'level', 'teacher', 'academic_year']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
        }


class StudentForm(forms.ModelForm):
    parents = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='PARENT'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        help_text='SÃ©lectionnez un ou plusieurs parents pour cet Ã©lÃ¨ve. Un parent peut avoir plusieurs enfants.',
        label='Parents'
    )
    
    class Meta:
        model = Student
        fields = [
            'student_number', 'first_name', 'last_name', 'date_of_birth',
            'photo', 'current_class', 'parents',
        ]
        exclude = ['user']  # Exclure explicitement le champ user pour Ã©viter les conflits
        widgets = {
            'student_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'current_class': forms.Select(attrs={'class': 'form-control'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
