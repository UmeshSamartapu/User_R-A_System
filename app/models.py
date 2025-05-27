from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    mobileNo: str
    githubUsername: str
    rollNo: str
    collegeName: str
    accessCode: str

class RegisterResponse(RegisterRequest):
    clientID: str
    clientSecret: str

class AuthRequest(BaseModel):
    email: EmailStr
    name: str
    rollNo: str
    accessCode: str
    clientID: str
    clientSecret: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int