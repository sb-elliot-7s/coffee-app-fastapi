from typing import Optional

from fastapi import UploadFile

from .interfaces.repositories_interface import CoffeeRepositoriesInterface
from .schemas import CreateCoffeeSchema, CreateRateSchema
from image_service.interfaces import ImageServiceInterface


class CoffeePresenter:
    def __init__(self, repository: CoffeeRepositoriesInterface):
        self.__repository = repository

    async def list_of_all_coffees(self, limit: int, skip: int):
        return await self.__repository \
            .list_of_all_coffees(limit=limit, skip=skip)

    async def detail_coffee(self, coffee_id: str):
        return await self.__repository.detail_coffee(coffee_id=coffee_id)

    async def delete_coffee(self, account, coffee_id: str):
        return await self.__repository \
            .delete_coffee(account=account, coffee_id=coffee_id)

    async def update_coffee(
            self, account, coffee_id: str, coffee_data: CreateCoffeeSchema,
            img_service: ImageServiceInterface,
            images: Optional[list[UploadFile]]):
        return await self.__repository.update_coffee(
            account=account, coffee_id=coffee_id, coffee_data=coffee_data,
            images=images, img_service=img_service)

    async def create_coffee(
            self, account, coffee_data: CreateCoffeeSchema,
            img_service: ImageServiceInterface,
            images: Optional[list[UploadFile]]):
        return await self.__repository \
            .create_coffee(account=account, coffee_data=coffee_data,
                           images=images, img_service=img_service)

    async def rate_coffee(
            self, account, coffee_id: str, rating_collection,
            rating: CreateRateSchema):
        return await self.__repository.rate_coffee(
            coffee_id=coffee_id, account=account,
            rating=rating, rating_collection=rating_collection
        )

    async def change_rate(
            self, account, rating_id: str, rating_collection,
            rating: CreateRateSchema):
        return await self.__repository.change_rate(
            rating_id=rating_id, account=account, rating=rating,
            rating_collection=rating_collection
        )
