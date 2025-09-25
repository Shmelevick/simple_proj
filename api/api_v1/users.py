from typing import Annotated

from fastapi import APIRouter, Depends
import fastapi_users
from sqlalchemy.ext.asyncio import AsyncSession


from api.api_v1.fastapi_users_routers import fastapi_users
from core.config import settings
from core.schemas import UserRead, UserCreate
from core.crud import get_all_users, create_user_crud
from core.models import db_helper
from core.schemas.user import UserUpdate


router = APIRouter(prefix=settings.api.v1.users, tags=["Users"])
router.include_router(router=fastapi_users.get_users_router(UserRead, UserUpdate))


@router.get("/", response_model=list[UserRead])
async def get_users(session: Annotated[AsyncSession, Depends(db_helper.session_get)]):
    users = await get_all_users(session)
    return users


@router.post("/create", response_model=UserRead)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_get)],
    user_data: UserCreate,
):
    new_user = await create_user_crud(session, user_data)
    return new_user
