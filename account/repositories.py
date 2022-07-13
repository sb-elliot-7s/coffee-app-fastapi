from datetime import datetime
from .interfaces.account_repositories_interface import \
    AccountRepositoryInterface
from .schemas import CreateAccountSchema
from .crud import AccountCRUD


class AccountRepository(AccountRepositoryInterface):
    def __init__(self, account_collection):
        self.__account_collection = account_collection
        self.__crud = AccountCRUD()

    async def create_account(self, password: str,
                             account_data: CreateAccountSchema):
        document = {
            'password': password,
            'created': datetime.utcnow(),
            'updated': None,
            'is_active': True,
            **account_data.dict(exclude_none=True, exclude={'password'})
        }
        result = await self.__crud.create_account(
            collection=self.__account_collection, document=document
        )
        return await self.__crud.find_account_by_id(
            collection=self.__account_collection, account_id=result.inserted_id
        )

    async def get_account_by_username(self, username: str):
        return await self.__account_collection.find_one({'username': username})
