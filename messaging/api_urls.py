from django.urls import path
from . import api_views

app_name = 'messaging_api'

urlpatterns = [
    path('conversations/', api_views.ConversationListView.as_view(), name='conversation_list'),
    path('conversations/create/', api_views.ConversationCreateView.as_view(), name='conversation_create'),
    path('conversations/<int:conversation_id>/messages/', api_views.ConversationMessagesView.as_view(), name='conversation_messages'),
    path('conversations/<int:conversation_id>/messages/create/', api_views.MessageCreateView.as_view(), name='message_create'),
]
