from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import users, calculations, auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI User Calculations – JWT Auth",
    version="0.1.0",
)

# --- Routers (IMPORTANT for tests) ---
# /users/register  -> used by test_users_integration.py
app.include_router(users.router, prefix="/users", tags=["users"])

# /calculations/... -> used by test_calculations_integration.py
app.include_router(calculations.router, prefix="/calculations", tags=["calculations"])

# /register and /login (JWT) -> used by front-end + tests
app.include_router(auth.router, tags=["auth"])

# --- Static files for Playwright E2E: /static/register.html, /static/login.html ---
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return {"message": "FastAPI User Calculations with JWT Auth"}
