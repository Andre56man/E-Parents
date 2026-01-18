from django.db import models
from django.contrib.auth import get_user_model
from core.models import Student, Class

User = get_user_model()


class Conversation(models.Model):
    """
    Modèle représentant une conversation entre utilisateurs
    """
    participants = models.ManyToManyField(User, related_name='conversations', verbose_name='Participants')
    subject = models.CharField(max_length=200, verbose_name='Sujet')
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='conversations',
        blank=True,
        null=True,
        verbose_name='Élève concerné'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    
    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.subject} - {', '.join([p.username for p in self.participants.all()])}"


class Message(models.Model):
    """
    Modèle représentant un message dans une conversation
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversation'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='sent_messages',
        verbose_name='Expéditeur',
        null=True,
        blank=True
    )
    content = models.TextField(verbose_name='Contenu')
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.sender.username} - {self.conversation.subject}"

