import json
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from objid import ObjID
from fastapi import Form


class CreateCoffeeSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]

    @classmethod
    def as_form(
            cls, title: Optional[str] = Form(None),
            description: Optional[str] = Form(None),
            price: Optional[float] = Form(None)
    ):
        return cls(title=title, description=description, price=price)


class CoffeeSchema(CreateCoffeeSchema):
    id: ObjID = Field(alias='_id')
    account_id: str
    is_active: bool = True
    rating: float = 0.0
    images: Optional[list[str]]
    created: datetime
    updated: Optional[datetime]

    @classmethod
    def from_list(cls, lst_str: str):
        return [
            {
                **x,
                '_id': ObjectId(x.get('_id'))
            } for x in json.loads(lst_str)
        ]

    @classmethod
    def from_obj(cls, obj: str):
        result: dict = json.loads(obj)
        return {
            **result,
            '_id': ObjectId(result.get('_id'))
        }

    class Config:
        json_encoders = {
            ObjID: lambda x: str(x),
            datetime: lambda x: x.strftime('%Y-%m-%d %H:%M')
        }


class CreateRateSchema(BaseModel):
    rating: int


class RateSchema(CreateRateSchema):
    id: ObjID = Field(alias='_id')
    coffee_id: str
    account_id: str
    created: datetime
    updated: Optional[datetime]

    class Config:
        json_encoders = {
            ObjID: lambda o: str(o),
            datetime: lambda x: x.strftime('%Y-%m-%d %H:%M')
        }
