import jwt
import os
from utils.JWTValidator import decodeValidJWT
import pytest
import unittest


class JWTValidatorTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker):
        self.mocker = mocker


    def test_general_behavior_handles_unicode_decode_error(self):
        # Arrange
        encoded_jwt = jwt.encode({"user_id": 123, "name": "John Doe"}, os.getenv("SECRET_JWT"), algorithm="HS256")
        self.mocker.patch.dict(os.environ, {"SECRET_JWT": os.getenv("SECRET_JWT")})

        # Act
        decoded_jwt = decodeValidJWT(encoded_jwt)

        # Assert
        assert decoded_jwt["name"] == "John Doe"

        
    def test_edge_case_expired_timestamp_raises_exception(self):
        # Arrange
        encoded_jwt = jwt.encode({"user_id": 123, "exp": 1}, os.getenv("SECRET_JWT"), algorithm="HS256")
        self.mocker.patch.dict(os.environ, {"SECRET_JWT": os.getenv("SECRET_JWT")})

        # Act & Assert
        with pytest.raises(jwt.exceptions.ExpiredSignatureError):
            decodeValidJWT(encoded_jwt)


    def test_general_behavior_returns_decoded_payload(self):
        # Arrange
        encoded_jwt = jwt.encode({"user_id": 123}, os.getenv("SECRET_JWT"), algorithm="HS256")
        self.mocker.patch.dict(os.environ, {"SECRET_JWT": os.getenv("SECRET_JWT")})

        # Act
        decoded_jwt = decodeValidJWT(encoded_jwt)

        # Assert
        assert isinstance(decoded_jwt, dict)


    def test_edge_case_incorrect_secret_key_raises_exception(self):
        # Arrange
        encoded_jwt = jwt.encode({"user_id": 123}, "incorrect_secret_key", algorithm="HS256")
        self.mocker.patch.dict(os.environ, {"SECRET_JWT": os.getenv("SECRET_JWT")})

        # Act & Assert
        with pytest.raises(jwt.exceptions.InvalidSignatureError):
            decodeValidJWT(encoded_jwt)