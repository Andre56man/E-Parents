from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list_view, name='conversation_list'),
    path('create/', views.create_conversation_view, name='create_conversation'),
    path('<int:conversation_id>/', views.conversation_detail_view, name='conversation_detail'),
    path('message/<int:message_id>/mark-read/', views.mark_message_read_view, name='mark_message_read'),
]

