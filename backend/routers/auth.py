# routes/auth.py

# 📦 Importation de FastAPI pour créer
# les routes, gérer les erreurs et dépendances
from fastapi import APIRouter, Depends, HTTPException, status

# 🔐 Importation d'un formulaire de type OAuth2
# (utilisé pour récupérer email et mot de passe)
from fastapi.security import OAuth2PasswordRequestForm

# 🛢️ Importation du type Session pour interagir
# avec la base de données via SQLAlchemy
from sqlalchemy.orm import Session

# 🔌 get_db est une fonction (dans database.py)
# qui donne une session DB utilisable dans la route
from database import get_db

# 🧍 Importation du modèle User (définit les
# colonnes de la table users)

# 🔐 Fonctions de sécurité personnalisées
from utils.security import verify_password, create_access_token, is_admin

# Importation des schémas d'entrée
# (UserCreate) et de sortie (UserOut)
from schemas.user import UserCreate, UserOut

# Importation des fonctions CRUD définies
# pour les utilisateurs
from crud import user as crud_user

from schemas.token import TokenResponse


# 🔁 Création d'un routeur FastAPI pour
# séparer les routes de login dans un
# fichier à part
router = APIRouter()


# 📥 Route POST vers /token : utilisée
# pour se connecter (login)
# Cette route reçoit des identifiants (email +
# mot de passe), et retourne un token JWT
# 📌 form_data va automatiquement contenir les
# champs "username" et "password" du formulaire
# C'est géré automatiquement par FastAPI grâce
# à OAuth2PasswordRequestForm
# 🔌 db est une instance de session SQLAlchemy
# injectée automatiquement
@router.post("/token", response_model=TokenResponse)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):

    # 🔎 On cherche l'utilisateur en base via son
    # email (form_data.username contient l'email)
    user = crud_user.get_user_by_email(db, form_data.username)

    # ❌ Si l'utilisateur n'existe pas OU que le
    # mot de passe est incorrect :
    # Attention : il faut passer la VALEUR du champ
    # (user.hashed_password) et non la colonne SQLAlchemy !
    # Mauvais : verify_password(form_data.password,
    # User.hashed_password)  # ceci passerait la colonne
    # Bon : verify_password(form_data.password,
    # user.hashed_password)   # ceci passe la valeur du hash
    if not user or not verify_password(form_data.password,
                                       user.hashed_password):
        # 👉 On lève une exception HTTP 401 (Unauthorized)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            # Message d'erreur lisible côté frontend
            detail="Email ou mot de passe incorrect",
            # Indique que l'authentification est requise
            headers={"WWW-Athenticate": "Bearer"},
        )
    # ✅ L'utilisateur est authentifié → on
    # peut lui créer un token JWT
    # Le token contiendra :
    # - "sub" : identifiant principal du
    # token (ici l'email, mais ça pourrait être l'ID)
    # - "role" : utile si on veut faire des
    # autorisations par rôle (admin/client/...)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )
    # 🔁 On retourne le token sous forme
    # de dictionnaire JSON
    # "access_token" : le JWT
    # "token_type" : spécifie le type (ici
    # "bearer", utilisé dans les headers Authorization)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Route POST pour l'inscription d'un
# nouvel utilisateur
@router.post("/register", response_model=UserOut)
# Cette ligne crée une route HTTP POST
# accessible via "/register"
# La réponse attendue est conforme au
# schéma Pydantic UserOut,
# ce qui signifie que le client recevra uniquement
# les champs définis dans UserOut (excluant le mot
# de passe par exemple).
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 'user: UserCreate' : FastAPI va automatiquement
    # valider et convertir les données JSON reçues
    # selon le modèle Pydantic UserCreate
    # (name,email, password, role).
    # 'db: Session = Depends(get_db)' : ici on utilise
    # une dépendance FastAPI pour injecter une session
    # SQLAlchemy de base de données.
    # Cette session est essentielle pour faire des
    # requêtes et manipuler la DB dans ce contexte.

    # Vérifie si un utilisateur existe déjà avec cet email
    db_user = crud_user.get_user_by_email(db, user.email)
    # Appel à la fonction CRUD qui interroge la
    # DB pour trouver un utilisateur avec cet email.
    # Important : cette vérification évite la création
    # de doublons, ce qui pourrait causer des conflits
    # d'authentification.

    if db_user:
        # Si un utilisateur avec cet email existe
        # déjà dans la base, on lève une exception HTTP
        # 400 (Bad Request).
        # HTTPException permet de renvoyer une réponse
        # d'erreur structurée à l'appelant (client API).
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
        # 'detail' est le message d'erreur envoyé dans
        # la réponse JSON, utile pour informer l'utilisateur
        # final.

    # Si l'email n'existe pas encore en DB, on
    # procède à la création du nouvel utilisateur
    return crud_user.create_user(db, user)
    # On appelle la fonction de création utilisateur
    # définie dans le CRUD.
    # Cette fonction va :
    # - Hasher le mot de passe pour sécuriser le
    # stockage (jamais stocker en clair !)
    # - Construire un objet User SQLAlchemy
    # - Ajouter cet objet à la session de la DB
    # - Commit (valider) la transaction pour
    # sauvegarder les changements en base
    # - Actualiser l'objet pour obtenir son ID
    # auto-généré et autres champs par défaut
    # Enfin, on retourne l'objet utilisateur créé,
    # qui sera converti en JSON grâce au response_model UserOut.


@router.get("/admin-only")
def admin_route(current_user=Depends(is_admin)):
    return {"message": "Bienvenue admin !"}
