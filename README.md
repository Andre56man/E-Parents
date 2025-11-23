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

## API REST pour applications externes (React Native, etc.)

Une API REST basée sur **Django REST Framework** et **JWT** est disponible pour consommer les données de la plateforme depuis une application mobile (par exemple React Native) ou un autre client.

Toutes les routes suivantes attendent (sauf indication contraire) un header d'authentification JWT :

```http
Authorization: Bearer <access_token>
```

### Authentification JWT

- **POST** `/api/auth/jwt/create/`
  - Authentifier un utilisateur et obtenir les tokens `access` et `refresh`.
  - Body JSON : `{ "username": "...", "password": "..." }`

- **POST** `/api/auth/jwt/refresh/`
  - Rafraîchir le token d'accès à partir du token `refresh`.

- **GET** `/api/auth/me/`
  - Récupérer les informations de l'utilisateur connecté (id, username, rôle, etc.).
  - **Code** :
    - `eparent/urls.py` (routes JWT /api/auth/...)
    - `core/api_views.py` (`MeView`)
    - `core/api_serializers.py` (`UserSerializer`)

### API Parent

Accessible uniquement si `role = PARENT`.

- **GET** `/api/parent/students/`
  - Liste des enfants (modèle `Student`) liés au parent connecté.
  - **Code** : `core/api_views.py` (`ParentStudentsListView`), `core/api_serializers.py` (`StudentSerializer`)

- **GET** `/api/parent/students/<student_id>/attendances/`
  - Liste des absences/retards d'un élève.
  - **Code** : `core/api_views.py` (`ParentStudentAttendancesView`), `core/api_serializers.py` (`AttendanceSerializer`)

- **GET** `/api/parent/students/<student_id>/grades/`
  - Liste des notes d'un élève (matière, enseignant, type de note, valeur, etc.).
  - **Code** : `core/api_views.py` (`ParentStudentGradesView`), `core/api_serializers.py` (`GradeSerializer`)

- **GET** `/api/parent/students/<student_id>/assignments/`
  - Liste des devoirs/examens à venir pour l'élève (via sa classe actuelle).
  - **Code** : `core/api_views.py` (`ParentStudentAssignmentsView`), `core/api_serializers.py` (`AssignmentSerializer`)

### API Enseignant

Accessible uniquement si `role = TEACHER`.

- **GET** `/api/teacher/classes/`
  - Liste des classes de l'enseignant (prof principal ou via matières enseignées).
  - **Code** : `core/api_views.py` (`TeacherClassesView`), `core/api_serializers.py` (`ClassSerializer`)

- **GET** `/api/teacher/classes/<class_id>/students/`
  - Liste des élèves d'une classe.
  - **Code** : `core/api_views.py` (`TeacherClassStudentsView`), `core/api_serializers.py` (`StudentSerializer`)

- **GET** `/api/teacher/students/<student_id>/grades/`
  - Liste des notes d'un élève (vue enseignant).
  - **Code** : `core/api_views.py` (`TeacherStudentGradesView`), `core/api_serializers.py` (`GradeSerializer`)

- **POST** `/api/teacher/grades/`
  - Créer une note pour un élève.
  - Body JSON (exemple) : `{ "student": 3, "subject": 2, "grade_type": "DEVOIR", "value": "15.00", "coefficient": "1.00", "comment": "", "date": "2025-11-21" }`
  - **Code** : `core/api_views.py` (`TeacherGradeCreateView`), `core/api_serializers.py` (`GradeSerializer`)

- **POST** `/api/teacher/attendances/`
  - Enregistrer une absence/retard.
  - Body JSON (exemple) : `{ "student": 3, "class_obj": 5, "subject": 2, "date": "2025-11-21", "status": "ABSENT", "reason": "", "justified": false }`
   - **Code** : `core/api_views.py` (`TeacherAttendanceCreateView`), `core/api_serializers.py` (`AttendanceSerializer`)

- **GET / POST** `/api/teacher/assignments/`
  - `GET` : liste des devoirs/examens créés par l'enseignant.
  - `POST` : créer un devoir/examen.
  - **Code** : `core/api_views.py` (`TeacherAssignmentsView`), `core/api_serializers.py` (`AssignmentSerializer`)

### API Notifications

Accessible à tout utilisateur authentifié.

- **GET** `/api/notifications/`
  - Liste des notifications de l'utilisateur.
  - Paramètre optionnel : `?is_read=true|false` pour filtrer.
  - **Code** : `notifications/api_views.py` (`NotificationListView`), `notifications/api_serializers.py` (`NotificationSerializer`)

- **GET** `/api/notifications/unread-count/`
  - Nombre de notifications non lues : `{ "count": <int> }`.
  - **Code** : `notifications/api_views.py` (`NotificationUnreadCountView`)

- **POST** `/api/notifications/<notification_id>/mark-read/`
  - Marquer une notification comme lue.
  - **Code** : `notifications/api_views.py` (`NotificationMarkReadView`)

- **POST** `/api/notifications/mark-all-read/`
  - Marquer toutes les notifications comme lues.
  - **Code** : `notifications/api_views.py` (`NotificationMarkAllReadView`)

### API Messagerie

Accessible à tout utilisateur authentifié.

- **GET** `/api/messaging/conversations/`
  - Liste des conversations où l'utilisateur est participant.
  - **Code** : `messaging/api_views.py` (`ConversationListView`), `messaging/api_serializers.py` (`ConversationSerializer`)

- **POST** `/api/messaging/conversations/create/`
  - Créer une nouvelle conversation.
  - Body JSON (exemple) : `{ "subject": "Sujet", "recipient": <user_id>, "student": <student_id | null> }`.
  - **Code** : `messaging/api_views.py` (`ConversationCreateView`)

- **GET** `/api/messaging/conversations/<conversation_id>/messages/`
  - Liste des messages d'une conversation (les messages des autres participants sont marqués comme lus).
  - **Code** : `messaging/api_views.py` (`ConversationMessagesView`), `messaging/api_serializers.py` (`MessageSerializer`)

- **POST** `/api/messaging/conversations/<conversation_id>/messages/create/`
  - Envoyer un message dans une conversation existante.
  - Body JSON : `{ "content": "Mon message" }`.
  - **Code** : `messaging/api_views.py` (`MessageCreateView`)

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

