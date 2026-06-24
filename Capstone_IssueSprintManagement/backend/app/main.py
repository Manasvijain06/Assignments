from fastapi import FastAPI
from app.database.mongodb import db

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API running"}

@app.get("/db-test")
def db_test():
    try:
        collections = db.list_collection_names()
        return {
            "status": "MongoDB Connected Successfully",
            "collections": collections
        }
    except Exception as e:
        return {
            "status": "MongoDB Connection Failed",
            "error": str(e)
        }