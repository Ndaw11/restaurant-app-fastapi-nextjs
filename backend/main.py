from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import auth
from routers import users


Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# inclusion d'une route de test
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def racine():
    return {"message": "Bienvenue dans ton API FastAPI 😎"}
