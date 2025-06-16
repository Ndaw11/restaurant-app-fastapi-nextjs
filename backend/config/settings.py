# Import de la classe BaseSettings depuis Pydantic.
# BaseSettings permet de définir une configuration basée sur des variables d'environnement.
from pydantic_settings import BaseSettings

# Définition d'une classe Settings qui hérite de BaseSettings.
# Cette classe va automatiquement charger les valeurs des variables d'environnement définies dans un fichier .env ou dans l’environnement système.
class Settings(BaseSettings):
    # URL de connexion à la base de données.
    # Exemple : "postgresql://user:password@localhost/dbname"
    DATABASE_URL: str

    # Clé secrète utilisée pour signer et vérifier les tokens JWT.
    # Doit être gardée secrète pour garantir la sécurité de l'application.
    SECRET_KEY: str

    # Algorithme utilisé pour encoder/décoder les tokens JWT.
    # Exemple courant : "HS256"
    ALGORITHM: str

    # Durée de validité du token d'accès (en minutes).
    # Par exemple, 30 signifie que le token expire au bout de 30 minutes.
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Classe de configuration interne à Pydantic.
    # Elle permet ici de spécifier le chemin vers le fichier .env qui contient les variables d'environnement.
    class Config:
        # Chemin relatif vers le fichier .env situé deux niveaux au-dessus du fichier actuel.
        # À adapter selon l’organisation de ton projet.
        env_file = "../../.env"  # important : pointer vers le bon dossier !

# Création d'une instance unique de la classe Settings.
# Grâce à cette instance, tu pourras accéder à toutes les variables de configuration en important simplement "settings" dans les autres modules.
settings = Settings()  # Ce settings-là, tu pourras l'importer partout dans ton projet pour accéder aux variables de config
