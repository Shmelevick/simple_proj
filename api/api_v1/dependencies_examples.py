from typing import Annotated
from fastapi import APIRouter, Depends, Header

from api.api_v1.helper import GreatHelper, FullHelper
from api.api_v1.cls_deps import (
    HeaderAccessDependency,
    TokenIntrospectResult,
    path_reader,
    PathReadDependency,
)


router = APIRouter(tags=["Dependencies Examples"])


@router.get("/singe-directory-dependency")
def single_directory_dependency(
    foobar: Annotated[str | None, Header(alias="smack_my_ass")] = None,
):
    return {"foobar": foobar}


def get_great_helper(
    helper_name: Annotated[str, Header(alias="x-helper-name")] = "HelperOne",
    default_helper: Annotated[str, Header(alias="x-header-name")] = "HeaderOne",
) -> GreatHelper:
    return GreatHelper(helper_name, default_helper)


@router.get("/class-example")
def class_inside_dep(helper: GreatHelper = Depends(get_great_helper)):
    return {"helper": helper.as_dict()}


@router.get("/class-is-dep-example")
def class_is_dep(helper: GreatHelper = Depends(FullHelper)):
    return {"helper": helper.as_dict()}


@router.get("/path-reader-from-method")
def path_reader_dependency(
    reader: Annotated[PathReadDependency, Depends(path_reader.as_dependency)],
):
    return {
        "reader": reader.read(foo="bar"),
    }


@router.get("/dynamic-validation")
def dynamic_validation(
    token_data: Annotated[
        TokenIntrospectResult, Depends(HeaderAccessDependency("ydx"))
    ],
):
    return {
        "token_data": token_data.model_dump(),
    }
