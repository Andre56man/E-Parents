# Architecture du Projet E-Parent

## Vue d'ensemble

Le projet E-Parent suit une architecture MVC (Modèle-Vue-Contrôleur) avec Django comme framework backend.

## Structure des applications

### 1. `accounts` - Gestion des comptes utilisateurs

**Responsabilités :**
- Authentification et autorisation
- Gestion des profils utilisateurs
- Journalisation des connexions
- Rôles utilisateurs (Parent, Enseignant, Administrateur)

**Modèles principaux :**
- `User` : Modèle utilisateur personnalisé avec rôles
- `LoginLog` : Journalisation des connexions

### 2. `core` - Application principale

**Responsabilités :**
- Gestion des élèves, classes, matières
- Gestion des notes et absences
- Gestion des devoirs
- Tableaux de bord par rôle

**Modèles principaux :**
- `School` : Établissement scolaire
- `Subject` : Matière
- `Class` : Classe
- `Student` : Élève
- `Grade` : Note
- `Attendance` : Absence/Retard
- `Assignment` : Devoir/Examen
- `ClassSubject` : Liaison classe-matière

### 3. `notifications` - Système de notifications

**Responsabilités :**
- Création et gestion des notifications
- Notifications automatiques (notes, absences, devoirs)
- Marquage des notifications comme lues

**Modèles principaux :**
- `Notification` : Notification

### 4. `messaging` - Système de messagerie

**Responsabilités :**
- Communication entre parents et enseignants
- Gestion des conversations
- Envoi de messages

**Modèles principaux :**
- `Conversation` : Conversation
- `Message` : Message

## Flux de données

### Authentification
1. Utilisateur se connecte → `accounts.views.login_view`
2. Vérification des identifiants
3. Journalisation de la connexion
4. Redirection vers le tableau de bord selon le rôle

### Ajout d'une note
1. Enseignant saisit une note → `core.views.add_grade_view`
2. Sauvegarde dans la base de données → `Grade`
3. Signal déclenché → `core.signals.notify_parent_on_grade`
4. Notification créée pour les parents → `notifications.models.create_notification`

### Consultation des notes (Parent)
1. Parent accède au tableau de bord → `core.views.parent_dashboard`
2. Affichage des enfants → `Student.objects.filter(parents=user)`
3. Affichage des notes récentes → `Grade.objects.filter(student__in=children)`

## Sécurité

### Authentification
- Mots de passe cryptés avec bcrypt (via Django)
- Sessions sécurisées
- Protection CSRF

### Autorisation
- Décorateurs `@login_required` pour les vues protégées
- Décorateurs `@user_passes_test` pour les rôles spécifiques
- Vérification des permissions dans les vues

### Journalisation
- Toutes les connexions sont journalisées dans `LoginLog`
- Logs d'application dans `logs/eparent.log`

## Base de données

### Relations principales

```
User (Parent) ──< Student >── Class
                      │
                      ├──< Grade >── Subject
                      │
                      └──< Attendance >── Class
                      
User (Teacher) ──< ClassSubject >── Subject
                      │
                      └──< Class
```

## API et endpoints

### URLs principales

- `/` : Tableau de bord (selon le rôle)
- `/accounts/login/` : Connexion
- `/accounts/register/` : Inscription
- `/accounts/profile/` : Profil utilisateur
- `/student/<id>/` : Détails d'un élève (parents)
- `/teacher/class/<id>/students/` : Liste des élèves (enseignants)
- `/notifications/` : Liste des notifications
- `/messaging/` : Messagerie

## Tests

Les tests doivent couvrir :
- Tests unitaires des modèles
- Tests d'intégration des vues
- Tests fonctionnels des workflows
- Tests de performance

## Déploiement

### Production
- Serveur web : Nginx
- Serveur WSGI : Gunicorn
- Base de données : PostgreSQL
- HTTPS obligatoire
- Sauvegardes automatiques

