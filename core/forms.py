from django import forms
from .models import School, Class, Student, Subject


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'phone', 'email']


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'level', 'school', 'teacher', 'academic_year']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_number', 'first_name', 'last_name', 'date_of_birth',
            'photo', 'current_class', 'parents',
        ]


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']
