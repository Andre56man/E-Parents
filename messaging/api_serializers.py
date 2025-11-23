from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'content',
            'is_read',
            'created_at',
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserMiniSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id',
            'subject',
            'student',
            'created_at',
            'updated_at',
            'participants',
            'last_message',
        ]

    def get_last_message(self, obj):
        msg = obj.messages.order_by('-created_at').first()
        if not msg:
            return None
        return MessageSerializer(msg).data
