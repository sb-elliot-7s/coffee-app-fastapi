import json
from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import Form
from pydantic import BaseModel, Field
from objid import ObjID


class BaseAccountSchema(BaseModel):
    username: str
    phone: Optional[int]
    date_birth: Optional[datetime]
    is_superuser: bool = False


class CreateAccountSchema(BaseAccountSchema):
    password: str = Field(min_length=5)


class UpdateAccountSchema(BaseModel):
    username: Optional[str]
    phone: Optional[int]

    @classmethod
    def as_form(cls, username: Optional[str] = Form(None),
                phone: Optional[int] = Form(None)):
        return cls(username=username, phone=phone)


class AccountSchema(BaseAccountSchema):
    id: ObjID = Field(alias='_id')
    profile_image: Optional[str]
    is_active: bool
    created: datetime
    updated: Optional[datetime]

    @classmethod
    def from_json(cls, _json: str):
        acc = json.loads(_json)
        return {**acc, '_id': ObjectId(acc.get('_id'))}

    class Config:
        json_encoders = {
            datetime: lambda value: value.strftime('%Y-%m-%d %H:%M'),
            ObjID: lambda value: str(value)
        }


class TokenSchema(BaseModel):
    access_token: str
