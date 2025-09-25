from typing import Annotated
from fastapi import APIRouter, Depends


from api.api_v1.fastapi_users_routers import current_user, current_super_user
from core.config import settings
from core.models.user import User
from core.schemas.user import UserRead


router = APIRouter(prefix=settings.api.v1.messages, tags=["Messages"])


@router.get("/")
def get_user_messages(user: User = Depends(current_user)):

    return {
        "messages": ("m1", "m2", "m3"),
        "user": UserRead.model_validate(user),
    }


@router.get("/secrets")
def get_superuser_messages(user: Annotated[User, Depends(current_super_user)]):
    return {
        "messages": ("secret_m1", "secret_m2", "secret_m3"),
        "user": UserRead.model_validate(user),
    }
