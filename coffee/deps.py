from fastapi import Depends

from database import database
from .repositories import CoffeeRepositories
from permissions import AccountPermission, token_service_data
from account.token_service import TokenService

coffee_collection = database.coffee
rating_collection = database.rating


async def get_coffee_collection(): yield coffee_collection


async def get_rating_collection(): yield rating_collection


async def get_repository(_coffee_collection=Depends(get_coffee_collection)):
    yield {
        'repository': CoffeeRepositories(coffee_collection=_coffee_collection)
    }


async def get_account_superuser(
        account=Depends(AccountPermission(
            token_service=TokenService(**token_service_data)).get_superuser)
):
    yield account


async def get_current_account(
        account=Depends(AccountPermission(
            token_service=TokenService(**token_service_data)).get_current_user)
):
    yield account
