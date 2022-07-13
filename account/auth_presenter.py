from .interfaces.account_repositories_interface import \
    AccountRepositoryInterface
from .interfaces.password_service_interface import PasswordServiceInterface
from .interfaces.token_service_interface import TokenServiceInterface
from .schemas import CreateAccountSchema
from exceptions import raise_user_exists, raise_incorrect_username_or_password


class AuthPresenter:
    def __init__(self, repository: AccountRepositoryInterface,
                 password_service: PasswordServiceInterface,
                 token_service: TokenServiceInterface):
        self.__token_service = token_service
        self.__password_service = password_service
        self.__repository = repository

    async def save_user(self, account_data: CreateAccountSchema):
        if await self.__repository \
                .get_account_by_username(username=account_data.username):
            raise_user_exists()
        hashed_password = await self.__password_service \
            .hashed_password(plain_password=account_data.password)
        return await self.__repository \
            .create_account(password=hashed_password, account_data=account_data)

    async def _authenticate(self, username: str, password: str):
        if not (account := await self.__repository
                .get_account_by_username(username)) \
                or not await self.__password_service \
                .verify_passwords(password, account['password']):
            raise_incorrect_username_or_password()
        return account

    async def login(self, username: str, password: str) -> dict:
        account = await self._authenticate(username=username, password=password)
        token = await self.__token_service \
            .encode_token(username=account['username'])
        return {'access_token': token}
