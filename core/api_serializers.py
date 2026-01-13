from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Attendance, Grade, Assignment, Class

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
        ]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'student_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'current_class',
        ]


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = [
            'id',
            'name',
            'level',
            'academic_year',
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'student',
            'student_name',
            'class_obj',
            'subject',
            'date',
            'status',
            'status_display',
            'reason',
            'justified',
        ]


class GradeSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)

    class Meta:
        model = Grade
        fields = [
            'id',
            'student',
            'subject',
            'subject_name',
            'teacher',
            'teacher_name',
            'grade_type',
            'value',
            'coefficient',
            'comment',
            'date',
        ]


class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_obj.name', read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id',
            'title',
            'description',
            'subject',
            'subject_name',
            'class_obj',
            'class_name',
            'teacher',
            'due_date',
            'is_exam',
        ]
