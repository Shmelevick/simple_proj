from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from core.models import User
from core.schemas.user import UserCreate


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    users = await session.scalars(stmt)
    return users.all()


async def create_user_crud(session: AsyncSession, user_create: UserCreate) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
