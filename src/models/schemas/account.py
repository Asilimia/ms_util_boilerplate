import datetime

import pydantic

from src.models.schemas.base import BaseSchemaModel


class AccountInCreate(BaseSchemaModel):
    username: str
    password: str




class AccountInUpdate(BaseSchemaModel):
    username: str | None = pydantic.Field(default=None)
    password: str | None = pydantic.Field(default=None)


class AccountInLogin(BaseSchemaModel):
    username: str
    password: str


class AccountInPin(BaseSchemaModel):
    username: str
    pin: str


class AccountWithToken(BaseSchemaModel):
    # token: str
    username: str
    is_verified: bool
    is_active: bool
    is_logged_in: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime | None = pydantic.Field(default=None)


class AccountInResponse(BaseSchemaModel):
    id: int
    authorized_account: AccountWithToken
