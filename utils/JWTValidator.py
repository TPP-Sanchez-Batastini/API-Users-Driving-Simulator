import jwt
import os

def decodeValidJWT(encoded_jwt):
    jwt_secret = os.getenv("SECRET_JWT")
    decoded_jwt = jwt.decode(encoded_jwt, jwt_secret, algorithms=["HS256"])
    return decoded_jwt