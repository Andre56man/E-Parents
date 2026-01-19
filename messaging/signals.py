from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message
from notifications.models import create_notification


@receiver(post_save, sender=Message)
def notify_participants_on_message(sender, instance, created, **kwargs):
    """
    Créer une notification pour les participants lorsqu'un nouveau message est envoyé
    Notifie tous les participants de la conversation sauf l'expéditeur
    """
    if created:
        conversation = instance.conversation
        sender_user = instance.sender
        
        # Notifier tous les participants sauf l'expéditeur
        if sender_user:
            participants = conversation.participants.exclude(id=sender_user.id)
        else:
            participants = conversation.participants.all()
        
        for participant in participants:
            # Créer une notification pour chaque participant
            if sender_user:
                sender_name = sender_user.get_full_name() or sender_user.username
            else:
                sender_name = "Un utilisateur"
            
            content_preview = instance.content[:100] + "..." if len(instance.content) > 100 else instance.content
            
            create_notification(
                recipient=participant,
                notification_type='MESSAGE',
                title=f'Nouveau message : {conversation.subject}',
                message=f'{sender_name} vous a envoyé un message : {content_preview}',
                student=conversation.student,
                class_obj=conversation.student.current_class if conversation.student and conversation.student.current_class else None
            )
