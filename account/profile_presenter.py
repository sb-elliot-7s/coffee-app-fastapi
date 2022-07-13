from typing import Optional

from fastapi import UploadFile
from .interfaces.profile_repositories_interface import \
    ProfileRepositoriesInterface

from account.schemas import UpdateAccountSchema


class ProfilePresenter:
    def __init__(self, repository: ProfileRepositoriesInterface):
        self.__repository = repository

    async def update_profile(
            self, account, updated_data: UpdateAccountSchema,
            image: Optional[UploadFile]
    ):
        return await self.__repository.update_profile(
            account=account, updated_data=updated_data, image=image
        )

    async def delete_account(self, account):
        return await self.__repository.delete_account(account=account)

    async def detail_account(self, account):
        return await self.__repository.detail_account(account=account)
