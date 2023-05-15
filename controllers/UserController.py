from routers.models import UserModels
from database.models import User
from sqlalchemy import insert
from database.engine import get_local_session
from fastapi import status
from utils.JWTValidator import encode_jwt
from utils.GoogleTokenValidator import validateOAuthToken


def create_user_in_db(userRegistration):
    if user_exists(userRegistration.email):
        raise Exception("Un usuario con ese e-mail ya existe dentro de la base de datos.")
    insert_new_user(userRegistration)
    return UserModels.DefaultResponse(
        message= "Usuario creado exitosamente.",
        status_code= status.HTTP_200_OK   
    )


def user_exists(email):
    try:
        session = get_local_session()
        queried = session.query(User).filter(User.email == str(email).lower())
        exists = session.query(queried.exists()).scalar()
        session.close()
        return exists
    except Exception as e:
        raise Exception(str(e))


def insert_new_user(userRegistration):
    session = get_local_session()
    statement = insert(User).values(
        username = userRegistration.name_to_show,
        email = str(userRegistration.email).lower(),
        password = userRegistration.password, # Should come hashed...
        federated_with = userRegistration.federated_with
    )
    try:
        session.execute(statement)
        session.commit()
        session.close()
    except Exception as e:
        raise Exception(str(e))


def login(userLogin: UserModels.UserLogin):
    session = get_local_session()
    queried = session.query(User).filter_by(
        email = str(userLogin.email).lower(),
        password = userLogin.password,
        federated_with = None
    )
    if session.query(queried.exists()).scalar:
        session.close()
        return get_public_user_data(userLogin.email)
    else:
        session.close()
        raise Exception("Usuario o contraseña erróneos. Intente nuevamente.")
    


def get_public_user_data(email):
    try:
        session = get_local_session()
        queried = session.query(User).filter(User.email == str(email).lower())
        user = queried.first()
        encoded_jwt = encode_jwt({
            "id": user.id, 
            "username": user.username, 
            "email": user.email
        })
        usr_response = UserModels.UserLogon(
            id = user.id,
            email = user.email,
            name_to_show = user.username
        )
        return UserModels.UserLogonResponse(
            message = "Sesión iniciada correctamente.",
            user = usr_response,
            jwt = encoded_jwt
        )
    except Exception as e:
        raise Exception(str(e))


async def loginWithGoogle(token):
    userData = await validateOAuthToken(token)
    if not user_exists(userData["email"]):
        userDataReg = UserModels.UserRegistration(
            name_to_show = userData["nameToShow"],
            email = userData["email"],
            federated_with = 'Google',
            password = None
        )
        create_user_in_db(userDataReg)
    return get_public_user_data(userData["email"])


