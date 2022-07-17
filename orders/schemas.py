from datetime import datetime

from pydantic import BaseModel, Field
from objid import ObjID
from typing import Optional


class OrderCoffee(BaseModel):
    id: ObjID = Field(alias='_id')
    order_id: str
    coffee_id: str
    quantity: int
    price: Optional[float]


class Order(BaseModel):
    id: ObjID = Field(alias='_id')
    account_id: str
    is_ordered: bool
    created: datetime

    total_amount: Optional[float]

    coffees_order: Optional[list[OrderCoffee]]

    class Config:
        json_encoders = {
            ObjID: lambda o: str(o)
        }
