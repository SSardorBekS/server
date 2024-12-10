from fastapi import APIRouter, Depends
from app.models.user import User
from app.auth.jwt import create_access_token

router = APIRouter()

@router.get("/")
async def get_subscription_details():
    return {"subscription": "Active"}
