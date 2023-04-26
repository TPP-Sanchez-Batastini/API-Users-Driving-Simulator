from fastapi import APIRouter
from fastapi import status, Body

router = APIRouter()

@router.get("/", status_code = status.HTTP_200_OK)
def get_users():
    return {
        "messsage": "Hi! Levels"
    }