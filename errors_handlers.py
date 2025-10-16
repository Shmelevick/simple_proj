import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from sqlalchemy.exc import DatabaseError

from pydantic import ValidationError
from icecream import ic

log = logging.Logger(__name__)


def register_errors_handlers(app: FastAPI) -> None:

    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_error(request: Request, exc: ValidationError):
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"message": "Unhandled error", "error": exc.errors()},
        )

    @app.exception_handler(DatabaseError)
    def handle_db_error(request: Request, exc: ValidationError) -> ORJSONResponse:
        log.error("Unhandled database error")
        ic(exc.__dict__)
        return ORJSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Opa("},
        )
