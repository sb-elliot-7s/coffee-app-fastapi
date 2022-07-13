from fastapi import APIRouter, status, Depends

from permissions import AccountPermission, token_service_data
from .deps import get_account_service
from .auth_presenter import AuthPresenter
from .schemas import AccountSchema, TokenSchema, CreateAccountSchema
from fastapi.security import OAuth2PasswordRequestForm

from .token_service import TokenService

account_router = APIRouter(prefix='/account', tags=['account'])


async def get_user(
        account=AccountPermission(
            token_service=TokenService(**token_service_data)).get_current_user,
):
    yield account


router_data = {
    'registration': {
        'path': '/registration',
        'status_code': status.HTTP_201_CREATED,
        'response_model': AccountSchema,
        'response_model_by_alias': False
    },
    'login': {
        'path': '/login',
        'status_code': status.HTTP_200_OK,
        'response_model': TokenSchema
    }
}


@account_router.post(**router_data.get('registration'))
async def registration(account_data: CreateAccountSchema,
                       service_data=Depends(get_account_service)):
    return await AuthPresenter(**service_data) \
        .save_user(account_data=account_data)


@account_router.post(**router_data.get('login'))
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                service_data=Depends(get_account_service)):
    return await AuthPresenter(**service_data) \
        .login(username=form_data.username, password=form_data.password)
