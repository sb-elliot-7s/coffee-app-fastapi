from typing import Optional

from fastapi import Depends, UploadFile, File

from database import database
from image_service.image_service import ImageService
from .profile_repositories import ProfileRepositories
from .schemas import UpdateAccountSchema
from .token_service import TokenService
from configs import get_configs
from .password_service import PasswordService
from passlib.context import CryptContext
from .repositories import AccountRepository

account_collection = database.account


async def get_account_collection():
    yield account_collection


async def get_account_service(
        _account_collection=Depends(get_account_collection)):
    yield {
        'token_service': TokenService(
            secret_key=get_configs().secret_key,
            algorithm=get_configs().algorithm,
            exp_time=get_configs().exp_time
        ),
        'password_service': PasswordService(
            context=CryptContext(schemes=['bcrypt'], deprecated='auto')
        ),
        'repository': AccountRepository(account_collection=_account_collection)
    }


async def get_repository(_account_collection=Depends(get_account_collection)):
    yield {
        'repository': ProfileRepositories(
            account_collection=_account_collection,
            image_service=ImageService(database=database)
        )
    }


async def get_updated_data(
        updated_data: UpdateAccountSchema = Depends(
            UpdateAccountSchema.as_form
        ),
        image: Optional[UploadFile] = File(None),
):
    yield {'updated_data': updated_data, 'image': image}
