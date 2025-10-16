import time
import logging
import aiohttp

from core.models import User
from core.schemas.user import UserRead, UserRegisteredNotification

log = logging.getLogger(__name__)
WEBHOOK_URL = "http://httpbin.org/post"


async def send_new_user_notification(user: User) -> None:
    # Создаём pydantic-модель
    notification = UserRegisteredNotification(
        user=UserRead.model_validate(user),
        ts=int(time.time()),
    )

    # Преобразуем в "чистый" dict — aiohttp сможет это сериализовать
    payload = notification.model_dump()  # <- pydantic v2: model_dump()
    log.info("User created with data: %s", payload)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload, timeout=10) as response:
                # безопасно читаем ответ как JSON
                data = await response.json()
                log.info("Sent webhook, got response: %s", data)
    except aiohttp.ClientError:
        log.exception("Failed to send webhook due to network/client error")
    except Exception:
        log.exception("Unexpected error while sending webhook")
