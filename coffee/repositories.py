from datetime import datetime
from typing import Optional

from bson import ObjectId
from .interfaces.repositories_interface import CoffeeRepositoriesInterface
from .schemas import CreateCoffeeSchema, CreateRateSchema
from fastapi import UploadFile, HTTPException, status
from image_service.interfaces import ImageServiceInterface
from exceptions import raise_obj_not_found
from .prepare_data import PrepareDataMixin
from .utils import Utils
from configs import get_configs
from .decorators import cache_detail_coffee, cache_coffees


class CoffeeRepositories(CoffeeRepositoriesInterface):

    def __init__(self, coffee_collection):
        self.__coffee_collection = coffee_collection
        self.__prepare_data = PrepareDataMixin()

    async def __get_coffee(self, **kwargs):
        if not (coffee := await self.__coffee_collection
                .find_one(filter=kwargs)):
            raise_obj_not_found(element='Coffee')
        return coffee

    @cache_coffees(ex=1 if get_configs().test else 100)
    async def list_of_all_coffees(self, limit: int, skip: int):
        cursor = self.__coffee_collection \
            .find() \
            .skip(skip) \
            .limit(limit) \
            .sort('created', -1)
        return [coffee async for coffee in cursor]

    @cache_detail_coffee(ex=100)
    async def detail_coffee(self, coffee_id: str):
        return await self.__get_coffee(_id=ObjectId(coffee_id))

    async def delete_coffee(self, account, coffee_id: str):
        result = await self.__coffee_collection \
            .delete_one({'_id': ObjectId(coffee_id), 'account_id': account.id})
        if not result.deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Coffee {coffee_id} not found'
            )

    async def update_coffee(
            self, account, coffee_id: str, coffee_data: CreateCoffeeSchema,
            images: Optional[list[UploadFile]],
            img_service: ImageServiceInterface):
        image_ids = await Utils().save_images(images, img_service)
        data = await self.__prepare_data \
            .prepare_update_data(account=account, coffee_data=coffee_data,
                                 coffee_id=coffee_id, image_ids=image_ids)
        if not (coffee := await self.__coffee_collection
                .find_one_and_update(**data)):
            raise_obj_not_found(element=f'Coffee {coffee_id} not found')
        return coffee

    async def create_coffee(self, account, coffee_data: CreateCoffeeSchema,
                            img_service: ImageServiceInterface,
                            images: Optional[list[UploadFile]]):
        image_ids = await Utils().save_images(images, img_service)
        document = await self.__prepare_data.prepare_create_data(
            coffee_data=coffee_data, account_id=account.id, image_ids=image_ids)
        result = await self.__coffee_collection.insert_one(document=document)
        return await self.__get_coffee(_id=ObjectId(result.inserted_id))

    async def rate_coffee(self, account, coffee_id: str, rating_collection,
                          rating: CreateRateSchema):
        doc = await self.__prepare_data.prepare_rating_data(
            account_id=account.id, coffee_id=coffee_id, rating=rating)
        result = await rating_collection.insert_one(document=doc)
        query = {'_id': ObjectId(result.inserted_id)}
        return await rating_collection.find_one(filter=query)

    async def change_rate(self, account, rating_id: str, rating_collection,
                          rating: CreateRateSchema):
        query = await self.__prepare_data \
            .query_rating(rating_id=rating_id, account_id=account.id)
        return await rating_collection.find_one_and_update(
            filter=query, update={'$set': {
                'updated': datetime.utcnow(),
                **rating.dict()}
            }, return_document=True)
