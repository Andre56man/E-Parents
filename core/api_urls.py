from django.urls import path
from . import api_views

app_name = 'core_api'

urlpatterns = [
    # Profil utilisateur connecté
    path('auth/me/', api_views.MeView.as_view(), name='auth_me'),

    # Endpoints Parent
    path('parent/students/', api_views.ParentStudentsListView.as_view(), name='parent_students'),
    path('parent/students/<int:student_id>/attendances/', api_views.ParentStudentAttendancesView.as_view(), name='parent_student_attendances'),
    path('parent/students/<int:student_id>/grades/', api_views.ParentStudentGradesView.as_view(), name='parent_student_grades'),
    path('parent/students/<int:student_id>/assignments/', api_views.ParentStudentAssignmentsView.as_view(), name='parent_student_assignments'),

    # Endpoints Enseignant
    path('teacher/classes/', api_views.TeacherClassesView.as_view(), name='teacher_classes'),
    path('teacher/classes/<int:class_id>/students/', api_views.TeacherClassStudentsView.as_view(), name='teacher_class_students'),
    path('teacher/students/<int:student_id>/grades/', api_views.TeacherStudentGradesView.as_view(), name='teacher_student_grades'),
    path('teacher/grades/', api_views.TeacherGradeCreateView.as_view(), name='teacher_grade_create'),
    path('teacher/attendances/', api_views.TeacherAttendanceCreateView.as_view(), name='teacher_attendance_create'),
    path('teacher/assignments/', api_views.TeacherAssignmentsView.as_view(), name='teacher_assignments'),
]
