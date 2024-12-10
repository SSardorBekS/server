import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://root:password@localhost:27017/kitobai?authSource=admin")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "subscription_platform")

settings = Settings()
