from typing import Optional

from .coffee_response_data import response_data
from fastapi import APIRouter, Depends, UploadFile, File
from .presenter import CoffeePresenter
from .schemas import CreateCoffeeSchema, CreateRateSchema
from image_service.image_service import ImageService
from database import database
from .deps import get_repository, get_account_superuser, \
    get_rating_collection, get_current_account

coffee_router = APIRouter(prefix='/coffee', tags=['coffee'])


@coffee_router.post(**response_data.get('rate_coffee'))
async def rate_coffee(
        coffee_id: str,
        rating: CreateRateSchema, account=Depends(get_current_account),
        repository=Depends(get_repository),
        rating_collection=Depends(get_rating_collection)
):
    return await CoffeePresenter(**repository) \
        .rate_coffee(account=account, rating=rating, coffee_id=coffee_id,
                     rating_collection=rating_collection)


@coffee_router.patch(**response_data.get('update_rate_coffee'))
async def change_rate_coffee(
        rating_id: str,
        rating: CreateRateSchema, account=Depends(get_current_account),
        repository=Depends(get_repository),
        rating_collection=Depends(get_rating_collection)
):
    return await CoffeePresenter(**repository) \
        .change_rate(account=account, rating=rating, rating_id=rating_id,
                     rating_collection=rating_collection)


@coffee_router.get(**response_data.get('all'))
async def list_of_all_coffees(
        limit: int = 20, skip: int = 0, repository=Depends(get_repository)):
    return await CoffeePresenter(**repository) \
        .list_of_all_coffees(limit=limit, skip=skip)


@coffee_router.get(**response_data.get('detail'))
async def detail_coffee(coffee_id: str, repository=Depends(get_repository)):
    return await CoffeePresenter(**repository) \
        .detail_coffee(coffee_id=coffee_id)


@coffee_router.delete(**response_data.get('delete'))
async def delete_coffee(coffee_id: str, account=Depends(get_account_superuser),
                        repository=Depends(get_repository)):
    return await CoffeePresenter(**repository) \
        .delete_coffee(account=account, coffee_id=coffee_id)


@coffee_router.patch(**response_data.get('patch'))
async def update_coffee(
        coffee_id: str,
        coffee_data: CreateCoffeeSchema = Depends(CreateCoffeeSchema.as_form),
        repository=Depends(get_repository),
        account=Depends(get_account_superuser),
        images: Optional[list[UploadFile]] = File(None)):
    return await CoffeePresenter(**repository).update_coffee(
        account=account, coffee_id=coffee_id, coffee_data=coffee_data,
        images=images, img_service=ImageService(database=database))


@coffee_router.post(**response_data.get('post'))
async def create_coffee(
        coffee_data: CreateCoffeeSchema = Depends(CreateCoffeeSchema.as_form),
        repository=Depends(get_repository),
        account=Depends(get_account_superuser),
        images: Optional[list[UploadFile]] = File(None)):
    return await CoffeePresenter(**repository).create_coffee(
        account=account, coffee_data=coffee_data, images=images,
        img_service=ImageService(database=database))
