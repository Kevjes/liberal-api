# app/main.py
from app.features.users.routes import router as users_router
from app.features.departments.routes import router as departments_router
from app.features.municipalities.routes import router as municipalities_router
from app.features.cards.routes import router as cards_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.features.auth.routes import router as auth_router
from app.core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:1356"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app.mount("/static", StaticFiles(directory="static"), name="static") 

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(departments_router)
app.include_router(municipalities_router)
app.include_router(cards_router)
# add another router