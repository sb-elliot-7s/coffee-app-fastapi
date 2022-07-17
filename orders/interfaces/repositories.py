from abc import ABC, abstractmethod


class OrderRepositoryInterface(ABC):
    @abstractmethod
    async def detail_order(self, account, order_id: str): pass

    @abstractmethod
    async def orders(
            self, account, skip: int, limit: int, is_ordered: bool
    ): pass

    @abstractmethod
    async def add_to_cart(self, coffee_id: str, account): pass

    @abstractmethod
    async def remove_from_cart(self, order_coffee_id: str, account): pass
