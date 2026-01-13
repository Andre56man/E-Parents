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
]

