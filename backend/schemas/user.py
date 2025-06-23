# schemas/user.py

# Importation des outils de Pydantic pour la
# validation des données
# BaseModel est la classe de base fournie par Pydantic.
# Quand tu hérites de BaseModel, tu obtiens tout un
# moteur de validation automatique, de sérialisation et
# de documentation.

from pydantic import BaseModel, EmailStr
from typing import Literal
# Importation d'Enum pour définir les rôles utilisateurs
from enum import Enum

# Importation de datetime pour gérer la date de création
from datetime import datetime

# 1. Définition d'une énumération (Enum) pour
# les rôles, identique à celle du modèle SQLAlchemy
# On hérite de str pour que les valeurs soient
# des chaînes et compatibles avec Pydantic/JSON


class UserRole(str, Enum):
    client = "client"  # Rôle par défaut
    staff = "staff"    # Employé
    admin = "admin"    # Administrateur

# 2. Schéma pour la création d’un utilisateur
# (ce que l’on attend comme input pour une inscription)


class UserCreate(BaseModel):
    name: str
    # Vérifie que l’email est bien valide
    email: EmailStr
    # Mot de passe en clair (sera haché plus tard)
    password: str
    # Rôle facultatif, par défaut "client"
    role: UserRole = UserRole.client

# 3. Schéma de sortie (ce qu’on renvoie
# au frontend/API, donc sans mot de passe)


class UserOut(BaseModel):
    id: int                      # ID de l’utilisateur
    name: str
    email: EmailStr             # Email valide
    role: UserRole              # Rôle de l’utilisateur
    created_at: datetime        # Date d’inscription
    is_active: bool             # Indique si le compte est actif

    class Config:
        # Permet à Pydantic de lire les objets
        # SQLAlchemy directement # (anciennement
        # rm_mode = True)
        from_attributes = True


class UpdateRole(BaseModel):
    role: Literal["client", "staff", "admin"]
