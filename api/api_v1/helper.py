from typing import Annotated, Generator

from fastapi import Header


class GreatHelper:
    def __init__(self, name: str, default: str) -> None:
        self.name = name
        self.default = default

    def as_dict(self) -> dict[str, str]:
        return {"name": self.name, "default": self.default}


class FullHelper(GreatHelper):
    def __init__(
        self,
        name: Annotated[str, Header(alias="x-helper-name")] = "HelperOne",
        default: Annotated[str, Header(alias="x-header-name")] = "HeaderOne",
    ):
        super().__init__(name, default)
