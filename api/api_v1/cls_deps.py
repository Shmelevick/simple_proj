from os import access
from threading import stack_size
from typing import Annotated, Generator, Self
from fastapi import HTTPException, Header, Request, status
from pydantic import BaseModel


# С Созданием экземпляра 1 раз
class PathReadDependency:
    def __init__(self, source: str) -> None:
        self.source = source
        self._request: Request | None = None
        self.foobar: str | None = ""

    def as_dependency(
        self, request: Request, foobar: Annotated[str, Header(alias="x-foobar")]
    ) -> Generator[Self, None, None]:
        self._request = request
        self.foobar = foobar
        yield self
        self.foobar = None
        self._request = None

    @property
    def path(self) -> str:
        if self._request is None:
            return ""

        return self._request.url.path

    def read(self, **kwargs: str) -> dict[str, (str | None) | dict[str, str]]:
        return {
            "source": self.source,
            "path": self.path,
            "foobar": self.foobar,
            "kwargs": kwargs,
        }


path_reader = PathReadDependency(source="abc/c/c/l")


# С Созданием экземпляра каждый раз (например, валидация токена)
class TokenData(BaseModel):
    id: int
    username: str


class TokenIntrospectResult(BaseModel):
    result: TokenData


class HeaderAccessDependency:
    def __init__(self, secret_token: str) -> None:
        self.secret_token = secret_token

    def validate(self, token: str) -> TokenIntrospectResult:
        if token != self.secret_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
            )

        return TokenIntrospectResult(result=TokenData(id=42, username="John Smith"))

    def __call__(
        self, token: Annotated[str, Header(alias="x-access-token")]
    ) -> TokenIntrospectResult:
        token_data = self.validate(token)
        return token_data


access_required = HeaderAccessDependency(secret_token="foo-bar-fizz-buzz")
