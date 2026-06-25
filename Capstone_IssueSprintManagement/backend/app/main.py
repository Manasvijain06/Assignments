from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router import auth

app = FastAPI(title="Issue Sprint Management System")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Issue Sprint Management System API"}