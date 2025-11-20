# Guide d'installation - E-Parent

## Prérequis

- Python 3.8 ou supérieur
- PostgreSQL 12 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel)

## Installation étape par étape

### 1. Cloner le projet

```bash
git clone <url-du-projet>
cd E_parent
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
```

### 3. Activer l'environnement virtuel

**Windows :**
```bash
venv\Scripts\activate
```

**Linux/Mac :**
```bash
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer la base de données PostgreSQL

1. Créer une base de données :
```sql
CREATE DATABASE eparent_db;
```

2. Créer un fichier `.env` à la racine du projet (copier depuis `.env.example`) :
```bash
cp .env.example .env
```

3. Modifier les paramètres dans `.env` selon votre configuration PostgreSQL.

### 6. Appliquer les migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte administrateur.

### 8. Collecter les fichiers statiques

```bash
python manage.py collectstatic
```

### 9. Lancer le serveur de développement

```bash
python manage.py runserver
```

Le site sera accessible à l'adresse : http://127.0.0.1:8000

## Configuration de production

Pour la production, assurez-vous de :

1. Définir `DEBUG=False` dans `.env`
2. Configurer `ALLOWED_HOSTS` avec votre domaine
3. Utiliser un serveur web (Nginx + Gunicorn)
4. Configurer HTTPS
5. Configurer les sauvegardes automatiques de la base de données

## Dépannage

### Erreur de connexion à la base de données

Vérifiez que :
- PostgreSQL est démarré
- Les identifiants dans `.env` sont corrects
- La base de données existe

### Erreur de modules manquants

Réinstallez les dépendances :
```bash
pip install -r requirements.txt
```

### Erreur de migrations

Supprimez les migrations et recréez-les :
```bash
python manage.py makemigrations
python manage.py migrate
```

