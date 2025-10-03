from fastapi import APIRouter

from core.schemas.user import UserRegisteredNotification


router = APIRouter()


@router.post("user-created")
def notify_user_created(info: UserRegisteredNotification):
    """
    Triggered when a user is created
    """
    ...
