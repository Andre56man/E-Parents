from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Admin custom management
    path('management/classes/', views.admin_classes_list_view, name='admin_classes_list'),
    path('management/classes/add/', views.admin_class_create_view, name='admin_class_create'),
    path('management/students/', views.admin_students_list_view, name='admin_students_list'),
    path('management/students/add/', views.admin_student_create_view, name='admin_student_create'),
    path('management/subjects/', views.admin_subjects_list_view, name='admin_subjects_list'),
    path('management/subjects/add/', views.admin_subject_create_view, name='admin_subject_create'),
    
    # Gestion des annonces
    path('management/announcements/', views.admin_announcements_list_view, name='admin_announcements_list'),
    path('management/announcements/add/', views.admin_announcement_create_view, name='admin_announcement_create'),
    path('management/announcements/<int:announcement_id>/edit/', views.admin_announcement_edit_view, name='admin_announcement_edit'),
    path('management/announcements/<int:announcement_id>/delete/', views.admin_announcement_delete_view, name='admin_announcement_delete'),
    
    # Vues parents
    path('student/<int:student_id>/', views.student_detail_view, name='student_detail'),
    
    # Vues enseignants
    path('teacher/class/<int:class_id>/students/', views.class_students_view, name='class_students'),
    path('teacher/add-grade/', views.add_grade_view, name='add_grade'),
    path('teacher/add-attendance/', views.add_attendance_view, name='add_attendance'),
    
    # ===== GESTION DES UTILISATEURS =====
    path('management/users/', views.admin_users_list_view, name='admin_users_list'),
    path('management/users/add/', views.admin_user_create_view, name='admin_user_create'),
    path('management/users/<int:user_id>/edit/', views.admin_user_edit_view, name='admin_user_edit'),
    path('management/users/<int:user_id>/delete/', views.admin_user_delete_view, name='admin_user_delete'),
    
    # ===== GESTION DES ABSENCES =====
    path('management/attendance/', views.admin_attendance_list_view, name='admin_attendance_list'),
    path('management/attendance/add/', views.admin_attendance_create_view, name='admin_attendance_create'),
    path('management/attendance/<int:attendance_id>/edit/', views.admin_attendance_edit_view, name='admin_attendance_edit'),
    path('management/attendance/<int:attendance_id>/delete/', views.admin_attendance_delete_view, name='admin_attendance_delete'),
    
    # ===== GESTION DES DEVOIRS =====
    path('management/assignments/', views.admin_assignment_list_view, name='admin_assignment_list'),
    path('management/assignments/add/', views.admin_assignment_create_view, name='admin_assignment_create'),
    path('management/assignments/<int:assignment_id>/edit/', views.admin_assignment_edit_view, name='admin_assignment_edit'),
    path('management/assignments/<int:assignment_id>/delete/', views.admin_assignment_delete_view, name='admin_assignment_delete'),
    
    # ===== GESTION DE L'EMPLOI DU TEMPS =====
    path('management/timetable/', views.admin_timetable_list_view, name='admin_timetable_list'),
    path('management/timetable/add/', views.admin_timetable_create_view, name='admin_timetable_create'),
    path('management/timetable/<int:timetable_id>/edit/', views.admin_timetable_edit_view, name='admin_timetable_edit'),
    path('management/timetable/<int:timetable_id>/delete/', views.admin_timetable_delete_view, name='admin_timetable_delete'),
    
    # ===== GESTION DES MATIÈRES PAR CLASSE =====
    path('management/class-subjects/', views.admin_class_subject_list_view, name='admin_class_subject_list'),
    path('management/class-subjects/add/', views.admin_class_subject_create_view, name='admin_class_subject_create'),
    path('management/class-subjects/<int:class_subject_id>/edit/', views.admin_class_subject_edit_view, name='admin_class_subject_edit'),
    path('management/class-subjects/<int:class_subject_id>/delete/', views.admin_class_subject_delete_view, name='admin_class_subject_delete'),
]

