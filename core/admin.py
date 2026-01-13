from django.contrib import admin
from .models import (
    Subject, Class, Student, Grade, 
    Attendance, Assignment, ClassSubject, Announcement
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'teacher', 'academic_year', 'created_at']
    list_filter = ['level', 'academic_year']
    search_fields = ['name', 'academic_year']
    autocomplete_fields = ['teacher']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_number', 'first_name', 'last_name', 'current_class', 'created_at']
    list_filter = ['current_class', 'created_at']
    search_fields = ['student_number', 'first_name', 'last_name']
    filter_horizontal = ['parents']
    autocomplete_fields = ['current_class']
    
    # Exclure le champ 'user' car on utilise 'parents' (ManyToMany) pour permettre plusieurs enfants par parent
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('student_number', 'first_name', 'last_name', 'date_of_birth', 'photo')
        }),
        ('Scolarité', {
            'fields': ('current_class',)
        }),
        ('Parents', {
            'fields': ('parents',),
            'description': 'Sélectionnez un ou plusieurs parents. Un parent peut avoir plusieurs enfants.',
        }),
    )
    
    # Exclure explicitement le champ 'user' des champs disponibles
    exclude = ['user']


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


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_obj', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at', 'class_obj']
    search_fields = ['title', 'message']
    readonly_fields = ['created_by', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'message', 'class_obj')
        }),
        ('Paramètres', {
            'fields': ('is_active',)
        }),
        ('Informations', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une nouvelle annonce
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
