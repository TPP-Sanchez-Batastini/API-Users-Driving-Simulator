from routers.models import UserModels
from database.models import User
from sqlalchemy import insert
from database.engine import get_local_session
from fastapi import status
import jwt
import os
import datetime
from datetime import timezone

def create_user_in_db(userRegistration: UserModels.UserRegistration):
    session = get_local_session()
    queried = session.query(User).filter(User.email == str(userRegistration.email).lower())
    if session.query(queried.exists()).scalar():
        raise Exception("Un usuario con ese e-mail ya existe dentro de la base de datos.")
    statement = insert(User).values(
        username = userRegistration.name_to_show,
        email = str(userRegistration.email).lower(),
        password = userRegistration.password # Should come hashed...
    )
    try:
        session.execute(statement)
        session.commit()
        session.close()
    except Exception as e:
        raise Exception(str(e))
    return UserModels.DefaultResponse(
        message= "Usuario creado exitosamente.",
        status_code= status.HTTP_200_OK   
    )


def login(userLogin: UserModels.UserLogin):
    session = get_local_session()
    queried = session.query(User).filter_by(
        email = str(userLogin.email).lower(),
        password = userLogin.password
    )
    if not session.query(queried.exists()).scalar:
        raise Exception("Usuario o contraseña erróneos. Intente nuevamente.")
    user = queried.first()
    jwt_secret = os.getenv("SECRET_JWT")
    encoded_jwt = jwt.encode(
        {
            "id": user.id, 
            "username": user.username, 
            "email": user.email,
            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(minutes=1)
        }, 
        jwt_secret, 
        algorithm="HS256"
    )
    return UserModels.UserLogonResponse(
        message = "Sesión iniciada correctamente.",
        user = UserModels.UserLogon(
            id = user.id,
            name_to_show = user.username
        ),
        jwt = encoded_jwt
    )

