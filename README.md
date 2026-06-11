# Migration d'un dataset vers MongoDB

## Contexte

Ce projet consiste à migrer les données d'un fichier CSV vers une base de données MongoDB.

L'objectif est de vérifier la qualité des données avant et après la migration, puis d'automatiser l'importation à l'aide d'un script Python.

## Fonctionnalités

- Lecture du fichier CSV avec pandas
- Analyse de la qualité des données
- Détection des valeurs manquantes
- Détection des doublons
- Vérification des types de données
- Connexion à MongoDB
- Création d'une base et d'une collection
- Importation des données
- Vérification de l'intégrité après migration
- Exemples d'opérations CRUD

## Prérequis

- Python 3.11
- MongoDB installé en local et sera exécuté avec Docker
- MongoDB Compass

## Installation

Création d'un environnement virtuel.

