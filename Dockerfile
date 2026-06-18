# partir d'une image python
FROM python:3.11

# creation du dossier de travail dans le conteneur
WORKDIR /app

# liste des dependances Python 
COPY requirements.txt .

# installation des dependances
RUN pip install --no-cache-dir -r requirements.txt

#copie du script de migration
COPY migration_csv.py .

# Lancement du script de migration au démarrage du conteneur
CMD ["python", "migration_csv.py"]