from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegistration(BaseModel):
    name_to_show: str
    email: EmailStr
    password: str | None
    federated_with: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class GoogleLogin(BaseModel):
    token: str


class DefaultResponse(BaseModel):
    message: str
    status_code: int


class UserLogon(BaseModel):
    name_to_show: str
    email: str
    id: int

class UserLogonResponse(BaseModel):
    message: str
    user: UserLogon
    jwt: str
    
