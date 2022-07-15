import aiofiles
import pytest
from httpx import AsyncClient

from conftest import retrieve_access_token
from main import app


class TestProfile:
    UPDATE_USERNAME = 'new_elliot'

    @pytest.mark.parametrize('username, status', [('elliot', 200)])
    @pytest.mark.asyncio
    async def test_detail_account(
            self, first_client_with_jwt_token, username, status
    ):
        response = await first_client_with_jwt_token.get(url='/profile/')
        assert response.status_code == status
        assert response.json()['username'] == username

    @pytest.mark.parametrize('username, phone, image_path', [
        (None, 7777, 'account/tests/test_profile_image.jpg'),
        (UPDATE_USERNAME, 1234567890, None),
    ])
    @pytest.mark.asyncio
    async def test_update_account(
            self, first_client_with_jwt_token, username, phone, image_path
    ):
        files = []
        if image_path:
            async with aiofiles.open(image_path, mode='rb') as file:
                image = ('image', ('test_image.jpg', await file.read()))
                files.append(image)
        response = await first_client_with_jwt_token.patch(
            url='/profile/',
            data={
                'username': username,
                'phone': phone
            },
            files=files if image_path else None
        )
        assert response.status_code == 200
        assert response.json()['phone'] == phone

    @pytest.fixture(scope='module')
    async def update_first_client_with_jwt(self, get_token_service):
        token = await retrieve_access_token(
            token_service=get_token_service,
            username=self.UPDATE_USERNAME
        )
        async with AsyncClient(app=app, base_url='http://testserver') as client:
            client.headers.update({'Authorization': f'Bearer {token}'})
            yield client

    @pytest.mark.asyncio
    async def test_delete_account(self, update_first_client_with_jwt):
        response = await update_first_client_with_jwt.delete(url='/profile/')
        assert response.json()['detail'] == f'Profile {self.UPDATE_USERNAME}' \
                                            f' has been deleted'
        assert response.status_code == 204
