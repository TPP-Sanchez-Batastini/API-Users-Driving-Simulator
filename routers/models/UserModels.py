from pydantic import BaseModel, EmailStr

class UserRegistration(BaseModel):
    name_to_show: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class DefaultResponse(BaseModel):
    message: str
    status_code: int


class UserLogon(BaseModel):
    name_to_show: str
    id: int

class UserLogonResponse(BaseModel):
    message: str
    user: UserLogon
    jwt: str
    
