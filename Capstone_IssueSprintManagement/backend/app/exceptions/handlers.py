from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.exceptions.user_exceptions import (
    UserNotFoundException,
    AdminAccessRequiredException,
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
    InvalidCredentialsException,
)

from app.exceptions.project_exceptions import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(UserNotFoundException)
    def user_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message}
        )

    @app.exception_handler(AdminAccessRequiredException)
    def admin_access_required_handler(request, exc):
        return JSONResponse(
            status_code=403,
            content={"detail": exc.message}
        )

    @app.exception_handler(UserAlreadyExistsException)
    def user_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )

    @app.exception_handler(InvalidPasswordEncodingException)
    def invalid_password_encoding_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message}
        )

    @app.exception_handler(InvalidCredentialsException)
    def invalid_credentials_handler(request, exc):
        return JSONResponse(
            status_code=401,
            content={"detail": exc.message}
        )

    @app.exception_handler(ProjectAlreadyExistsException)
    def project_already_exists_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )

    @app.exception_handler(ProjectNotFoundException)
    def project_not_found_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message}
        )

    @app.exception_handler(MemberAlreadyAssignedException)
    def member_already_assigned_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )

    @app.exception_handler(MemberNotAssignedException)
    def member_not_assigned_handler(request, exc):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )