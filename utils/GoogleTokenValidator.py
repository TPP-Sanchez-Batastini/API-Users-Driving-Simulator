from google.oauth2 import id_token
from google.auth.transport import requests as reqGoogle
import os
import requests

async def validateOAuthToken(token):
    try:
        CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
        try:
            idinfo = id_token.verify_oauth2_token(token, reqGoogle.Request(), CLIENT_ID)
            userid = idinfo['sub']
        except ValueError:
            raise Exception("Token OAuth2 Inválido.")
        google_response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        resp = google_response.json()
        return {
            "nameToShow": resp["name"],
            "email": resp["email"]
        }
    except Exception as e:
        raise Exception(f"Error al traducir Token a Sesion: {str(e)}")
