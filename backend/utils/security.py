# Importation des modules nécessaires

# Importation des modules FastAPI pour gérer
# les dépendances, les exceptions, et les statuts HTTP
from fastapi import Depends, HTTPException, status

# OAuth2PasswordBearer est utilisé pour extraire
# automatiquement le token Bearer depuis les requêtes
from fastapi.security import OAuth2PasswordBearer

# Modules de la bibliothèque 'python-jose' pour
# décoder et vérifier les tokens JWT
from jose import JWTError, jwt

# Session SQLAlchemy pour accéder à la base
# de données
from sqlalchemy.orm import Session

# On importe le modèle User pour pouvoir faire
# une requête sur la base de données
from models.user import User

# Fonction utilitaire pour obtenir une
# session de base de données
from database import get_db

# Pour gérer les dates d'expiration du token
from datetime import datetime, timedelta

# Pour hacher et vérifier les mots de passe
from passlib.context import CryptContext
from config.settings import settings


# 🔐 Clé secrète utilisée pour signer les JWT
# En production, il faut la stocker dans un fichier
# .env pour qu'elle reste confidentielle
# SECRET_KEY = "devsecret"

# ⚙️ Algorithme utilisé pour signer le token JWT
# HS256 = HMAC avec SHA-256 (couramment utilisé pour JWT)
# ALGORITHM = "HS256"

# ⏱️ Durée de validité d'un token JWT (en minutes)
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ⚙️ Création d'un contexte de hachage
# avec passlib
# "bcrypt" est un algorithme sécurisé
# pour hacher les mots de passe
# deprecated="auto" signifie qu'il gère
# automatiquement les anciennes versions si besoin
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Fonction pour vérifier si un mot de
# passe "en clair" correspond au mot de passe "haché"


def verify_password(plain_password: str, hashed_password: str):
    # Utilise le contexte de passlib pour
    # omparer le mot de passe saisi avec le hash
    return pwd_context.verify(plain_password, hashed_password)

# 🔒 Fonction pour hacher un mot de passe
# en clair (lors de l'inscription par exemple)


def hash_password(password: str):
    # Utilise bcrypt pour transformer le mot
    # de passe en une chaîne illisible (hashée)
    return pwd_context.hash(password)


# 🪙 Fonction pour créer un token JWT
# `data` : les infos à inclure dans le
# token (ex: {"sub": user.email})
# `expires_delta` : durée de vie personnalisée
# du token (optionnelle)
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    # Copie les données envoyées pour ne pas
    # les modifier directement
    to_encode = data.copy()

    # Calcule la date d'expiration du token :
    #  maintenant + durée spécifiée
    # Si aucune durée n'est spécifiée, on prend
    # 15 minutes par défaut
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))

    # Ajoute une clé "exp" (expiration)
    # au payload JWT
    to_encode.update({"exp": expire})

    # Crée le JWT signé avec la clé secrète
    # et l'algorithme spécifié
    # Le résultat est une chaîne de caractères
    # qu'on peut renvoyer au frontend
    return jwt.encode(to_encode, settings.SECRET_KEY,
                      algorithm=settings.ALGORITHM)


# On instancie un schéma OAuth2 pour extraire
# le token dans le header Authorization
# FastAPI va automatiquement chercher un header
# Authorization: Bearer <token> dans les requêtes
# `tokenUrl="/token"` indique l'URL qui gère
# l'authentification et la génération du token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Fonction pour obtenir l'utilisateur actuellement
# connecté (représenté par le token JWT)
# Le token est récupéré automatiquement depuis
# le header grâce à Depends(oauth2_scheme)
# La base de données est également injectée
# automatiquement avec Depends(get_db)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> User:

    # Exception personnalisée à lever si le token
    # est invalide ou que l'utilisateur n'existe pas
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # On décode le token JWT avec la clé secrète
        # et l'algorithme prévu
        # Si le token est falsifié, expiré ou mal
        # formé → cela lève une JWTError
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])

        # On récupère l'email (stocké dans "sub"
        # quand le token a été créé)
        email = payload.get("sub")
        if not isinstance(email, str):
            raise credentials_exception
        # Si aucun email n'est trouvé dans le
        # payload → token invalide
        if email is None:
            raise credentials_exception

    # Si une erreur est levée pendant le décodage
    # du token → on rejette l'accès
    except JWTError:
        raise credentials_exception

    # Requête SQLAlchemy pour récupérer l'utilisateur
    # en base grâce à son email
    user = db.query(User).filter(User.email == email).first()

    # Si aucun utilisateur n'est trouvé dans
    # la base → token invalide
    if user is None:
        raise credentials_exception

    # Si tout est ok → on retourne l'objet
    # tilisateur (donc il est authentifié)
    return user


# Fonction de sécurité qui permet de restreindre
# l'accès à certaines routes
# Elle prend en paramètre le rôle requis pour
# accéder à la route (ex: "admin", "client", etc.)

def require_role(role: str):
    # Fonction interne qui va vérifier si l'utilisateur
    # actuellement connecté a bien le rôle requis
    # Elle dépend de `get_current_user`, donc elle extrait et
    # valide automatiquement le JWT pour récupérer l'utilisateur
    def role_checker(current_user: User = Depends(get_current_user)):

        # Si le rôle de l'utilisateur ne correspond pas à celui exigé
        if current_user.role.value != role:

            # On lève une erreur 403 Forbidden (accès interdit)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accés interdit"
            )

        # Sinon, on retourne l'utilisateur (il est donc bien autorisé)
        return current_user

# On retourne la fonction `role_checker` (c'est une
# fonction retournée dynamiquement — principe des *closures*
#  en Python)
    return role_checker


# On crée des versions prêtes à l'emploi de la fonction
# `require_role` pour chaque rôle :
is_admin = require_role("admin")
is_staff = require_role("staff")
is_client = require_role("client")
