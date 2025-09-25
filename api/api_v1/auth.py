from fastapi import APIRouter


from api.api_v1.fastapi_users_routers import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from core.config import settings
from core.schemas.user import UserCreate, UserRead
from .users import router as users_router


router = APIRouter(prefix=settings.api.v1.auth, tags=["Auth"])

# /login /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=True,
    )
)

# /register
router.include_router(router=fastapi_users.get_register_router(UserRead, UserCreate))

# /verify
router.include_router(router=fastapi_users.get_verify_router(UserRead))

# /reset /forgot router
router.include_router(fastapi_users.get_reset_password_router())
