# import  des librairies utilisées
import pandas as pd
from datetime import datetime
from pymongo import MongoClient

import os

# Logging : 
 
import logging
from datetime import datetime

#initialisation des logging
logging.basicConfig(
    filename="Loggs_migration.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")


# Creation d'une classe contenant les fonctions ETL

class Migration :

    """ Automatisation de la migration d'un fichier CSV vers MongoDB.
      Étapes : 
      1. Connexion à MongoDB 
      2. Extraction du fichier CSV 
      3. Contrôle et nettoyage des données 
      4. Conversion des lignes en documents 
      5. Chargement dans MongoDB 
      """
    
    def __init__( self, uri_mongodb: str, nom_base: str, nom_collection: str ) -> None:
        self.uri_mongodb = uri_mongodb
        self.nom_base = nom_base 
        self.nom_collection = nom_collection 
        self.client = None 
        self.collection = None

    # Connexion avec Mongodb : 
    def connexion(self):
        """Établir la connexion avec MongoDB et vérifier que le serveur répond."""
        logging.info("Début de la connexion à MongoDB")

        try :
            
            #tantative de connexion et attente de 5 sec
            self.client = MongoClient(self.uri_mongodb, serverSelectionTimeoutMS=5000)

            # creation de la base de données et de la collection 
            base_de_donnees = self.client[self.nom_base]
            self.collection = base_de_donnees[self.nom_collection]

            print("Connexion à MongoDB réussie.")
            logging.info("Connexion avec mangoDB établie")

        except Exception as e:
            print (e)

# Extraction:
    def extraction(self,path : str) -> pd.DataFrame:

        """Lire le fichier CSV et retourner un DataFrame."""
        logging.info(" Debut d'extraction du fichier CSV")

        dataset = pd.read_csv(path)
        
        logging.info(" fin de l'extraction du fichier CSV")
        return dataset

# Traitement :
    def traitement(self,dataset: pd.DataFrame) -> list[dict]:
        """Contrôler, nettoyer et convertir les données en documents MongoDB."""
        logging.info("Début du traitement des données")

        print("\n--- Contrôle avant nettoyage ---") 
        print("Nombre de lignes :", len(dataset)) 
        print("Nombre de doublons :", dataset.duplicated().sum())

        

        # Vérification des valeurs manquantes
        valeurs_manquantes = dataset.isna().sum()

        # si au moins une valeur a une valeur manquante on l'affiche
        if (valeurs_manquantes > 0).any():
            print("\n Attention valeurs manquantes detectées : ")
            print(valeurs_manquantes)
            logging.warning( "Valeurs manquantes détectées : %s", valeurs_manquantes.to_list() )
        
        
        # Standardisation des noms des patients : 
        dataset["Name"] = dataset["Name"].str.title()

        # Conversion des dates:
        dataset['Date of Admission'] = pd.to_datetime(dataset['Date of Admission'])
        dataset['Discharge Date'] = pd.to_datetime(dataset['Discharge Date'])

        # # Conversion des colonnes textuelles:
        colonnes_str = ['Gender', 'Blood Type', 'Medical Condition', 'Doctor', 'Hospital', 'Insurance Provider','Admission Type', 'Medication', 'Test Results']
        dataset[colonnes_str] = dataset[colonnes_str].astype('string')

        # Conversion des colonnes entières: 
        colonnes_int = ['Age','Room Number']
        dataset[colonnes_int] = dataset[colonnes_int].astype('int')

        # Conversion de la facturation 
        dataset["Billing Amount"] = ( dataset["Billing Amount"] .astype("float64"))

        # # Suppression des lignes entièrement dupliquées et reset des index
        dataset_cleaned = dataset.drop_duplicates().reset_index(drop=True)

        print("\n--- Contrôle après nettoyage ---") 
        print("Nombre de lignes :", len(dataset_cleaned))
        print( "Nombre de doublons supprimés :", len(dataset) - len(dataset_cleaned))

        # covertion du dataframe en liste de dictionaire 
        documents = dataset_cleaned.to_dict(orient="records")

        logging.info("Fin du traitement : %s documents préparés",len(documents))

        return documents


#Chargement:
    def chargement(self,documents: list[dict]) -> None:
    
        """Remplacer les données existantes puis insérer les documents nettoyés."""

        logging.info(" Début du chargement des données")

        #suppression 
        resultat_suppression = self.collection.delete_many({})

        print(
            "Documents supprimés avant rechargement pour éviter les doublons :",
            resultat_suppression.deleted_count
        )

        logging.info("%s documents supprimés avant rechargement", resultat_suppression.deleted_count)
        
        # Insertion : 
        print( " chargement des nouveaux documents")
        self.collection.insert_many(documents)

        nombre_documents = self.collection.count_documents({})

        logging.info("Fin du chargement : %s documents présents dans MongoDB", nombre_documents )

    def fermer_connexion(self) -> None: 
        """Fermer proprement la connexion MongoDB.""" 
        if self.client is not None:
             self.client.close() 
             logging.info("Connexion MongoDB fermée")




def main():
    # utilisation du local host
    uri_mongodb = os.getenv( "MONGO_URI", "mongodb://localhost:27017/" )

    mig = Migration( uri_mongodb = uri_mongodb, nom_base="healthcare_db", nom_collection="patients" )
    try:
        mig.connexion()
        dataset = mig.extraction("healthcare_dataset.csv")
        documents = mig.traitement(dataset)
        mig.chargement(documents)

        print("\nMigration terminée avec succès.")
    finally:
          mig.fermer_connexion()



if __name__ == "__main__":
    main()

