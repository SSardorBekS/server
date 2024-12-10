from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import users_collection, days_collection
from app.models.user import User, UserInDB, RegisterUser
from app.auth.security import verify_password, hash_password
from app.auth.jwt import create_access_token

router = APIRouter()

@router.post("/days")
async def create_day(user: RegisterUser):
    existing_user = await days_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": False,
    }
    await users_collection.insert_one(new_user)
    return {"message": "Day created successfully"}

@router.get("/days")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
