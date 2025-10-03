import time
from core.models import User

import aiohttp
import logging

from core.schemas.user import UserRead, UserRegisteredNotification


log = logging.getLogger(__name__)


WEBHOOK_URL = "http://httpbin.org/post"


async def send_new_user_notification(user: User) -> None:
    wh_data = UserRegisteredNotification(
        user=UserRead.model_validate(user), ts=int(time.time())
    )
    log.info("User created with data: %s", wh_data)

    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK_URL, json=wh_data) as response:
            data = await response.json()
            log.info("Sent webhook, got response: %s", data)
