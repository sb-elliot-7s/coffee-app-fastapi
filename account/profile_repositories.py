from typing import Optional

from bson import ObjectId
from fastapi import UploadFile

from .interfaces.profile_repositories_interface import \
    ProfileRepositoriesInterface
from .schemas import UpdateAccountSchema
from .crud import AccountCRUD
from image_service.interfaces import ImageServiceInterface


class ProfileRepositories(ProfileRepositoriesInterface):

    def __init__(self, account_collection,
                 image_service: ImageServiceInterface):
        self.__image_service = image_service
        self.__account_collection = account_collection
        self.__crud = AccountCRUD()

    async def __save_image(self, image: Optional[UploadFile]):
        if image:
            return await self.__image_service.write_image(image, image.filename)

    async def update_profile(
            self, account, updated_data: UpdateAccountSchema,
            image: Optional[UploadFile]
    ):
        return await self.__crud.update(
            collection=self.__account_collection,
            account_id=account.id,
            image_id=await self.__save_image(image=image),
            document=updated_data.dict(exclude_none=True)
        )

    async def delete_account(self, account):
        return await self.__crud.delete(
            collection=self.__account_collection, _id=ObjectId(account.id)
        )

    async def detail_account(self, account):
        return await self.__crud.find_account_by_id(
            collection=self.__account_collection, account_id=account.id
        )
