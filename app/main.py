from fastapi import FastAPI

from app.database import Base, engine
from app.routers import users, calculations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User & Calculation API",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(calculations.router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
