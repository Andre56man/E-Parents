from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Student, Grade, Attendance, Assignment, Class, Subject,
    ClassSubject, Announcement
)
from .forms import ClassForm, StudentForm, SubjectForm, AnnouncementForm


def home_view(request):
    """
    Page d'accueil publique - accessible même pour les utilisateurs connectés
    """
    from notifications.models import Notification
    
    # Date de début de la semaine (lundi)
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Annonces publiques actives (modèle Announcement)
    announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-created_at')[:10]
    
    # Devoirs de la semaine à venir
    week_assignments = Assignment.objects.filter(
        due_date__date__gte=today,
        due_date__date__lte=end_of_week
    ).order_by('due_date')[:10]
    
    # Statistiques générales
    total_students = Student.objects.count()
    total_classes = Class.objects.count()
    
    # Notes récentes de la semaine
    recent_grades = Grade.objects.filter(
        date__gte=start_of_week,
        date__lte=end_of_week
    ).order_by('-date')[:5]
    
    context = {
        'announcements': announcements,
        'week_assignments': week_assignments,
        'total_students': total_students,
        'total_classes': total_classes,
        'recent_grades': recent_grades,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
    }
    
    return render(request, 'core/home.html', context)


def is_parent(user):
    return user.is_authenticated and user.is_parent()


def is_teacher(user):
    return user.is_authenticated and user.is_teacher()


def is_admin(user):
    return user.is_authenticated and user.is_admin()


@login_required
def dashboard_view(request):
    """
    Vue du tableau de bord selon le rôle de l'utilisateur
    """
    user = request.user
    
    if user.is_parent():
        return parent_dashboard(request)
    elif user.is_teacher():
        return teacher_dashboard(request)
    elif user.is_admin():
        return admin_dashboard(request)
    else:
        messages.error(request, 'Rôle non reconnu.')
        return redirect('accounts:logout')


def parent_dashboard(request):
    """
    Tableau de bord pour les parents
    """
    user = request.user
    children = Student.objects.filter(parents=user)
    
    context = {
        'children': children,
        'recent_grades': Grade.objects.filter(
            student__in=children
        ).order_by('-date', '-created_at')[:10],
        'recent_attendances': Attendance.objects.filter(
            student__in=children
        ).order_by('-date', '-created_at')[:10],
        'upcoming_assignments': Assignment.objects.filter(
            class_obj__in=[child.current_class for child in children if child.current_class]
        ).filter(due_date__gte=timezone.now()).order_by('due_date')[:10],
    }
    
    return render(request, 'core/parent/dashboard.html', context)


def teacher_dashboard(request):
    """
    Tableau de bord pour les enseignants
    """
    user = request.user
    classes = Class.objects.filter(teacher=user)
    class_subjects = ClassSubject.objects.filter(teacher=user)
    
    # Statistiques
    total_students = Student.objects.filter(
        current_class__in=classes
    ).count()
    
    recent_grades = Grade.objects.filter(
        teacher=user
    ).order_by('-created_at')[:10]
    
    upcoming_assignments = Assignment.objects.filter(
        teacher=user,
        due_date__gte=timezone.now()
    ).order_by('due_date')[:10]
    
    context = {
        'classes': classes,
        'class_subjects': class_subjects,
        'total_students': total_students,
        'recent_grades': recent_grades,
        'upcoming_assignments': upcoming_assignments,
    }
    
    return render(request, 'core/teacher/dashboard.html', context)


def admin_dashboard(request):
    """
    Tableau de bord pour les administrateurs
    """
    # Statistiques globales
    total_students = Student.objects.count()
    total_teachers = request.user.__class__.objects.filter(role='TEACHER').count()
    total_parents = request.user.__class__.objects.filter(role='PARENT').count()
    total_classes = Class.objects.count()
    total_subjects = Subject.objects.count()
    total_grades = Grade.objects.count()
    total_assignments = Assignment.objects.count()
    
    # Taux d'absences récentes
    recent_attendances = Attendance.objects.filter(
        date__gte=timezone.now().date() - timedelta(days=30)
    )
    absence_rate = (recent_attendances.filter(status='ABSENT').count() / 
                   max(recent_attendances.count(), 1)) * 100
    
    # Moyennes par classe
    classes_with_avg = Class.objects.annotate(
        avg_grade=Avg('students__grades__value')
    ).filter(avg_grade__isnull=False).order_by('-avg_grade')[:10]
    
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        'total_classes': total_classes,
        'total_subjects': total_subjects,
        'total_grades': total_grades,
        'total_assignments': total_assignments,
        'absence_rate': round(absence_rate, 2),
        'classes_with_avg': classes_with_avg,
    }
    
    return render(request, 'core/admin/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_classes_list_view(request):
    classes = Class.objects.select_related('teacher').order_by('level', 'name')
    return render(request, 'core/admin/classes_list.html', {'classes': classes})


@login_required
@user_passes_test(is_admin)
def admin_class_create_view(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Classe créée avec succès.")
            return redirect('core:admin_classes_list')
    else:
        form = ClassForm()
    return render(request, 'core/admin/class_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def admin_students_list_view(request):
    students = Student.objects.select_related('current_class').order_by('last_name', 'first_name')
    return render(request, 'core/admin/students_list.html', {'students': students})


@login_required
@user_passes_test(is_admin)
def admin_student_create_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Élève créé avec succès.")
            return redirect('core:admin_students_list')
    else:
        form = StudentForm()
    return render(request, 'core/admin/student_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def admin_subjects_list_view(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'core/admin/subjects_list.html', {'subjects': subjects})


@login_required
@user_passes_test(is_admin)
def admin_subject_create_view(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière créée avec succès.")
            return redirect('core:admin_subjects_list')
    else:
        form = SubjectForm()
    return render(request, 'core/admin/subject_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def admin_announcements_list_view(request):
    """Liste des annonces pour l'admin"""
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'core/admin/announcements_list.html', {'announcements': announcements})


@login_required
@user_passes_test(is_admin)
def admin_announcement_create_view(request):
    """Créer une nouvelle annonce"""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, "Annonce créée avec succès.")
            return redirect('core:admin_announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'core/admin/announcement_form.html', {'form': form, 'action': 'Créer'})


@login_required
@user_passes_test(is_admin)
def admin_announcement_edit_view(request, announcement_id):
    """Modifier une annonce"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, "Annonce modifiée avec succès.")
            return redirect('core:admin_announcements_list')
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'core/admin/announcement_form.html', {'form': form, 'announcement': announcement, 'action': 'Modifier'})


@login_required
@user_passes_test(is_admin)
def admin_announcement_delete_view(request, announcement_id):
    """Supprimer une annonce"""
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, "Annonce supprimée avec succès.")
        return redirect('core:admin_announcements_list')
    return render(request, 'core/admin/announcement_delete.html', {'announcement': announcement})


@login_required
@user_passes_test(is_parent)
def student_detail_view(request, student_id):
    """
    Vue détaillée d'un élève pour les parents
    """
    user = request.user
    student = get_object_or_404(Student, id=student_id, parents=user)
    
    # Notes avec moyennes par matière
    grades = Grade.objects.filter(student=student).order_by('-date')
    subjects_avg = {}
    for grade in grades:
        if grade.subject not in subjects_avg:
            subjects_avg[grade.subject] = []
        subjects_avg[grade.subject].append(float(grade.value))
    
    for subject in subjects_avg:
        subjects_avg[subject] = round(sum(subjects_avg[subject]) / len(subjects_avg[subject]), 2)
    
    # Absences récentes
    attendances = Attendance.objects.filter(student=student).order_by('-date')[:20]
    
    # Devoirs à venir
    if student.current_class:
        assignments = Assignment.objects.filter(
            class_obj=student.current_class,
            due_date__gte=timezone.now()
        ).order_by('due_date')
    else:
        assignments = []
    
    context = {
        'student': student,
        'grades': grades,
        'subjects_avg': subjects_avg,
        'attendances': attendances,
        'assignments': assignments,
    }
    
    return render(request, 'core/parent/student_detail.html', context)


@login_required
@user_passes_test(is_teacher)
def class_students_view(request, class_id):
    """
    Vue de la liste des élèves d'une classe pour les enseignants
    """
    class_obj = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(current_class=class_obj).order_by('last_name', 'first_name')
    
    context = {
        'class_obj': class_obj,
        'students': students,
    }
    
    return render(request, 'core/teacher/class_students.html', context)


@login_required
@user_passes_test(is_teacher)
def add_grade_view(request):
    """
    Vue pour ajouter une note (enseignants)
    """
    if request.method == 'POST':
        # Traitement du formulaire (à implémenter avec un formulaire)
        messages.success(request, 'Note ajoutée avec succès!')
        return redirect('core:dashboard')
    
    user = request.user
    classes = Class.objects.filter(teacher=user)
    subjects = Subject.objects.filter(class_subjects__teacher=user).distinct()
    
    context = {
        'classes': classes,
        'subjects': subjects,
    }
    
    return render(request, 'core/teacher/add_grade.html', context)


@login_required
@user_passes_test(is_teacher)
def add_attendance_view(request):
    """
    Vue pour ajouter une absence/retard (enseignants)
    """
    if request.method == 'POST':
        # Traitement du formulaire (à implémenter avec un formulaire)
        messages.success(request, 'Absence/retard enregistré avec succès!')
        return redirect('core:dashboard')
    
    user = request.user
    classes = Class.objects.filter(teacher=user)
    
    context = {
        'classes': classes,
    }
    
    return render(request, 'core/teacher/add_attendance.html', context)

