from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # TODO
    tokenUrl="auth/jwt/login"
)
