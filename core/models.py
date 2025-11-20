from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class School(models.Model):
    """
    Modèle représentant un établissement scolaire
    """
    name = models.CharField(max_length=200, verbose_name='Nom de l\'établissement')
    address = models.TextField(verbose_name='Adresse')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Téléphone')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Établissement'
        verbose_name_plural = 'Établissements'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    Modèle représentant une matière
    """
    name = models.CharField(max_length=100, verbose_name='Nom de la matière')
    code = models.CharField(max_length=10, unique=True, verbose_name='Code')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Matière'
        verbose_name_plural = 'Matières'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Class(models.Model):
    """
    Modèle représentant une classe
    """
    LEVEL_CHOICES = [
        ('PRIMAIRE', 'Primaire'),
        ('COLLEGE', 'Collège'),
        ('LYCEE', 'Lycée'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='Nom de la classe')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Niveau')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes', verbose_name='Établissement')
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'TEACHER'},
        related_name='classes_taught',
        verbose_name='Professeur principal'
    )
    academic_year = models.CharField(max_length=20, verbose_name='Année scolaire', default='2024-2025')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
        ordering = ['level', 'name']
        unique_together = ['name', 'academic_year', 'school']
    
    def __str__(self):
        return f"{self.name} - {self.academic_year}"


class Student(models.Model):
    """
    Modèle représentant un élève
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': 'PARENT'},
        verbose_name='Compte utilisateur',
        blank=True,
        null=True,
    )
    
    student_number = models.CharField(max_length=20, unique=True, verbose_name='Numéro d\'élève')
    first_name = models.CharField(max_length=100, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, verbose_name='Nom')
    date_of_birth = models.DateField(verbose_name='Date de naissance')
    photo = models.ImageField(upload_to='students/photos/', blank=True, null=True, verbose_name='Photo')
    
    current_class = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name='Classe actuelle'
    )
    
    parents = models.ManyToManyField(
        User,
        related_name='children',
        limit_choices_to={'role': 'PARENT'},
        verbose_name='Parents'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Élève'
        verbose_name_plural = 'Élèves'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_number})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Grade(models.Model):
    """
    Modèle représentant une note
    """
    TYPE_CHOICES = [
        ('DEVOIR', 'Devoir'),
        ('CONTROLE', 'Contrôle'),
        ('EXAMEN', 'Examen'),
        ('ORAL', 'Oral'),
        ('TP', 'Travaux Pratiques'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', verbose_name='Élève')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades', verbose_name='Matière')
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'TEACHER'},
        related_name='grades_given',
        verbose_name='Enseignant'
    )
    
    grade_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Type de note')
    value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name='Note'
    )
    coefficient = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0.1)],
        verbose_name='Coefficient'
    )
    comment = models.TextField(blank=True, null=True, verbose_name='Commentaire')
    date = models.DateField(verbose_name='Date')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.value}/20"


class Attendance(models.Model):
    """
    Modèle représentant une absence ou un retard
    """
    STATUS_CHOICES = [
        ('ABSENT', 'Absent'),
        ('RETARD', 'Retard'),
        ('JUSTIFIE', 'Absence justifiée'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name='Élève')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendances', verbose_name='Classe')
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='attendances',
        blank=True,
        null=True,
        verbose_name='Matière'
    )
    
    date = models.DateField(verbose_name='Date')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Statut')
    reason = models.TextField(blank=True, null=True, verbose_name='Raison')
    justified = models.BooleanField(default=False, verbose_name='Justifié')
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendances_created',
        verbose_name='Créé par'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Absence/Retard'
        verbose_name_plural = 'Absences/Retards'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.student} - {self.get_status_display()} - {self.date}"


class Assignment(models.Model):
    """
    Modèle représentant un devoir ou examen
    """
    title = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(verbose_name='Description')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments', verbose_name='Matière')
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments', verbose_name='Classe')
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'TEACHER'},
        related_name='assignments',
        verbose_name='Enseignant'
    )
    
    due_date = models.DateTimeField(verbose_name='Date limite')
    is_exam = models.BooleanField(default=False, verbose_name='Examen')
    file = models.FileField(upload_to='assignments/files/', blank=True, null=True, verbose_name='Fichier joint')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Devoir/Examen'
        verbose_name_plural = 'Devoirs/Examens'
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.title} - {self.class_obj}"


class ClassSubject(models.Model):
    """
    Modèle de liaison entre une classe et une matière (avec enseignant)
    """
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects', verbose_name='Classe')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='class_subjects', verbose_name='Matière')
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'TEACHER'},
        related_name='subjects_taught',
        verbose_name='Enseignant'
    )
    
    hours_per_week = models.IntegerField(default=0, verbose_name='Heures par semaine')
    
    class Meta:
        verbose_name = 'Matière de classe'
        verbose_name_plural = 'Matières de classe'
        unique_together = ['class_obj', 'subject']
    
    def __str__(self):
        return f"{self.class_obj} - {self.subject}"

