from datetime import datetime
from bson import ObjectId
from exceptions import raise_obj_not_found
from .interfaces.repositories import OrderRepositoryInterface
from .mixins import AggPipelineMixin
from .responses_data import coffee_order_completely_removed_response


class OrderRepository(AggPipelineMixin, OrderRepositoryInterface):

    def __init__(
            self, order_collection, order_coffee_collection, coffee_collection):
        self.__coffee_collection = coffee_collection
        self.__order_coffee_collection = order_coffee_collection
        self.__order_collection = order_collection

    async def __save_order(self, account):
        document = {
            'account_id': account.id, 'is_ordered': False,
            'created': datetime.utcnow()
        }
        return await self.__order_collection.insert_one(document=document)

    async def __get_order_coffee(self, **kwargs):
        return await self.__order_coffee_collection.find_one(filter=kwargs)

    async def detail_order(self, account, order_id: str):
        pipeline = self.get_order_pipeline(order_id, account)
        return (await self.__order_collection.aggregate(pipeline).to_list(1))[0]

    async def orders(self, account, skip: int, limit: int, is_ordered: bool):
        pipeline = self.get_orders_pipeline(
            skip=skip, limit=limit, is_ordered=is_ordered, account=account)
        return [o async for o in self.__order_collection.aggregate(pipeline)]

    async def __get_coffee(self, coffee_id: str) -> dict:
        if not (coffee := await self.__coffee_collection
                .find_one({'_id': ObjectId(coffee_id)})):
            raise_obj_not_found(element='Coffee not found')
        return coffee

    async def __create_coffee_order(
            self, order_id: str, coffee_id: str, coffee_price: float) -> dict:
        document = {
            'order_id': order_id, 'coffee_id': coffee_id, 'quantity': 1,
            'price': coffee_price
        }
        result = await self.__order_coffee_collection.insert_one(document)
        return await self.__get_order_coffee(_id=ObjectId(result.inserted_id))

    async def __update_coffee_order(self, order_id: str, coffee_id: str):
        query = {'order_id': order_id, 'coffee_id': coffee_id}
        update = {'$inc': {'quantity': 1}}
        return await self.__order_coffee_collection.find_one_and_update(
            filter=query, update=update, return_document=True)

    async def __create_or_update_coffee_order(
            self, order_id: str, coffee_id: str, coffee: dict) -> dict:
        if not (_ := await self.__get_order_coffee(order_id=order_id,
                                                   coffee_id=coffee_id)):
            return await self.__create_coffee_order(
                order_id, coffee_id, coffee_price=coffee['price'])
        return await self.__update_coffee_order(order_id, coffee_id)

    async def add_to_cart(self, coffee_id: str, account):
        if not (order := await self.__order_collection.find_one(
                filter=self.filter(account_id=account.id, is_ordered=False))):
            order_result = await self.__save_order(account=account)
            order = await self.__order_collection \
                .find_one(filter={'_id': ObjectId(order_result.inserted_id)})
        coffee = await self.__get_coffee(coffee_id=coffee_id)
        return await self.__create_or_update_coffee_order(
            order_id=str(order['_id']), coffee_id=coffee_id, coffee=coffee)

    async def __get_coffee_order_or_not_found(self, order_coffee_id):
        if not (order_coffee := await self.__get_order_coffee(
                _id=ObjectId(order_coffee_id))):
            raise_obj_not_found(element=f'Order Coffee {order_coffee_id}')
        return order_coffee

    async def __delete_one_position(self, order_coffee_id: str):
        return await self.__order_coffee_collection.find_one_and_update(
            filter={'_id': ObjectId(order_coffee_id)},
            update={'$inc': {'quantity': -1}},
            return_document=True)

    async def __completely_remove_coffee_order(self, order_coffee_id: str):
        result = await self.__order_coffee_collection \
            .delete_one(filter={'_id': ObjectId(order_coffee_id)})
        if not result.deleted_count:
            raise_obj_not_found(element=f'Coffee Order {order_coffee_id}')
        return coffee_order_completely_removed_response(order_coffee_id)

    async def remove_from_cart(self, order_coffee_id: str, account):
        ord_coffee = await self.__get_coffee_order_or_not_found(order_coffee_id)
        return await self.__delete_one_position(order_coffee_id) \
            if ord_coffee['quantity'] > 1 \
            else await self.__completely_remove_coffee_order(order_coffee_id)
