from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile

from image_service.interfaces import ImageServiceInterface
from ..schemas import CreateCoffeeSchema, CreateRateSchema


class CoffeeRepositoriesInterface(ABC):

    @abstractmethod
    async def list_of_all_coffees(self, limit: int, skip: int):
        pass

    @abstractmethod
    async def detail_coffee(self, coffee_id: str):
        pass

    @abstractmethod
    async def delete_coffee(self, account, coffee_id: str):
        pass

    @abstractmethod
    async def update_coffee(
            self, account, coffee_id: str, coffee_data: CreateCoffeeSchema,
            images: Optional[list[UploadFile]],
            img_service: ImageServiceInterface
    ):
        pass

    @abstractmethod
    async def create_coffee(
            self, account, coffee_data: CreateCoffeeSchema,
            images: Optional[list[UploadFile]],
            img_service: ImageServiceInterface
    ):
        pass

    @abstractmethod
    async def rate_coffee(
            self, coffee_id: str,
            account,
            rating_collection,
            rating: CreateRateSchema
    ):
        pass

    @abstractmethod
    async def change_rate(
            self, rating_id: str,
            account,
            rating_collection,
            rating: CreateRateSchema
    ): pass
