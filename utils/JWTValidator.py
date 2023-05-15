import jwt
import os
import datetime
from datetime import timezone

def decodeValidJWT(encoded_jwt):
    jwt_secret = os.getenv("SECRET_JWT")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_secret, algorithms=["HS256"])
    return decoded_jwt


def encode_jwt(user):
    jwt_secret = os.getenv("SECRET_JWT")
    encoded_jwt = jwt.encode(
        {
            "id": user["id"], 
            "username": user["username"], 
            "email": user["email"],
            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(minutes=120)
        }, 
        jwt_secret, 
        algorithm="HS256"
    )
    return encoded_jwt