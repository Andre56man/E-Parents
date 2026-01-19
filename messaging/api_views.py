from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from core.models import Student
from .api_serializers import ConversationSerializer, MessageSerializer, UserMiniSerializer

User = get_user_model()


class ParentContactsView(generics.ListAPIView):
    """
    Renvoie tous les profs et admins pour qu’un parent puisse démarrer une conversation
    """
    serializer_class = UserMiniSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Tous les profs + administration
        return User.objects.filter(role__in=['TEACHER', 'ADMIN'])
    

class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')


class ConversationMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=self.request.user)
        # Marquer les messages des autres comme lus
        Message.objects.filter(
            conversation=conversation,
            sender__in=conversation.participants.exclude(id=self.request.user.id)
        ).update(is_read=True)
        return conversation.messages.all().order_by('created_at')


class ConversationCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        subject = request.data.get('subject', '').strip()
        recipient_id = request.data.get('recipient')
        student_id = request.data.get('student')

        if not subject or not recipient_id:
            return Response({'detail': 'Sujet et destinataire requis.'}, status=status.HTTP_400_BAD_REQUEST)

        recipient = get_object_or_404(User, id=recipient_id)
        conversation = Conversation.objects.create(subject=subject)
        conversation.participants.add(request.user, recipient)

        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                conversation.student = student
                conversation.save()
            except Student.DoesNotExist:
                pass

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        content = request.data.get('content', '').strip()
        if not content:
            return Response({'detail': 'Le message ne peut pas être vide.'}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content,
        )

        # Marquer les messages précédents des autres comme lus
        Message.objects.filter(
            conversation=conversation,
            sender__in=conversation.participants.exclude(id=request.user.id)
        ).update(is_read=True)

        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)