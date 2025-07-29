from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from app.database import engine, Base
from app.routers import user_route, auth_route, subject_route

load_dotenv()  # Load variables from .env

# Important: Ensure that the models are imported before creating the tables
from app.models import user_has_role_model, user_model, role_model, subject_model

# Create the database tables
if os.getenv("DB_CREATE_ALL_TABLE") == "true":
    print("---> Creating all tables, please wait... <---")
    Base.metadata.create_all(bind=engine)
    print("---> Creating all tables completed. <---")


app = FastAPI(title="School Management System API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
prefix = "/api"

app.include_router(auth_route.router, prefix=prefix)
app.include_router(user_route.router, prefix=prefix)
app.include_router(subject_route.router, prefix=prefix)
