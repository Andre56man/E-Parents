from django.contrib import admin
from .models import (
    School, Subject, Class, Student, Grade, 
    Attendance, Assignment, ClassSubject
)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone', 'email', 'created_at']
    search_fields = ['name', 'address']
    list_filter = ['created_at']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'school', 'teacher', 'academic_year', 'created_at']
    list_filter = ['level', 'academic_year', 'school']
    search_fields = ['name', 'academic_year']
    autocomplete_fields = ['teacher']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_number', 'first_name', 'last_name', 'current_class', 'created_at']
    list_filter = ['current_class', 'created_at']
    search_fields = ['student_number', 'first_name', 'last_name']
    filter_horizontal = ['parents']
    autocomplete_fields = ['user', 'current_class']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'value', 'grade_type', 'date', 'teacher', 'created_at']
    list_filter = ['grade_type', 'date', 'subject', 'created_at']
    search_fields = ['student__first_name', 'student__last_name', 'subject__name']
    autocomplete_fields = ['student', 'subject', 'teacher']
    date_hierarchy = 'date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'class_obj', 'date', 'status', 'justified', 'created_by', 'created_at']
    list_filter = ['status', 'justified', 'date', 'created_at']
    search_fields = ['student__first_name', 'student__last_name']
    autocomplete_fields = ['student', 'class_obj', 'subject', 'created_by']
    date_hierarchy = 'date'


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'class_obj', 'teacher', 'due_date', 'is_exam', 'created_at']
    list_filter = ['is_exam', 'due_date', 'subject', 'created_at']
    search_fields = ['title', 'description']
    autocomplete_fields = ['subject', 'class_obj', 'teacher']
    date_hierarchy = 'due_date'


@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'subject', 'teacher', 'hours_per_week']
    list_filter = ['class_obj', 'subject']
    search_fields = ['class_obj__name', 'subject__name']
    autocomplete_fields = ['class_obj', 'subject', 'teacher']

