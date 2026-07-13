import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.mongodb import connect_db, close_db
from app.exceptions.handlers import register_exception_handlers
from app.router import auth, admin, project, issue, sprint, profile


app = FastAPI(title="Issue Sprint Management System")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

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
app.include_router(admin.router, prefix="/users", tags=["Users"])
app.include_router(project.router, prefix="/projects", tags=["Projects"])
app.include_router(issue.router, prefix="/projects", tags=["Issues"])
app.include_router(sprint.router, prefix="/sprints", tags=["Sprints"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])

@app.get("/")
def root():
    """
    Health check endpoint.
    """
    return {"message": "Issue Sprint Management System API"}