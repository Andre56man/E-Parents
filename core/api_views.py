from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Student, Attendance, Grade, Assignment, Class, ClassSubject
from .api_serializers import (
    UserSerializer,
    StudentSerializer,
    AttendanceSerializer,
    GradeSerializer,
    AssignmentSerializer,
    ClassSerializer,
)

User = get_user_model()


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_parent())


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher())


class ParentStudentsListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        return Student.objects.filter(parents=self.request.user).select_related('current_class')


class ParentStudentAttendancesView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id, parents=self.request.user)
        return Attendance.objects.filter(student=student).select_related('class_obj', 'subject', 'student').order_by('-date', '-created_at')


class ParentStudentGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id, parents=self.request.user)
        return Grade.objects.filter(student=student).select_related('subject', 'teacher').order_by('-date', '-created_at')


class ParentStudentAssignmentsView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id, parents=self.request.user)
        if not student.current_class:
            return Assignment.objects.none()
        return Assignment.objects.filter(
            class_obj=student.current_class
        ).order_by('due_date')


class TeacherClassesView(generics.ListAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        user = self.request.user
        direct_classes = Class.objects.filter(teacher=user)
        via_subjects = Class.objects.filter(class_subjects__teacher=user)
        return (direct_classes | via_subjects).distinct().select_related('school')


class TeacherClassStudentsView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        class_obj = get_object_or_404(Class, id=class_id)
        return Student.objects.filter(current_class=class_obj).order_by('last_name', 'first_name')


class TeacherStudentGradesView(generics.ListAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        return Grade.objects.filter(student=student).select_related('subject', 'teacher').order_by('-date', '-created_at')


class TeacherGradeCreateView(generics.CreateAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class TeacherAttendanceCreateView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TeacherAssignmentsView(generics.ListCreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return Assignment.objects.filter(teacher=self.request.user).select_related('class_obj', 'subject').order_by('due_date')

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
