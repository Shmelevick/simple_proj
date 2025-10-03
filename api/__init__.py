from fastapi import APIRouter

from .api_v1 import router as api_v1_router
from .webhooks import webhooks_router
from core.config import settings

router = APIRouter()
router.include_router(api_v1_router, prefix=settings.api.prefix)
router.include_router(webhooks_router, prefix="/hook", tags=["webhook"])
