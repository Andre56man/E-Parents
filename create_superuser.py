"""
Script pour créer un superutilisateur rapidement
Usage: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eparent.settings')
django.setup()

from accounts.models import User

# Créer un superutilisateur par défaut
username = 'admin'
email = 'admin@eparent.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        role='ADMIN',
        first_name='Administrateur',
        last_name='E-Parent'
    )
    print(f"Superutilisateur créé avec succès!")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print(f"L'utilisateur '{username}' existe déjà.")

