# Importation de la session SQLAlchemy pour
# interagir avec la base de données
from sqlalchemy.orm import Session

# Importation du modèle User
# UserRole est utilisé pour l'attribution du rôle (Enum)
from models.user import User, UserRole


# Importation du schéma d'entrée pour la création d'un utilisateur
from schemas.user import UserCreate

# Importation de Passlib pour le hachage du mot de passe
from passlib.context import CryptContext


# 1. Création d'un contexte de hachage de mot de passe avec bcrypt
# Cela permettra de sécuriser les mots de passe des utilisateurs
# Bcrypt est une fonction de hachage de mot de
# passe conçue pour être résistante
# aux attaques, notamment par force brute et par table arc-en-ciel.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email):
    # Exécute une requête
    # SELECT * FROM users WHERE email = ...
    # .first() renvoie le premier résultat
    # trouvé ou None s'il n'y a pas de correspondance
    return db.query(User).filter(User.email == email).first()


# 3. Fonction pour créer un nouvel utilisateur
# dans la base de données

def create_user(db: Session, user: UserCreate):
    # Hachage du mot de passe fourni par l'utilisateur
    # via bcrypt pour qu'il ne soit jamais stocké en clair
    hashed_password = pwd_context.hash(user.password)

    # Création d'un objet User (modèle SQLAlchemy) avec
    # les données de l'utilisateur
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    # Ajout de l'objet à la session de base de données
    #  (mais pas encore enregistré)
    db.add(db_user)

    # Validation des modifications (INSERT dans la base)
    db.commit()

    # Rafraîchissement de l'objet pour obtenir
    # son ID généré et les champs mis à jour
    db.refresh(db_user)

    # Retourne l'utilisateur nouvellement créé
    # (avec son ID, date, etc.)
    return db_user


def get_all_users(db: Session):
    return db.query(User).all()


def update_user_role(db: Session, user_id: int, role: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        try:
            # Problème initial :
            # user.role = role  # ❌ Erreur : on ne peut
            # pas assigner une simple chaîne à un champ Enum
            # user.role = UserRole(role)  # ❌ Erreur
            # de typage avec certains linters
            # Solution : utiliser setattr pour forcer
            # l'assignation de l'énumération
            # ✅ Correct pour SQLAlchemy et le linter
            setattr(user, "role", UserRole(role))
        except ValueError:
            # Si le rôle n'est pas valide (ex: "superadmin"),
            # on ne modifie rien et on retourne None
            return None
        db.commit()
        db.refresh(user)
    return user
