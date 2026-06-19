# Migration d'un dataset vers MongoDB

## Contexte

Ce projet consiste à migrer les données d'un fichier CSV vers une base de données MongoDB.

Dans un premier temps j'ai realisé un prototype avec un notebook objectif est de vérifier la qualité des données avant et après la migration tester la connexion avec la base de données Mongodb, puis d'automatiser l'importation à l'aide d'un script Python.

la solution utilise Docker Compose afin de lancer automatiquement:
- un conteneur MongoDB.
- un conteneur Python qui execute le scripte de migration.
- un volume pour stocker les données de MongoDB.
- un volume pour rendre le CSV accessible au script de migration.


## Fonctionnalités

- Lecture du fichier CSV avec pandas
- Analyse de la qualité des données
- Détection des valeurs manquantes
- Détection et suppression des doublons
- Vérification des types de données
- Connexion à MongoDB
- Création d'une base et d'une collection
- Importation des données dasn MongoDB
- Vérification de l'intégrité après migration
- Vérification du nombre de documents après migration
- Journalisation des étapes dans un fichier Loggs_migration.log

## Architecture du projet


Structure du dépôt GitHub : 

mongodb-data-migration-python/
│
├──> data/     (CSV à placer ici)
│   └──> .gitkeep 
│
├──> init-mongo/
│   └──> init-utilisateur.js
│
├──> migration_csv.py
├──> Dockerfile
├──> docker-compose.yml
├──> requirements.txt
├──> .env.example
├──> .gitignore
└──> README.md

Image créée sur Docker hub : 

Docker Hub
  └──> image contenant :
      ├──> Python
      ├──> pandas
      ├──> pymongo
      └──> migration_csv.py    

## Prérequis

- MongoDB installé en local et sera exécuté avec Docker
- Docker Desktop
- Docker Compose
- MongoDB Compass, pour verifier les données chargées
- Git

Python n'a pas besoin d'être installé localement pour exécuter la migration avec Docker, car le script est lancé dans un conteneur Python.

## Schéma de la base de données

La base MongoDB utilisée dans ce projet est "healthcare_db".

Elle contient une collection principale appelée "patients".

Chaque document de la collection représente une admission médicale issue du fichier CSV.


healthcare_db                           Type
└──> patients
    ├──> _id                           <Object>
    ├──> Name                          <Object>
    ├──> Age                            <Int>
    ├──> Gender                        <Object>
    ├──> Blood Type                    <Object>
    ├──> Medical Condition             <Object>
    ├──> Date of Admission              <Date>
    ├──> Doctor                        <Object>
    ├──> Hospital                      <Object>
    ├──> Insurance Provider            <Object>
    ├──> Billing Amount                <float>
    ├──> Room Number                    <Int>
    ├──> Admission Type                <Object>
    ├──> Discharge Date                 <Date>
    ├──> Medication                    <Object>
    └──> Test Results                  <Object>


## Description des conteneurs

Le conteneur MongoDB stocke les données migrées depuis le fichier CSV.
un volume Docker est utiliser afin de conserver les données

Conteneur de migration Python
Le conteneur Python exécute le script migration_csv.py.

Le script réalise les étapes suivantes :

- connexion à MongoDB ;
- lecture du fichier CSV ;
- contrôle des données ;
- nettoyage des doublons ;
- conversion des types ;
- transformation du DataFrame en documents MongoDB ;
- insertion des documents dans la collection ;
- vérification du nombre final de documents.

## Volumes utilisés

mongo_data :  conservation des données de la la base de données MongoDB

./data:/data:ro  Accées au fichier CSV depuis le conteneur Python, le dossier data/ contient le fichier CSV utilisé pour la migration

## Roles Utilisateurs 
Creation d'un fichier init-utilisateurs.js permettant de créer des roles.

admin_user      : administration avec tout les droits
migration_user  : migration des données avec les droits d'ecriture et de lécture
reader_user     : avec un role d'ecriture simple

## variables environnements

Integration d'un fichier exemple de variable environnement permettant d'avoir une idée sur la structure du fichier .env à avoir 

## Lancement du projet avec Docker Compose

- Dans un premier temps on place le fichier CSV dans le dossier data/ avec le nom :
    data/healthcare_dataset.csv

- Puis on lance la migration avec la commande suivante (Cela demande à Compose de vérifier et récupérer l’image avant de lancer les conteneurs.):
    docker compose up --pull always

## Vérification du bon fonctionnement

Après l'exécution, le terminal doit afficher un bilan similaire :

Connexion à MongoDB réussie.

--- Contrôle avant nettoyage ---
Nombre de lignes : 55500
Nombre de doublons : 534

--- Contrôle après nettoyage ---
Nombre de lignes : 54966
Nombre de doublons supprimés : 534

Migration terminée avec succès.
