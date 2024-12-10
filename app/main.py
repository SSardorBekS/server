from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.subscription_routes import router as subscription_router
from app.routes.transciption import app as transciption_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Subscription Platform")

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(subscription_router, prefix="/subscription", tags=["Subscription"])
app.include_router(transciption_router, prefix="/transciption", tags=["transciption"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Subscription Platform!"}
