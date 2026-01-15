from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec rôles
    """
    ROLE_CHOICES = [
        ('PARENT', 'Parent'),
        ('TEACHER', 'Enseignant'),
        ('ADMIN', 'Administrateur'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='PARENT',
        verbose_name='Rôle'
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres autorisés."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name='Numéro de téléphone'
    )
    
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Date de naissance'
    )
    
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Adresse'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de modification'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Compte actif'
    )
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_parent(self):
        return self.role == 'PARENT'
    
    def is_teacher(self):
        return self.role == 'TEACHER'
    
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    

    expo_push_token = models.CharField(max_length=255, blank=True, null=True)

class LoginLog(models.Model):
    """
    Journalisation des connexions pour la sécurité
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_logs',
        verbose_name='Utilisateur'
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name='Adresse IP'
    )
    
    user_agent = models.TextField(
        blank=True,
        null=True,
        verbose_name='User Agent'
    )
    
    login_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Heure de connexion'
    )
    
    success = models.BooleanField(
        default=True,
        verbose_name='Connexion réussie'
    )
    
    class Meta:
        verbose_name = 'Journal de connexion'
        verbose_name_plural = 'Journaux de connexion'
        ordering = ['-login_time']
    
    def __str__(self):
        status = "Succès" if self.success else "Échec"
        return f"{self.user.username} - {status} - {self.login_time}"

