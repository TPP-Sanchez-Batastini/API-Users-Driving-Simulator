from fastapi import APIRouter, status, HTTPException
from routers.models import UserModels
from controllers import UserController

router = APIRouter()

@router.get("/", status_code = status.HTTP_200_OK)
async def get_users():
    return {
        "messsage": "Hi! Users"
    }


@router.post("/register", status_code = status.HTTP_200_OK, response_model = UserModels.DefaultResponse)
async def create_user(userRegistration: UserModels.UserRegistration):
    try:
        if userRegistration.password is None or userRegistration.password == "":
            raise HTTPException(
                status_code = 422, 
                detail= "La contraseña no puede estar vacía."
            )
        response = UserController.create_user_in_db(userRegistration)
        return response
    except Exception as e:
        raise HTTPException(
            status_code = 500, 
            detail= str(e)
        )


@router.post("/login", status_code = status.HTTP_200_OK, response_model = UserModels.UserLogonResponse)
async def create_user(userLogin: UserModels.UserLogin):
    try:
        response = UserController.login(userLogin)
        return response
    except Exception as e:
        raise HTTPException(
            status_code = 500, 
            detail= str(e)
        )
    

@router.post("/login_google", status_code = status.HTTP_200_OK, response_model = UserModels.UserLogonResponse)
async def login_with_google(userLogin: UserModels.GoogleLogin):
    try:
        return await UserController.loginWithGoogle(userLogin.token)
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )
