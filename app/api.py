from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import UserAccounts, UserProgress
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
app.include_router(UserProgress.router, prefix="/levels", tags=["Level Progress"])

@app.get("/", tags=["Home"])
def get_root():
    return {
        "message": "First endpoint"
    }