from .interfaces.repositories import OrderRepositoryInterface


class OrderPresenter:
    def __init__(self, repository: OrderRepositoryInterface):
        self.__repository = repository

    async def get_order(self, account, order_id: str):
        return await self.__repository \
            .detail_order(account=account, order_id=order_id)

    async def get_orders(
            self, account, skip: int, limit: int, is_ordered: bool):
        return await self.__repository \
            .orders(account=account, skip=skip, limit=limit,
                    is_ordered=is_ordered)

    async def add_to_cart(self, coffee_id: str, account):
        return await self.__repository \
            .add_to_cart(coffee_id=coffee_id, account=account)

    async def remove_from_cart(self, order_coffee_id: str, account):
        return await self.__repository \
            .remove_from_cart(order_coffee_id=order_coffee_id, account=account)
