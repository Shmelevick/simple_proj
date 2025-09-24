from loguru import logger
import uuid
from typing import TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from core.models import User
from core.models.types.user_id import UserIdType

if TYPE_CHECKING:
    from fastapi import Request


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(self, user: User, request: "Request | None" = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: "Request | None" = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: "Request | None" = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )
