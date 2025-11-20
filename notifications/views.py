from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notification


@login_required
def notification_list_view(request):
    """
    Vue de la liste des notifications
    """
    notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    unread_count = notifications.count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    
    return render(request, 'notifications/list.html', context)


@login_required
@require_http_methods(["POST"])
def mark_as_read_view(request, notification_id):
    """
    Vue pour marquer une notification comme lue
    """
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.mark_as_read()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification non trouvée'})


@login_required
@require_http_methods(["POST"])
def mark_all_as_read_view(request):
    """
    Vue pour marquer toutes les notifications comme lues
    """
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})


@login_required
def unread_count_view(request):
    """
    Vue API pour obtenir le nombre de notifications non lues
    """
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})

