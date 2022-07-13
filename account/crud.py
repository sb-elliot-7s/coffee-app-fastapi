from typing import Optional

from bson import ObjectId

from exceptions import raise_obj_not_found
from fastapi import HTTPException, status


class AccountCRUD:

    @staticmethod
    async def _filter(collection, **kwargs):
        if not (account := await collection.find_one(filter=kwargs)):
            raise_obj_not_found(element='Account')
        return account

    async def find_account_by_id(self, collection, account_id: str):
        return await self._filter(
            collection=collection, _id=ObjectId(account_id))

    async def find_account_by_username(self, collection, username: str):
        return await self._filter(collection=collection, username=username)

    @staticmethod
    async def create_account(collection, document: dict):
        return await collection.insert_one(document=document)

    @staticmethod
    async def update(
            collection, account_id: str, document: dict,
            image_id: Optional[ObjectId]):
        if _ := await collection.find_one(
                filter={'username': document.get('username')}
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username exists'
            )
        if image_id:
            document.update({'profile_image': str(image_id)})
        q = {'_id': ObjectId(account_id)}
        update = {'$set': document}
        if not (account := await collection.find_one_and_update(
                filter=q, update=update, return_document=True)):
            raise_obj_not_found(element='Account')
        return account

    @staticmethod
    async def delete(collection, **kwargs):
        return await collection.delete_one(filter=kwargs)
