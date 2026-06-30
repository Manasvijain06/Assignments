from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import auth
from app.database.mongodb import connect_db, close_db

app = FastAPI(title="Issue Sprint Management System")

# -------------------------
# CORS CONFIG
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# LIFECYCLE EVENTS
# -------------------------
@app.on_event("startup")
def startup_db():
    connect_db()


@app.on_event("shutdown")
def shutdown_db():
    close_db()

# -------------------------
# ROUTES
# -------------------------
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    return {"message": "Issue Sprint Management System API"}