from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile

from account.schemas import UpdateAccountSchema


class ProfileRepositoriesInterface(ABC):
    @abstractmethod
    async def update_profile(
            self, account, updated_data: UpdateAccountSchema,
            image: Optional[UploadFile]
    ): pass

    @abstractmethod
    async def delete_account(self, account):
        pass

    @abstractmethod
    async def detail_account(self, account):
        pass
