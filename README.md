# E-Parent - Plateforme de Suivi Scolaire

## Description

E-Parent est une plateforme numérique de suivi scolaire et académique permettant aux parents de suivre la scolarité de leurs enfants en temps réel. Le système facilite la communication entre les établissements scolaires, les enseignants et les parents.

## Objectifs

- Fournir aux parents un accès rapide et sécurisé aux informations scolaires
- Offrir aux enseignants un outil simple pour la saisie et la gestion des notes et absences
- Faciliter la communication entre les parents et les établissements
- Améliorer la transparence et la réactivité dans le suivi des élèves

## Technologies utilisées

- **Backend** : Django (Python)
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de données** : PostgreSQL
- **Architecture** : MVC (Modèle-Vue-Contrôleur)

## Installation

### Prérequis

- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Cloner le projet :
```bash
git clone <url-du-projet>
cd E_parent
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
```

3. Activer l'environnement virtuel :
- Windows : `venv\Scripts\activate`
- Linux/Mac : `source venv/bin/activate`

4. Installer les dépendances :
```bash
pip install -r requirements.txt
```

5. Configurer la base de données :
- Créer une base de données PostgreSQL nommée `eparent_db`
- Modifier les paramètres de connexion dans `eparent/settings.py` si nécessaire

6. Appliquer les migrations :
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Créer un superutilisateur :
```bash
python manage.py createsuperuser
```
Ou utilisez le script rapide :
```bash
python create_superuser.py
```
(Crée un admin avec username: `admin` et password: `admin123`)

8. Lancer le serveur de développement :
```bash
python manage.py runserver
```

Le site sera accessible à l'adresse : http://127.0.0.1:8000

**Note importante :** L'inscription publique est désactivée. Seuls les administrateurs peuvent créer des comptes via l'interface d'administration Django (http://127.0.0.1:8000/admin). Voir `docs/GUIDE_ADMIN.md` pour plus de détails.

## Structure du projet

```
E_parent/
├── eparent/              # Configuration principale Django
├── accounts/             # Application d'authentification
├── core/                 # Application principale (élèves, classes, notes)
├── notifications/       # Système de notifications
├── messaging/           # Système de messagerie
├── static/              # Fichiers statiques (CSS, JS, images)
├── templates/           # Templates HTML
├── media/               # Fichiers médias uploadés
└── manage.py            # Script de gestion Django
```

## Profils utilisateurs

### Parent
- Consulter les notes et moyennes de leurs enfants
- Visualiser les absences et retards
- Consulter le planning des devoirs et examens
- Recevoir des notifications
- Échanger des messages avec les enseignants

### Enseignant
- Saisir et modifier les notes et absences
- Publier les devoirs et annonces
- Consulter les listes d'élèves par classe
- Communiquer avec les parents

### Administrateur
- Gérer les comptes utilisateurs
- Gérer les classes, matières et enseignants
- Consulter les statistiques globales
- Superviser la sécurité et la maintenance

## Sécurité

- Authentification par identifiant et mot de passe crypté (bcrypt)
- Gestion des rôles et permissions distinctes
- Journalisation des connexions
- Connexion sécurisée (HTTPS en production)
- Sauvegarde régulière de la base de données
- Conformité RGPD

## Tests

```bash
python manage.py test
```

## Documentation

Voir le dossier `docs/` pour la documentation complète du projet.

## Auteurs

Équipe de développement - Projet de Génie Logiciel (S5)

## Licence

Ce projet est développé dans le cadre académique.

