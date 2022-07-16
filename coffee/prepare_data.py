from datetime import datetime

from bson import ObjectId

from coffee.schemas import CreateCoffeeSchema, CreateRateSchema


class PrepareDataMixin:
    @staticmethod
    async def prepare_update_data(account, coffee_data: CreateCoffeeSchema,
                                  coffee_id: str, image_ids: list):
        return {
            'filter': {
                '_id': ObjectId(coffee_id),
                'account_id': account.id
            },
            'update': {
                '$set': {
                    **coffee_data.dict(exclude_none=True),
                    'updated': datetime.utcnow()},
                '$push': {'images': {'$each': image_ids or []}}
            },
            'return_document': True
        }

    @staticmethod
    async def prepare_create_data(coffee_data: CreateCoffeeSchema,
                                  account_id: str, image_ids: list):
        return {
            **coffee_data.dict(exclude_none=True),
            'account_id': account_id,
            'rating': 0.0,
            'created': datetime.utcnow(),
            'images': image_ids or []
        }

    @staticmethod
    async def prepare_rating_data(
            account_id: str, coffee_id: str, rating: CreateRateSchema):
        return {
            'account_id': account_id,
            'coffee_id': coffee_id,
            'created': datetime.utcnow(),
            **rating.dict()
        }

    @staticmethod
    async def query_rating(rating_id: str, account_id: str):
        return {'_id': ObjectId(rating_id), 'account_id': account_id}
