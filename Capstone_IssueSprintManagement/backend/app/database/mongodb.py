import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = None
db = None


def connect_db():
    """
    Connect to MongoDB database.
    """
    global client, db

    if not MONGO_URL:
        raise ValueError("MONGO_URL is missing in environment variables")

    if not DATABASE_NAME:
        raise ValueError("DATABASE_NAME is missing in environment variables.")

    client = MongoClient(MONGO_URL)
    db = client[DATABASE_NAME]

    print("MongoDB connected successfully")

def close_db():
    """
    Close the MongoDB connection.
    """
    global client

    if client:
        client.close()
        print("MongoDB connection closed")