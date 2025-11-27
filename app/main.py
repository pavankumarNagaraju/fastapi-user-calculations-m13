from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import users, calculations, auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI User Calculations - JWT Auth",
    version="0.3.0",
)

# CORS (for front-end / Playwright)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, tags=["auth"])  # /register, /login
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(calculations.router, prefix="/calculations", tags=["calculations"])

# Static files (register.html, login.html)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "JWT auth + calculations API is running"}
