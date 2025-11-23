from django.urls import path
from . import api_views

app_name = 'notifications_api'

urlpatterns = [
    path('', api_views.NotificationListView.as_view(), name='list'),
    path('unread-count/', api_views.NotificationUnreadCountView.as_view(), name='unread_count'),
    path('<int:notification_id>/mark-read/', api_views.NotificationMarkReadView.as_view(), name='mark_read'),
    path('mark-all-read/', api_views.NotificationMarkAllReadView.as_view(), name='mark_all_read'),
]
