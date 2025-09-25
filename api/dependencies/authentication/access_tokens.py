from typing import TYPE_CHECKING
from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from icecream import ic

from core.models import db_helper, AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: "AsyncSession" = Depends(db_helper.session_get),
):
    token = AccessToken.get_db(session=session)
    ic(token)
    yield token
