from fastapi import Depends

from account.token_service import TokenService
from configs import get_configs
from database import database
from orders.repositories import OrderRepository
from permissions import AccountPermission
from coffee.deps import get_coffee_collection

order_collection = database.order
order_coffee_collection = database.order_coffee


async def get_order_collection():
    yield order_collection


async def get_order_coffee_collection():
    yield order_coffee_collection


async def get_service_data(
        _order_collection=Depends(get_order_collection),
        _order_coffee_collection=Depends(get_order_coffee_collection),
        _coffee_collection=Depends(get_coffee_collection)
):
    yield {
        'repository': OrderRepository(
            order_collection=_order_collection,
            order_coffee_collection=_order_coffee_collection,
            coffee_collection=_coffee_collection
        )
    }


async def get_account(account=Depends(
    AccountPermission(token_service=TokenService(
        secret_key=get_configs().secret_key, exp_time=get_configs().exp_time,
        algorithm=get_configs().algorithm
    )).get_current_user
)):
    yield account
