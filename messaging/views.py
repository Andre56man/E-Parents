from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from django.db.models import Q
from .models import Conversation, Message
from core.models import Student
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def conversation_list_view(request):
    """
    Vue de la liste des conversations
    """
    user = request.user
    conversations = Conversation.objects.filter(participants=user).order_by('-updated_at')
    
    context = {
        'conversations': conversations,
    }
    
    return render(request, 'messaging/conversation_list.html', context)


@login_required
def conversation_detail_view(request, conversation_id):
    """
    Vue de détail d'une conversation
    """
    user = request.user
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=user)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=user,
                content=content
            )
            # Marquer les messages précédents comme lus pour les autres participants
            Message.objects.filter(
                conversation=conversation,
                sender__in=conversation.participants.exclude(id=user.id)
            ).update(is_read=True)
            
            messages.success(request, 'Message envoyé avec succès!')
            return redirect('messaging:conversation_detail', conversation_id=conversation_id)
        else:
            messages.error(request, 'Le message ne peut pas être vide.')
    
    message_list = conversation.messages.all().order_by('created_at')
    
    # Marquer les messages comme lus
    Message.objects.filter(
        conversation=conversation,
        sender__in=conversation.participants.exclude(id=user.id)
    ).update(is_read=True)
    
    context = {
        'conversation': conversation,
        'messages': message_list,
    }
    
    return render(request, 'messaging/conversation_detail.html', context)


@login_required
def create_conversation_view(request):
    """
    Vue pour créer une nouvelle conversation
    """
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        recipient_id = request.POST.get('recipient')
        student_id = request.POST.get('student', '')
        
        if subject and recipient_id:
            recipient = get_object_or_404(request.user.__class__, id=recipient_id)
            
            conversation = Conversation.objects.create(subject=subject)
            conversation.participants.add(request.user, recipient)
            
            if student_id:
                try:
                    student = Student.objects.get(id=student_id)
                    conversation.student = student
                    conversation.save()
                except Student.DoesNotExist:
                    # ID élève invalide : on ignore simplement le lien élève
                    pass
            
            messages.success(request, 'Conversation créée avec succès!')
            return redirect('messaging:conversation_detail', conversation_id=conversation.id)
        else:
            messages.error(request, 'Veuillez remplir tous les champs requis.')
    
    # Liste des utilisateurs avec qui on peut converser
    if request.user.is_parent():
        # Les parents peuvent converser avec les enseignants
        recipients = request.user.__class__.objects.filter(role='TEACHER')
        children = Student.objects.filter(parents=request.user)
    elif request.user.is_teacher():
        # Les enseignants peuvent converser avec les parents
        recipients = request.user.__class__.objects.filter(role='PARENT')
        children = Student.objects.none()
    else:
        recipients = request.user.__class__.objects.exclude(id=request.user.id)
        children = Student.objects.none()
    
    context = {
        'recipients': recipients,
        'children': children,
    }
    
    return render(request, 'messaging/create_conversation.html', context)
