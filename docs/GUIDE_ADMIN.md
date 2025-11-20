# Guide Administrateur - E-Parent

## Création de comptes utilisateurs

Dans E-Parent, **seuls les administrateurs peuvent créer des comptes utilisateurs**. Les utilisateurs (parents, enseignants) ne peuvent pas s'inscrire eux-mêmes.

### Accéder à l'interface d'administration

1. Connectez-vous avec votre compte administrateur sur : http://127.0.0.1:8000/admin
2. Utilisez vos identifiants de superutilisateur

### Créer un nouveau compte utilisateur

1. Dans l'interface d'administration, cliquez sur **"Utilisateurs"** dans la section **"ACCOUNTS"**
2. Cliquez sur le bouton **"Ajouter Utilisateur"** en haut à droite
3. Remplissez le formulaire :
   - **Nom d'utilisateur** : Identifiant unique pour la connexion
   - **Mot de passe** : Mot de passe sécurisé (minimum 8 caractères recommandé)
   - **Confirmation du mot de passe** : Retapez le mot de passe
   - **Email** : Adresse email de l'utilisateur
   - **Prénom** : Prénom de l'utilisateur
   - **Nom** : Nom de l'utilisateur
   - **Rôle** : Sélectionnez le rôle (Parent, Enseignant, ou Administrateur)
   - **Numéro de téléphone** : (Optionnel)
   - **Date de naissance** : (Optionnel)
   - **Adresse** : (Optionnel)
4. Cliquez sur **"Enregistrer"**

### Types de rôles

#### Parent
- Peut consulter les notes, absences et devoirs de ses enfants
- Peut recevoir des notifications
- Peut communiquer avec les enseignants

#### Enseignant
- Peut saisir et modifier les notes
- Peut enregistrer les absences/retards
- Peut publier des devoirs
- Peut consulter les listes d'élèves
- Peut communiquer avec les parents

#### Administrateur
- Accès complet au système
- Peut gérer tous les comptes utilisateurs
- Peut gérer les classes, matières, élèves
- Accès à l'interface d'administration Django

### Créer un compte élève

Les élèves ne sont pas des utilisateurs du système. Pour créer un élève :

1. Allez dans **"Core"** > **"Élèves"**
2. Cliquez sur **"Ajouter Élève"**
3. Remplissez les informations :
   - **Compte utilisateur** : Sélectionnez un compte Parent (l'élève sera lié à ce parent)
   - **Numéro d'élève** : Numéro unique d'identification
   - **Prénom** et **Nom**
   - **Date de naissance**
   - **Classe actuelle** : Sélectionnez la classe de l'élève
   - **Parents** : Sélectionnez les parents associés (peut être plusieurs)
4. Cliquez sur **"Enregistrer"**

### Conseils de sécurité

- Utilisez des mots de passe forts (minimum 8 caractères, mélange de lettres, chiffres et symboles)
- Ne partagez jamais les identifiants des comptes administrateur
- Vérifiez régulièrement les journaux de connexion dans **"Login Logs"**
- Désactivez les comptes inactifs en décochant **"Compte actif"** dans le profil utilisateur

### Gestion des classes et matières

1. **Créer une classe** : Core > Classes > Ajouter Classe
2. **Créer une matière** : Core > Matières > Ajouter Matière
3. **Associer une matière à une classe** : Core > Matières de classe > Ajouter

### Statistiques et rapports

Les administrateurs peuvent consulter :
- Le nombre total d'élèves, enseignants, parents
- Les taux d'absences
- Les moyennes par classe
- Les journaux de connexion

Tout cela est accessible depuis le tableau de bord administrateur : http://127.0.0.1:8000/

