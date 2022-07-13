from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from account.interfaces.token_service_interface import TokenServiceInterface
from configs import get_configs
from exceptions import raise_obj_not_found
from account.schemas import AccountSchema
from account.deps import get_account_collection


class AccountPermission:
    OAUTH_TOKEN = OAuth2PasswordBearer(tokenUrl='/account/login')

    def __init__(self, token_service: TokenServiceInterface):
        self._token_service = token_service

    async def __decode_token(self, token: str):
        payload = await self._token_service.decode_token(token=token)
        if not (username := payload.get('sub')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Empty sub field'
            )
        return username

    async def __get_account(self, token, account_collection, **_filters):
        _filters.update({'username': await self.__decode_token(token=token)})
        if (account := await account_collection
                .find_one(filter=_filters)) is None:
            raise_obj_not_found(element='Account')
        return AccountSchema(**account)

    async def get_current_user(
            self, token: str = Depends(OAUTH_TOKEN),
            account_collection=Depends(get_account_collection)):
        return await self.__get_account(
            is_active=True,
            token=token,
            account_collection=account_collection
        )

    async def get_superuser(
            self, account_collection=Depends(get_account_collection),
            token: str = Depends(OAUTH_TOKEN)):
        return await self.__get_account(
            is_active=True, is_superuser=True,
            account_collection=account_collection, token=token)


token_service_data = {
    'algorithm': get_configs().algorithm,
    'exp_time': get_configs().exp_time,
    'secret_key': get_configs().secret_key
}
