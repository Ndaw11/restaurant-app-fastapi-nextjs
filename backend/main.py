from fastapi import FastAPI
from routers import demo_router
from database import Base,engine


app = FastAPI()

#inclusion d'une route de test 
app.include_router(demo_router.router)

@app.get("/")
def racine():
    return {"message": "Bienvenue dans ton API FastAPI 😎"}


# Crée les tables (à remplacer plus tard par Alembic)
Base.metadata.create_all(bind=engine)