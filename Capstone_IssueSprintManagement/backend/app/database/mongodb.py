import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = None
db = None
users_collection = None

def connect_db():
    global client, db, users_collection

    MONGO_URL = os.getenv("MONGO_URL")

    if not MONGO_URL:
        raise ValueError("MONGO_URL is missing in environment variables")

    client = MongoClient(MONGO_URL)

    db = client.issue_sprint_db

    users_collection = db.users
    print("MongoDB connected successfully")

def close_db():
    global client

    if client:
        client.close()
        print("MongoDB connection closed")