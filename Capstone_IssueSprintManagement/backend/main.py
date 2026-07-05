import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.handlers import register_exception_handlers
from app.router import auth, admin, project, issue
from app.database.mongodb import connect_db, close_db


app = FastAPI(title="Issue Sprint Management System")
# -------------------------
# LIFECYCLE EVENTS
# -------------------------
@app.on_event("startup")
def startup_db():
    connect_db()


@app.on_event("shutdown")
def shutdown_db():
    close_db()

register_exception_handlers(app)

FRONTEND_URL = os.getenv("FRONTEND_URL","http://localhost:5173")
# -------------------------
# CORS CONFIG
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTES
# -------------------------
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/users", tags=["Role Checks"])
app.include_router(project.router, prefix="/projects", tags=["Projects"])
app.include_router(issue.router, prefix="/projects", tags=["Issues"])

@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {"message": "Issue Sprint Management System API"}