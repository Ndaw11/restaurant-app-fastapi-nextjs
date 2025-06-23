# models/user.py

# Importation des types de colonnes SQL (Integer,
# String, etc.) et outils pour les modèles SQLAlchemy
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Column, Integer, String, DateTime, Boolean
# ⚠️ Importe Base depuis database.py
from database import Base

# Importation de datetime pour gérer les dates
from datetime import datetime

# Importation du module enum de Python pour
# définir des rôles comme énumération
import enum


# 1. Définition d'une énumération représentant les
# différents rôles possibles d'un utilisateur
class UserRole(enum.Enum):
    # Rôle par défaut, un utilisateur normal
    client = "client"
    # Employé du restaurant, peut gérer les commandes ou menus
    staff = "staff"
    # Administrateur, accès complet au système
    admin = "admin"


# 2. Définition du modèle User qui
# représente la table "users" dans
# la base de données
class User(Base):
    __tablename__ = "users"  # Nom de la table SQL

    # Identifiant unique pour chaque
    # utilisateur (clé primaire)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String, index=True, nullable=False)

    # Adresse email unique, non nulle, utilisée
    # pour l'identification de l'utilisateur
    email = Column(String, unique=True, index=True, nullable=False)

    # Mot de passe chiffré (jamais stocker
    # en clair), non nul
    hashed_password = Column(String, nullable=False)

    # Rôle de l'utilisateur (client, staff, admin),
    # utilise l'énumération UserRole
    role = Column(SqlEnum(UserRole), default=UserRole.client)

    # Date et heure de création de l'utilisateur,
    # par défaut la date actuelle
    created_at = Column(DateTime, default=datetime.utcnow)

    # Champ indiquant si le compte est
    # actif ou désactivé
    is_active = Column(Boolean, default=True)
