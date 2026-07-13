import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = None
db = None
users_collection = None
projects_collection = None

def connect_db():
    """
    Create MongoDB connection when the FastAPI application starts.
    """
    global client, db, users_collection, projects_collection

    if not MONGO_URL:
        raise ValueError("MONGO_URL is missing in environment variables")

    client = MongoClient(MONGO_URL)
    db = client[DATABASE_NAME]

    users_collection = db.users
    projects_collection = db.projects
    print("MongoDB connected successfully")

def close_db():
    """
    Close MongoDB connection when the FastAPI application shuts down.
    """
    global client

    if client:
        client.close()
        print("MongoDB connection closed")