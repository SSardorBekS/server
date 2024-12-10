from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DATABASE_NAME]
users_collection = db.get_collection("users")
sessions_collection = db.get_collection("sessions")
transcriptions_collection = db.get_collection("transcriptions")
audio_files_collection = db.get_collection("audio_files")
days_collection = db.get_collection("days")