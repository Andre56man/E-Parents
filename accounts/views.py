from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import UserRegistrationForm, UserLoginForm
from .models import LoginLog
import logging

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register_view(request):
    """
    Vue d'inscription - DÉSACTIVÉE
    Seuls les administrateurs peuvent créer des comptes via l'interface d'administration
    """
    messages.info(request, 'L\'inscription publique est désactivée. Seuls les administrateurs peuvent créer des comptes.')
    return redirect('core:home')


def login_view(request):
    """
    Vue de connexion avec journalisation
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Journalisation de la connexion
            LoginLog.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
            
            logger.info(f'Connexion réussie: {user.username} depuis {get_client_ip(request)}')
            messages.success(request, f'Bienvenue {user.get_full_name() or user.username}!')
            
            # Redirection selon le rôle
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            # Journalisation de l'échec de connexion
            username = request.POST.get('username', '')
            if username:
                try:
                    user = form.get_user()
                    if user:
                        LoginLog.objects.create(
                            user=user,
                            ip_address=get_client_ip(request),
                            user_agent=request.META.get('HTTP_USER_AGENT', ''),
                            success=False
                        )
                except:
                    pass
            
            logger.warning(f'Tentative de connexion échouée depuis {get_client_ip(request)}')
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Vue de déconnexion
    """
    user = request.user
    logout(request)
    logger.info(f'Déconnexion: {user.username}')
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """
    Vue du profil utilisateur
    """
    return render(request, 'accounts/profile.html', {'user': request.user})

