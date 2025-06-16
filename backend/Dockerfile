# 1. Image de base légère avec Python 3.11
FROM python:3.11-slim

# 2. Variables d'environnement pour le confort
# Empeche python de creer des fichiers .pyc inutiles
ENV PYTHONDONTWRITEBYTECODE 1 
#Les logs saffichent immediatement dans le terminal
ENV PYTHONUNBUFFERED 1

# 3. Dossier de travail
WORKDIR /app

# 4. Installation des dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copier tout le projet backend
COPY . .

# 6. Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]