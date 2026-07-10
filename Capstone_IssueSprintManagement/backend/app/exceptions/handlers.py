from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.user_exceptions import (
    UserNotFoundException,
    AdminAccessRequiredException,
    UserAlreadyExistsException,
    InvalidPasswordEncodingException,
    InvalidCredentialsException,
)

from app.exceptions.project_exceptions import (
    MemberAlreadyAssignedException,
    MemberNotAssignedException,
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
)

from app.exceptions.issue_exceptions import (
    AssigneeRequiredException,
    InvalidIssueStatusTransitionException,
    InvalidParentIssueException,
    IssueNotFoundException,
    CommentNotFoundException,
    CommentPermissionDeniedException,
)

from app.exceptions.sprint_exceptions import (
    DoneIssueCannotBeAddedException,
    InvalidSprintStatusException,
    IssueAlreadyInSprintException,
    SprintAlreadyExistsException,
    SprintCreationFailedException,
    SprintNotFoundException,
)

def register_exception_handlers(app: FastAPI):
    """
    Register custom exception handlers.
    """

    @app.exception_handler(UserNotFoundException)
    def user_not_found_handler(request: Request, exc:UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message}
        )

    @app.exception_handler(AdminAccessRequiredException)
    def admin_access_required_handler(request: Request, exc: AdminAccessRequiredException):
        return JSONResponse(
            status_code=403,
            content={"detail": exc.message}
        )

    @app.exception_handler(UserAlreadyExistsException)
    def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )

    @app.exception_handler(InvalidPasswordEncodingException)
    def invalid_password_encoding_handler(request: Request, exc: InvalidPasswordEncodingException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message}
        )

    @app.exception_handler(InvalidCredentialsException)
    def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(
            status_code=401,
            content={"detail": exc.message}
        )

    @app.exception_handler(ProjectAlreadyExistsException)
    def project_already_exists_handler(request: Request, exc:ProjectAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )

    @app.exception_handler(ProjectNotFoundException)
    def project_not_found_handler(request: Request, exc: ProjectNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message}
        )

    @app.exception_handler(MemberAlreadyAssignedException)
    def member_already_assigned_handler(request: Request, exc: MemberAlreadyAssignedException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )

    @app.exception_handler(MemberNotAssignedException)
    def member_not_assigned_handler(request: Request, exc: MemberNotAssignedException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message}
        )


    @app.exception_handler(IssueNotFoundException)
    def issue_not_found_handler(request: Request, exc: IssueNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )


    @app.exception_handler(InvalidIssueStatusTransitionException)
    def invalid_issue_status_handler(request: Request, exc: InvalidIssueStatusTransitionException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message},
        )


    @app.exception_handler(AssigneeRequiredException)
    def assignee_required_handler(request: Request, exc: AssigneeRequiredException):
        return JSONResponse(
            status_code=403,
            content={"detail": exc.message},
        )


    @app.exception_handler(InvalidParentIssueException)
    def invalid_parent_issue_handler(request: Request, exc: InvalidParentIssueException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )


    @app.exception_handler(SprintNotFoundException)
    def sprint_not_found_handler(request: Request, exc: SprintNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )


    @app.exception_handler(SprintCreationFailedException)
    def sprint_creation_failed_handler(request: Request, exc: SprintCreationFailedException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )


    @app.exception_handler(DoneIssueCannotBeAddedException)
    def done_issue_handler(request: Request, exc: DoneIssueCannotBeAddedException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )


    @app.exception_handler(IssueAlreadyInSprintException)
    def issue_already_in_sprint_handler(request: Request, exc: IssueAlreadyInSprintException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message},
        )


    @app.exception_handler(SprintAlreadyExistsException)
    def sprint_already_exists_handler(request: Request, exc: SprintAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={"detail": exc.message},
        )


    @app.exception_handler(InvalidSprintStatusException)
    def invalid_sprint_status_handler(request: Request, exc: InvalidSprintStatusException):
        return JSONResponse(
            status_code=400,
            content={"detail": exc.message},
        )

    @app.exception_handler(CommentNotFoundException)
    def comment_not_found_handler(request: Request, exc: CommentNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": exc.message},
        )

    @app.exception_handler(CommentPermissionDeniedException)
    def comment_permission_denied_handler(
        request: Request,
        exc: CommentPermissionDeniedException,
    ):
        return JSONResponse(
            status_code=403,
            content={"detail": exc.message},
        )