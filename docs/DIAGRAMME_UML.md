# Diagrammes UML - E-Parent

## Diagramme de cas d'utilisation

### Acteurs
- **Parent** : Consulte les informations de ses enfants
- **Enseignant** : Saisit les notes, absences, publie les devoirs
- **Administrateur** : Gère le système et les utilisateurs

### Cas d'utilisation principaux

#### Pour les Parents
1. Se connecter
2. Consulter les notes de ses enfants
3. Consulter les absences/retards
4. Consulter les devoirs à venir
5. Recevoir des notifications
6. Échanger des messages avec les enseignants

#### Pour les Enseignants
1. Se connecter
2. Saisir/modifier les notes
3. Enregistrer les absences/retards
4. Publier des devoirs
5. Consulter les listes d'élèves
6. Communiquer avec les parents

#### Pour les Administrateurs
1. Se connecter
2. Gérer les comptes utilisateurs
3. Gérer les classes et matières
4. Consulter les statistiques
5. Superviser le système

## Diagramme de classes

```
User
├── role (PARENT, TEACHER, ADMIN)
├── phone_number
└── date_of_birth

Student
├── user (OneToOne)
├── student_number
├── first_name
├── last_name
├── current_class (ForeignKey)
└── parents (ManyToMany)

Class
├── name
├── level (PRIMAIRE, COLLEGE, LYCE)
├── school (ForeignKey)
├── teacher (ForeignKey)
└── academic_year

Subject
├── name
└── code

Grade
├── student (ForeignKey)
├── subject (ForeignKey)
├── teacher (ForeignKey)
├── value
├── grade_type
└── date

Attendance
├── student (ForeignKey)
├── class_obj (ForeignKey)
├── date
├── status (ABSENT, RETARD, JUSTIFIE)
└── justified

Assignment
├── title
├── subject (ForeignKey)
├── class_obj (ForeignKey)
├── teacher (ForeignKey)
└── due_date

Notification
├── recipient (ForeignKey)
├── notification_type
├── title
├── message
├── student (ForeignKey)
└── is_read

Conversation
├── participants (ManyToMany)
├── subject
└── student (ForeignKey)

Message
├── conversation (ForeignKey)
├── sender (ForeignKey)
├── content
└── is_read
```

## Diagramme de séquence - Ajout d'une note

```
Enseignant -> Vue: Saisir une note
Vue -> Contrôleur: POST /teacher/add-grade/
Contrôleur -> Modèle: Grade.objects.create()
Modèle -> Base de données: INSERT
Base de données -> Signal: post_save
Signal -> Notification: create_notification()
Notification -> Base de données: INSERT
Notification -> Parent: Notification créée
```

## Diagramme d'activité - Connexion

```
[Début] -> [Saisie identifiants]
-> [Vérification] -> {Identifiants valides?}
-> Oui -> [Création session] -> [Journalisation] -> [Redirection tableau de bord] -> [Fin]
-> Non -> [Message d'erreur] -> [Retour formulaire] -> [Début]
```

## Diagramme de déploiement

```
[Client Web]
    |
    v
[Nginx] (Reverse Proxy)
    |
    v
[Gunicorn] (WSGI Server)
    |
    v
[Django Application]
    |
    v
[PostgreSQL Database]
```

