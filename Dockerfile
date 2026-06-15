# partir d'une image python
FROM python:3.11

# creation du dossier de travail dans le conteneur
WORKDIR /app

# liste des dependances Python 
COPY requirements.txt .

# installation des dependances
RUN pip install --no-cache-dir -r requirements.txt

#copie du script de migration
COPY main.py .

# Lancement du script main.py au lancement du conteneur
CMD ["python", "main.py"]