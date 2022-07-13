from fastapi import APIRouter, status, Depends, responses

from permissions import AccountPermission, token_service_data
from .profile_presenter import ProfilePresenter
from .deps import get_updated_data, get_repository
from .schemas import AccountSchema
from .token_service import TokenService

profile_routers = APIRouter(prefix='/profile', tags=['profile'])


async def get_user(
        account=Depends(AccountPermission(
            token_service=TokenService(**token_service_data)).get_current_user)
):
    yield account


response_data = {
    'update': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        'response_model': AccountSchema,
        'response_model_by_alias': False
    },
    'delete': {
        'path': '/',
        'status_code': status.HTTP_204_NO_CONTENT
    },
    'get': {
        'path': '/',
        'status_code': status.HTTP_200_OK,
        'response_model': AccountSchema,
        'response_model_by_alias': False
    }
}


@profile_routers.patch(**response_data.get('update'))
async def update_account(
        updated_data=Depends(get_updated_data),
        account=Depends(get_user),
        repository=Depends(get_repository),
):
    return await ProfilePresenter(**repository).update_profile(
        account=account,
        updated_data=updated_data['updated_data'],
        image=updated_data['image']
    )


@profile_routers.delete(**response_data.get('delete'))
async def delete_account(
        account=Depends(get_user),
        repository=Depends(get_repository)
):
    if not (_ := await ProfilePresenter(**repository)
            .delete_account(account=account)):
        return responses.JSONResponse({'detail': 'Profile not deleted'})
    return responses. \
        JSONResponse({'detail': f'Profile {account.username} has been deleted'})


@profile_routers.get(**response_data.get('get'))
async def detail_account(
        account=Depends(get_user),
        repository=Depends(get_repository)
):
    return await ProfilePresenter(**repository).detail_account(account=account)
