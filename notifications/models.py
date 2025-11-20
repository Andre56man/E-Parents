from django.db import models
from django.contrib.auth import get_user_model
from core.models import Student, Class

User = get_user_model()


class Notification(models.Model):
    """
    Modèle représentant une notification
    """
    TYPE_CHOICES = [
        ('GRADE', 'Nouvelle note'),
        ('ATTENDANCE', 'Absence/Retard'),
        ('ASSIGNMENT', 'Nouveau devoir'),
        ('ANNOUNCEMENT', 'Annonce'),
        ('MESSAGE', 'Message'),
    ]
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Destinataire'
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Type de notification'
    )
    
    title = models.CharField(max_length=200, verbose_name='Titre')
    message = models.TextField(verbose_name='Message')
    
    # Liens optionnels vers d'autres objets
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='notifications',
        blank=True,
        null=True,
        verbose_name='Élève concerné'
    )
    
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='notifications',
        blank=True,
        null=True,
        verbose_name='Classe concernée'
    )
    
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Marquer la notification comme lue"""
        self.is_read = True
        self.save()


def create_notification(recipient, notification_type, title, message, student=None, class_obj=None):
    """
    Fonction utilitaire pour créer une notification
    """
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        student=student,
        class_obj=class_obj
    )
    return notification

