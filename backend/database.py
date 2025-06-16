# Import de la fonction create_engine de SQLAlchemy
# Elle permet de créer une connexion (engine) vers la base de données.
from sqlalchemy import create_engine

# Import de sessionmaker et declarative_base du module ORM de SQLAlchemy
# - sessionmaker : pour créer des sessions de connexion à la base de données
# - declarative_base : pour créer la classe de base de tous les modèles ORM
from sqlalchemy.orm import sessionmaker, declarative_base

# Import de l’objet settings depuis le fichier config/settings.py
# settings contient toutes les variables de configuration chargées depuis le .env
from config.settings import settings

# Création de l’engine SQLAlchemy à partir de l’URL de la base de données
# Cette URL provient de settings.DATABASE_URL et contient toutes les infos de connexion
engine = create_engine(settings.DATABASE_URL)

# Création d'une classe SessionLocal via sessionmaker
# Cela permettra de créer des sessions indépendantes pour interagir avec la base
# - autocommit=False : les changements doivent être validés manuellement
# - autoflush=False : empêche l'envoi automatique des changements à la base tant qu'on n'appelle pas flush() ou commit()
# - bind=engine : attache la session à l'engine (connexion à la base)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # ⚠️ Correction de "bing" → "bind"

# Création de la base de toutes les classes ORM
# Tous tes modèles SQLAlchemy devront hériter de cette classe Base
Base = declarative_base()  # ⚠️ Correction de "BAse" → "Base"
