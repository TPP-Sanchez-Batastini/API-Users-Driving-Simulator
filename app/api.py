from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import UserAccounts, UserProgress, Levels
from database.engine import initialize_database

app = FastAPI()
initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserAccounts.router, prefix="/users", tags=["Users"])
app.include_router(UserProgress.router, prefix="/user_progress", tags=["Level Progress"])
app.include_router(Levels.router, prefix="/levels", tags=["Levels"])