from abc import ABC, abstractmethod

from account.schemas import CreateAccountSchema


class AccountRepositoryInterface(ABC):
    @abstractmethod
    async def get_account_by_username(self, username: str): pass

    @abstractmethod
    async def create_account(
            self, password: str, account_data: CreateAccountSchema): pass
