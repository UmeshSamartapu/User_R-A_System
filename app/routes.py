from fastapi import APIRouter, HTTPException
from .models import RegisterRequest, RegisterResponse, AuthRequest, TokenResponse
from .auth import generate_client_credentials, create_access_token
from .db import users_collection

router = APIRouter()

@router.post("/evaluation-service/register", response_model=RegisterResponse)
async def register_user(data: RegisterRequest):
    exists = await users_collection.find_one({
        "$or": [
            {"email": data.email},
            {"mobileNo": data.mobileNo},
            {"rollNo": data.rollNo},
            {"githubUsername": data.githubUsername},
            {"accessCode": data.accessCode}
        ]
    })
    if exists:
        raise HTTPException(status_code=400, detail="User already registered.")

    clientID, clientSecret = generate_client_credentials()
    user_data = data.dict()
    user_data.update({"clientID": clientID, "clientSecret": clientSecret, "tokenIssued": False})
    await users_collection.insert_one(user_data)
    return RegisterResponse(**user_data)

@router.post("/evaluation-service/auth", response_model=TokenResponse)
async def authenticate_user(data: AuthRequest):
    user = await users_collection.find_one({
        "email": data.email,
        "name": data.name,
        "rollNo": data.rollNo,
        "accessCode": data.accessCode,
        "clientID": data.clientID,
        "clientSecret": data.clientSecret
    })
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    if user.get("tokenIssued"):
        raise HTTPException(status_code=403, detail="Token already issued.")

    token, expiry = create_access_token({"sub": user["email"]})
    await users_collection.update_one({"_id": user["_id"]}, {"$set": {"tokenIssued": True}})
    return TokenResponse(access_token=token, expires_in=expiry)