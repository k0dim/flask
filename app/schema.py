from typing import Any, Dict, Optional, Type

from errors import ApiError
from pydantic import BaseModel, EmailStr, ValidationError


class UserSchema(BaseModel):

    email: EmailStr
    password: str


class PatchUser(BaseModel):

    email: Optional[EmailStr]
    password: Optional[str]


class AdsSchema(BaseModel):

    title: str
    description: str


class PatchAds(BaseModel):

    title: Optional[str]
    description: Optional[str]


SCHEMA_TYPE = Type[UserSchema] | Type[PatchUser] | Type[AdsSchema] | Type[PatchAds]


def validate(schema: SCHEMA_TYPE, data: Dict[str, Any], exclude_none: bool = True) -> dict:
    try:
        validated = schema(**data).dict(exclude_none=exclude_none)
    except ValidationError as error:
        raise ApiError(400, error.errors())
    return validated